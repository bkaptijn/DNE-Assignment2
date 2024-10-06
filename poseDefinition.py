
#
# A normalised pose sorts the keypoints by Y coordinate then by X coordinate
# then assigns id's to the keypoints in this order (starting at 1)
# then create a list with these keypoint id's but in the ordering of the
# keypoints along the x axis (only considering their x coordinate)
#
# By definition the coordinate for the y axis is always id's 1 to N for N
# given keypoints so we could also generate this
#
def toNormalizedPose(keypoints):
    sKP = sorted(keypoints, key=lambda k: (k[1], k[0]))

    enumsortedKP = list(enumerate(sKP, start=1))
    
    lX = sorted(enumsortedKP, key=lambda k: k[1][0])
    lY = sorted(enumsortedKP, key=lambda k: k[1][1])

    idsX = [i[0] for i in lX]
    idsY = [i[0] for i in lY]
    
    print(idsX)

    idsX.reverse() # the webcam seems to mirror on the X axis, this corrects this

    print(idsX)

    return (
        idsX,
        idsY
    )

#
# relaxes a pose item using the definition of a pose Definition Item
# (with item the X or Y axis part of a pose(Definition) is meant).
# Relaxation means that the tuples within the definition item indicate which
# elements in the pose item are sorted ascending and its elements put in the
# pose item's list as elements without tuples. For instance:
#
# given a pose item : [1,2,4,3,5]
# and given a definition item : [(2),(1),(5,3,4)]
# the result becomes [1,2,3,4,5]
#
# note that this method does not look at or compare the id's itself
# it only sorts certain parts of an item as indicated in the definition item
#
def relax(pose, poseDefinitionItem):
    i = 0
    res = []
    for item in poseDefinitionItem:
        if type(item) is tuple:
            e = i + len(item)
            res = res + sorted(pose[i:e])
            i = e
        else:
            res.append(pose[i])
            i = i + 1
    return res

#
# relaxes both items of a pose according to a pose definition,
# see the description of the relax() method for more information
#
def relaxPose(pose, poseDefinition):
    return (
        relax(pose[0], poseDefinition[0]),
        relax(pose[1], poseDefinition[1])
    )

#
# relaxes a pose definition item by sorting the tuples within ascending
# and putting it's elements directly in the list (removing the tuples)
# For instance:
# [(1),(2),(4,3,5)] becomes [1,2,3,4,5]
#
def relaxDefinition(poseDefinitionItem):
    res = []
    for item in poseDefinitionItem:
        if type(item) is tuple:
            res = res + sorted(item)
        else:
            res.append(item)
    return res
   
#
# relaxes both items of a pose definition, see the description of
# the relaxDefinition() method for more information
#
def relaxPoseDefinition(poseDefinition):
    return (
        relaxDefinition(poseDefinition[0]),
        relaxDefinition(poseDefinition[1])
    )

def match(keypoints, poseDefinition):
    print(poseDefinition)
    relaxedPoseDefinition = relaxPoseDefinition(poseDefinition)
    print("relaxed pose definition:")
    print(relaxedPoseDefinition)
    pose = toNormalizedPose(keypoints)
    print("normalized pose:")
    print(pose)
    if(len(pose[0]) != len(relaxedPoseDefinition[0])):
        print("no match: not the same number of keypoints")
        return False
    relaxedPose = relaxPose(pose, poseDefinition)
    print("relaxed normalized pose:")
    print(relaxedPose)
    return relaxedPose == relaxedPoseDefinition

#                   __ right arm on the right of right shoulder
#                  /  \
#      _head____   (1) - hand above head
#     (  2---3  )   |
#     ( 4 \ / 5 )   |
#     (/___6___\)   |
#    (7)        \   /
#               (8-9)  - shoulders / elbow below head and left shoulder
#            \______/   head between shoulders
#
# Note due to a shortcoming (see comment below) one also needs to make the left
# shoulder to be above the right shoulder. It could also be a feature
#
raisedRightArmDefinition = (
    [7,(4,2,6,3,5),8,(9,1)],
    [(1),(2,3,4,5,6),(7),(8,9)]
)
#
# TODO note but this first attempt fails to address
# when for instance a left shoulder is below the right shoulder and you want
# to allow for this which could be improved when the id's in the x axis part would
# be matched with the tuple in the y axis part and then the id's
# that match the same y axis tuple would be sorted ascending keeping
# the order in the x axis intact in relation to how they match the y-axis tuples
#
# so:
#
#(
#    [7,(4,2,6,3,5),8,(9,1)],
#    [(1),(2,3,4,5,6),(7,8,9)]
#)
#
# becomes:
#
#(
#    [2,(1,1,1,1,1),2,(2,0)],   <-- references to which tuple in the Y axis part
#    [(1),(2,3,4,5,6),(7,8,9)]  <-- three tuples (0,1 and 2) in the Y axis part
#)
#
# and then is used to check the pose item for the X axis if the id's in it
# are in the indicated tuples of the Y axis of the definition and the elements
# of the same y axis tuple are sorted in the X axis pose
#
# which makes the pose [8,4,6,3,5,2,9,7,1] match the definition
# as [7,2,3,4,5,6,8,1,9] will match [7,2,3,4,5,6,8,1,9] (after relaxation)
#
# but this could be made configurable as like other types of constraints
# and relaxations (like 3 keypoints need to be more or less in line (streched arm))
#
