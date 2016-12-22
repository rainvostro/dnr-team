#!/bin/bash
# Resizes all the training images to the same size and 
# saves them to PNG format using ImageMagick then classify them into subfolders by the label accordingly.
#
# Tasks:
# - resize the images
# - save to PNG format
# - subfolder images to train and val directories
#
# In addition, a label file at the image level is generated
# using information from the exams metadata table (see generate_labels.py).
#
# Author: Thomas Schaffter (thomas.schaff...@gmail.com) and DNR Team
# 

IMAGES_DIRECTORY="/trainingData"
EXAMS_METADATA_FILENAME="/metadata/exams_metadata.tsv"
IMAGES_CROSSWALK_FILENAME="/metadata/images_crosswalk.tsv"
PREPROCESS_DIRECTORY="/preprocessedData"
WRITEABLE_METADATA_DIRECTORY="/$PREPROCESS_DIRECTORY/metadata"
IMAGE_LABELS_FILENAME="$PREPROCESS_DIRECTORY/metadata/image_labels.txt" #2

PREPROCESS_IMAGES_DIRECTORY="$PREPROCESS_DIRECTORY/images" 
PREPROCESS_IMAGES_TRAIN_DIRECTORY="$PREPROCESS_IMAGES_DIRECTORY/train"
PREPROCESS_IMAGES_VAL_DIRECTORY="$PREPROCESS_IMAGES_DIRECTORY/val"
PREPROCESS_IMAGES_TRAIN_CLASS0_DIRECTORY="$PREPROCESS_IMAGES_TRAIN_DIRECTORY/0"
PREPROCESS_IMAGES_TRAIN_CLASS1_DIRECTORY="$PREPROCESS_IMAGES_TRAIN_DIRECTORY/1"
PREPROCESS_IMAGES_VAL_CLASS0_DIRECTORY="$PREPROCESS_IMAGES_VAL_DIRECTORY/0"
PREPROCESS_IMAGES_VAL_CLASS1_DIRECTORY="$PREPROCESS_IMAGES_VAL_DIRECTORY/1"

mkdir -p $PREPROCESS_IMAGES_DIRECTORY #1
mkdir -p $WRITEABLE_METADATA_DIRECTORY
mkdir -p $PREPROCESS_IMAGES_TRAIN_DIRECTORY 
mkdir -p $PREPROCESS_IMAGES_VAL_DIRECTORY 
mkdir -p $PREPROCESS_IMAGES_TRAIN_CLASS0_DIRECTORY #3
mkdir -p $PREPROCESS_IMAGES_TRAIN_CLASS1_DIRECTORY #4
mkdir -p $PREPROCESS_IMAGES_VAL_CLASS0_DIRECTORY #5
mkdir -p $PREPROCESS_IMAGES_VAL_CLASS1_DIRECTORY #6

echo "Resizing and converting $(find $IMAGES_DIRECTORY -name "*.dcm" | wc -l) DICOM images to PNG format"
find $IMAGES_DIRECTORY/ -name "*.dcm" | parallel --will-cite "convert {} -resize 500x500! $PREPROCESS_IMAGES_DIRECTORY/{/.}.png" # faster than mogrify
echo "PNG images have been successfully saved to $PREPROCESS_IMAGES_DIRECTORY/."

echo "Generating image labels to $IMAGE_LABELS_FILENAME"
python generate_image_labels.py $EXAMS_METADATA_FILENAME $IMAGES_CROSSWALK_FILENAME $IMAGE_LABELS_FILENAME
# Replace the .dcm extension to .png
sed -i 's/.dcm/.png/g' $IMAGE_LABELS_FILENAME

echo "Done resizing!"

python subfoldering.py $PREPROCESS_IMAGES_DIRECTORY $IMAGE_LABELS_FILENAME $PREPROCESS_IMAGES_TRAIN_CLASS0_DIRECTORY $PREPROCESS_IMAGES_TRAIN_CLASS1_DIRECTORY $PREPROCESS_IMAGES_VAL_CLASS0_DIRECTORY $PREPROCESS_IMAGES_VAL_CLASS1_DIRECTORY $EXAMS_METADATA_FILENAME $IMAGE_CROSSWALK_FILENAME
echo "Done subfoldering!"
