from xml.etree.ElementTree import PI
import cv2

def fetch_pipeline(roi):
    pipeline = Pipeline([
        ('cropper', Cropper(roi)),
        ('grayscale', ToGrayscale())
    ])
    return pipeline

class Pipeline:
    def __init__(self, components):
        self.components = components

    def fit(self, X, y=None):
        for component_name, component in self.components:
            component.fit(X, y)
        return self

    def transform(self, X, y=None):
        new_X = X
        for component_name, component in self.components:
            new_X = component.transform(new_X)
        return new_X

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X, y)

class Cropper:
    def __init__(self, roi):
        # assert len(roi) == 4 
        self.roi = roi

    def __crop_to_roi(self, image):
        return image[self.roi[0]:self.roi[1], self.roi[2]:self.roi[3]]

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return self.__crop_to_roi(X)

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X, y)

class ToGrayscale:
    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return cv2.cvtColor(X, cv2.COLOR_BGR2GRAY)

    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X, y)