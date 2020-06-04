# camera.py
# import the necessary packages
import cv2

# defining face detector
ds_factor = 0.6


class VideoCamera(object):
    def __init__(self):
        # capturing video
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        # releasing camera
        self.video.release()

    def get_frame(self, SendText=None):
        # extracting frames
        ret, frame = self.video.read()
        frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor,
                           interpolation=cv2.INTER_AREA)
        font = cv2.FONT_HERSHEY_COMPLEX
        if SendText != None:
            cv2.putText(frame, SendText, (50, 50), font,
                        1, (255, 0, 0), 2, cv2.LINE_AA)  # Our operations on the frame come here
        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
