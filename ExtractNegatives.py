import numpy as np
import cv2
import google.cloud as gc
import random
import glob
import os

class Video:
    def __init__(self,path):
        self.cap = cv2.VideoCapture(path)
        self.length = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))        
        if self.length == 0:
            print("setting length manually")
            self.length = 10000
        
    def random_image(self):
        global counter
        #holder of output frames
        frame_to_write=list()
        
        #which random frames to grab
        frame_number=list()
        
        #draw random numbers
        for x in range(10):
            frame_number.append(random.randint(1, self.length))
        
        #sort frame numbers
        frame_number.sort()
        print("Grabbing frames %s" %frame_number)
        
        #some videos don't honor this due to codecs, do it manually, a bit ugly.        
        self.cap.set(1,frame_number[0])        
        if int(self.cap.get(1)) ==0:
            print("Codec not read, iterating manually")
            fcount=0
            while fcount not in frame_number:
                self.cap.grab()
                fcount = fcount +1 
                if fcount in frame_number:            
                    ret,frame=self.cap.read()
                    frame_to_write.append(frame)
                    fcount = fcount +1
                    #break the video when past the last number
                    if fcount > max(frame_number):
                        break
        else:
            for f in frame_number:
                self.cap.set(1,f) #the proper way for videos that can read the codec.
                ret,frame=self.cap.read()                
                frame_to_write.append(frame)
        
        #write the frames    
        print(len(frame_to_write))
        
        for fr in frame_to_write:
            filename="C:/Users/Ben/Dropbox/GoogleCloud/Negatives/" + str(counter) +".jpg"
            cv2.imwrite(filename, fr)    
            counter=counter+1

if __name__ == "__main__":
    vids=glob.glob("F:/**/*.tlv", recursive=True)
    print(vids)
    counter=0
    for vid in vids:        
        vid_instance=Video(vid)
        vid_instance.random_image()