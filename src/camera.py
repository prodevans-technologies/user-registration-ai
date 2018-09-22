import cv2
import threading
import os

from src.scripts import label_image


class RecordingThread (threading.Thread):
    def __init__(self, name, camera, file_path):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera
        self.path = "./photos/"+file_path+"/"

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
                    # Getting the ROI for storing the photos
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

        # Counter
        self.counter = 0
        # Thread for recording
        self.recordingThread = None

        # Haar cascade
        # https://github.com/Itseez/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
        self.face_cascade = cv2.CascadeClassifier(
            'haarcascade_frontalface_default.xml')

        # Capture status
        self.capture_status = True

        # Meta data path
        self.model_file = "train_meta/retrained_graph.pb"
        self.label_file = "train_meta/retrained_labels.txt"

        # Detect image count
        self.image_count = 0

        # folder path
        self.dir_path = "tmp/"

    def __del__(self):
        self.cap.release()

    def get_frame(self, email, save):

        # Capture the frame
        ret, frame = self.cap.read()
        # Converting into the gray scale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detecting the faces avaliable in image
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)

            if save and self.counter <= 100:
                # File path to store the image
                path = "./photos/" + email + "/"

                # Creating the path if not exists
                if not os.path.exists(path):
                    os.mkdir(path)

                for (x, y, w, h) in faces:
                    # Getting the ROI for storing the photos
                    roi_color = frame[y:y + h, x:x + w]
                    # Drowing the rectangel
                    cv2.rectangle(frame, (x, y), (x + w, y + h),(255, 0, 0), 2)
                    # Incrementaing
                    self.counter += 1
                    # Writing the image into the fs
                    cv2.imwrite(path + str(self.counter)+".jpeg", roi_color)

            else:
                self.capture_status = False
                self.counter = 0


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

    # def start_capture(self, file_path):
    #     self.is_record = True
    #     self.recordingThread = RecordingThread(
    #         "Video Recording Thread", self.cap, file_path)
    #     self.recordingThread.start()

    def check_capture(self):
        # self.counter
        return self.capture_status

    def detect_person(self):
        # Capture the frame
        ret, frame = self.cap.read()
        # Converting into the gray scale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detecting the faces avaliable in image
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        if ret:

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                roi_color = frame[y:y + h, x:x + w]
                self.image_count += 1
                file_name = self.dir_path + str(self.image_count)+".jpeg"
                cv2.imwrite(file_name,roi_color)
                results, labels, top_k = label_image.detectLabel(self.dir_path + str(self.image_count)+".jpeg", self.model_file, self.label_file)
                template = "{} (score={:0.5f})"
                for i in top_k:
                    print(template.format(labels[i], results[i]))
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, labels[top_k[0]], (x, y + h), font, 1, (200,255,255), 2, cv2.LINE_AA)
            # Converting the image
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

        else:
            return None