import pafy
import cv2

# I am trying to get a livestream from youtube but I am getting an error from CV2 about the type of the url (m3u8)
# based on everything I can see online I'm not doing anything wrong and after some research I'm unsure where the problem lies
# has there been a change to youtube?
# has

# search youtube for term
# get urls into list
# choose one url
# 


url = "https://youtu.be/50htNHgohpQ"
pafy.set_api_key("AIzaSyBDQ96Z6bFmhOZH5710G2sWaIdMX9CypfA")
video = pafy.new(url)
# print(video)
streams = video.streams
for i in streams:
    print(i)
      
# get best resolution regardless of format
best = video.getbest()
  
print(best.resolution, best.extension)
  

# best = video.getbest(preftype="mp4")
# # print(best.url)

capture = cv2.VideoCapture(best.url)

# # capture = cv2.VideoCapture("https://youtu.be/ydYDqZQpim8")

# while capture.isOpened():
while capture.isOpened():
    grabbed, frame = capture.read()
    print(frame)
    if frame is not None:
        # cv2.imshow('frame',frame)
        cv2.imwrite('from_livestream.png', frame)
        print("saved frame")
    else:
        print("frame is none")
# # cv2.imshow('image', grabbed)
# # cv2.waitKey(0)
# # ...