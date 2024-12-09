import numpy as np
from albumentations import (
    CLAHE,
    CenterCrop,
    ChannelShuffle,
    CoarseDropout,
    Compose,
    Cutout,
    ElasticTransform,
    GaussianBlur,
    GaussNoise,
    GridDistortion,
    HorizontalFlip,
    HueSaturationValue,
    IAASharpen,
    NoOp,
    Normalize,
    OneOf,
    OpticalDistortion,
    RandomBrightness,
    RandomBrightnessContrast,
    RandomCrop,
    RandomGamma,
    RandomRotate90,
    RandomSizedCrop,
    Rotate,
    ShiftScaleRotate,
    ToGray,
    VerticalFlip,
)
from albumentations.pytorch import ToTensor, ToTensorV2

MEAN = np.array([0.485, 0.456, 0.406])
STD = np.array([0.229, 0.224, 0.225])


def get_transforms_test():
    transforms = Compose(
        [
            Normalize(mean=(MEAN[0], MEAN[1], MEAN[2]), std=(STD[0], STD[1], STD[2])),
            ToTensorV2(),
        ]
    )
    return transforms


def denormalize(z, mean=MEAN.reshape(-1, 1, 1), std=STD.reshape(-1, 1, 1)):
    return std * z + mean
