#pip install list:
# pytube
# opencv-python
# pillow
"""
Outputs an image with the average colors from a video
Created : November 17, 2022

V 1.0
- initial file

V 1.1 
- Update to batch process whatever is in the 'input' folder

"""


from pytube import YouTube
import cv2
import os 
import shutil
from PIL import Image, ImageStat, ImageDraw

"""
Global Configurations

INPUT_FOLDER (str) : relative filepath of input folder (put in videos)
OUTPUT_FOLDER (str) : relative filepath of the output folder (outputs pngs and frames)
PREVIEW_OUTPUT (bool) : whether or not to preview the png outputs
"""
INPUT_FOLDER = "input" 
OUTPUT_FOLDER = "output"
PREVIEW_OUTPUT = False 


#Get average colour of frames
def get_average_colour(image_name, colour_list, frame_folder):
  image = Image.open(frame_folder+"/"+image_name)
  average = ImageStat.Stat(image).mean
  colour_list.append(average)
  
def get_colour_list(download_folder, download_name, frame_folder):
  #Get frames from video (once every second)
  vidcap = cv2.VideoCapture(download_folder+"/"+download_name+".mp4")
  fps = vidcap.get(cv2.CAP_PROP_FPS)
  success,image = vidcap.read()
  count = 0
  colour_list = []
  while success:
    if count % round(fps) == 0:
      frame_name = "frame%d.jpg" % count
      cv2.imwrite(frame_folder+"/"+frame_name, image)     # save frame as JPEG file
      get_average_colour(frame_name, colour_list, frame_folder)
    success,image = vidcap.read()
    count += 1
  return colour_list

def image_scale(index, scale):
  return int(index * scale)

def average_colours(download_name):
  download_folder = INPUT_FOLDER
  # download_name = "test"
  frame_folder = os.path.join(OUTPUT_FOLDER,download_name, "frames")

  # try:
  #   shutil.rmtree(download_folder)
  # except FileNotFoundError:
  #   print(download_folder + " folder does not exist. Creating one!")

  #Make sure folders exist
  os.makedirs(download_folder, exist_ok=True)
  os.makedirs(frame_folder, exist_ok=True)

  #Download video
  # print("downloading video...")
  # video = YouTube(video_url)
  # stream = video.streams.filter(mime_type="video/mp4",res="360p").all()[0]
  # stream.download(download_folder, download_name)


  print(f"Averaging colours for {download_name}")
  colour_list = get_colour_list(download_folder, download_name, frame_folder)

  print(f"Writing image for {download_name}")
  output_image = Image.new('RGB', (len(colour_list), len(colour_list)), color = 'white')
  d = ImageDraw.Draw(output_image)

  for index, value in enumerate(colour_list):
    d.line((index,len(colour_list), index, 0), fill=(int(value[0]),int(value[1]),int(value[2])))
  
  output_image = output_image.resize((1920,1080),resample=Image.BILINEAR)
  output_image.format = "PNG"
  output_image.save(
    os.path.join(OUTPUT_FOLDER, f"{download_name}.png"), format="PNG" # save to output
  )
  if PREVIEW_OUTPUT: 
    output_image.show()


if __name__ == "__main__": 
  # average_colours(str(input("Enter a YouTube video URL:")))
  print("Reminder : Please put the name of the folder into the `INPUT_FOLDER` config")
  # average_colours(str(input("Enter a file name:")))

  # set current working directory to file directory
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  
  # Folder for images
  input_files = os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)) , INPUT_FOLDER))
  
  # iterate over all files
  for video_file in input_files:
    video_name = video_file.rsplit(".",1)[0] # Split file to get before .mp4
    average_colours(video_name)

  print("Complete")

