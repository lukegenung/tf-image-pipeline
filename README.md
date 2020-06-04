# Overview
Data preparation process for training an image classifier on video files.

This pipeline can be used to convert video files into images for ML training data.
Enables easy labelling of training data and image cleaning.


# To Use

video_to_mp4.py - Convert video files to MP4

mp4_to_jpeg.py - Convert MP4 files to JPEG images for training TF classifier

image_sort_gui.py - GUI to quickly label the training images by copying them into separate folders (manual labelling task)

remove_background.py - Crop out the background of training images to reduce undesired features in training images

Lastly, the TensorFlow image classifier can be trained using: python retrain.py --image_dir ~/flower_photos

More TF info here: https://www.tensorflow.org/hub/tutorials/image_retraining

And here: https://codelabs.developers.google.com/codelabs/tensorflow-for-poets/#0
