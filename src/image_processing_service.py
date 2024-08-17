# image_processing_service.py

from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import cv2
import numpy as np
import io
from PIL import Image as PILImage

app = Flask(__name__)
api = Api(app)
CORS(app)

class ImageProcessor:
    def resize(self, image, size):
        return cv2.resize(image, size)

    def adjust_contrast(self, image):
        alpha = 1.5  # Contrast control (1.0-3.0)
        beta = 0    # Brightness control (0-100)
        return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    def denoise(self, image):
        return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

class FeatureExtractor:
    def __init__(self):
        self.orb = cv2.ORB_create()

    def detect_keypoints(self, image):
        keypoints, _ = self.orb.detectAndCompute(image, None)
        return keypoints

    def compute_descriptors(self, image, keypoints):
        _, descriptors = self.orb.compute(image, keypoints)
        return descriptors

class ImageProcessingService:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.feature_extractor = FeatureExtractor()

    def process_image(self, image):
        image = np.array(image)
        image = self.image_processor.resize(image, (800, 600))
        image = self.image_processor.adjust_contrast(image)
        image = self.image_processor.denoise(image)
        return PILImage.fromarray(image)

    def extract_features(self, image):
        image = np.array(image)
        keypoints = self.feature_extractor.detect_keypoints(image)
        descriptors = self.feature_extractor.compute_descriptors(image, keypoints)
        return keypoints, descriptors

    def preprocess_for_reconstruction(self, images):
        processed_images = []
        for image in images:
            processed_image = self.process_image(image)
            keypoints, descriptors = self.extract_features(processed_image)
            processed_images.append({
                'image': processed_image,
                'keypoints': keypoints,
                'descriptors': descriptors
            })
        return processed_images

image_processing_service = ImageProcessingService()

class ImageProcessingResource(Resource):
    def post(self):
        image_files = request.files.getlist('images')
        images = []
        for image_file in image_files:
            image_data = image_file.read()
            image = PILImage.open(io.BytesIO(image_data))
            images.append(image)

        processed_images = image_processing_service.preprocess_for_reconstruction(images)
        return jsonify({'processed_images': len(processed_images)}), 200

api.add_resource(ImageProcessingResource, '/process')

if __name__ == '__main__':
    app.run(debug=True)