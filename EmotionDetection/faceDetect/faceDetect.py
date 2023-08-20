import cv2 as cv
import mediapipe as mp


class FaceDetection():
    def __init__(self, source = 1):
        self.vdo = cv.VideoCapture(source)

        self.faceDetection = mp.solutions.face_detection.FaceDetection()
        self.faceDraw = mp.solutions.drawing_utils

        self.faceCount = 0

    def detect(self):
        while True:
            captured, frame = self.vdo.read()

            frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            faces = self.faceDetection.process(frameRGB)

            self.faceCount = len(faces.detections)
            for ids, face in enumerate(faces.detections):
                self.faceDraw.draw_detection(frame, face)
                # print(ids, face)


            cv.imshow("Face Detection", frame)
            cv.putText(frame, f"Faces: {self.faceCount}", (20, 20), cv.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

            if cv.waitKey(10) == ord('q'):
                break

        self.vdo.release()
        cv.destroyAllWindows()


if __name__ == "__main__":
    FD = FaceDetection()
    FD.detect()

