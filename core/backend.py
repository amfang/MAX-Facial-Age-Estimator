
import logging
from config import DEFAULT_MODEL_PATH, DEFAULT_DETECTOR_PATH
import os
import io
import cv2
import numpy as np
from core.src.SSRNET_model import SSR_net
import sys
from mtcnn.mtcnn import MTCNN
from PIL import Image
from keras import backend
import tensorflow as tf
global graph

logger = logging.getLogger()
def draw_label(image, point, label, font=cv2.FONT_HERSHEY_SIMPLEX,
               font_scale=1, thickness=2):
    size = cv2.getTextSize(label, font, font_scale, thickness)[0]
    x, y = point
    cv2.rectangle(image, (x, y - size[1]), (x + size[0], y), (255, 0, 0), cv2.FILLED)
    cv2.putText(image, label, point, font, font_scale, (255, 255, 255), thickness)


def read_still_image(still_img):
    image = Image.open(io.BytesIO(still_img))
    image = np.array(image)
    return image


class ModelWrapper(object):
    """Model wrapper for SavedModel format"""
    def __init__(self, path=DEFAULT_MODEL_PATH, detector_path=DEFAULT_DETECTOR_PATH):
        logger.info('Loading model from: {}...'.format(path))
        logger.info('Loading face detector from: {}...'.format(detector_path))

        # for face detection
        self.detector = MTCNN()
        try:
            os.mkdir('./img')
        except OSError:
            pass

        # load model and weights
        self.img_size = 64
        self.stage_num = [3, 3, 3]
        self.lambda_local = 1
        self.lambda_d = 1

        # load pre-trained model
        self.model = SSR_net(self.img_size, self.stage_num, self.lambda_local, self.lambda_d)()
        self.model_path = path
        self.detector_path = detector_path
        self.model.load_weights(self.model_path)

        self.graph = tf.get_default_graph()

        self.face_cascade = cv2.CascadeClassifier(detector_path)

        logger.info('Loaded model')

    def predict(self, x):
        input_img = x

        # python version
        pyFlag = ''
        if len(sys.argv) < 3:
            pyFlag = '2'  # default to use moviepy to show, this can work on python2.7 and python3.5
        elif len(sys.argv) == 3:
            pyFlag = sys.argv[2]  # python version
        else:
            print('Wrong input!')
            sys.exit()

        detected = ''  # make this not local variable
        ad = 0.4


        img_h, img_w, _ = np.shape(input_img)
        input_img = cv2.resize(input_img, (1024, int(1024 * img_h / img_w)))
        img_h, img_w, _ = np.shape(input_img)

        # for webcam
        gray_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
        detected = self.face_cascade.detectMultiScale(gray_img, 1.1)
        dd=[]
        for i in range(len(detected)):
            dd.append({'box':detected[i]})
        detected=dd
        faces = np.empty((len(detected), self.img_size, self.img_size, 3))

        for i, d in enumerate(detected):
            x1, y1, w, h = d['box']
            x2 = x1 + w
            y2 = y1 + h
            xw1 = max(int(x1 - ad * w), 0)
            yw1 = max(int(y1 - ad * h), 0)
            xw2 = min(int(x2 + ad * w), img_w - 1)
            yw2 = min(int(y2 + ad * h), img_h - 1)
            cv2.rectangle(input_img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            # cv2.rectangle(img, (xw1, yw1), (xw2, yw2), (255, 0, 0), 2)
            faces[i, :, :, :] = cv2.resize(input_img[yw1:yw2 + 1, xw1:xw2 + 1, :], (self.img_size, self.img_size))

        if len(detected) > 0:
            with self.graph.as_default():
                predicted_ages = self.model.predict(faces)

        # prediction results with BBX & AGES
        pred_res = []
        for i, d in enumerate(detected):
            # if d['confidence'] > 0.95:
            pre_age=predicted_ages[i].astype(int)
            pred_res.append([{'box': d['box'], 'age':pre_age}])

        return pred_res
