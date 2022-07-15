import cv2
import time
import serial
import threading

ARDUINO_SERIAL = serial.Serial('com3',9600)
time.sleep(2)
print (ARDUINO_SERIAL.readline())
print ("You have new message from Arduino")

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') 
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml') 
smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml') 

# apakah sedang terhubung dengan arduino
is_comm = False
# siklus / proses jeda baca
cycles = 0
THRESHOLD_CYCLES = 20 #cycles

DELAY_TIME = 4

def call_arduino():
	global is_comm
	global cycles
	try :
		ARDUINO_SERIAL.write("1".encode())
		print ("STATE->OPEN")
		time.sleep(DELAY_TIME)
		ARDUINO_SERIAL.write("0".encode())
		print ("STATE->OFF")
		is_comm = False
		cycles = 0
	except Exception as e :
		print(e)

def detect(gray, frame): 
	global is_comm
	global cycles

	faces = face_cascade.detectMultiScale(gray, 1.3, 5) 
	for (x, y, w, h) in faces: 
		cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (255, 0, 0), 2) 
		roi_gray = gray[y:y + h, x:x + w] 
		roi_color = frame[y:y + h, x:x + w] 
		smiles = smile_cascade.detectMultiScale(roi_gray, 1.9, 50) 

		if(len(smiles) > 0):
			cycles += 1
			if(cycles >= THRESHOLD_CYCLES) :
				if(is_comm != True):
					is_comm = True
					comm = threading.Thread(target=call_arduino, args=())
					comm.start()
		else :
			cycles = 0

		for (sx, sy, sw, sh) in smiles: 
			cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2) 

	if(len(faces) < 1):
		if(is_comm != True):
			ARDUINO_SERIAL.write("0".encode())
			cycles = 0

	return frame 


video_capture = cv2.VideoCapture(0) 
while True: 
	# Captures video_capture frame by frame 
	_, frame = video_capture.read()  
	
	# To capture image in monochrome                     
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   
	  
	# calls the detect() function     
	canvas = detect(gray, frame)    
	
	# Displays the result on camera feed                      
	cv2.imshow('Video', canvas)  
	
	# The control breaks once q key is pressed                         
	if cv2.waitKey(1) & 0xff == ord('q'):                
	     break

# Release the capture once all the processing is done. 
video_capture.release()                                  
cv2.destroyAllWindows() 