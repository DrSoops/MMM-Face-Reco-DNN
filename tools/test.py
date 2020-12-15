from imutils.video import FPS, VideoStream
import imutils
import cv2

vs = VideoStream("nvarguscamerasrc sensor_id=0 ! nvvidconv !  appsink").start()

originalFrame = vs.read()
cv2.imwrite("IMAGE_NAME.png", originalFrame)
vs.stream.release()