import os
import argparse
from pipelines import DetectHumanPose2D
from tensorflow.keras.models import load_model
from paz.backend.image import write_image, load_image
from dataset import JOINT_CONFIG, FLIP_CONFIG


# check for numpy implementation of Munkers
# images directory name should be consistant with the readme
parser = argparse.ArgumentParser(description='Test keypoints network')
parser.add_argument('-i', '--image_path', default='images',
                    help='Path to the image')
parser.add_argument('-m', '--model_weights_path', default='models_weights_tf',
                    help='Path to the model weights')
args = parser.parse_args()

image_path = os.path.join(args.image_path, 'image1.jpg')
model_path = os.path.join(args.model_weights_path, 'HigherHRNet')
model = load_model(model_path)
print("\n==> Model loaded!\n")
image = load_image(image_path)

dataset = 'COCO'
# data_with_center - needed for 3D pose estimation
data_with_center = False
if data_with_center:
    joint_order = JOINT_CONFIG[dataset + '_WITH_CENTER']
    fliped_joint_order = FLIP_CONFIG[dataset + '_WITH_CENTER']
else:
    joint_order = JOINT_CONFIG[dataset]
    fliped_joint_order = FLIP_CONFIG[dataset]


detect = DetectHumanPose2D(model, joint_order, fliped_joint_order,
                           dataset, data_with_center)
output = detect(image)
write_image('output/result.jpg', output['image'])
