import logging

from beeprint import pp

log = logging.getLogger()

HTTP_RETRY_ATTEMPTS = 3
HTTP_RETRY_WAIT_SECS = 30

SUPPORTED_DISTRO_LIST = ["ubuntu", "ubi", "centos", "rockylinux"]


L4T_BASE_IMAGE_NAME = "nvcr.io/nvidian/nvidia-l4t-base"
