import cv2 as cv
import mediapipe as mp
# import numpy as np
import time


class FaceDetection():
    def __init__(self, source = 1):
        self.vdo = cv.VideoCapture(source, cv.CAP_DSHOW)
        self.vdo.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
        self.vdo.set(cv.CAP_PROP_FRAME_HEIGHT, 720)

        self.faceDetection = mp.solutions.face_detection.FaceDetection(0.8)
        self.faceDraw = mp.solutions.drawing_utils

        self.faceCount = 0
        self.faceList = []

    def processFrame(self, frame):
        try:
            frameGR = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            frameGR = cv.resize(frameGR, (48, 48), interpolation=cv.INTER_LINEAR)
        except:
            print("Failed to catch frame.")

        return frameGR


    def detect(self):
        # t1 = 0
        while True:
            captured, frame = self.vdo.read()
            self.faceCount = 0
            self.faceList = []

            frameShape = frame.shape
            frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            faces = self.faceDetection.process(frameRGB)

            if faces.detections:
                self.faceCount = len(faces.detections)
                for face in faces.detections:
                    bboxR = face.location_data.relative_bounding_box
                    # bbox[y1, x1, y2, x2]
                    bbox = (int(bboxR.ymin*frameShape[0]), int(bboxR.xmin*frameShape[1]), int((bboxR.ymin + bboxR.height)*frameShape[0]), int((bboxR.xmin + bboxR.width)*frameShape[1]))

                    faceOnly = self.processFrame(frame[bbox[0] : bbox[2], bbox[1] : bbox[3]])
                    self.faceList.append(faceOnly)

                    # Display detection
                    self.faceDraw.draw_detection(frame, face)
                    cv.putText(frame, f"Confidence: {int(face.score[0] * 100)}",(int(bboxR.xmin * frameShape[1]), int(bboxR.ymin * frameShape[0]) -10), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                    # print(ids, face)

            print(self.faceList)

            # Check FPS
            # t2 = time.time()
            # fps = 1/(t2 - t1)
            # t1 = t2
            # cv.putText(frame, f"FPS: {int(fps)}", (20, 30), cv.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 200, 0), 1)

            # Display detection
            cv.putText(frame, f"Faces: {self.faceCount}", (20, 20), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
            cv.imshow("Face Detection", frame)

            if cv.waitKey(100) == ord('q'):
                break

        self.vdo.release()
        cv.destroyAllWindows()


if __name__ == "__main__":
    FD = FaceDetection()
    FD.detect()

