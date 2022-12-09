import cv2

thres = 0.5

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

classNames = []
classFile = "Resources/coco.names"

with open(classFile, 'rt') as f:
    classNames = f.read().strip('\n').split('\n')

config = "Resources/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weights = "Resources/frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weights, config)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

while True:
    success, img = cap.read()
    classIds, confs, bbox = net.detect(img, confThreshold = thres)

    print(classIds, bbox)
    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            cv2.rectangle(img, box, color = (255, 0, 255), thickness = 2)
            cv2.putText(img, classNames[classId-1].upper(), (box[0]+10, box[1]+30), cv2.FONT_ITALIC, 1, (0, 255, 255), 2)
            cv2.putText(img, str(round(confidence*100, 2)), (box[0]+200, box[1]+30), cv2.FONT_ITALIC, 1, (0, 255, 255), 2)

    cv2.imshow("Detection", img)

    cv2.waitKey(1)