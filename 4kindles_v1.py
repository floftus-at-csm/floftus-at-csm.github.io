# aim is to create a large image that is split up into smaller images which are displayed on the kindle
# files: kindle1.png, kindle2.png etc., a large_image.png
# all black and white, no alpha channels
# I will then need to push the change to github to ensure the change registers
# 
# Aesthetics: smaller shapes blown up, a dense background image with smaller light 'clear'/transparent layers on top

from time import sleep
from PIL import Image, ImageDraw
import git
from fefe_image_processing import PIL_processes, general, scikit
import random
import time

source_image_folder = "source_images/"
images = general.load_images_in_folder(source_image_folder)
print(random.choice(images))

# take a random 3 images
# combine two - then edge that image
# create 'watermark' with third - layer onto combined image

for i in range(2):
    img1 = random.choice(images)
    img2 = random.choice(images)
    img3 = random.choice(images)
    img4 = random.choice(images)
    mask = random.choice(images)
    # print(images[0])
    # img1 = images[0]
    # img2 = images[1]
    # img3 = images[2]
    # mask = images[6]

    img1 = PIL_processes.grayscale(img1)
    img2 = PIL_processes.grayscale(img2)
    img3 = PIL_processes.grayscale(img3)
    mask = PIL_processes.grayscale(mask)
    img4 = PIL_processes.grayscale(img4)

    img2 = PIL_processes.PIL_enhance_edges(img2)
    # img2 = PIL_processes.PIL_invert(contoured)

    
    composited1 = Image.composite(img1, img2, mask)
    # composited1.show()
    # composited1 = PIL_processes.PIL_contrast(composited1, 1.25)
    # composited1.show()

    solarised= PIL_processes.solarize(img3, 130)
    # img4 = PIL_processes.PIL_invert(img4)
    composited1 = Image.composite(composited1, solarised, img3)
    composited1 = PIL_processes.PIL_contrast(composited1, 1.65) 
    composited1 = PIL_processes.PIL_brightness(composited1, 1.25)
    composited1.show()
    


    width, height = composited1.size
    composited1 = PIL_processes.resize_image(composited1, int(width/2), int(height/2))
    width, height = composited1.size
    print("the width is: ", width)
    print("the height is: ", height)
    
    left = random.randint(0, 400)
    top = random.randint(0, 300)

    # I should add a bit of spacing to account for the gap!
    cropped_img = composited1.crop((left, top, left+800, top+600))
    cropped_img2 = composited1.crop((left+800, top, left+1600, top+600))

    cropped_img3 = composited1.crop((left, top+600, left+800, top+1200))
    cropped_img4 = composited1.crop((left+800, top+600, left+1600, top+1200))

    rotated1 = PIL_processes.PIL_rotate(cropped_img, 90)
    rotated2 = PIL_processes.PIL_rotate(cropped_img2, -90)
    rotated3 = PIL_processes.PIL_rotate(cropped_img3, 90)
    rotated4 = PIL_processes.PIL_rotate(cropped_img4, -90)

    # edges = PIL_processes.PIL_edges(composited1)
    # edges.show()

    # contoured = PIL_processes.PIL_contour(img3, 50)
    # contoured = PIL_processes.PIL_invert(contoured)
    # width, height = contoured.size
    # contoured = PIL_processes.resize_image(contoured, int(width/2), int(height/2))
    # composited1.paste(contoured, (200, 160), contoured)
    # composited1.show()

    final_image = Image.new('L', (600, 800))
    final_image2 = Image.new('L', (600, 800))

    final_image3 = Image.new('L', (600, 800))
    final_image4 = Image.new('L', (600, 800))
    

    final_image.paste(rotated1, (0,0))
    final_image2.paste(rotated2, (0,0))
    final_image3.paste(rotated3, (0,0))
    final_image4.paste(rotated4, (0,0))
    # final_image.paste(cropped_img, (0,0), cropped_img)
    # final_image.show()
    # final_image2.show()

    final_image.save("public/image1.png")
    final_image2.save("public/image2.png")

    final_image3.save("public/image3.png")
    final_image4.save("public/image4.png")


    repo = git.Repo('.git')
    # repo.index.commit("Is this on?")
    repo.git.commit('-am', 'test commit')
    repo.git.push()

    time.sleep(105)