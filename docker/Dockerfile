FROM nvidia/cuda:11.6.0-cudnn8-devel-ubuntu20.04
ENV DEBIAN_FRONTEND=noninteractive

## System packages
# I'm used to using `apt` but it complains that it doesn't have a stable
#   command-line interface, so let's use `apt-get` instead
RUN apt-get update \
 && apt-get -y install \
    git \
    python3 \
    python3-dev \
    python3-pip \
 && rm -rf /var/cache/apt/*

## Python packages
COPY docker/requirements.txt /opt/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install astunparse numpy ninja pyyaml setuptools cmake cffi typing_extensions future six requests dataclasses

# install torch from source
RUN git clone --recursive https://github.com/pytorch/pytorch
WORKDIR pytorch
ENV PYTORCH_BUILD_VERSION=1.8.2
ENV PYTORCH_BUILD_NUMBER=1
ENV USE_CUDA=1 USE_CUDNN=1
ENV TORCH_CUDA_ARCH_LIST="3.5" TORCH_NVCC_FLAGS="-Xfatbin -compress-all"
ENV CMAKE_PREFIX_PATH="$(dirname $(which conda))/../"
ENV MAX_JOBS=2
RUN python setup.py clean \
    && python setup.py install

RUN pip3 install -r /opt/requirements.txt \
 && rm -rf /root/.cache/pip

RUN mkdir /root/.ssh

COPY bin /opt
COPY data /opt

WORKDIR /opt
