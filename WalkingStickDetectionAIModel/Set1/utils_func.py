import os
import glob

def remove_images():
  files = glob.glob('images/*.jpg')
  for i in files:
    os.remove(i)

def make_dir(dir_name):
  if not os.path.exists(dir_name):
    os.mkdir(dir_name)
