# import logging
# from config import DEFAULT_MODEL_PATH
# import os
# import io
import cv2
import numpy as np
global graph
# import sys
# from PIL import Image
# import pygame
# from keras import backend
# import tensorflow as tf
# import matplotlib
# from matplotlib import pyplot as plt
# import matplotlib.patches as patches

from mtcnn.mtcnn import MTCNN
from core.src.SSRNET_model import SSR_net

#from moviepy.editor import *

weight_file = "./assets/ssrnet_3_3_3_64_1.0_1.0.h5"

model = SSR_net(64, [3, 3, 3], 1, 1)()
model.load_weights(weight_file)

detector = MTCNN()

def draw_label(image, point, label, font=cv2.FONT_HERSHEY_SIMPLEX,
               font_scale=1, thickness=2):
    size = cv2.getTextSize(label, font, font_scale, thickness)[0]
    x, y = point
    cv2.rectangle(image, (x, y - size[1]), (x + size[0], y), (255, 0, 0), cv2.FILLED)
    cv2.putText(image, label, point, font, font_scale, (255, 255, 255), thickness)


def detection_estimation(input_img):
    img_h, img_w, _ = np.shape(input_img)
    input_img = cv2.resize(input_img, (1024, int(1024 * img_h / img_w)))
    img_h, img_w, _ = np.shape(input_img)
    detected = detector.detect_faces(input_img)
    faces = np.empty((len(detected), 64, 64, 3))
    for i, d in enumerate(detected):
        if d['confidence'] > 0.95:
            x1, y1, w, h = d['box']
            x2 = x1 + w
            y2 = y1 + h
            xw1 = max(int(x1 - 0.4 * w), 0)
            yw1 = max(int(y1 - 0.4 * h), 0)
            xw2 = min(int(x2 + 0.4 * w), img_w - 1)
            yw2 = min(int(y2 + 0.4 * h), img_h - 1)
            cv2.rectangle(input_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            # cv2.rectangle(img, (xw1, yw1), (xw2, yw2), (255, 0, 0), 2)
            faces[i, :, :, :] = cv2.resize(input_img[yw1:yw2 + 1, xw1:xw2 + 1, :], (64, 64))

    if len(detected) > 0:
        predicted_ages = model.predict(faces)

    for i, d in enumerate(detected):
        if d['confidence'] > 0.8:
            x1,y1,w,h = d['box']
            label = "{}".format(int(predicted_ages[i]))
            draw_label(input_img, (x1, y1), label)
    return input_img


