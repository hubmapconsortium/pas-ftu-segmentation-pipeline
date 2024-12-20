import sys

sys.path.insert(0, "../")
import warnings

warnings.simplefilter("ignore")

import os
import pickle
import time
from os.path import join as opj

import numpy as np
import pandas as pd
from get_config import get_config
from get_fold_idxs_list import get_fold_idxs_list
from run import run
from utils import elapsed_time, fix_seed

start = time.time()
# dataset = "kidney"
dataset = "colon"

if __name__ == "__main__":
    # config
    fix_seed(2021)
    config = get_config(dataset)
    FOLD_LIST = config["FOLD_LIST"]
    VERSION = config["VERSION"]
    INPUT_PATH = config["INPUT_PATH"]
    OUTPUT_PATH = config["OUTPUT_PATH"]
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    device = config["device"]

    # import data
    train_df = pd.read_csv(opj(INPUT_PATH, "train.csv"))
    if dataset == "colon":
        train_df = train_df.rename(columns={"predicted": "encoding"})
        train_df = train_df[train_df.id != "HandE_B005_CL_b_RGB_topright"]
    info_df = pd.read_csv(opj(INPUT_PATH, "HuBMAP-20-dataset_information.csv"))
    sub_df = pd.read_csv(opj(INPUT_PATH, "sample_submission.csv"))
    print("train_df.shape = ", train_df.shape)
    print("info_df.shape  = ", info_df.shape)
    print("sub_df.shape = ", sub_df.shape)

    # dataset
    data_df = []
    for data_path in config["train_data_path_list"]:
        _data_df = pd.read_csv(opj(data_path, "data.csv"))
        _data_df["data_path"] = data_path
        data_df.append(_data_df)
    data_df = pd.concat(data_df, axis=0).reset_index(drop=True)

    data_df = data_df[data_df["std_img"] > 10].reset_index(drop=True)
    data_df["binned"] = np.round(
        data_df["ratio_masked_area"] * config["multiplier_bin"]
    ).astype(int)
    data_df["is_masked"] = data_df["binned"] > 0

    trn_df = data_df.copy()
    trn_df["binned"] = trn_df["binned"].apply(
        lambda x: config["binned_max"] if x >= config["binned_max"] else x
    )
    trn_df_1 = trn_df[trn_df["is_masked"] == True]
    print(trn_df["is_masked"].value_counts())
    print(trn_df_1["binned"].value_counts())
    print("mean = ", int(trn_df_1["binned"].value_counts().mean()))

    info_df["image_name"] = info_df["image_file"].apply(lambda x: x.split(".")[0])
    patient_mapper = {}
    for x, y in info_df[["image_name", "patient_number"]].values:
        patient_mapper[x] = y

    if dataset == "kidney":
        data_df["patient_number"] = data_df["filename_img"].apply(
            lambda x: patient_mapper[x.split("_")[0]]
        )
    elif dataset == "colon":
        data_df["patient_number"] = data_df["filename_img"].apply(
            lambda x: (
                patient_mapper["_".join(x.split("_")[0:5])]
                if x.split("_")[0] == "CL"
                else patient_mapper["_".join(x.split("_")[0:6])]
            )
        )

    val_patient_numbers_list = [
        # [67377, 67026], # fold0
        # [67548, 67112], # fold1
        # [68138, 67026], # fold2
        # [67377, 67112], # fold3
        [67112],  # [67377], # fold0
        [67112],  # [67548], # fold1
        [67112],  # [67026], # fold2
        [67112],  # [67112], # fold3
    ]

    # train
    for seed in config["split_seed_list"]:
        trn_idxs_list, val_idxs_list = get_fold_idxs_list(
            data_df, val_patient_numbers_list
        )
        with open(opj(config["OUTPUT_PATH"], f"trn_idxs_list_seed{seed}"), "wb") as f:
            pickle.dump(trn_idxs_list, f)
        with open(opj(config["OUTPUT_PATH"], f"val_idxs_list_seed{seed}"), "wb") as f:
            pickle.dump(val_idxs_list, f)
        run(seed, data_df, None, trn_idxs_list, val_idxs_list)

    # score
    score_list = []
    for seed in config["split_seed_list"]:
        for fold in config["FOLD_LIST"]:
            log_df = pd.read_csv(
                opj(config["OUTPUT_PATH"], f"log_seed{seed}_fold{fold}.csv")
            )
            score_list.append(log_df["val_score"].max())
    print("CV={:.4f}".format(sum(score_list) / len(score_list)))

print("Run time = ", elapsed_time(start))
