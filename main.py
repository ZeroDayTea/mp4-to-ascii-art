import os 
import cv2
import time
from pydub import AudioSegment
from pydub.playback import play
from threading import Thread
import math
from PIL import Image

# Ascii characters used to create the output 
#ASCII_CHARS = [" ", ",", ":", ";", "+", "*", "?", "%", "O", "#", "@"]
#ASCII_CHARS = [" ", ".", "°", ";", "+", "*", "?", "%", "S", "O", "#", "@"]
#ASCII_CHARS = [' ', '.', '°', '*', 'o', 'O', '#', '@']
ASCII_CHARS = [" ", ".", ",", "-", "~", ":", ";", "=", "!", "E", "#", "$", "@"]
#ASCII_CHARS = [" ", ".", ",", "-", "~", ":", ";", "=", "!", "*", "%", "O", "#", "@"]
#ASCII_CHARS = [" ", ".", ",", "~", ":", "!", "*", "%", "O", "S", "#", "@"]
MAX_WIDTH = os.get_terminal_size().columns
FRAMERATE = 60
VIDEO_FILE = "bakemonogatari.mp4"
AUDIO_FILE = "bakemonogatari.mp3"
pixeltocharfactor = math.floor(250//(len(ASCII_CHARS) - 1))

def resized_gray_image(image, new_width=MAX_WIDTH):
    width,height = image.size
    aspect_ratio = float(width * 2.5)/height #2.5 modifier on width to offset vertical scaling of ascii chars
    new_height = math.floor(new_width / aspect_ratio)
    resized_gray_image = image.resize((new_width,new_height)).convert('L')
    return resized_gray_image

def pix2chars(image):
    pixels = image.getdata()
    characters = ""
    for pixel in pixels:
        char = ASCII_CHARS[int(pixel/pixeltocharfactor)]
        characters += char
    return characters

def generate_frame(image,new_width=MAX_WIDTH):
    new_image_data = pix2chars(resized_gray_image(image))

    total_pixels = len(new_image_data)

    ascii_image = "\n".join([new_image_data[index:(index+new_width)] for index in range(0, total_pixels, new_width)])
    ascii_image = ascii_image.strip()

    print(ascii_image)
    #os.system('cls' if os.name == 'nt' else 'clear')

def play_sound():
    sound = AudioSegment.from_mp3(AUDIO_FILE)
    play(sound)
        
def main():
    thread = Thread(target=play_sound)
    thread.start()
    time.sleep(2)
    cap = cv2.VideoCapture(VIDEO_FILE)
    
    FRAMERATE = cap.get(cv2.CAP_PROP_FPS)
    sleep_time = 1/FRAMERATE

    while True:
        start = time.time()
        ret,frame = cap.read()
        generate_frame(Image.fromarray(frame), MAX_WIDTH)
        start += sleep_time
        sleepTime = start - time.time()
        if(sleepTime >= 0):
            time.sleep(sleepTime)
        else:
            time.sleep(sleep_time)
        
if __name__=="__main__":
    main()
    