# import umap.umap_ as umap
import pickle

import umap

train_data = pickle.load(open("feature_train", "rb"))
test_data = pickle.load(open("feature_test", "rb"))

embedding = umap.UMAP().fit_transform(train_data)
