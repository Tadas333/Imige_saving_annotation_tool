import cv2
import numpy as np
import time
import argparse



# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--input", required=True,
# 	help="path to input video")

# ap.add_argument("-o", "--output", required=True,
# 	help="output dir")
# args = vars(ap.parse_args())


vidcap = cv2.VideoCapture("45_4.mp4")
success,image = vidcap.read()
count = 0;

#INPUT_FILE='img_70.jpg'
#OUTPUT_FILE='predicted.jpg'


LABELS_FILE='coco.names'
CONFIG_FILE='yolov3.cfg'
WEIGHTS_FILE='yolov3.weights'
CONFIDENCE_THRESHOLD=0.8

LABELS = open(LABELS_FILE).read().strip().split("\n")


# number of frames to skip
numFrameToSave = 10

#print "I am in success"
while success: # check success here might break your program
  success,image = vidcap.read() #success might be false and image might be None
  #check success here
  if not success:
    break

  # on every numFrameToSave 
  if (count % numFrameToSave ==0):


        np.random.seed(4)
        COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
            dtype="uint8")


        net = cv2.dnn.readNetFromDarknet(CONFIG_FILE, WEIGHTS_FILE)

        #image = cv2.imread(INPUT_FILE)
        (H, W) = image.shape[:2]

        # determine only the *output* layer names that we need from YOLO
        ln = net.getLayerNames()
        ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
            swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()


        #print("[INFO] YOLO took {:.6f} seconds".format(end - start))
        print(count)

        # initialize our lists of detected bounding boxes, confidences, and
        # class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                if classID == 8:
                    confidence = scores[classID]

                    # filter out weak predictions by ensuring the detected
                    # probability is greater than the minimum probability
                    if confidence > CONFIDENCE_THRESHOLD:
                        cv2.imwrite("outputs/img_%3d.jpg" % count, image)
                        #args["input"]
                        print("saved")
        



    #cv2.imwrite("img_%3d.jpg" % count, image)   

  if cv2.waitKey(10) == 27:                     
      break
  count += 1
