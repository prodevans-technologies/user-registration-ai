import cv2
import threading
import os


class RecordingThread (threading.Thread):
    def __init__(self, name, camera, file_path):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera
        self.path = "./images/"+file_path+"/"

        # Creating the path
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        # self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))

        # Haar cascade
        # https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def run(self):
        i = 0
        while self.isRunning:
            # Reading the image
            ret, frame = self.cap.read()
            # Converting into the gray scale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detecting the faces avaliable in image
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            if ret:
                for (x, y, w, h) in faces:
                    # Getting the ROI for storing the images
                    roi_color = frame[y:y + h, x:x + w]
                    # Drowing the rectangel
                    cv2.rectangle(frame, (x, y), (x + w, y + h),(255, 0, 0), 2)
                    # Incrementaing
                    i += 1
                    # Writing the image into the fs
                    cv2.imwrite(self.path + str(i)+".jpeg", roi_color)
            if i > 100:
                self.isRunning = False

    def stop(self):
        self.isRunning = False

    def get_status(self):
        return self.isRunning

    def __del__(self):
        # self.out.release()
        pass


class VideoCamera(object):
    def __init__(self):
        # Open a camera
        self.cap = cv2.VideoCapture(0)

        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None

        # Haar cascade
        # https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
        self.face_cascade = cv2.CascadeClassifier(
            'haarcascade_frontalface_default.xml')

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()

        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)

            # Record video
            # if self.is_record:
            #     if self.out == None:
            #         fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            #         self.out = cv2.VideoWriter('./static/video.avi',fourcc, 20.0, (640,480))

            #     ret, frame = self.cap.read()
            #     if ret:
            #         self.out.write(frame)
            # else:
            #     if self.out != None:
            #         self.out.release()
            #         self.out = None

            return jpeg.tobytes()

        else:
            return None

    def start_capture(self, file_path):
        self.is_record = True
        self.recordingThread = RecordingThread(
            "Video Recording Thread", self.cap, file_path)
        self.recordingThread.start()

    def check_capture(self):
        if self.recordingThread != None:
            return self.recordingThread.get_status()

