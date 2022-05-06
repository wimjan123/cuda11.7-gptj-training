from shipitdata import *

from beeprint import pp  # type: ignore

def test_supported_distros_by_arch_arm64():
    """Ensure distros for "arm64" are pulled from sbsa shipit data."""

    input_json = """{
   "cand_number" : "003",
   "product_name" : "cuda-r11-4",
   "rel_label" : "11.4.0",
   "targets" : {
      "linux-aarch64" : [
         "archives",
         "ubuntu2004"
      ],
      "linux-sbsa" : [
         "archives",
         "conda",
         "rhel8",
         "ubuntu2004"
      ],
      "linux-x86_64" : [
         "archives",
         "conda",
         "rhel7",
         "rhel8",
         "ubuntu1804",
         "ubuntu2004"
      ]
   },
   "web_user" : "foo"
}"""
    sd = ShipitData(shipit_json=input_json)
    pp(sd)
    assert sd.supported_distros_by_arch("arm64") == {"ubi8", "centos8", "ubuntu2004"}
