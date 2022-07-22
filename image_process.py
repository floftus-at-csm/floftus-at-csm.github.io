# aim is to create a large image that is split up into smaller images which are displayed on the kindle
# files: kindle1.png, kindle2.png etc., a large_image.png
# all black and white, no alpha channels
# I will then need to push the change to github to ensure the change registers
# 
# Aesthetics: smaller shapes blown up, a dense background image with smaller light 'clear'/transparent layers on top

from time import sleep
from PIL import Image, ImageDraw
import git
from fefe_image_processing import PIL_processes, general
import random
import time

source_image_folder = "source_images/"
images = general.load_images_in_folder(source_image_folder)
print(random.choice(images))

# take a random 3 images
# combine two - then edge that image
# create 'watermark' with third - layer onto combined image

for i in range(15):
    img1 = random.choice(images)
    img2 = random.choice(images)
    img3 = random.choice(images)
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

    img2 = PIL_processes.PIL_enhance_edges(img2)
    # img2 = PIL_processes.PIL_invert(contoured)

    
    composited1 = Image.composite(img1, img2, mask)
    composited1.show()
    composited1 = PIL_processes.PIL_contrast(composited1, 1.25)
    # composited1.show()

    # countoured = PIL_processes.PIL_contour(img3, 50)
    # img3 = PIL_processes.PIL_invert(contoured)
    # composited1 = Image.composite(composited1, img3, mask)
    # to here

    width, height = composited1.size
    composited1 = PIL_processes.resize_image(composited1, int(width/3), int(height/3))
    width, height = composited1.size

    left = random.randint(0, width-1200)
    top = random.randint(0, height-800)

    cropped_img = composited1.crop((left, top, left+600, top+800))
    cropped_img2 = composited1.crop((left+600, top, left+1200, top+800))


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

    final_image.paste(cropped_img, (0,0))
    final_image2.paste(cropped_img2, (0,0))
    # final_image.paste(cropped_img, (0,0), cropped_img)
    # final_image.show()
    # final_image2.show()

    final_image.save("public/image1.png")
    final_image2.save("public/image2.png")

    repo = git.Repo('.git')
    # repo.index.commit("Is this on?")
    repo.git.commit('-am', 'test commit')
    repo.git.push()

    time.sleep(105)