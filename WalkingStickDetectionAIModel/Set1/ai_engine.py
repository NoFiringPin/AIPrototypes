from pathlib import Path

import cv2
import torch
import board
import neopixel
import time


from utils_func import remove_images, make_dir

model = torch.hub.load('ultralytics/yolov5', 'custom', path='helmet.pt')
pixels = neopixel.NeoPixel(board.D18, 1)
helmet_detected = False

def blink_red():
        delay = 1
        blink_num = 5
        while blink_num > 0:
                pixels[0] = (255,0,0)
                time.sleep(delay)
                pixels[0] = (0,0,0)
                time.sleep(delay)
                blink_num -= 1
        
def blink_green():
        delay = 1
        blink_num = 5
        while blink_num > 0:
                pixels[0] = (0,255,0)
                time.sleep(delay)
                pixels[0] = (0,0,0)
                time.sleep(delay)
                blink_num -= 1

        



class AiEngine:
    def __int__(self):
        pass

    def __fetch_helmets(self, img_path):
        imgs = [img_path]  # batch of images

        # Inference
        results = model(imgs)
        df = results.pandas().xyxy[0]
        # print(df)
        helmets = []
        for index, row in df.iterrows():
            p1 = (int(row['xmin']), int(row['ymin']))
            p2 = (int(row['xmax']), int(row['ymax']))
            helmets.append((p1, p2, round(row['confidence'] * 100, 2)))

        return helmets

    def __draw_helmets(self, helmets, image, color=(255, 0, 0), thickness=2,
                       fontScale=1, font=cv2.FONT_HERSHEY_SIMPLEX):                            

        for start_point, end_point, confidence in helmets:
            print('Processing image for helmet...')    
            # Using cv2.rectangle() method
            # Draw a rectangle with blue line borders of thickness of 2 px
            image = cv2.rectangle(image, start_point, end_point, color, thickness)
            #blink_green()
            # org
            org = (start_point[0], start_point[1] - 10)
            # Using cv2.putText() method
            image = cv2.putText(image, f'Helmet {confidence}%', org, font,
                                fontScale, color, thickness, cv2.LINE_AA)
        if len(helmets) > 0 and confidence >= 60:
                helmet_detected = True
                print('Helmet detected!')
                time.sleep(1)
                print(f'Confidence is {confidence} %')
                blink_green()
        elif len(helmets) > 0 and confidence < 60:
                print('Helmet detected, but confidence is low...')
                print(f'Confidence is {confidence} %')
        else:
                print('No helmet detected...')
                blink_red()
                
        return image

    def process_image(self, img_path, save_image=False):
        helmets = self.__fetch_helmets(img_path)
        # print(helmets)
        # Reading an image in default mode
        image = cv2.imread(img_path)
        self.__draw_helmets(helmets, image)
        if save_image:
            cv2.imwrite('out_' + img_path, image)
        return image

    def write_video(self, cap, output_path, video_path):
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float `width`
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float `height`
        fps = 15  # Use less numb of frames to make the video slower
        output_path = Path(video_path).stem + '_output.mp4'
        output_dim = (int(width), int(height))
        out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), int(fps), output_dim)
        return out, output_path

    def process_video(self, video_path=0, save_video=False):
        i = 0
        output_path = None
        # Create a VideoCapture object and read from input file
        # If the input is the camera, pass 0 instead of the video file name
        cap = cv2.VideoCapture(video_path)

        # Check if camera opened successfully
        if (cap.isOpened() == False):
            print("Error opening video stream or file")

        if save_video:
            out, output_path = self.write_video(cap, output_path, video_path)

        make_dir('images')
        # Read until video is completed
        while (cap.isOpened()):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if ret:
                # Filename
                img_path = f'images/img{i}.jpg'

                # Using cv2.imwrite() method
                # Saving the image
                cv2.imwrite(img_path, frame)

                image = self.process_image(img_path)

                # Displaying the image
                # cv2.imshow(f'image{i}', image)

                if save_video:
                    out.write(image)
                # Press Q on keyboard to  exit
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
                i += 1
            # Break the loop
            else:
                break

        # When everything done, release the video capture object
        cap.release()
        if save_video:
            out.release()

        # Closes all the frames
        cv2.destroyAllWindows()
        remove_images()

        return output_path


