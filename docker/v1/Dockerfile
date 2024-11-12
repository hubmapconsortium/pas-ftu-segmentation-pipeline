FROM nvidia/cuda:11.6.1-cudnn8-devel-ubuntu20.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
 && apt-get -y install \
    git \
    python3 \
    python3-dev \
    python3-pip \
    wget \
 && rm -rf /var/cache/apt/*

## Python packages
COPY docker/v1/requirements.txt /opt/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html

RUN pip3 install -r /opt/requirements.txt \
 && rm -rf /root/.cache/pip

WORKDIR /opt/models
RUN wget \
    https://hubmap-pipeline-assets.s3.us-east-1.amazonaws.com/ftu-segmentation-models/glomerulus/model_seed0_fold0_bestscore.pth \
    https://hubmap-pipeline-assets.s3.us-east-1.amazonaws.com/ftu-segmentation-models/glomerulus/model_seed0_fold1_bestscore.pth \
    https://hubmap-pipeline-assets.s3.us-east-1.amazonaws.com/ftu-segmentation-models/glomerulus/model_seed0_fold2_bestscore.pth \
    https://hubmap-pipeline-assets.s3.us-east-1.amazonaws.com/ftu-segmentation-models/glomerulus/model_seed0_fold3_bestscore.pth

RUN mkdir /root/.ssh

COPY bin /opt
COPY data /opt

WORKDIR /opt
