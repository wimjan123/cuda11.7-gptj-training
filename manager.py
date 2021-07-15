#!/usr/bin/env python3

# @author Jesus Alvarez <sw-cuda-installer@nvidia.com>

"""Container scripts template injector and pipeline trigger."""

#
# !! IMPORTANT !!
#
# Editors of this file should use https://github.com/python/black for auto formatting.
#

# >>> REALLY IMPORTANT NOTICE ABOUT DEPENDENCIES... <<<
#
# 1. Dependency handling is done in two places, cudaRcImage.groovy in the jenkins pipeline library code
#
#    a: Dependencies will be added automatically to the kitmaker trigger builder images
#
# 2. Gitlab pipeline "prepare" stage.
#
#    a: This needs to be updated manually at the moment, to do this go to
#    https://gitlab-master.nvidia.com/cuda-installer/cuda/-/pipelines/new and set the variable to "REBUILD_BUILDER=true" and
#    run it. This will run the gitlab builder image rebuild to include the new dependencies.
#
import re
import os
import pathlib
import logging
import logging.config
import shutil
import glob
import sys
import io
import select
import time
import json
import subprocess
import collections
from packaging import version

import jinja2
from jinja2 import Environment, Template
from plumbum import cli, local
from plumbum.cmd import rm, grep, cut, sort, find
import yaml
import glom
import docker
import git
import deepdiff
import requests
from retry import retry

# >>> REALLY IMPORTANT NOTICE ABOUT DEPENDENCIES... <<<
#
# 1. Dependency handling is done in two places, cudaRcImage.groovy in the jenkins pipeline library code
#
#    a: Dependencies will be added automatically to the kitmaker trigger builder images
#
# 2. Gitlab pipeline "prepare" stage.
#
#    a: This needs to be updated manually at the moment, to do this go to
#    https://gitlab-master.nvidia.com/cuda-installer/cuda/-/pipelines/new and set the variable to "REBUILD_BUILDER=true" and
#    run it. This will run the gitlab builder image rebuild to include the new dependencies.
#

log = logging.getLogger()

HTTP_RETRY_ATTEMPTS = 3
HTTP_RETRY_WAIT_SECS = 30

SUPPORTED_DISTRO_LIST = ["ubuntu", "ubi", "centos"]


class UnknownCudaRCDistro(Exception):
    """An exception that is raised when a match connot be made against a distro from Shipit global.json"""

    pass


class RequestsRetry(Exception):
    """An exception to handle retries for requests http gets"""

    pass


class ImageRegistryLoginRetry(Exception):
    """An exception to handle retries for container registry login"""

    pass


class ImagePushRetry(Exception):
    """An exception to handle retries for pushing container images"""

    pass


class ImageDeleteRetry(Exception):
    """An exception to handle retries for image deletion"""

    pass


@retry(
    (ImageRegistryLoginRetry),
    tries=HTTP_RETRY_ATTEMPTS,
    delay=HTTP_RETRY_WAIT_SECS,
    logger=log,
)
def auth_registries(push_repos):
    repos = {}
    for repo, metadata in push_repos.items():
        if metadata.get("only_if", False) and not os.getenv(metadata["only_if"]):
            log.info("repo: '%s' only_if requirement not satisfied", repo)
            continue
        user = os.getenv(metadata["user"])
        if not user:
            user = metadata["user"]
        passwd = os.getenv(metadata["pass"])
        if not passwd:
            passwd = metadata["pass"]
        repos[metadata["registry"]] = {"user": user, "pass": passwd}

    if not repos:
        log.fatal("Could not retrieve registry credentials. Environment not set?")
        sys.exit(1)

    # docker login
    for repo, data in repos.items():
        log.info(f"Logging into {repo}")
        #  log.debug(f"USER: {data['user']} PASS: {data['pass']}")
        result = shellcmd(
            "docker",
            ("login", repo, f"-u" f"{data['user']}", f"-p" f"{data['pass']}",),
            printOutput=False,
            returnOut=True,
        )
        if result.returncode > 0:
            raise ImageRegistryLoginRetry()
        else:
            log.info(f"Docker login to '{repo}' was successful.")


def shellcmd(bin, args, printOutput=True, returnOut=False):
    """Run the shell command with specified arguments for skopeo/docker

    args        -- A tuple of arguments.
    printOutput -- If True, the output of the command will be send to the logger.
    returnOut   -- Return a tuple of the stdout, stderr, and return code. Default: returns true if the command
                 succeeded.
    """
    if "skopeo" in bin:
        bin_name = local["/usr/bin/skopeo"]
    elif "docker" in bin:
        # find docker
        if pathlib.Path("/usr/local/bin/docker").exists():
            bin_name = local["/usr/local/bin/docker"]
        elif pathlib.Path("/usr/bin/docker").exists():
            bin_name = local["/usr/bin/docker"]
        else:
            raise Exception("Can't find docker client executable!")
    else:
        log.error("%s is not supported by method - shellcmd", bin)
        sys.exit(1)
    out = ""
    err = ""
    p = bin_name.popen(
        args=args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
        # do something with line
        out += line
        if printOutput:
            log.info(line)
    for line in io.TextIOWrapper(p.stderr, encoding="utf-8"):
        err += line
        if printOutput:
            log.error(line)
    p.communicate()
    if returnOut:
        Output = collections.namedtuple("output", "returncode stdout stderr")
        return Output(p.returncode, out, err)
    if p.returncode != 0:
        #  log.error("See log output...")
        return False
    return True


class Manager(cli.Application):
    """CUDA CI Manager"""

    PROGNAME = "manager.py"
    VERSION = "0.0.1"

    manifest = None
    ci = None

    manifest_path = cli.SwitchAttr(
        "--manifest", str, excludes=["--shipit-uuid"], help="Select a manifest to use.",
    )

    shipit_uuid = cli.SwitchAttr(
        "--shipit-uuid",
        str,
        excludes=["--manifest"],
        help="Shipit UUID used to build release candidates (internal)",
    )

    def _load_manifest_yaml(self):
        log.debug(f"Loading manifest: {self.manifest_path}")
        with open(self.manifest_path, "r") as f:
            self.manifest = yaml.load(f, yaml.Loader)

    def _load_rc_push_repos_manifest_yaml(self):
        push_repo_path = pathlib.Path("manifests/rc-push-repos.yml")
        log.debug(f"Loading push repos manifest: {push_repo_path}")
        obj = {}
        with open(push_repo_path, "r") as f:
            obj = yaml.load(f, yaml.Loader)
        return obj

    def load_ci_yaml(self):
        with open(".gitlab-ci.yml", "r") as f:
            self.ci = yaml.load(f, yaml.Loader)

    def _load_app_config(self):
        with open("manager-config.yaml", "r") as f:
            logging.config.dictConfig(yaml.safe_load(f.read())["logging"])

    # Get data from a object by dotted path. Example "cuda."v10.0".cuda_requires"
    def get_data(self, obj, *path, can_skip=False):
        try:
            data = glom.glom(obj, glom.Path(*path))
        except glom.PathAccessError:
            if can_skip:
                return
            # raise glom.PathAccessError
            log.error(f'get_data path: "{path}" not found!')
        else:
            return data

    # Returns a unmarshalled json object
    @retry(
        (RequestsRetry),
        tries=HTTP_RETRY_ATTEMPTS,
        delay=HTTP_RETRY_WAIT_SECS,
        logger=log,
    )
    def get_http_json(self, url):
        r = requests.get(url)
        log.debug("response status code %s", r.status_code)
        #  log.debug("response body %s", r.json())
        if r.status_code == 200:
            log.info("http json get successful")
        else:
            raise RequestsRetry()
        return r.json()

    def main(self):
        self._load_app_config()
        if not self.nested_command:  # will be ``None`` if no sub-command follows
            log.fatal("No subcommand given!")
            print()
            self.help()
            return 1
        elif len(self.nested_command[1]) < 2 and any(
            "generate" in arg for arg in self.nested_command[1]
        ):
            log.error(
                "Subcommand 'generate' missing  required arguments! use 'generate --help'"
            )
            return 1
        elif not any(halp in self.nested_command[1] for halp in ["-h", "--help"]):
            log.info("cuda ci manager start")
            if not self.shipit_uuid and self.manifest_path:
                self._load_manifest_yaml()


@Manager.subcommand("trigger")
class ManagerTrigger(Manager):
    DESCRIPTION = "Trigger for changes."

    repo = None

    trigger_all = False
    trigger_explicit = []

    key = ""
    pipeline_name = "default"

    CI_API_V4_URL = "https://gitlab-master.nvidia.com/api/v4"
    CI_PROJECT_ID = 12064

    dry_run = cli.Flag(
        ["-n", "--dry-run"], help="Show output but don't make any changes."
    )

    no_test = cli.Flag(["--no-test"], help="Don't run smoke tests")

    no_scan = cli.Flag(["--no-scan"], help="Don't run security scans")

    no_push = cli.Flag(["--no-push"], help="Don't push images to the registries")

    rebuildb = cli.Flag(
        ["--rebuild-builder"],
        help="Force rebuild of the builder image used to build the cuda images.",
    )

    branch = cli.SwitchAttr(
        "--branch",
        str,
        help="The branch to trigger against on Gitlab.",
        default="master",
    )

    distro = cli.SwitchAttr(
        "--os-name",
        str,
        group="Targeted",
        excludes=["--manifest", "--trigger-override"],
        help="The distro name without version information",
        default=None,
    )

    distro_version = cli.SwitchAttr(
        "--os-version",
        str,
        group="Targeted",
        excludes=["--manifest", "--trigger-override"],
        help="The distro version",
        default=None,
    )

    release_label = cli.SwitchAttr(
        "--release-label",
        str,
        group="Targeted",
        excludes=["--manifest", "--trigger-override"],
        help="The cuda release label. Example: 11.2.0",
        default=None,
    )

    arch = cli.SwitchAttr(
        "--arch",
        cli.Set("x86_64", "ppc64le", "arm64", case_sensitive=False),
        group="Targeted",
        excludes=["--manifest", "--trigger-override"],
        help="Generate container scripts for a particular architecture",
    )

    candidate_number = cli.SwitchAttr(
        "--candidate-number",
        str,
        group="Targeted",
        excludes=["--manifest", "--trigger-override"],
        help="The CUDA release candidate number",
        default=None,
    )

    candidate_url = cli.SwitchAttr(
        "--candidate-url",
        str,
        group="Targeted",
        excludes=["--manifest", "--trigger-override"],
        help="The CUDA release candidate url",
        default=None,
    )

    webhook_url = cli.SwitchAttr(
        "--webhook-url",
        str,
        group="Targeted",
        excludes=["--manifest", "--trigger-override"],
        help="The url to POST to when the job is done. POST will include a list of tags pushed",
        default=None,
    )

    branch = cli.SwitchAttr(
        "--branch",
        str,
        group="Targeted",
        help="The branch to trigger against on gitlab.",
        default=None,
    )

    trigger_override = cli.SwitchAttr(
        "--trigger-override",
        str,
        excludes=["--shipit-uuid"],
        help="Override triggering from gitlab with a variable",
        default=None,
    )

    l4t = cli.Flag(["--l4t"], help="Flag the pipeline as being for L4T",)

    def ci_pipeline_by_name(self, name):
        #  log.debug(f"have pipeline_name: {name}")
        #  rgx = re.compile(fr"^\s+- \$(?!all)(.*_{name}_.*) == \"true\"$")
        rgx = re.compile(fr"^\s+- if: '\$([\w\._]*{name}[\w\._]*)\s+==\s.true.'$")
        ci_vars = []
        with open(".gitlab-ci.yml", "r") as fp:
            for _, line in enumerate(fp):
                match = rgx.match(line)
                if match:
                    ci_vars.append(match.groups(0)[0])
        return ci_vars

    def ci_pipelines(
        self, cuda_version, distro, distro_version, arch,
    ):
        """Returns a list of pipelines extracted from the gitlab-ci.yml

        Iterates .gitlab-ci.yml line by line looking for a match on the pipeline variable.

        For example:

            - if: '$ubuntu20_04_11_3_1 == "true"'

        Every pipeline has this variable defined, and that is used with the gitlab trigger api to trigger explicit
        pipelines.

        Returns a list of pipeline variables to pass to the gitlab API.

        All arguments to this function can be None, in that case all of the pipelines are returned.
        """
        if cuda_version:
            distro_list_by_cuda_version = self.supported_distro_list_by_cuda_version(
                version
            )
            #  log.debug(f"distro_list_by_cuda_version: {distro_list_by_cuda_version}")

        if not cuda_version:
            cuda_version = "(\d{1,2}_\d{1,2}_?\d?)"
        if not distro:
            distro = "(ubuntu\d{2}_\d{2})?(?(2)|([a-z]*\d))"
        elif not distro_version:
            distro = f"({distro}\d)"
            if "ubuntu" in distro:
                distro = "(ubuntu\d{2}_\d{2})"
        else:
            distro = f"{distro}{distro_version}"

        # Full match regex without known cuda version with distro and distro version in one group
        #  ^\s+- if: '\$((ubuntu)?(?(2)(\d{2}_\d{2})|([a-z]*)(\d))_(\d{1,2}_\d{1,2}_?\d?)_(x86_64|arm64|ppc64le))\s+==\s.true.'$

        # Full match regex without known cuda version and distro and distro version in separate groups
        #  ^\s+- if: '\$((ubuntu\d{2}_\d{2})?(?(2)|([a-z]*\d))_(\d{1,2}_\d{1,2}_?\d?)_(x86_64|arm64|ppc64le))\s+==\s.true.'$

        rgx_temp = fr"^\s+- if: '\$({distro}_{cuda_version})\s+==\s.true.'$"
        #  log.debug(f"regex_matcher: {rgx_temp}")
        rgx = re.compile(rgx_temp)
        ci_vars = []
        with open(".gitlab-ci.yml", "r") as fp:
            for _, line in enumerate(fp):
                match = rgx.match(line)
                if match:
                    ci_vars.append(match.groups(0)[0])
        return ci_vars

    def get_cuda_version_from_trigger(self, trigger):
        rgx = re.compile(r".*cuda-?([\d\.]+).*$")
        match = rgx.match(trigger)
        if (match := rgx.match(trigger)) is not None:
            return match.group(1)
        else:
            log.info(f"Cuda version not found in trigger!")

    def get_pipeline_name_from_trigger(self, trigger):
        rgx = re.compile(r".*name:(\w+)$")
        if (match := rgx.match(trigger)) is not None:
            return match.group(1)

    def get_distro_version_from_trigger(self, trigger):
        rgx = re.compile(r".*cuda([\d\.]+).*$")
        match = rgx.match(trigger)
        if match is not None:
            return match.group(1)
        else:
            log.warning(f"Could not extract version from trigger: '{trigger}'!")

    def supported_distro_list_by_cuda_version(self, version):
        if not version:
            return
        distros = ["ubuntu", "ubi", "centos"]
        keys = self.parent.manifest[self.key].keys()

        # There are other keys in the cuda field other than distros, we need to strip those out
        def get_distro_name(name):
            r = re.compile("[a-zA-Z]+")
            return r.findall(name)[0]

        return [f for f in keys if get_distro_name(f) in distros]

    def check_explicit_trigger(self):
        """Checks for a pipeline trigger command and builds a list of pipelines to trigger.

        Checks for a trigger command in the following order:

        - git commit message
        - trigger_override command line flag

        Returns True if pipelines have been found matching the trigger command.
        """
        self.repo = git.Repo(pathlib.Path("."))
        commit = self.repo.commit("HEAD")
        rgx = re.compile(r"ci\.trigger = (.*)")
        log.debug("Commit message: %s", repr(commit.message))

        if self.trigger_override:
            log.info("Using trigger override!")
            # check for illegal characters
            if not re.search(
                r"^(?:[cuda]+[\d\.]*(?:[_a-z0-9]*)?,?)+$", self.trigger_override
            ):
                raise Exception(
                    "Regex match for trigger override failed! Allowed format is 'cuda<version>(_<distro_with_version>)[,...]' ex: 'cuda11.0.3' or 'cuda10.2_centos8`"
                )
            pipeline = self.trigger_override
        else:
            match = rgx.search(commit.message)
            if not match:
                log.debug("No explicit trigger found in commit message.")
                return False
            else:
                log.info("Explicit trigger found in commit message")
                pipeline = match.groups(0)[0].lower()

        if "all" in pipeline:
            log.info("Triggering ALL of the jobs!")
            self.trigger_all = True
            return True
        else:
            jobs = []
            jobs.append(pipeline)
            log.debug(f"jobs: {jobs}")

            if "," in pipeline:
                jobs = [x.strip() for x in pipeline.split(",")]

            for job in jobs:
                version = self.get_cuda_version_from_trigger(job)
                if not version:
                    self.pipeline_name = self.get_pipeline_name_from_trigger(job)

                log.debug("cuda_version: %s" % version)
                log.debug("pipeline_name: %s" % self.pipeline_name)

                self.key = f"cuda_v{version}"
                if self.pipeline_name != "default":
                    self.key = f"cuda_v{version}_{self.pipeline_name}"

                distro = next((d for d in SUPPORTED_DISTRO_LIST if d in job), None)
                distro_version = None
                if distro:
                    # The trigger specifies a distro
                    assert not any(  # distro should not contain digits
                        char.isdigit() for char in distro
                    )
                    distro_version = (
                        re.match(f"^.*{distro}([\d\.]*)", job).groups(0)[0] or None
                    )

                arch = next(
                    (arch for arch in ["x86_64", "ppc64le", "arm64"] if arch in job),
                    None,
                )

                log.debug(
                    f"job: '{job}' name: '{self.pipeline_name}' version: '{version}' distro: '{distro}' distro_version: '{distro_version}' arch: '{arch}'"
                )

                # Any or all of the variables passed to this function can be None
                for cvar in self.ci_pipelines(version, distro, distro_version, arch):
                    #  log.debug(f"self.pipeline_name: {self.pipeline_name} cvar: {cvar}")
                    if self.pipeline_name and not "default" in self.pipeline_name:
                        pipeline_vars = self.ci_pipeline_by_name(self.pipeline_name)
                    else:
                        pipeline_vars = self.ci_pipelines(
                            version, distro, distro_version, arch
                        )

                    #  __import__("pprint").pprint(pipeline_vars)
                    #  sys.exit(1)

                    for cvar in pipeline_vars:
                        if not cvar in self.trigger_explicit:
                            log.info("Triggering '%s'", cvar)
                            self.trigger_explicit.append(cvar)

            return True

    def kickoff(self):
        url = os.getenv("CI_API_V4_URL") or self.CI_API_V4_URL
        project_id = os.getenv("CI_PROJECT_ID") or self.CI_PROJECT_ID
        dry_run = os.getenv("DRY_RUN") or self.dry_run
        no_test = os.getenv("NO_TEST") or self.no_test
        no_scan = os.getenv("NO_SCAN") or self.no_scan
        no_push = os.getenv("NO_PUSH") or self.no_push
        rebuildb = os.getenv("REBUILD_BUILDER") or self.rebuildb
        token = os.getenv("CI_JOB_TOKEN")
        if not token:
            log.warning("CI_JOB_TOKEN is unset!")
        ref = os.getenv("CI_COMMIT_REF_NAME") or self.branch
        payload = {"token": token, "ref": ref, "variables[TRIGGER]": "true"}
        if self.trigger_all:
            payload["variables[all]"] = "true"
        elif self.trigger_explicit:
            for job in self.trigger_explicit:
                payload[f"variables[{job}]"] = "true"
        if no_scan:
            payload[f"variables[NO_SCAN]"] = "true"
        if no_test:
            payload[f"variables[NO_TEST]"] = "true"
        if no_push:
            payload[f"variables[NO_PUSH]"] = "true"
        if rebuildb:
            payload[f"variables[REBUILD_BUILDER]"] = "true"
        if self.l4t:
            payload[f"variables[L4T]"] = "true"
        final_url = f"{url}/projects/{project_id}/trigger/pipeline"
        log.info("url %s", final_url)
        log.info("payload %s", payload)
        if not self.dry_run:
            r = requests.post(final_url, data=payload)
            log.debug("response status code %s", r.status_code)
            log.debug("response body %s", r.json())
        else:
            log.info("In dry-run mode so not making gitlab trigger POST")

    def kickoff_from_kitmaker(self):
        url = os.getenv("CI_API_V4_URL") or self.CI_API_V4_URL
        project_id = os.getenv("CI_PROJECT_ID") or self.CI_PROJECT_ID
        dry_run = os.getenv("DRY_RUN") or self.dry_run
        no_test = os.getenv("NO_TEST") or self.no_test
        no_scan = os.getenv("NO_SCAN") or self.no_scan
        no_push = os.getenv("NO_PUSH") or self.no_push
        token = os.getenv("CI_JOB_TOKEN")
        if not token:
            log.warning("CI_JOB_TOKEN is unset!")
        ref = os.getenv("CI_COMMIT_REF_NAME") or self.branch
        payload = {"token": token, "ref": self.branch, "variables[KITMAKER]": "true"}
        if no_scan:
            payload[f"variables[NO_SCAN]"] = "true"
        if no_test:
            payload[f"variables[NO_TEST]"] = "true"
        if no_push:
            payload[f"variables[NO_PUSH]"] = "true"
        if self.l4t:
            payload[f"variables[L4T]"] = "true"
        payload[f"variables[TRIGGER]"] = "true"
        payload[f"variables[RELEASE_LABEL]"] = self.release_label
        payload[f"variables[IMAGE_TAG_SUFFIX]"] = f"-{self.candidate_number}"
        payload[f"variables[CANDIDATE_URL]"] = self.candidate_url
        payload[f"variables[WEBHOOK_URL]"] = self.webhook_url

        final_url = f"{url}/projects/{project_id}/trigger/pipeline"
        log.info("url %s", final_url)
        masked_payload = payload.copy()
        masked_payload["token"] = "[ MASKED ]"
        log.info("payload %s", masked_payload)

        if not self.dry_run:
            r = requests.post(final_url, data=payload)
            log.debug("response status code %s", r.status_code)
            log.debug("response body %s", r.json())
        else:
            log.info("In dry-run mode so not making gitlab trigger POST")

    def main(self):
        if self.dry_run:
            log.info("Dryrun mode enabled. Not making changes")

        if self.parent.shipit_uuid:
            # Make sure all of our arguments are present
            if any(
                [
                    not i
                    for i in [
                        self.release_label,
                        self.candidate_number,
                        self.candidate_url,
                        self.webhook_url,
                        self.branch,
                    ]
                ]
            ):
                # Plumbum doesn't allow this check
                log.error(
                    """Missing arguments (one or all): ["--release_label", "--candidate-number", "--candidate_url", "--webhook-url", "--branch"]"""
                )
                sys.exit(1)
            log.debug("Triggering gitlab kitmaker pipeline using shipit source")
            self.kickoff_from_kitmaker()
        else:
            self.check_explicit_trigger()
            if self.trigger_all or self.trigger_explicit:
                self.kickoff()


@Manager.subcommand("push")
class ManagerContainerPush(Manager):
    DESCRIPTION = (
        "Login and push to the container registries.\n"
        "Use either --image-name, --os-name, --os-version, --cuda-version 'to push images' or --readme 'to push readmes'."
    )

    dry_run = cli.Flag(["-n", "--dry-run"], help="Show output but don't do anything!")

    image_name = cli.SwitchAttr(
        "--image-name",
        str,
        requires=["--os-name", "--os-version", "--cuda-version"],
        excludes=["--readme"],
        help="The image name to tag",
        default="",
    )

    distro = cli.SwitchAttr(
        "--os-name",
        str,
        requires=["--image-name", "--os-version", "--cuda-version"],
        help="The distro to use",
        default=None,
    )

    distro_version = cli.SwitchAttr(
        "--os-version",
        str,
        requires=["--image-name", "--os-name", "--cuda-version"],
        help="The distro version",
        default=None,
    )

    cuda_version = cli.SwitchAttr(
        "--cuda-version",
        str,
        requires=["--image-name", "--os-name", "--os-version"],
        help="The cuda version to use. Example: '10.1'",
        default=None,
    )

    image_tag_suffix = cli.SwitchAttr(
        "--tag-suffix",
        str,
        help="The suffix to append to the tag name. Example 10.1-base-centos6<suffix>",
        default="",
    )

    arch = cli.SwitchAttr(
        "--arch",
        cli.Set("x86_64", "ppc64le", "arm64", case_sensitive=False),
        requires=["--image-name", "--os-name", "--os-version", "--cuda-version"],
        help="Push images for a particular architecture",
    )

    pipeline_name = cli.SwitchAttr(
        "--pipeline-name",
        str,
        help="The name of the pipeline the deploy is coming from",
    )

    tag_manifest = cli.SwitchAttr("--tag-manifest", str, help="A list of tags to push",)

    readme = cli.Flag("--readme", help="Path to the README.md",)

    l4t = cli.Flag(["--l4t"], help="Flag the push as being for L4T",)

    client = None
    repos = []
    repos_dict = {}
    tags = []
    key = ""
    #  copy_failed = False
    repo_creds = {}

    def setup_repos(self):
        # 09:43 Sat Jul 10 2021: jesusa: Disabled at the distro level because it has historically not been used.
        #  distro_push_repos = self.get_data(
        #      self.parent.manifest,
        #      self.key,
        #      f"{self.distro}{self.distro_version}",
        #      "push_repos",
        #  )
        push_repos = self.get_data(self.parent.manifest, self.key, "push_repos")
        excluded_repos = self.get_data(
            self.parent.manifest,
            self.key,
            f"{self.distro}{self.distro_version}",
            self.arch,
            "exclude_repos",
            can_skip=True,
        )

        #  __import__("pprint").pprint(self.parent.manifest)
        #  __import__("pprint").pprint(push_repos)
        #  print(self.key)
        #  sys.exit(1)
        for repo, metadata in push_repos.items():
            if "gitlab-master" in repo:
                # Images have already been pushed to gitlab by this point
                log.debug(f"Skipping push to {repo}")
                continue
            if metadata.get("only_if", False) and not os.getenv(metadata["only_if"]):
                log.info("repo: '%s' only_if requirement not satisfied", repo)
                continue
            if push_repos and repo not in push_repos:
                log.info("repo: '%s' is excluded for this image", repo)
                continue
            if excluded_repos and repo in excluded_repos:
                log.info("repo: '%s' is excluded for this image", repo)
                continue
            #  if self.arch not in metadata["image_name"]:
            #      log.debug(f"{repo} does not contain an entry for arch: {self.arch}")
            #      continue
            user = os.getenv(metadata["user"])
            if not user:
                user = metadata["user"]
            passwd = os.getenv(metadata["pass"])
            if not passwd:
                passwd = metadata["pass"]
            registry = metadata["image_name"]
            self.repo_creds[registry] = {"user": user, "pass": passwd}
            self.repos.append(registry)
        if not self.repos:
            log.fatal(
                "Could not retrieve container image repo credentials. Environment not set?"
            )
            sys.exit(1)

    @retry(
        (ImagePushRetry),
        tries=HTTP_RETRY_ATTEMPTS,
        delay=HTTP_RETRY_WAIT_SECS,
        logger=log,
    )
    def push_images(self):
        with open(self.tag_manifest) as f:
            tags = f.readlines()
        stags = [x.strip() for x in tags]
        for tag in stags:
            if not tag:
                continue
            log.info("Processing image: %s:%s", self.image_name, tag)
            for repo in self.repos:
                log.info("COPYING to: %s:%s", repo, tag)
                if self.dry_run:
                    log.debug("dry-run; not copying")
                    continue
                if shellcmd(
                    "skopeo",
                    (
                        "copy",
                        "--all",
                        "--src-creds",
                        "{}:{}".format("gitlab-ci-token", os.getenv("CI_JOB_TOKEN")),
                        "--dest-creds",
                        "{}:{}".format(
                            self.repo_creds[repo]["user"],
                            self.repo_creds[repo]["pass"],
                        ),
                        f"docker://{self.image_name}:{tag}",
                        f"docker://{repo}:{tag}",
                    ),
                ):
                    log.info("Copy was successful")
                    #  self.copy_failed = False
                else:
                    raise ImagePushRetry()
                #  if self.copy_failed:
                #      log.warning("Copy failed!")
                #      log.error("Errors were encountered copying images!")
                #      sys.exit(1)

    #  def auth_registries(self):
    #      for repo, metadata in self.parent.manifest[self.key].items():
    #          registry = {}
    #          if repo in (
    #              "gitlab-master",
    #              "artifactory",
    #              "nvcr.io",
    #          ):  # TODO: push to Nvidia Registry
    #              log.debug(f"Skipping push to {repo}")
    #              continue
    #          if metadata.get("only_if", False) and not os.getenv(metadata["only_if"]):
    #              log.info("repo: '%s' only_if requirement not satisfied", repo)
    #              continue
    #          user = os.getenv(metadata["user"])
    #          if not user:
    #              user = metadata["user"]
    #          passwd = os.getenv(metadata["pass"])
    #          if not passwd:
    #              passwd = metadata["pass"]
    #          self.repo_creds[repo] = {"user": user, "pass": passwd}
    #          for arch in ("x86_64", "ppc64le", "arm64"):
    #              registry[f"README-{arch}.md"] = metadata["registry"][arch]
    #          self.repos_dict[repo] = registry

    #      if not self.repos_dict:
    #          log.fatal("Could not retrieve registry credentials. Environment not set?")
    #          sys.exit(1)
    #      # docker login
    #      result = shellcmd(
    #          "docker",
    #          (
    #              "login",
    #              f"-u" f"{self.repo_creds['docker.io']['user']}",
    #              f"-p" f"{self.repo_creds['docker.io']['pass']}",
    #          ),
    #          printOutput=False,
    #          returnOut=True,
    #      )
    #      if result.returncode > 0:
    #          log.error(result.stderr)
    #          log.error("Docker login failed!")
    #          sys.exit(1)
    #      else:
    #          log.info("Docker login was successful.")

    def push_readmes(self):
        if self.dry_run:
            log.debug(
                f"dry-run mode: otherwise; docker pushrm could happen for -> {self.repos_dict['docker.io']}"
            )
        else:
            for readme, repo in self.repos_dict["docker.io"].items():
                # docker pushrm
                result = shellcmd(
                    "docker",
                    ("pushrm", "-f", f"doc/{readme}", f"{repo}"),
                    printOutput=False,
                    returnOut=True,
                )
                if result.returncode > 0:
                    log.error(result.stderr)
                    log.error("Docker pushrm was unsuccessful for %s", repo)
                else:
                    log.info("Docker pushrm was successful for %s", repo)

    def main(self):
        log.debug("dry-run: %s", self.dry_run)
        if self.readme:
            self.key = f"push_repos"
            self.auth_registries()
            self.push_readmes()
        else:
            self.key = f"cuda_v{self.cuda_version}"
            if self.pipeline_name:
                self.key = f"cuda_v{self.cuda_version}_{self.pipeline_name}"
            self.client = docker.DockerClient(
                base_url="unix://var/run/docker.sock", timeout=600
            )
            self.setup_repos()
            self.push_images()
        log.info("Done")


@Manager.subcommand("generate")
class ManagerGenerate(Manager):
    DESCRIPTION = "Generate Dockerfiles from templates."

    cuda = {}
    dist_base_path = None  # pathlib object. The parent "base" path of output_path.
    output_manifest_path = None  # pathlib object. The path to save the shipit manifest.
    output_path = {}  # The product of parsing the input templates
    key = ""
    cuda_version_is_release_label = False
    cuda_version_regex = re.compile(r"cuda_v([\d\.]+)(?:_(\w+))?$")

    product_name = ""
    candidate_number = ""

    template_env = Environment(
        extensions=["jinja2.ext.do"], trim_blocks=True, lstrip_blocks=True
    )

    generate_ci = cli.Flag(["--ci"], help="Generate the gitlab pipelines only.",)

    generate_all = cli.Flag(["--all"], help="Generate all of the templates.",)

    generate_readme = cli.Flag(["--readme"], help="Generate all readmes.",)

    generate_tag = cli.Flag(
        ["--tags"], help="Generate all supported and unsupported tag lists.",
    )

    distro = cli.SwitchAttr(
        "--os-name",
        str,
        group="Targeted",
        excludes=["--all", "--readme", "--tags"],
        help="The distro to use.",
        default=None,
    )

    distro_version = cli.SwitchAttr(
        "--os-version",
        str,
        group="Targeted",
        excludes=["--all", "--readme", "--tags"],
        help="The distro version",
        default=None,
    )

    cuda_version = cli.SwitchAttr(
        "--cuda-version",
        str,
        excludes=["--all", "--readme", "--tags"],
        group="Targeted",
        help="[DEPRECATED for newer cuda versions!] The cuda version to use. Example: '11.2'",
        default=None,
    )

    release_label = cli.SwitchAttr(
        "--release-label",
        str,
        excludes=["--readme", "--tags"],
        group="Targeted",
        help="The cuda version to use. Example: '11.2.0'",
        default=None,
    )

    #  arch = cli.SwitchAttr(
    #      "--arch",
    #      cli.Set("x86_64", "ppc64le", "arm64", case_sensitive=False),
    #      excludes=["--all", "--readme", "--tags"],
    #      group="Targeted",
    #      help="Generate container scripts for a particular architecture.",
    #  )

    pipeline_name = cli.SwitchAttr(
        "--pipeline-name",
        str,
        excludes=["--all", "--readme", "--tags"],
        group="Targeted",
        help="Use a pipeline name for manifest matching.",
        default="default",
    )

    flavor = cli.SwitchAttr(
        "--flavor", str, help="Identifier passed to template context.",
    )

    #
    # WAR ONLY USED FOR L4T and will be removed in the future
    #
    cudnn_json_path = cli.SwitchAttr(
        "--cudnn-json-path",
        str,
        group="L4T",
        help="File path to json encoded file containing cudnn package metadata.",
    )

    def supported_distro_list_by_cuda_version(self, version):
        if not version:
            return
        distros = ["ubuntu", "ubi", "centos"]
        keys = self.parent.manifest[self.key].keys()

        # There are other keys in the cuda field other than distros, we need to strip those out
        def get_distro_name(name):
            r = re.compile("[a-zA-Z]+")
            return r.findall(name)[0]

        return [f for f in keys if get_distro_name(f) in distros]

    def supported_arch_list(self):
        ls = []
        for k in glom.glom(
            self.parent.manifest,
            glom.Path(self.key, f"{self.distro}{self.distro_version}"),
        ):
            if k in ["x86_64", "ppc64le", "arm64"]:
                ls.append(k)
        return ls

    def cudnn_versions(self, arch):
        obj = []
        for k, v in self.cuda[arch]["components"].items():
            if k.startswith("cudnn") and v:
                obj.append(k)
        return obj

    def matched(self, key):
        match = self.cuda_version_regex.match(key)
        if match:
            return match

    # extracts arbitrary keys and inserts them into the templating context
    def extract_keys(self, val, arch=None):
        rgx = re.compile(r"^v\d+\.\d")
        for k, v in val.items():
            if rgx.match(k):
                # Do not copy cuda version keys
                continue
            # These top level keys should be ignored since they are processed elsewhere
            if k in [
                "exclude_repos",
                "build_version",
                "components",
                *self.supported_arch_list(),
                *self.supported_distro_list_by_cuda_version(
                    self.cuda_version or self.release_label
                ),
            ]:
                continue
            if arch:
                self.cuda[arch][k] = v
            else:
                self.cuda[k] = v

    # For cudnn templates, we need a custom template context
    def output_cudnn_template(self, cudnn_version_name, input_template, output_path):
        new_ctx = {
            "cudnn": self.cuda["cudnn"],
            "version": self.cuda["version"],
            "image_tag_suffix": self.cuda["image_tag_suffix"],
            "os": self.cuda["os"],
        }
        for arch in self.arches:
            cudnn_manifest = self.cuda[arch]["components"][cudnn_version_name]
            if cudnn_manifest:
                if "source" in cudnn_manifest:
                    cudnn_manifest["basename"] = os.path.basename(
                        cudnn_manifest["source"]
                    )
                    cudnn_manifest["dev"]["basename"] = os.path.basename(
                        cudnn_manifest["dev"]["source"]
                    )
                new_ctx[arch] = {}
                new_ctx[arch]["cudnn"] = cudnn_manifest

        #  __import__("pprint").pprint(new_ctx)
        log.debug("cudnn template context: %s", new_ctx)
        #  sys.exit()
        self.output_template(
            input_template=input_template, output_path=output_path, ctx=new_ctx
        )

    def output_template(self, input_template, output_path, ctx=None):
        ctx = ctx if ctx is not None else self.cuda
        #  print(output_path)
        #  raise

        def write_template(arch=None):
            with open(input_template) as f:
                log.debug("Processing template %s", input_template)
                new_output_path = pathlib.Path(output_path)
                extension = ".j2"
                name = input_template.name
                if "dockerfile" in input_template.name.lower():
                    new_filename = "Dockerfile"
                elif ".jinja" in str(input_template):
                    extension = ".jinja"
                    new_filename = (
                        name[: -len(extension)] if name.endswith(extension) else name
                    )
                else:
                    new_filename = (
                        name[len("base-") : -len(extension)]
                        if name.startswith("base-") and name.endswith(extension)
                        else name
                    )
                if arch:
                    new_filename += f"-{arch}"
                template = self.template_env.from_string(f.read())
                if not new_output_path.exists():
                    log.debug(f"Creating {new_output_path}")
                    new_output_path.mkdir(parents=True)
                log.info(f"Writing {new_output_path}/{new_filename}")
                with open(f"{new_output_path}/{new_filename}", "w") as f2:
                    f2.write(template.render(cuda=ctx))
                #  sys.exit(1)

        if any(f in input_template.as_posix() for f in ["cuda.repo", "ml.repo"]):
            for arch in self.arches:
                ctx["target_arch"] = arch
                if "arm64" in arch:
                    ctx["target_arch"] = "sbsa"
                #  output_path =
                write_template(arch)
        else:
            write_template()

    def prepare_context(self):
        # checks the cudnn components and ensures at least one is installed from the public "machine-learning" repo
        def use_ml_repo(arch):
            use_ml_repo = False
            # First check the manifest to see if a ml repo url is specified
            #  log.debug(
            #      f"self.key: {self.key} distro: {self.distro}{self.distro_version} arch: {arch}"
            #  )
            ml_repo_url = self.get_data(
                self.parent.manifest,
                self.key,
                f"{self.distro}{self.distro_version}",
                "ml_repo_url",
                can_skip=True,
            )
            if not ml_repo_url:
                log.warning(
                    f"ml_repo_url not set for {self.key}.{self.distro}{self.distro_version}.{arch} in manifest"
                )
                return False
            use_ml_repo = True
            # if a cudnn component contains "source", then it is installed from a different source than the public machine
            # learning repo
            # If any of the cudnn components lack the source key, then the ML repo should be used
            for comp, val in self.cuda[arch]["components"].items():
                if next(
                    (True for mlcomp in ["cudnn", "nccl"] if mlcomp in comp), False
                ):
                    if val and "source" in val:
                        use_ml_repo = False
            return use_ml_repo

        conf = self.parent.manifest
        if self.release_label:
            major = self.release_label.split(".")[0]
            minor = self.release_label.split(".")[1]
        else:
            major = self.cuda_version.split(".")[0]
            minor = self.cuda_version.split(".")[1]

        self.image_tag_suffix = self.get_data(
            conf,
            self.key,
            f"{self.distro}{self.distro_version}",
            "image_tag_suffix",
            can_skip=True,
        )
        if not self.image_tag_suffix:
            self.image_tag_suffix = ""

        # The templating context. This data structure is used to fill the templates.
        self.cuda = {
            "flavor": self.flavor,
            "version": {
                "release_label": self.cuda_version,
                #  if self.cuda_version_is_release_label
                #  else (self.release_label or legacy_release_label),
                "major": major,
                "minor": minor,
                "major_minor": f"{major}.{minor}",
            },
            "arches": self.arches,
            "os": {"distro": self.distro, "version": self.distro_version},
            "image_tag_suffix": self.image_tag_suffix,
        }

        self.extract_keys(
            self.get_data(conf, self.key, f"{self.distro}{self.distro_version}",)
        )

        for arch in self.arches:
            self.cuda[arch] = {}
            # Only set in version < 11.0
            self.cuda[arch]["build_version"] = self.get_data(
                conf,
                self.key,
                f"{self.distro}{self.distro_version}",
                arch,
                "components",
                "build_version",
                can_skip=True,
            )
            self.cuda[arch]["components"] = self.get_data(
                conf,
                self.key,
                f"{self.distro}{self.distro_version}",
                arch,
                "components",
            )
            self.cuda[arch]["use_ml_repo"] = use_ml_repo(arch)
            self.extract_keys(
                self.get_data(
                    conf, self.key, f"{self.distro}{self.distro_version}", arch,
                ),
                arch=arch,
            )

        legacy_release_label = None
        #  if build_version:
        #      legacy_release_label = f"{self.cuda_version}.{build_version}"
        #  log.debug(f"build_version: {build_version}")

        log.debug("template context %s" % (self.cuda))
        #  __import__("pprint").pprint(self.cuda)
        #  sys.exit(1)

    def generate_cudnn_scripts(self, base_image, input_template):
        for arch in self.arches:
            for pkg in self.cudnn_versions(arch):
                if not "cudnn" in self.cuda:
                    self.cuda["cudnn"] = {}
                self.cuda["cudnn"]["target"] = base_image
                self.output_cudnn_template(
                    cudnn_version_name=pkg,
                    input_template=pathlib.Path(input_template),
                    output_path=pathlib.Path(f"{self.output_path}/{base_image}/{pkg}"),
                )

    # CUDA 8 uses a deprecated image layout
    def generate_containerscripts_cuda_8(self):
        for img in ["devel", "runtime"]:
            base = img
            if img == "runtime":
                # for CUDA 8, runtime == base
                base = "base"
            temp_path = self.cuda["template_path"]
            log.debug("temp_path: %s, output_path: %s", temp_path, self.output_path)
            self.output_template(
                input_template=pathlib.Path(f"{temp_path}/{base}/Dockerfile.jinja"),
                output_path=pathlib.Path(f"{self.output_path}/{img}"),
            )
            # We need files in the base directory
            for filename in pathlib.Path(f"{temp_path}/{base}").glob("*"):
                if "Dockerfile" in filename.name:
                    continue
                log.debug("Checking %s", filename)
                if ".jinja" in filename.name:
                    self.output_template(filename, f"{self.output_path}/{img}")
                else:
                    log.info(f"Copying {filename} to {self.output_path}/{img}")
                    shutil.copy(filename, f"{self.output_path}/{img}")
            # cudnn image
            self.generate_cudnn_scripts(img, f"{temp_path}/cudnn/Dockerfile.jinja")

    def generate_containerscripts(self):
        for img in ["base", "devel", "runtime"]:
            self.cuda["target"] = img

            globber = f"*"
            if "legacy" in self.cuda["template_path"]:
                temp_path = pathlib.Path(self.cuda["template_path"], img)
                cudnn_template_path = pathlib.Path(
                    self.cuda["template_path"], f"cudnn/Dockerfile.jinja"
                )
                input_template = f"{temp_path}/Dockerfile.jinja"
            else:
                temp_path = pathlib.Path(self.cuda["template_path"])
                input_template = pathlib.Path(temp_path, f"{img}-dockerfile.j2")
                cudnn_template_path = pathlib.Path(temp_path, "cudnn-dockerfile.j2")
                globber = f"{img}-*"

            log.debug(
                "template_path: %s, output_path: %s", temp_path, self.output_path,
            )

            self.output_template(
                input_template=pathlib.Path(input_template),
                output_path=pathlib.Path(f"{self.output_path}/{img}"),
            )

            # copy files
            log.debug(f"temp_path: {temp_path} img: {img}")
            for filename in pathlib.Path(temp_path).glob(globber):
                log.info(f"have template: {filename}")
                if "dockerfile" in filename.name.lower():
                    continue
                log.debug("Checking %s", filename)
                #  __import__("pprint").pprint(self.cuda)
                #  sys.exit(1)
                if not self.cuda[self.cuda["arches"][0]][
                    "use_ml_repo"
                ] and "nvidia-ml" in str(filename):
                    log.warning("Not setting ml-repo!")
                    continue
                if any(f in filename.name for f in [".j2", ".jinja"]):
                    self.output_template(filename, f"{self.output_path}/{img}")

            # cudnn image
            if "base" not in img:
                self.generate_cudnn_scripts(img, cudnn_template_path)

    # fmt: off
    def generate_gitlab_pipelines(self):

        manifest = self.parent.manifest
        ctx = {"manifest_path": self.parent.manifest_path}

        def get_cudnn_components(key, distro, arch):
            comps = {}
            for comp, val in manifest[key][distro][arch]["components"].items():
                if "cudnn" in comp and val:
                    #  print(comp, val)
                    comps[comp] = {}
                    comps[comp]["version"] = val["version"]
            return comps

        for k, _ in manifest.items():
            if (match := self.matched(k)) is None:
                log.debug("No match for %s" % k)
                continue

            log.info("Adding pipeline '%s'" % k)
            cuda_version = match.group(1)
            if (pipeline_name := match.group(2)) is None:
                pipeline_name = "default"
            log.debug("matched cuda_version: %s" % cuda_version)
            log.debug("matched pipeline_name: %s" % pipeline_name)

            if cuda_version not in ctx:
                ctx[cuda_version] = {}
            ctx[cuda_version][pipeline_name] = {}
            ctx[cuda_version][pipeline_name]["cuda_version_yaml_safe"] = cuda_version.replace(".", "_")

            key = f"cuda_v{cuda_version}"
            if pipeline_name and pipeline_name != "default":
                key = f"cuda_v{cuda_version}_{pipeline_name}"

            #  log.debug("key: '%s'" % key)
            #  log.debug("cuda_version: '%s'" % cuda_version)
            ctx[cuda_version][pipeline_name]["dist_base_path"] = self.get_data(manifest, key, "dist_base_path")
            ctx[cuda_version][pipeline_name]["pipeline_name"] = self.pipeline_name

            for distro, _ in manifest[key].items():
                dmrgx = re.compile(r"(?P<name>[a-zA-Z]+)(?P<version>[\d\.]+)$")
                if (dm := dmrgx.match(distro)) is None:
                    continue

                #  log.debug("distro: '%s'" % distro)
                #  log.debug("pipeline_name: '%s'" % pipeline_name)
                if not "distros" in ctx[cuda_version][pipeline_name]:
                    ctx[cuda_version][pipeline_name]["distros"] = {}
                ctx[cuda_version][pipeline_name]["distros"][distro] = {}
                ctx[cuda_version][pipeline_name]["distros"][distro]["name"] = dm.group('name')
                ctx[cuda_version][pipeline_name]["distros"][distro]["version"] = dm.group('version')
                ctx[cuda_version][pipeline_name]["distros"][distro]["yaml_safe"] = distro.replace(".", "_")
                image_tag_suffix = self.get_data(manifest, key, distro, "image_tag_suffix", can_skip=True)
                ctx[cuda_version][pipeline_name]["distros"][distro]["image_tag_suffix"] = ""

                if image_tag_suffix:
                    ctx[cuda_version][pipeline_name]["distros"][distro]["image_tag_suffix"] = image_tag_suffix

                ctx[cuda_version][pipeline_name]["distros"][distro]["arches"] = []

                for arch, _ in manifest[key][distro].items():
                    if arch not in ["arm64", "ppc64le", "x86_64"]:
                        continue

                    #  log.debug("arch: '%s'" % arch)
                    no_os_suffix = self.get_data(manifest, key, distro, "no_os_suffix", can_skip=True)
                    ctx[cuda_version][pipeline_name]["image_name"] = self.get_data(manifest, key, "image_name")

                    if "no_os_suffix" not in ctx[cuda_version][pipeline_name]["distros"][distro]:
                        ctx[cuda_version][pipeline_name]["distros"][distro]["no_os_suffix"] = {}

                    ctx[cuda_version][pipeline_name]["distros"][distro]["no_os_suffix"] = (True if no_os_suffix else False)
                    ctx[cuda_version][pipeline_name]["distros"][distro]["arches"].append(arch)

                    if "cudnn" not in ctx[cuda_version][pipeline_name]["distros"][distro]:
                        ctx[cuda_version][pipeline_name]["distros"][distro]["cudnn"] = {}
                    cudnn_comps = get_cudnn_components(key, distro, arch)
                    if cudnn_comps:
                        ctx[cuda_version][pipeline_name]["distros"][distro]["cudnn"][arch] = cudnn_comps

        #  __import__('pprint').pprint(ctx)
        #  log.debug(f"ci pipline context: {ctx}")
        #  sys.exit(1)

        input_template = pathlib.Path("templates/gitlab/gitlab-ci.yml.jinja")
        with open(input_template) as f:
            log.debug("Processing template %s", input_template)
            output_path = pathlib.Path(".gitlab-ci.yml")
            template = self.template_env.from_string(f.read())
            with open(output_path, "w") as f2:
                f2.write(template.render(cuda=ctx))
            #  sys.exit(1)

    def generate_readmes(self):

        distros = []  # local list variable to hold different distros

        # to capture all release labels and corresponding Dockerfile's paths
        release_info = {}
        cuda_release_info = {}

        manifest = self.parent.manifest
        path = {"manifest_path": self.parent.manifest_path}

        def get_releaseInfo_and_dockerfilePath(path):

            for dirpath, directories, files in os.walk(path):
                refPath = dirpath.split("dist/")
                for file in files:
                    if file == "Dockerfile":
                        labels = {}
                        releaseLabel = ""
                        dockerfilePath = os.path.join(refPath[1], file)
                        dockerfilePathList = dockerfilePath.split("/")

                        for value in dockerfilePathList:
                            if re.compile(r"([\d\.]+)").match(value):
                                labels[1] = value
                            if "cudnn" in value:
                                labels[2] = value
                            if value in ("base", "devel", "runtime"):
                                labels[3] = value
                            if re.compile(r"centos*|ubuntu*|ubi*").match(value):
                                operating_system = value.split("-")
                                labels[4] = operating_system[0]
                                distros.append(labels[4])

                        for key in sorted(labels.keys()):
                            if not releaseLabel:
                                releaseLabel = releaseLabel + labels[key]
                            else:
                                releaseLabel = releaseLabel + "-" + labels[key]

                        # storing all release info in a dictionary variable
                        release_info[dockerfilePath] = releaseLabel

        for key, _ in manifest.items():
            if match := self.matched(key):
                if self.cuda_version_regex.match(key):
                    path['dist_base_path'] = self.get_data(manifest, key, "dist_base_path")
                    path['release_label'] = self.get_data(manifest, key, "release_label")
                    # log.debug(ctx)
                    get_releaseInfo_and_dockerfilePath(path['dist_base_path'])
                    break  # to keep data for latest available version only

        dist_path_list = path['dist_base_path'].split("/")

        # to get all unique supported operating system names
        distros = set(distros)
        os_name = []  # to store names in required format like "CentOS 8", "Ubuntu 20.04" etc.

        for OS in distros:
            if "centos" in OS:
                distro = OS.split("centos")
                os_name.append(f'CentOS {distro[1]}')
            elif "ubuntu" in OS:
                distro = OS.split("ubuntu")
                os_name.append(f'Ubuntu {distro[1]}')
            else:
                distro = OS.split("ubi")
                os_name.append(f'UBI {distro[1]}')

        # to help populate the OS types in all readmes in a sorted manner
        for keys in sorted(release_info.keys(), reverse=True):
            cuda_release_info[keys] = release_info[keys]

        for arch in ("x86_64", "arm64", "ppc64le"):
            # a data structure to manipulate readme template
            readme = {'latest_version': dist_path_list[1],
                      'release_label': path['release_label'],
                      'cuda_release_info': cuda_release_info,
                      'os_name': os_name,
                      'arch': arch}

            input_template = pathlib.Path("templates/doc/README.md.jinja")
            with open(input_template) as rf:
                log.debug("Processing template %s for architecture %s", input_template, arch)
                output_path = pathlib.Path(f'doc/README-{arch}.md')
                template = self.template_env.from_string(rf.read())
                with open(output_path, "w") as wf:
                    wf.write(template.render(readme=readme))
                log.debug("README-%s.md created under doc/", arch)

    def generate_tags(self):

        tag_list = []  # local list variable to hold tags from dockerhub
        distros_list = []  # local list variable to hold distros from dockerhub
        cuda_releases = {}  # local dict variable for all CUDA releases
        unsupported_release_labels = []  # to grab unsupported CUDA releases from manifest.yaml
        unsupported_distros = []  # to grab unsupported CUDA distros from manifest.yaml
        # for all supported CUDA releases
        supported_cuda_releases = {}
        supported_distros = []

        docker_repo = "docker.io/nvidia/cuda"

        def get_repo_tags(repo):
            return shellcmd(
                "skopeo",
                ("list-tags", f"docker://{repo}"),
                printOutput=False,
                returnOut=True
            )

        try:
            tag_dict = json.loads(get_repo_tags(docker_repo).stdout)
        except:
            log.error("Some problem occurred in getting tags from DockerHub")
            sys.exit(1)

        for key in tag_dict.keys():
            if "Tags" in key:
                tag_list = list(tag_dict[key])

        for tags in tag_list:
            if "ubuntu" in tags:
                ubuntu_tags = tags.split("-")
                for tag in ubuntu_tags:
                    if "ubuntu" in tag:
                        distros_list.append(tag)
            elif "centos" in tags:
                centos_tags = tags.split("-")
                distros_list.append(centos_tags[len(centos_tags)-1])
            elif "ubi" in tags:
                ubi_tags = tags.split("-")
                distros_list.append(ubi_tags[len(ubi_tags)-1])
        distros_set = set(distros_list)

        manifest = self.parent.manifest

        for key, _ in manifest.items():
            if match := self.matched(key):
                if self.cuda_version_regex.match(key):
                    new_key = key.split("v")
                    cuda_releases[new_key[1]] = self.get_data(manifest, key, "release_label")
            if key == "unsupported":
                unsupported_distros = self.get_data(manifest, key, "distros")
                unsupported_release_labels = self.get_data(manifest, key, "release_label")

        for distro in distros_set:
            if distro not in unsupported_distros:
                supported_distros.append(distro)

        for key, value in cuda_releases.items():
            if value not in unsupported_release_labels:
                supported_cuda_releases[key] = cuda_releases[key]

        # update cuda_releases with unsupported release info
        for label in unsupported_release_labels:
            if re.compile(r"([\d\.]+)$").match(str(label)):
                cuda_releases[str(label)] = label
            else:  # to handle special cases like 11.0 RC and 11.0 Update 1
                tag = label.split(" ")
                if len(tag) == 2:
                    cuda_releases[tag[0]] = label
                else:
                    cuda_releases[(tag[0]+"."+tag[len(tag)-1])] = label
        # log.debug(cuda_releases)

        supported = {'cuda_tags': tag_list,
                     'supported_distros': sorted(supported_distros, reverse=True),
                     'supported_cuda_releases': supported_cuda_releases}

        unsupported = {'cuda_tags': tag_list,
                       'cuda_releases': cuda_releases,
                       'unsupported_distros': sorted(unsupported_distros, reverse=True),
                       'unsupported_cuda_releases': unsupported_release_labels,
                       'supported_distros': sorted(supported_distros, reverse=True)}

        for tag in ("supported", "unsupported"):
            if "unsupported" in tag:
                tags = unsupported
            else:
                tags = supported
            input_template = pathlib.Path(f'templates/doc/{tag}-tags.md.Jinja')
            with open(input_template) as rf:
                log.debug("Processing template %s for %s tags", input_template, tag)
                output_path = pathlib.Path(f'doc/{tag}-tags.md')
                template = self.template_env.from_string(rf.read())
                with open(output_path, "w") as wf:
                    wf.write(template.render(tags=tags))

    # fmt: on
    def get_shipit_funnel_json(self):
        modified_cuda_version = self.release_label.replace(".", "-")
        funnel_distro = self.distro
        if any(distro in funnel_distro for distro in ["centos", "ubi"]):
            funnel_distro = "rhel"
        modified_distro_version = self.distro_version.replace(".", "")
        modified_arch = self.arch.replace("_", "-")
        if modified_arch == "arm64":
            modified_arch = "sbsa"
        shipit_distro = f"{funnel_distro}{modified_distro_version}"
        if "tegra" in self.product_name:
            shipit_distro = "l4t"
            modified_arch = "aarch64"
        last_dot_index = self.release_label.rfind(".")

        platform_name = (
            f"{shipit_distro}-{self.product_name}-linux-{modified_arch}.json"
        )
        shipit_json = f"http://cuda-internal.nvidia.com/funnel/{self.parent.shipit_uuid}/{platform_name}"
        log.info(f"Retrieving funnel json from: {shipit_json}")
        return self.parent.get_http_json(shipit_json)

    def get_shipit_global_json(self):
        global_json = f"http://cuda-internal.nvidia.com/funnel/{self.parent.shipit_uuid}/global.json"
        log.info(f"Retrieving global json from: {global_json}")
        return self.parent.get_http_json(global_json)

    # Returns a list of packages used in the templates
    def template_packages(self):
        # 21:31 Tue Jul 13 2021 FIXME (jesusa): this func feels like a hack
        log.info(f"current directory: {os.getcwd()}")
        temp_dir = "ubuntu"
        if any(distro in self.distro for distro in ["centos", "ubi"]):
            temp_dir = "redhat"
        # sometimes the old ways are the best ways...
        cmd = (
            find[
                f"templates/{temp_dir}/",
                "-type",
                "f",
                "-iname",
                "*.j2",
                "-exec",
                "grep",
                "^ENV\ NV_.*_VERSION\ .*$",
                "{}",
                ";",
            ]
            | cut["-f", "2", "-d", " "]
            | sort["-u"]
        )
        log.debug(f"command: {cmd}")
        # When docker:stable (alpine) has python 3.9...
        #  return [x.removesuffix("_component_version") for x in cmd().splitlines()]
        return [
            x[3 : -len("_VERSION")].lower()
            for x in cmd().splitlines()
            if "_VERSION" in x and not "CUDA_LIB" in x
        ]

    def pkg_rel_from_package_name(self, name, version):
        rgx = re.search(fr"[\w\d-]*{version}-(\d)_?", name)
        if rgx:
            return rgx.group(1)

    def shipit_components(self, shipit_json, packages):
        components = {}

        fragments = shipit_json["fragments"]

        def fragment_by_name(name):
            name_with_hyphens = name.replace("_", "-")
            for k, v in fragments.items():
                for k2, v2 in v.items():
                    if any(x in v2["name"] for x in [name, name_with_hyphens]):
                        return v2

        for pkg in packages:
            #  log.debug(f"package: {pkg}")
            fragment = fragment_by_name(pkg)
            if not fragment:
                log.warning(f"{pkg} was not found in the fragments json!")
                continue

            name = fragment["name"]
            version = fragment["version"]

            pkg_rel = self.pkg_rel_from_package_name(name, version)
            assert pkg_rel  # should always have a value

            pkg_no_prefix = pkg[len("cuda_") :] if pkg.startswith("cuda_") else pkg

            # rename "devel" to "dev" to keep things consistant with ubuntu
            if "_devel" in pkg_no_prefix:
                pkg_no_prefix = pkg_no_prefix.replace("_devel", "_dev")

            log.debug(
                f"component: {pkg_no_prefix} version: {version} pkg_rel: {pkg_rel}"
            )

            components.update({f"{pkg_no_prefix}": {"version": f"{version}-{pkg_rel}"}})

        return components

    def kitpick_repo_url(self, global_json):
        repo_distro = self.distro
        if any(x in repo_distro for x in ["ubi", "centos"]):
            repo_distro = "rhel"
        clean_distro = "{}{}".format(repo_distro, self.distro_version.replace(".", ""))
        #  arch = self.arch
        #  if "ubuntu" in repo_distro and arch == "ppc64le":
        #      arch = "ppc64el"
        #  elif arch == "arm64":
        #      arch = "sbsa"
        #  suffix = f"{clean_distro}/{arch}"
        #  if "tegra" in self.product_name:
        #      arch = "arm64"
        #      suffix = f"l4t/{arch}"
        return f"http://cuda-internal.nvidia.com/release-candidates/kitpicks/{self.product_name}/{self.release_label}/{self.candidate_number}/repos/{clean_distro}"

    def latest_l4t_base_image(self):
        l4t_base_image = "nvcr.io/nvidian/nvidia-l4t-base"
        #  return f"{l4t_base_image}:r32_CUDA_10.2.460_RC_006"
        #  return f"{l4t_base_image}:r32.2"
        # bash equivalent
        #  /usr/bin/skopeo list-tags docker://nvcr.io/nvidian/nvidia-l4t-base | jq -r '.["Tags"] | .[]' | grep "^r[[:digit:]]*\." | sort -r -n | head -n 1
        out = shellcmd(
            "skopeo",
            ("list-tags", f"docker://{l4t_base_image}"),
            printOutput=False,
            returnOut=True,
        )
        try:
            tag_dict = json.loads(out.stdout)
        except:
            log.error(
                f"Some problem occurred in getting tags from NGC (nvcr.io): {out.stderr}"
            )
            sys.exit(1)
        tag_list = []
        # TODO: refactor
        for key in tag_dict.keys():
            if "Tags" in key:
                tag_list = list(tag_dict[key])
        tag_list2 = []
        for tag in tag_list:
            # Match r32\.*
            #  if re.match("^r[\d]*\.", tag):
            # Match r32_CUDA
            if re.match("^r[\d_]*CUDA", tag):
                tag_list2.append(tag)
        return f"{l4t_base_image}:{sorted(tag_list2, reverse=True)[0]}"

    def shipit_manifest(self):
        # 22:31 Tue Jul 13 2021 FIXME: (jesusa) this function is way too long to be considered good practice in python
        log.debug("Building the shipit manifest")
        gjson = self.get_shipit_global_json()
        self.product_name = gjson["product_name"]
        self.candidate_number = gjson["cand_number"]
        log.info(f"Product Name: '{self.product_name}'")
        log.info(f"Candidate Number: '{self.candidate_number}'")
        log.info(f"Release label: {self.release_label}")

        def supported_distros(distros):
            sdistros = []
            for distro in distros:
                if "wsl" in distro or (
                    "rhel" not in distro
                    and not any(f in distro for f in SUPPORTED_DISTRO_LIST)
                ):
                    continue
                if "rhel" in distro:
                    sdistros.append("ubi" + distro[len(distro) - 1 :])
                    sdistros.append("centos" + distro[len(distro) - 1 :])
                else:
                    sdistros.append(distro)
            return sdistros

        def nested_gjson_data(data):
            for k, v in data.items():
                if isinstance(v, dict):
                    for pair in nested_gjson_data(v):
                        yield (k, *pair)
                else:
                    if "distros" in k:
                        yield ([v])
                    else:
                        yield (k, v)

        reldata = {}
        for plat, distros in gjson["targets"].items():
            if "windows" in plat:
                continue
            os, arch = plat.split("-")
            if "sbsa" in arch:
                arch = "arm64"
            if not os in reldata:
                reldata[os] = {}
            if not arch in reldata[os]:
                reldata[os][arch] = {}
            reldata[os][arch]["distros"] = supported_distros(distros)

        if self.dist_base_path.exists:
            log.warning(f"Removing path '{self.dist_base_path}'")
            rm["-rf", self.dist_base_path]()
        self.dist_base_path.mkdir(parents=True, exist_ok=False)
        self.output_manifest_path = pathlib.Path(f"{self.dist_base_path}/manifest.yml")

        release_key = f"cuda_v{self.release_label}"
        self.parent.manifest = {
            release_key: {
                "dist_base_path": self.dist_base_path.as_posix(),
                "push_repos": ["artifactory"],
            }
        }

        for platform in nested_gjson_data(reldata):
            #  print(platform)
            os = platform[0]
            self.arch = platform[1]
            distros = platform[2]
            log.debug(f"os: '{os}' arch: '{self.arch}' distros: {distros}")
            for distro in distros:
                rgx = re.search(r"(\D*)(\d*)", distro)
                if rgx:
                    self.distro = rgx.group(1)
                    self.distro_version = rgx.group(2).replace("04", ".04")
                else:
                    raise UnknownCudaRCDistro("Distro '{distro}' has an unknown format")

                platform = f"{self.distro}{self.distro_version}"
                if "tegra" in self.product_name:
                    platform = "l4t"
                    if not self.cudnn_json_path:
                        log.error("Argument `--cudnn-json-path` is not set!")
                        sys.exit(1)

                #  print(platform)
                #  continue
                #  self.set_output_path(platform)

                #  if delete and self.dist_base_path.exists:
                #      #  raise
                #      log.warning(f"Removing path '{self.dist_base_path}'")
                #      rm["-rf", self.dist_base_path]()
                #  platform = f"{target}-{self.arch}"
                if "tegra" in self.product_name:
                    platform = f"{platform}-cuda"
                self.output_path = pathlib.Path(f"{self.dist_base_path}/{platform}")

                sjson = self.get_shipit_funnel_json()

                pkgs = self.template_packages()

                log.debug(f"template packages: {pkgs}")
                components = self.shipit_components(sjson, pkgs)

                # TEMP WAR: populate cudnn component for L4T
                if "l4t" in platform:
                    cudnn_comp = {
                        "cudnn8": {
                            "version": "",
                            "source": "",
                            "dev": {"source": "", "md5sum": ""},
                        }
                    }
                    #  print(self.cudnn_json_path)
                    with open(pathlib.Path(self.cudnn_json_path), "r") as f:
                        cudnn = json.loads(f.read())
                    for x in cudnn:
                        artpath = f"https://urm.nvidia.com/artifactory/{x['repo']}/{x['path']}/{x['name']}"
                        if "arm64" in x["name"]:
                            if "-dev_" in x["name"]:
                                #  cudnn_comp["cudnn8"]["dev"]["version"] = x["version"]
                                cudnn_comp["cudnn8"]["dev"]["source"] = artpath
                                cudnn_comp["cudnn8"]["dev"]["md5sum"] = x["actual_md5"]
                            else:
                                cudnn_comp["cudnn8"]["version"] = x["version"]
                                cudnn_comp["cudnn8"]["source"] = artpath
                                cudnn_comp["cudnn8"]["md5sum"] = x["actual_md5"]
                    if cudnn_comp:
                        #  print(cudnn_comp)
                        components.update(cudnn_comp)

                image_name = "gitlab-master.nvidia.com:5005/cuda-installer/cuda/release-candidate/cuda"
                template_path = "templates/ubuntu"
                if "ubuntu" not in self.distro:
                    template_path = "templates/redhat"
                #  if all(x in self.product_name for x in ["tegra", "10-2"]):
                #      template_path = "templates/ubuntu/legacy"

                #  if not "x86_64" in self.arch:
                #      image_name = f"gitlab-master.nvidia.com:5005/cuda-installer/cuda/release-candidate/cuda"
                base_image = f"{self.distro}:{self.distro_version}"
                if "ubi" in self.distro:
                    base_image = f"registry.access.redhat.com/ubi{self.distro_version}/ubi:latest"
                requires = ""

                key = "push_repos"
                if "tegra" in self.product_name:
                    key = "l4t_push_repos"
                prepos = self._load_rc_push_repos_manifest_yaml()[key]
                auth_registries(prepos)

                if "tegra" in self.product_name:
                    base_image = self.latest_l4t_base_image()
                    requires = "cuda>=10.2"
                    image_name = (
                        f"gitlab-master.nvidia.com:5005/cuda-installer/cuda/l4t-cuda"
                    )

                manifest = self.parent.manifest[release_key]
                manifest["image_name"] = image_name
                if not platform in manifest:
                    manifest[platform] = {
                        "base_image": base_image,
                        "image_tag_suffix": f"-{gjson['cand_number']}",
                        "template_path": template_path,
                        "repo_url": self.kitpick_repo_url(gjson),
                    }

                manifest[platform][f"{self.arch}"] = {
                    "requires": requires,
                    "components": components,
                }

        #  sys.exit(1)
        manifest.update({"push_repos": prepos})
        self.parent.manifest[release_key] = manifest
        log.info(f"Writing shipit manifest: {self.output_manifest_path}")
        self.write_shipit_manifest(self.parent.manifest)
        #  __import__("pprint").pprint(self.parent.manifest)
        #  sys.exit(1)

    def write_shipit_manifest(self, manifest):
        yaml_str = yaml.dump(manifest)
        with open(self.output_manifest_path, "w") as f:
            f.write(yaml_str)

    def set_output_path(self, target):
        self.output_path = pathlib.Path(f"{self.dist_base_path}/{target}")
        if not self.parent.shipit_uuid and self.output_path.exists:
            log.warning(f"Removing {self.output_path}")
            rm["-rf", self.output_path]()
        log.debug(f"self.output_path: '{self.output_path}' target: '{target}'")
        log.debug(f"Creating {self.output_path}")
        self.output_path.mkdir(parents=True, exist_ok=False)

    def target_all(self):
        log.debug("Generating all container scripts!")
        rgx = re.compile(
            # use regex101.com to debug with gitlab-ci.yml as the search text
            r"^(?P<distro>[a-zA-Z]*)(?P<distro_version>[\d\.]*)-v(?P<cuda_version>[\d\.]*)(?:-(?!cudnn|test|scan|deploy)(?P<pipeline_name>\w+))?"
        )

        for ci_job, _ in self.parent.ci.items():
            if (match := rgx.match(ci_job)) is None:
                #  log.debug("continuing")
                continue
            #  print(match.groups())
            #  continue
            self.distro = match.group("distro")
            self.distro_version = match.group("distro_version")
            self.cuda_version = match.group("cuda_version")
            if self.cuda_version.count(".") > 1:
                self.cuda_version_is_release_label = True
            self.pipeline_name = match.group("pipeline_name")
            #  self.arch = match.group("arch")

            log.debug("ci_job: '%s'" % ci_job)

            self.key = f"cuda_v{self.release_label}"
            if not self.release_label and self.cuda_version:
                self.key = f"cuda_v{self.cuda_version}"

            if self.pipeline_name:
                self.key = f"cuda_v{self.cuda_version}_{self.pipeline_name}"

            self.dist_base_path = pathlib.Path(
                self.parent.get_data(self.parent.manifest, self.key, "dist_base_path")
            )

            log.debug("dist_base_path: %s" % (self.dist_base_path))
            log.debug(
                "Generating distro: '%s' distro_version: '%s' cuda_version: '%s' release_label: '%s' "
                % (
                    self.distro,
                    self.distro_version,
                    self.cuda_version,
                    self.release_label,
                )
            )
            self.targeted()
            self.cuda_version_is_release_label = False

        if not self.dist_base_path:
            log.error("dist_base_path not set!")
            sys.exit(1)

    def target_all_kitmaker(self):
        log.debug("Generating all container scripts! (for kitmaker)")

        key = f"cuda_v{self.release_label}"
        self.cuda_version = self.release_label
        #  self.pipeline_name = "default"
        for k, v in self.parent.manifest[key].items():
            if any(x in k for x in SUPPORTED_DISTRO_LIST):
                log.debug(f"Working on {k}")
                rgx = re.search(r"(\D*)([\d\.]*)", k)
                self.distro = rgx.group(1)
                self.distro_version = rgx.group(2)
                self.cuda_version_is_release_label = True

                #  self.dist_base_path = pathlib.Path(
                #      self.parent.get_data(self.parent.manifest, key, "dist_base_path")
                #  )

                #  log.debug("dist_base_path: %s" % (self.dist_base_path))
                log.debug(
                    "Generating distro: '%s' distro_version: '%s' cuda_version: '%s' release_label: '%s' "
                    % (
                        self.distro,
                        self.distro_version,
                        self.cuda_version,
                        self.release_label,
                    )
                )
                self.targeted()
                self.cuda_version_is_release_label = False

    def targeted(self):
        self.key = f"cuda_v{self.release_label}"
        if not self.release_label and self.cuda_version:
            self.key = f"cuda_v{self.cuda_version}"
        if self.pipeline_name and self.pipeline_name != "default":
            self.key = f"cuda_v{self.release_label}_{self.pipeline_name}"
        log.debug(f"self.key: {self.key}")
        self.arches = self.supported_arch_list()
        log.debug(f"self.arches: {self.arches}")

        #  for arch in self.supported_arch_list():
        #      if not self.generate_all:
        #          # FIXME: No need to go through this again if coming from target_all
        #          log.debug(
        #              "Have distro: '%s' version: '%s' arch: '%s' cuda: '%s' pipeline: '%s'",
        #              self.distro,
        #              self.distro_version,
        #              arch,
        #              self.cuda_version or self.release_label,
        #              self.pipeline_name,
        #          )

        self.dist_base_path = pathlib.Path(
            self.parent.get_data(
                self.parent.manifest, self.key, "dist_base_path", can_skip=False,
            )
        )
        log.debug(f"self.dist_base_path: {self.dist_base_path}")
        #  if not self.output_manifest_path:
        self.set_output_path(f"{self.distro}{self.distro_version}")
        log.debug(f"self.output_manifest_path: {self.output_manifest_path}")

        self.prepare_context()

        #  if self.cuda_version == "8.0":
        #      self.generate_containerscripts_cuda_8()
        #  else:
        self.generate_containerscripts()

    def main(self):
        if self.parent.shipit_uuid:
            log.debug("Have shippit source, generating manifest and scripts")
            self.dist_base_path = pathlib.Path("kitpick")
            self.shipit_manifest()
            self.target_all_kitmaker()
        else:
            if (
                (self.generate_all and not self.parent.shipit_uuid)
                or self.generate_ci
                or self.generate_readme
                or self.generate_tags
            ):
                self.generate_gitlab_pipelines()
            else:
                # Make sure all of our arguments are present
                if any(
                    [
                        not i
                        for i in [
                            self.arch,
                            self.distro,
                            self.distro_version,
                            self.release_label,
                        ]
                    ]
                ):
                    # Plumbum doesn't allow this check
                    log.error(
                        """Missing arguments (one or all): ["--arch", "--os", "--os-version", "--release-label"]"""
                    )
                    sys.exit(1)
            if not self.generate_ci:
                self.parent.load_ci_yaml()
                if self.generate_all:
                    self.target_all()
                elif self.generate_readme:
                    self.generate_readmes()
                elif self.generate_tag:
                    self.generate_tags()
                else:
                    self.targeted()
        log.info("Done")


@Manager.subcommand("staging-images")
class ManagerStaging(Manager):
    DESCRIPTION = "Staging image management"

    repos = [
        "gitlab-master.nvidia.com:5005/cuda-installer/cuda",
        "gitlab-master.nvidia.com:5005/cuda-installer/cuda/cuda-arm64",
        "gitlab-master.nvidia.com:5005/cuda-installer/cuda/cuda-ppc64le",
        "gitlab-master.nvidia.com:5005/cuda-installer/cuda/l4t-cuda",
        "gitlab-master.nvidia.com:5005/cuda-installer/cuda/release-candidate/cuda",
        "gitlab-master.nvidia.com:5005/cuda-installer/cuda/release-candidate/cuda-arm64",
        "gitlab-master.nvidia.com:5005/cuda-installer/cuda/release-candidate/cuda-ppc64le",
    ]

    delete_all = cli.Flag(["--delete-all"], help="Delete all of the staging images.")

    repo = cli.SwitchAttr(
        "--repo",
        cli.Set(*repos, case_sensitive=False),
        excludes=["--delete-all"],
        group="Targeted",
        help="Delete only from a specific repo.",
    )

    #  distro = cli.SwitchAttr(
    #      "--os-name",
    #      str,
    #      group="Targeted",
    #      excludes=["--delete-all"],
    #      help="The distro to use.",
    #      default=None,
    #  )

    #  distro_version = cli.SwitchAttr(
    #      "--os-version",
    #      str,
    #      group="Targeted",
    #      excludes=["--delete-all"],
    #      help="The distro version",
    #      default=None,
    #  )

    #  cuda_version = cli.SwitchAttr(
    #      "--cuda-version",
    #      str,
    #      excludes=["--delete-all"],
    #      group="Targeted",
    #      help="[DEPRECATED for newer cuda versions!] The cuda version to use. Example: '11.2'",
    #      default=None,
    #  )

    #  release_label = cli.SwitchAttr(
    #      "--release-label",
    #      str,
    #      excludes=["--delete-all"],
    #      group="Targeted",
    #      help="The cuda version to use. Example: '11.2.0'",
    #      default=None,
    #  )

    #  arch = cli.SwitchAttr(
    #      "--arch",
    #      cli.Set("x86_64", "ppc64le", "arm64", case_sensitive=False),
    #      excludes=["--delete-all"],
    #      group="Targeted",
    #      help="Generate container scripts for a particular architecture.",
    #  )

    def get_repo_tags(self, repo):
        return shellcmd(
            "skopeo",
            ("list-tags", f"docker://{repo}"),
            printOutput=False,
            returnOut=True,
        )

    def delete_all_tags(self):
        for repo in self.repos:
            self.delete_all_tags_repo(repo)

    @retry(
        (ImageDeleteRetry),
        tries=HTTP_RETRY_ATTEMPTS,
        delay=HTTP_RETRY_WAIT_SECS,
        logger=log,
    )
    def delete_all_tags_repo(self, repo):
        out = self.get_repo_tags(repo)
        if out.returncode > 0:
            log.fatal("Could not use skopeo to gat a list of images!")
            sys.exit(1)
        tags = json.loads(out.stdout)["Tags"]
        for tag in tags:
            log.debug(f"deleting {repo}:{tag}")
            out2 = shellcmd(
                "skopeo",
                ("delete", f"docker://{repo}:{tag}"),
                printOutput=False,
                returnOut=True,
            )
            if out2.returncode > 0:
                log.info(f"deleted {repo}:{tag}")
            else:
                raise ImageDeleteRetry()

    def main(self):
        if self.delete_all:
            self.delete_all_tags()
        elif self.repo:
            self.delete_all_tags_repo(self.repo)
        else:
            log.fatal("No flags defined!")
            print()
            self.help()
            return 1


if __name__ == "__main__":
    Manager.run()
