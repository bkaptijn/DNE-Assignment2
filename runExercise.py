from mmpose.apis import MMPoseInferencer
from collections import defaultdict
import poseDefinition as pd

inferencer = MMPoseInferencer('human', device='cpu')
result_generator = inferencer('webcam:1', show=True)
 
#
# filters out keypoints with a key point score below and up until a given treshold
# returns the keypoints in a list discarding the rest of the mmpose inferencer result dict
#
def filterKP(result, treshold):
    kp = list(enumerate(result['predictions'][0][0]['keypoints']))
    score = list(enumerate(result['predictions'][0][0]['keypoint_scores']))
    return [a[1] for a in kp if score[a[0]][1] > treshold]
 
def runloop():
    print("Starting webcam so get ready... use CTRL-C to quit without rasing your right arm properly")
    running = True
    while running:
         result = next(result_generator)
         confidentKP = filterKP(result, 0.5) # get the keypoints with enough score (kp's with score lower than 0.5 do not get visualised also)
         if(pd.match(confidentKP, pd.raisedRightArmDefinition)):
             print("You raised your right arm in the right way according to the definition ;-)")
             running = False
         print(result)

runloop()

print("Bye!")
