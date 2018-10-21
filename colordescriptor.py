import numpy as np
import cv2
import imutils

class colorDescriptor:
    def __init__(self, bins):
        self.bins = bins
    # store the number of bins for the 3D histogram

    def describe(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        features = []  # convert the image to the HSV color space and initialize the features used to quantify the image
        (h, w) = image.shape[:2]
        (cX, cY) = (int(w * 0.5), int(h * 0.5))  # grab the dimensions and compute the center of the image
        segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h), (0, cX, cY, h)]
        # divide image into 4 rectangles (top-left, top-right, bottom-right, bottom-left)
        (axesX, axesY) = (
        int(w * 0.75) // 2, int(h * 0.75) // 2)  # construct elliptical mask representing center of image
        ellipMask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)

        for (startX, endX, startY, endY) in segments:
            # construct a mask for each corner of the image, subtracting elliptical center from it
            cornerMask = np.zeros(image.shape[:2], dtype="uint8")
            cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
            cornerMask = cv2.subtract(cornerMask, ellipMask)
            # extract a color histogram from image, then update feature vector
            hist = self.histogram(image, cornerMask)
            features.extend(hist)

        # extract a color histogram from the elliptical region and update the feature vector
        hist = self.histogram(image, ellipMask)
        features.extend(hist)
        return features

    def histogram(self, image, mask):
        # extract a 3D color histogram from the masked region of image, using the supplied number of bins per channel
        hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins, [0, 180, 0, 256, 0, 256])

        if imutils.is_cv2():
            hist = cv2.normalize(hist).flatten()
        else:
            hist = cv2.normalize(hist, hist).flatten()
        return hist