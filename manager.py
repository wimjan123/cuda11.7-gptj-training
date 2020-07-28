#!/usr/bin/env python3

# @author Jesus Alvarez <sw-cuda-installer@nvidia.com>

"""Container scripts template injector and pipeline trigger."""

#
# !! IMPORTANT !!
#
# Editors of this file should use https://github.com/python/black for auto formatting.
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

import jinja2
from jinja2 import Environment, Template
from plumbum import cli
from plumbum.cmd import rm
import yaml
import glom
import docker
import git
import deepdiff
import requests


log = logging.getLogger()


class Manager(cli.Application):
    """CUDA CI Manager"""

    PROGNAME = "manager.py"
    VERSION = "0.0.1"

    manifest = None
    ci = None
    changed = False

    manifest_path = cli.SwitchAttr(
        "--manifest", str, help="Select a manifest to use", default="manifest.yaml"
    )

    def _load_manifest_yaml(self):
        log.debug(f"Loading manifest: {self.manifest_path}")
        with open(self.manifest_path, "r") as f:
            self.manifest = yaml.load(f, yaml.Loader)

    def load_ci_yaml(self):
        with open(".gitlab-ci.yml", "r") as f:
            self.ci = yaml.load(f, yaml.Loader)

    def _load_app_config(self):
        with open("manager-config.yaml", "r") as f:
            logging.config.dictConfig(yaml.safe_load(f.read())["logging"])

    def triggered(self):
        """Triggers pipelines on gitlab"""
        pass

    # Get data from a object by dotted path. Example "cuda."v10.0".cuda_requires"
    def get_data(self, obj, *path, can_skip=False):
        try:
            data = glom.glom(obj, glom.Path(*path))
        except glom.PathAccessError:
            if can_skip:
                return
            raise glom.PathAccessError
        return data

    def main(self):
        self._load_app_config()
        if not self.nested_command:  # will be ``None`` if no sub-command follows
            log.error("No subcommand given!")
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
            self._load_manifest_yaml()


@Manager.subcommand("trigger")
class ManagerTrigger(Manager):
    DESCRIPTION = "Trigger for changes."

    repo = None
    manifest_current = None
    manifest_previous = None
    changed = set()
    trigger_all = False
    trigger_explicit = []
    key = ""
    pipeline_name = "default"

    dry_run = cli.Flag(
        ["-n", "--dry-run"], help="Show output but don't make any changes."
    )

    trigger_override = cli.SwitchAttr(
        "--trigger-override",
        str,
        help="Override triggering from gitlab with a variable.",
        default=None,
    )

    def ci_distro_variables(self, distro):
        log.debug(f"have distro: {distro}")
        rgx = re.compile(fr"^\s+- \$(?!all)({distro}\w+) == \"true\"$")
        ci_vars = []
        with open(".gitlab-ci.yml", "r") as fp:
            for _, line in enumerate(fp):
                match = rgx.match(line)
                if match:
                    ci_vars.append(match.groups(0)[0])
        return ci_vars

    def ci_pipeline_variables(self, name):
        log.debug(f"have pipeline_name: {name}")
        rgx = re.compile(fr"^\s+- \$(?!all)(.*_{name}_.*) == \"true\"$")
        ci_vars = []
        with open(".gitlab-ci.yml", "r") as fp:
            for _, line in enumerate(fp):
                match = rgx.match(line)
                if match:
                    ci_vars.append(match.groups(0)[0])
        return ci_vars

    def ci_cuda_version_distro_arch_variables(self, version, distro, arch):
        rgx = re.compile(fr"^\s+- \$(?!all)({distro}.{version}.{arch}) == \"true\"$")
        ci_vars = []
        with open(".gitlab-ci.yml", "r") as fp:
            for _, line in enumerate(fp):
                match = rgx.match(line)
                if match:
                    ci_vars.append(match.groups(0)[0])
        return ci_vars

    def get_cuda_version_from_trigger(self, trigger):
        rgx = re.compile(r".*cuda([\d\.]+).*$")
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
        self.repo = git.Repo(pathlib.Path("."))
        commit = self.repo.commit("HEAD")
        rgx = re.compile(r"ci\.trigger = (.*)")
        log.debug("Commit message: %s", repr(commit.message))

        if self.trigger_override:
            log.info("Using trigger override!")
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
                log.debug("pipeline_name: '%s'" % self.pipeline_name)

                self.key = f"cuda_v{version}"
                if self.pipeline_name != "default":
                    self.key = f"cuda_v{version}_{self.pipeline_name}"

                distro_list = ["ubuntu", "ubi", "centos"]
                if version:
                    distro_list = self.supported_distro_list_by_cuda_version(version)

                distro = next(
                    (distro for distro in distro_list if distro in job), None,
                )

                arch = next(
                    (arch for arch in ["x86_64", "ppc64le", "arm64"] if arch in job),
                    None,
                )

                log.debug(
                    f"job: '{job}' name: {self.pipeline_name} version: {version} distro: {distro} arch: {arch}"
                )

                log.debug(f"distro_list: '{distro_list}'")

                cijobs = []
                if version and distro:
                    if not arch:
                        arch = "\w+"
                    cijobs = self.ci_cuda_version_distro_arch_variables(
                        version, distro, arch
                    )
                elif version and not distro and not arch:
                    for distro2 in self.supported_distro_list_by_cuda_version(version):
                        cijobs.extend(
                            self.ci_cuda_version_distro_arch_variables(
                                version, distro2, "\w+",
                            )
                        )
                elif self.pipeline_name:
                    cijobs = self.ci_pipeline_variables(self.pipeline_name)
                else:
                    cijobs = self.ci_distro_variables(job)

                for cvar in cijobs:
                    log.info("Triggering '%s'", cvar)
                    self.trigger_explicit.append(cvar)

            return True

    def load_last_manifest(self):
        self.repo = git.Repo(pathlib.Path("."))
        # XXX: HEAD~1 would not work for merges...
        commit = self.repo.commit("HEAD~1")
        log.debug("getting previous manifest from git commit %s", commit.hexsha)
        blob = commit.tree / self.manifest_path
        with io.BytesIO(blob.data_stream.read()) as f:
            tf = f.read().decode("utf-8")
        self.manifest_previous = yaml.load(tf, yaml.Loader)

    def load_current_manifest(self):
        log.debug(
            "current manifest from git commit %s", self.repo.commit("HEAD").hexsha
        )
        with open(self.manifest_path, "r") as f:
            self.manifest_current = yaml.load(f, yaml.Loader)

    # Remove stuff we don't care about before compare. Typically yaml placeholders.
    def prune_objects(self):
        for manifest in [self.manifest_current, self.manifest_previous]:
            manifest.pop("redhat7")
            manifest.pop("redhat6")
            manifest.pop("push_repos")

    # returns true if changes have been detected
    def deep_compare(self):
        rgx = re.compile(r"root\['([\w\.\d]*)'\]\['cuda'\]\['v(\d+\.\d+)")

        # Uncomment this to see the files being compared in the logs
        #  log.debug("manifest previous: %s", self.manifest_previous)
        #  log.debug("manifest current: %s", self.manifest_current)

        ddiff = deepdiff.DeepDiff(
            self.manifest_previous,
            self.manifest_current,
            verbose_level=0,
            exclude_paths=[
                "root['redhat6']",
                "root['redhat7']",
                "root['redhat8']",
                "root['push_repos']",
            ],
        ).to_dict()

        if not ddiff:
            log.info("No changes detected! 🍺")
            return False

        #  pprint(self.manifest_previous)
        #  pprint(self.manifest_current)
        log.debug("Have ddif: %s", ddiff)

        items_added = ddiff.get("dictionary_item_added", None)
        items_removed = ddiff.get("dictionary_item_removed", None)
        items_changed = ddiff.get("values_changed", None)

        # FIXME: not DRY
        if items_added and items_removed:
            # parse added or removed items
            for obj in ddiff["dictionary_item_added"].union(
                ddiff["dictionary_item_removed"]
            ):
                match = rgx.match(obj)
                if match:
                    item = match.group(1) + "_cuda" + match.group(2)
                    self.changed.add(item.replace(".", "_"))
        elif items_added:
            for obj in items_added:
                match = rgx.match(obj)
                if match:
                    item = match.group(1) + "_cuda" + match.group(2)
                    self.changed.add(item.replace(".", "_"))
        elif items_removed:
            for obj in items_removed:
                match = rgx.match(obj)
                if match:
                    item = match.group(1) + "_cuda" + match.group(2)
                    self.changed.add(item.replace(".", "_"))

        if items_changed:
            for obj in items_changed:
                match = rgx.match(obj)
                if match:
                    item = match.group(1) + "_cuda" + match.group(2)
                    self.changed.add(item.replace(".", "_"))

        log.debug("manifest root changes: %s", self.changed)
        return True

    def kickoff(self):
        url = os.getenv("CI_API_V4_URL")
        project_id = os.getenv("CI_PROJECT_ID")
        dry_run = os.getenv("DRY_RUN")
        token = os.getenv("CI_JOB_TOKEN")
        ref = os.getenv("CI_COMMIT_REF_NAME")
        payload = {"token": token, "ref": ref, "variables[TRIGGER]": "true"}
        if self.trigger_all:
            payload["variables[all]"] = "true"
        elif self.trigger_explicit:
            for job in self.trigger_explicit:
                payload[f"variables[{job}]"] = "true"
        else:
            for job in self.changed:
                payload[f"variables[{job}]"] = "true"
        if dry_run:
            payload[f"variables[DRY_RUN]"] = "true"
        log.debug("payload %s", payload)
        if not self.dry_run:
            r = requests.post(
                f"{url}/projects/{project_id}/trigger/pipeline", data=payload
            )
            log.debug("response status code %s", r.status_code)
            log.debug("response body %s", r.json())
        else:
            log.info("In dry-run mode so not making gitlab trigger POST")

    def main(self):
        if not self.check_explicit_trigger():
            self.load_last_manifest()
            self.load_current_manifest()
        if self.trigger_all or self.trigger_explicit or self.deep_compare():
            self.kickoff()


@Manager.subcommand("push")
class ManagerContainerPush(Manager):
    DESCRIPTION = "Login and push to the container registries"

    image_name = cli.SwitchAttr(
        "--image-name", str, help="The image name to tag", default="", mandatory=True
    )

    distro = cli.SwitchAttr(
        "--os", str, help="The distro to use.", default=None, mandatory=True
    )

    distro_version = cli.SwitchAttr(
        "--os-version", str, help="The distro version", default=None, mandatory=True
    )

    dry_run = cli.Flag(["-n", "--dry-run"], help="Show output but don't do anything!")

    cuda_version = cli.SwitchAttr(
        "--cuda-version",
        str,
        help="The cuda version to use. Example: '10.1'",
        default=None,
        mandatory=True,
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
        requires=["--image-name", "--os", "--os-version", "--cuda-version"],
        help="Push images for a particular architecture.",
    )

    pipeline_name = cli.SwitchAttr(
        "--pipeline-name",
        str,
        help="The name of the pipeline the deploy is coming from",
    )

    client = None
    repos = []
    tags = []
    key = ""

    def docker_login(self):
        distro_push_repos = self.get_data(
            self.parent.manifest,
            self.key,
            f"{self.distro}{self.distro_version}",
            "push_repos",
        )
        excluded_repos = self.get_data(
            self.parent.manifest,
            self.key,
            f"{self.distro}{self.distro_version}",
            self.arch,
            "exclude_repos",
            can_skip=True,
        )
        for repo, metadata in self.parent.manifest["push_repos"].items():
            if metadata.get("only_if", False) and not os.getenv(metadata["only_if"]):
                log.info("repo: '%s' only_if requirement not satisfied", repo)
                continue
            if distro_push_repos and repo not in distro_push_repos:
                log.info("repo: '%s' is excluded for this image", repo)
                continue
            if excluded_repos and repo in excluded_repos:
                log.info("repo: '%s' is excluded for this image", repo)
                continue
            if self.arch not in metadata["registry"]:
                log.debug(f"{repo} does not contain an entry for {self.arch}")
                continue
            creds = False
            user = os.getenv(metadata["user"])
            if not user:
                user = metadata["user"]
            passwd = os.getenv(metadata["pass"])
            if not passwd:
                passwd = metadata["pass"]
            registry = metadata["registry"][self.arch]
            if repo == "docker.io":
                registry = f"docker.io/{registry}"
            if self.client.login(username=user, password=passwd, registry=registry):
                if "docker.io" in registry:
                    # docker.io designation not needed in the image name for pushes to docker hub, only
                    # for login
                    registry = metadata["registry"][self.arch]
                self.repos.append(registry)
                log.info("Logged into %s", registry)
        if not self.repos:
            log.fatal(
                "Docker login failed! Did not log into any repositories. Environment not set?"
            )
            sys.exit(1)

    # Check the image tag to see if it contains a suffix. This is used for special builds.
    # A tag with a suffix looks like:
    #
    #  10.0-cudnn7-devel-centos6-patched
    #  10.0-devel-centos6-patched
    #
    def _tag_contains_suffix(self, img):
        if len(img.tags) == 0:
            log.debug("img has no tags!")
            return False
        fields = img.tags[0].split(":")[1].split("-")
        is_cudnn = [s for s in fields if "cudnn" in s]
        if (is_cudnn and len(fields) > 4) or (not is_cudnn and len(fields) > 3):
            log.debug("tag contains suffix")
            return True
        elif len(fields) == 2 or f"{self.distro}{self.distro_version}" in fields[:-1]:
            log.debug("tag does not contain suffix")
            return False
        elif f"{self.distro}{self.distro_version}" in fields[:-1]:
            log.debug("tag contains suffix")
            return True
        log.debug("tag does not contain suffix")

    def _should_push_image(self, img):
        if len(img.tags) == 0:
            log.debug("img has no tags!")
            return False
        log.debug(f"Have image tags {img.tags}")
        # Ensure the tag contains the target cuda version and distro version
        match = all(
            key in str(img.tags)
            for key in [self.cuda_version, f"{self.distro}{self.distro_version}"]
        )
        # If the tag has a suffix but we are not expecting one, then fail
        if not self.image_tag_suffix and self._tag_contains_suffix(img):
            log.debug("Tag suffix detected in image tag")
            match = False
        # All together now
        if (
            not match
            or "-test_" in str(img.tags)
            # a suffix is expected but the image does not contain what we expect
            or (self.image_tag_suffix and self.image_tag_suffix not in str(img.tags))
        ):
            log.debug("Image will not be pushed.")
            return False
        return True

    def push_images(self):
        for img in self.client.images.list(
            name=self.image_name, filters={"dangling": False}
        ):
            log.debug("img: %s", str(img.tags))
            if not self._should_push_image(img):
                log.debug("Skipping")
                continue
            log.info("Processing image: %s, id: %s", img.tags, img.short_id)
            for repo in self.repos:
                for k, v in [
                    [x, y] for tag in img.tags for (x, y) in [tag.rsplit(":", 1)]
                ]:
                    tag = v
                    if self.dry_run:
                        log.info(
                            "Tagged %s:%s (%s), %s", repo, tag, img.short_id, False
                        )
                        log.info("Would have pushed: %s:%s", repo, tag)
                        continue
                    tagged = img.tag(repo, tag)
                    log.info("Tagged %s:%s (%s), %s", repo, tag, img.short_id, tagged)
                    if tagged:
                        # FIXME: only push if the image has changed
                        for line in self.client.images.push(
                            repo, tag, stream=True, decode=True
                        ):
                            log.info(line)

    def main(self):
        log.debug("dry-run: %s", self.dry_run)
        self.key = f"cuda_v{self.cuda_version}"
        if self.pipeline_name:
            self.key = f"cuda_v{self.cuda_version}_{self.pipeline_name}"
        self.client = docker.DockerClient(
            base_url="unix://var/run/docker.sock", timeout=600
        )
        self.docker_login()
        self.push_images()
        log.info("Done")


@Manager.subcommand("generate")
class ManagerGenerate(Manager):
    DESCRIPTION = "Generate Dockerfiles from templates."

    cuda = {}
    output_path = {}
    dist_base_path = ""
    key = ""

    template_env = Environment(
        extensions=["jinja2.ext.do"], trim_blocks=True, lstrip_blocks=True
    )

    generate_all = cli.Flag(
        ["--all"],
        excludes=["--os", "--os-version", "--cuda-version"],
        help="Generate all of the templates.",
    )

    generate_ci = cli.Flag(["--ci"], help="Generate the gitlab pipelines only.",)

    distro = cli.SwitchAttr(
        "--os",
        str,
        group="Targeted",
        requires=["--os-version", "--cuda-version"],
        excludes=["--all"],
        help="The distro to use.",
        default=None,
    )

    distro_version = cli.SwitchAttr(
        "--os-version",
        str,
        group="Targeted",
        requires=["--os", "--cuda-version"],
        excludes=["--all"],
        help="The distro version",
        default=None,
    )

    cuda_version = cli.SwitchAttr(
        "--cuda-version",
        str,
        excludes=["--all"],
        group="Targeted",
        requires=["--os", "--os-version"],
        help="The cuda version to use. Example: '10.1'",
        default=None,
    )

    arch = cli.SwitchAttr(
        "--arch",
        cli.Set("x86_64", "ppc64le", "arm64", case_sensitive=False),
        excludes=["--all"],
        group="Targeted",
        requires=["--os", "--os-version", "--cuda-version"],
        help="Generate container scripts for a particular architecture.",
    )

    pipeline_name = cli.SwitchAttr(
        "--pipeline-name",
        str,
        excludes=["--all"],
        group="Targeted",
        requires=["--os", "--os-version", "--cuda-version"],
        help="Use a pipeline name for manifest matching.",
        default="default",
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

    def cudnn_versions(self):
        obj = []
        for k, v in self.cuda["components"].items():
            if k.startswith("cudnn") and v:
                obj.append(k)
        return obj

    # extracts arbitrary keys and inserts them into the templating context
    def extract_keys(self, val):
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
                *self.supported_distro_list_by_cuda_version(self.cuda_version),
            ]:
                continue
            self.cuda[k] = v

    # For cudnn templates, we need a custom template context
    def output_cudnn_template(self, cudnn_version_name, template_path, output_path):
        cudnn_manifest = self.cuda["components"][cudnn_version_name]
        if "source" in cudnn_manifest:
            cudnn_manifest["basename"] = os.path.basename(cudnn_manifest["source"])
            cudnn_manifest["dev"]["basename"] = os.path.basename(
                cudnn_manifest["dev"]["source"]
            )

        new_ctx = {
            "cudnn": self.cuda["components"][cudnn_version_name],
            "arch": self.arch,
            "version": self.cuda["version"],
            "image_tag_suffix": self.cuda["image_tag_suffix"],
            "os": self.cuda["os"],
        }
        log.debug("cudnn template context: %s", new_ctx)
        self.output_template(
            template_path=template_path, output_path=output_path, ctx=new_ctx
        )

    def output_template(self, template_path, output_path, ctx=None):
        ctx = ctx if ctx is not None else self.cuda
        with open(template_path) as f:
            log.debug("Processing template %s", template_path)
            new_output_path = pathlib.Path(output_path)
            new_filename = template_path.name[:-6]
            template = self.template_env.from_string(f.read())
            if not new_output_path.exists():
                log.debug(f"Creating {new_output_path}")
                new_output_path.mkdir(parents=True)
            log.info(f"Writing {new_output_path}/{new_filename}")
            with open(f"{new_output_path}/{new_filename}", "w") as f2:
                f2.write(template.render(cuda=ctx))

    def prepare_context(self):
        # checks the cudnn components and ensures at least one is installed from the public "machine-learning" repo
        def use_ml_repo():
            use_ml_repo = False
            # First check the manifest to see if a ml repo url is specified
            if not self.get_data(
                self.parent.manifest,
                self.key,
                f"{self.distro}{self.distro_version}",
                self.arch,
                "ml_repo_url",
                can_skip=True,
            ):
                return use_ml_repo
            # if a cudnn component contains "source", then it is installed from a different source than the public machine
            # learning repo
            # If any of the cudnn components lack the source key, then the ML repo should be used
            for comp, val in self.cuda["components"].items():
                if next(
                    (True for mlcomp in ["cudnn", "nccl"] if mlcomp in comp), False
                ):
                    if val and "source" not in val:
                        use_ml_repo = True
            return use_ml_repo

        conf = self.parent.manifest
        major = self.cuda_version.split(".")[0]
        minor = self.cuda_version.split(".")[1]

        build_version = self.get_data(
            conf,
            self.key,
            f"{self.distro}{self.distro_version}",
            self.arch,
            "components",
            "build_version",
        )

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
            "use_ml_repo": False,
            "version": {
                "full": f"{self.cuda_version}.{build_version}",
                "major": major,
                "minor": minor,
                "build": build_version,
            },
            "os": {"distro": self.distro, "version": self.distro_version},
            "arch": self.arch,
            "image_tag_suffix": self.image_tag_suffix,
            "components": self.get_data(
                conf,
                self.key,
                f"{self.distro}{self.distro_version}",
                self.arch,
                "components",
            ),
        }
        self.cuda["use_ml_repo"] = use_ml_repo()

        # Users of manifest.yaml are allowed to set arbitrary keys for inclusion in the templates
        # and the discovered keys are injected into the template context.
        # We only checks at three levels in the manifest
        self.extract_keys(
            self.get_data(conf, self.key, f"{self.distro}{self.distro_version}",)
        )
        self.extract_keys(
            self.get_data(
                conf, self.key, f"{self.distro}{self.distro_version}", self.arch,
            )
        )
        log.info("cuda version %s" % (self.cuda_version))
        log.debug("template context %s" % (self.cuda))
        #  sys.exit(1)

    def generate_cudnn_scripts(self, base_image, template_path):
        for pkg in self.cudnn_versions():
            self.cuda["components"][pkg]["target"] = base_image
            self.output_cudnn_template(
                cudnn_version_name=pkg,
                template_path=pathlib.Path(f"{template_path}/cudnn/Dockerfile.jinja"),
                output_path=pathlib.Path(f"{self.output_path}/{base_image}/{pkg}"),
            )

    # CUDA 8 uses a deprecated image layout
    def generate_containerscripts_cuda_8(self):
        for img in ["devel", "runtime"]:
            base = img
            if img == "runtime":
                # for CUDA 8, runtime == base
                base = "base"
            # cuda image
            temp_path = self.parent.manifest[f"{self.distro}{self.distro_version}"][
                "template_path"
            ]
            log.debug("temp_path: %s, output_path: %s", temp_path, self.output_path)
            self.output_template(
                template_path=pathlib.Path(f"{temp_path}/{base}/Dockerfile.jinja"),
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
            self.generate_cudnn_scripts(img, temp_path)

    def generate_containerscripts(self):
        for img in ["base", "devel", "runtime"]:
            # cuda image
            temp_path = self.cuda["template_path"]
            self.cuda["target"] = img
            log.debug("temp_path: %s, output_path: %s", temp_path, self.output_path)
            self.output_template(
                template_path=pathlib.Path(f"{temp_path}/{img}/Dockerfile.jinja"),
                output_path=pathlib.Path(f"{self.output_path}/{img}"),
            )
            # copy files
            for filename in pathlib.Path(f"{temp_path}/{img}").glob("*"):
                if "Dockerfile" in filename.name:
                    continue
                log.debug("Checking %s", filename)
                if ".jinja" in filename.name:
                    self.output_template(filename, f"{self.output_path}/{img}")
                else:
                    log.info(f"Copying {filename} to {self.output_path}/{img}")
                    shutil.copy(filename, f"{self.output_path}/{img}")
            # cudnn image
            if "base" not in img:
                self.generate_cudnn_scripts(img, temp_path)

    # FIXME: Probably a much nicer way to do this with GLOM...
    # FIXME: Turn off black auto format for this function...
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

        def matched(key):
            match = rgx.match(k)
            if match:
                return match

        for k, _ in manifest.items():
            rgx = re.compile(r"cuda_v([\d\.]+)(?:_(\w+))?$")
            if (match := matched(k)) is None:
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
            ctx[cuda_version][pipeline_name]["yaml_safe"] = cuda_version.replace(".", "_")

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
                ctx[cuda_version][pipeline_name][distro] = {}
                ctx[cuda_version][pipeline_name][distro]["name"] = dm.group('name')
                ctx[cuda_version][pipeline_name][distro]["version"] = dm.group('version')
                ctx[cuda_version][pipeline_name][distro]["yaml_safe"] = distro.replace(".", "_")
                image_tag_suffix = self.get_data(manifest, key, distro, "image_tag_suffix", can_skip=True)
                ctx[cuda_version][pipeline_name][distro]["image_tag_suffix"] = ""
                ctx[cuda_version][pipeline_name][distro]["image_name"] = {}

                if image_tag_suffix:
                    ctx[cuda_version][pipeline_name][distro]["image_tag_suffix"] = image_tag_suffix

                ctx[cuda_version][pipeline_name][distro]["arches"] = []

                for arch, _ in manifest[key][distro].items():
                    if arch not in ["arm64", "ppc64le", "x86_64"]:
                        continue

                    #  log.debug("arch: '%s'" % arch)
                    no_os_suffix = self.get_data(manifest, key, distro, arch, "no_os_suffix", can_skip=True)
                    latest = self.get_data(manifest, key, distro, arch, "latest", can_skip=True)
                    ctx[cuda_version][pipeline_name][distro]["image_name"][arch] = self.get_data(manifest, key, distro, arch, "image_name")

                    if "latest" not in ctx[cuda_version][pipeline_name][distro]:
                        ctx[cuda_version][pipeline_name][distro]["latest"] = {}

                    ctx[cuda_version][pipeline_name][distro]["latest"][arch] = (True if latest else False)

                    if "no_os_suffix" not in ctx[cuda_version][pipeline_name][distro]:
                        ctx[cuda_version][pipeline_name][distro]["no_os_suffix"] = {}

                    ctx[cuda_version][pipeline_name][distro]["no_os_suffix"][arch] = (True if no_os_suffix else False)
                    ctx[cuda_version][pipeline_name][distro]["arches"].append(arch)

                    if "cudnn" not in ctx[cuda_version][pipeline_name][distro]:
                        ctx[cuda_version][pipeline_name][distro]["cudnn"] = {}

                    ctx[cuda_version][pipeline_name][distro]["cudnn"][arch] = get_cudnn_components(key, distro, arch)

        log.debug(f"ci pipline context: {ctx}")

        template_path = pathlib.Path("templates/gitlab/gitlab-ci.yml.jinja")
        with open(template_path) as f:
            log.debug("Processing template %s", template_path)
            output_path = pathlib.Path(".gitlab-ci.yml")
            template = self.template_env.from_string(f.read())
            with open(output_path, "w") as f2:
                f2.write(template.render(cuda=ctx))

        #  sys.exit(1)

    # fmt: on
    def target_all(self):
        log.debug("Generating all container scripts!")
        rgx = re.compile(
            # use regex101.com to debug with gitlab-ci.yml as the search text
            r"^(?P<distro>[a-zA-Z]*)(?P<distro_version>[\d\.]*)-v(?P<cuda_version>[\d\.]*)(?:-(?!cudnn|test|scan|deploy)(?P<pipeline_name>\w+))?-(?P<arch>arm64|ppc64le|x86_64)"
        )

        for ci_job, _ in self.parent.ci.items():
            if (match := rgx.match(ci_job)) is None:
                continue
            self.distro = match.group("distro")
            self.distro_version = match.group("distro_version")
            self.cuda_version = match.group("cuda_version")
            self.pipeline_name = match.group("pipeline_name")
            self.arch = match.group("arch")

            log.debug("ci_job: '%s'" % ci_job)
            self.key = f"cuda_v{self.cuda_version}"
            if self.pipeline_name:
                self.key = f"cuda_v{self.cuda_version}_{self.pipeline_name}"

            self.dist_base_path = self.parent.get_data(
                self.parent.manifest, self.key, "dist_base_path",
            )

            log.debug("dist_base_path: %s" % (self.dist_base_path))
            log.debug(
                "Generating distro: '%s' distro_version: '%s' cuda_version: '%s' arch: '%s'"
                % (self.distro, self.distro_version, self.cuda_version, self.arch)
            )

            self.targeted()

        if not self.dist_base_path:
            log.error("dist_base_path not set!")

        #  sys.exit()

    def targeted(self):
        arches = []
        if not self.arch:
            arches = self.supported_arch_list()
        else:
            arches = [self.arch]
        for arch in arches:
            self.arch = arch
            log.debug(
                "Have distro: '%s' version: '%s' arch: '%s' cuda: '%s' pipeline: '%s'",
                self.distro,
                self.distro_version,
                self.arch,
                self.cuda_version,
                self.pipeline_name,
            )
            target = f"{self.distro}{self.distro_version}"
            self.key = f"cuda_v{self.cuda_version}"
            if self.pipeline_name and self.pipeline_name != "default":
                self.key = f"cuda_v{self.cuda_version}_{self.pipeline_name}"

            self.dist_base_path = self.parent.get_data(
                self.parent.manifest, self.key, "dist_base_path", can_skip=False,
            )

            self.output_path = pathlib.Path(
                f"{self.dist_base_path}/{target}-{self.arch}"
            )

            if self.output_path.exists:
                log.debug(f"Removing {self.output_path}")
                rm["-rf", self.output_path]()

            log.debug(f"Creating {self.output_path}")
            self.output_path.mkdir(parents=True, exist_ok=False)
            self.prepare_context()

            if self.cuda_version == "8.0":
                self.generate_containerscripts_cuda_8()
            else:
                self.generate_containerscripts()

    def main(self):
        self.generate_gitlab_pipelines()
        if self.generate_ci:
            sys.exit(1)
        self.parent.load_ci_yaml()
        if self.generate_all:
            self.target_all()
        else:
            self.targeted()
        log.info("Done")


if __name__ == "__main__":
    Manager.run()
