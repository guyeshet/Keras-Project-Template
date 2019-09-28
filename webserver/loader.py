import os
from collections import Counter

import numpy as np
from keras.engine.saving import load_model

from utils.utils import from_env, get_root
from webserver.storage.factory import StorageFactory

model = None
MODEL_TYPE = from_env('MODEL_TYPE', 'uk_target_only_native_speakers')
MODEL_NUM = from_env('MODEL_NUM', "64812b64080b4668ac824c9ca75b6c04")


def predict_class_audio(MFCCs):
    '''
    Predict class based on MFCC samples
    :param MFCCs: Numpy array of MFCCs
    :param model: Trained model
    :return: Predicted class of MFCC segment group
    '''
    global model
    MFCCs = MFCCs.reshape(MFCCs.shape[0], MFCCs.shape[1], MFCCs.shape[2], 1)
    y_predicted = model.predict_classes(MFCCs, verbose=0)
    return Counter(list(y_predicted)).most_common(1)[0][0]


def load(from_cloud=True):
    # The current served model based on the experiment type

    global model

    storage = StorageFactory.default()
    file_path = storage.load_model(MODEL_TYPE, MODEL_NUM)
    model = load_model(file_path)

    # BUG fix - initializing the model with an empty vector
    model.predict(np.zeros((1, 13, 30, 1)))

load()