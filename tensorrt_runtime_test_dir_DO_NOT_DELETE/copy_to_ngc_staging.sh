#!/bin/bash

image_name="urm.nvidia.com/sw-gpu-cuda-installer-docker-local/cuda/l4t-cuda"
image_name_ngc="nvcr.io/ea-linux4tegra"
image_name_product="l4t-cuda"
image_name_trt_product="l4t-tensorrt"

tags=("10.2.460-cudnn8-devel-ubuntu18.04-006"
      "10.2.460-cudnn8-runtime-ubuntu18.04-006"
      "10.2.460-base-ubuntu18.04-006"
      "10.2.460-runtime-ubuntu18.04-006"
      "10.2.460-devel-ubuntu18.04-006"
      "10.2.460-tensorrt8-runtime-ubuntu18.04-006"
)

parse_image_tag() {
    local image=$1 # in the form of <image_name>:<tag>
    # dumps to stdout a comma separated tuple of image_name,cuda_version,tag,distro,arch,tag_suffix,image

    # 10.2.460-cudnn8-devel-ubuntu18.04-006

    if [[ $image =~ ([0-9]*).([0-9]*).([0-9]*)-([a-z0-9]*)?-?(base|runtime|devel)-ubuntu18.04 ]]; then
        # for match in ${BASH_REMATCH[1]} ${BASH_REMATCH[2]} ${BASH_REMATCH[3]} ${BASH_REMATCH[4]} ${BASH_REMATCH[5]}; do
        #     # mandatory
        #     if [[ -z $match ]]; then
        #         return 1
        #     fi
        # done
        printf "%s" "${BASH_REMATCH[1]},${BASH_REMATCH[2]},${BASH_REMATCH[3]},${BASH_REMATCH[4]},${BASH_REMATCH[5]}"
    else
        return 1
    fi
}

for tag in "${tags[@]}"; do
  t=$(parse_image_tag $tag)
  cuda_version=$(echo $t | cut -f1-3 -d, | sed 's/,/./g')
  dlfw=$(echo $t | cut -f4 -d, )
  type=$(echo $t | cut -f5 -d, )
  if [[ ${dlfw} =~ base|runtime|devel ]]; then
      type="${dlfw}"
      unset dlfw
  fi

  # echo "tag: $tag"
  # echo "cuda_version: ${cuda_version}"
  # echo "dlfw: ${dlfw}"
  # echo "type: ${type}"

  skopeo="/usr/bin/skopeo copy docker://${image_name}:${tag} "
  if [[ "${type}" =~ "runtime" ]]; then
      if [[ ${dlfw} =~ tensor ]]; then
          # FIXME: get trt version from image label
          cmd="${skopeo} docker://${image_name_ngc}/${image_name_trt_product}-runtime:r8.0.1"
      elif [[ ${dlfw} =~ cudnn ]]; then
          cmd="${skopeo} docker://${image_name_ngc}/l4t-cudnn-runtime:r8.2.1.32-cuda10.2"
      else
          cmd="${skopeo} docker://${image_name_ngc}/${image_name_product}-runtime:${cuda_version}${dlfw:+`echo -${dlfw}`}"
      fi
  elif [[ "${type}" =~ "devel" ]]; then
      continue
  elif [[ "${type}" =~ "base" ]]; then
      cmd="${skopeo} docker://${image_name_ngc}/${image_name_product}-base:${cuda_version}${dlfw:+`echo -${dlfw}`}"
  fi
  echo "Running command: '${cmd}'"
  ${cmd}
done
