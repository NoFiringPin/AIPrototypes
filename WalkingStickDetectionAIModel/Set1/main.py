import subprocess
from ai_engine import AiEngine

ai_engine = AiEngine()

#with open("take_picture.py") as f:
	#exec(f.read())
	
subprocess.run(["python", "take_picture.py"])


#img = ai_engine.process_image('helmet.jpg', save_image=True)
img = ai_engine.process_image('picture.jpg', save_image=True)
#output_path = ai_engine.process_video(video_path='helmet.mp4', save_video=True)

