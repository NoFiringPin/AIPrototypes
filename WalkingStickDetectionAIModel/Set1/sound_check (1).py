import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)

buzzerPin = 18
GPIO.setup(buzzerPin, GPIO.OUT)
buzzer = GPIO.PWM(buzzerPin, 440)

noteID = 16
letters = ('c','c#','d','d#','e','f','f#','g','g#','a','a#','b')
notes = {}

for i in range(2,4):
	for l in letters:
		f = 2 ** ((noteID-49)/12) * 440
		notes[f'{l}{i}'] = f
		noteID = noteID + 1		
		#print(f'{l}{i}', f)
		
notes['pause'] = 1
		
song=[
	("c2",0.5),
	("d2",0.5),
	("e2",0.5),
	("f2",0.5),
	("g2",0.5),
	("a2",0.5),
	("b2",0.5),
	("c3",0.5),
	("b2",0.5),
	("a2",0.5),
	("g2",0.5),
	("f2",0.5),
	("e2",0.5),
	("d2",0.5),
	("c2",0.5),
]


song=[
	("f2",0.25),
	("a2",0.25),
	("b2",0.50),

	("f2",0.25),
	("a2",0.25),
	("b2",0.50),

	("f2",0.25),
	("a2",0.25),
	("b2",0.25),
	("e3",0.25),

	("d3",0.5),
	("b2",0.25),
	("c3",0.25),

	("b2",0.25),
	("g2",0.25),
	("e2",1),
#	("pause",0.25),
	("d2",0.25),

	("e2",0.25),
	("g2",0.25),
	("e2",1.25),
	
]

for note, dur in song:
	buzzer.ChangeFrequency(notes[note])
	if note != 'pause':
		print(f'playing {note}')
		buzzer.start(50)
		time.sleep(dur)
		buzzer.stop()
	else:
		print(f'playing {note}')
		time.sleep(dur)
	

#for i in range(4):#
#	buzzer.ChangeFrequency(notes()
#	buzzer.start(50)
#	print("BEEP!!")
#	time.sleep(0.5)
#	buzzer.stop()
#	print("Be Quite!!")
#	time.sleep(0.25)
