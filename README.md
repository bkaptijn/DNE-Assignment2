# Assignment 2, Deep Neural Engineering (23-24)
## topic : project 3

This is a tiny example exercise project that goes together with the report and is intended for educational purpose only

## Installation

You will need to install MMPose as described on their website: https://mmpose.readthedocs.io/en/latest/installation.html

Note that at step 3 you may need to indicate to install a mmcv version below 2.2.0, so use

mim install “mmcv>=2.0.1,<2.2.0”

You might need to change the webcam id in the runExercise.py script (for the MacBook M3 it is webcam:1, but it might be different on other hardware.. you can also make it use a default by omitting the number : so just "webcam" instead of "webcam:1")

tested on a MacBook M3, the gpu of a M3 does not seem to be supported though as mmpose seems to use unsupported features not (yet) implemented 
for PyTorch icw such processors, but cpuonly works ok

## How to run:

from a terminal while in this folder do:

python runExercise.py

## hint

If all goes well, a screen with your webcam stream pops up. This example has been created with the assumption you sit behind a laptop with the webcam
capturing you. Now the script does not end until the webcam captures a certain pose as programmed in the pose definition which is:

1) you sit straight, looking forward to the camera
2) you move your right should a little bit below the level of your left shoulder
3) you raise your right arm at the right of your right shoulder

also:

4) you make sure the pose estimator (you will see the skeleton estimated viasualised) does not find keypoints of your hand or below your shoulders (this could be improved upon)
5) note that the webcam will show you mirrored (might depend on your system). If raising your right arm does not show your arm at the left of the screen being raised, comment
   line 24 of poseDefinition.py
6) if you want to force the script to end, just do a CTRL-C in the terminal
7) you might want to read the comments in the poseDefinition.py script to understand the exercise
8) the script logs how it captures keypoints and matches it with the pose definition to stdout

If you pose properly according to the definition, your goal has been reached and the script ends

## extra stuff in this repository

To see the algorithm in action also the test-inference.py script can be used. It will process two images in the input folder. The first image is wrong (wrong arm) and the second one will be recognized as matching the posture definition defined in poseDefinition.py

Also you can find an example movie in the output/visualisations folder of a typical webcam session (sped up as each frame is the result of an inference which takes a second or so with cpu only). You can easily generate such thing by editing the runExercise.pu script to add an extra "out_dir='output'" argument to the inferencer instantiation (line 6), as also described in the mmpose documentation
