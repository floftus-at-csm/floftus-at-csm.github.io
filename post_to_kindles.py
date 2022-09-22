from time import sleep
from PIL import Image, ImageDraw
import git
from fefe_image_processing import PIL_processes, general, scikit
import random
import time

source_image_folder = "individuals/"

images = general.load_images_in_folder(source_image_folder)

final_image = Image.new('L', (600, 800))
final_image2 = Image.new('L', (600, 800))
final_image3 = Image.new('L', (600, 800))
final_image4 = Image.new('L', (600, 800))

im_to_post1 = PIL_processes.resize_image(images[random.randint(0, len(images)-1)], 600, 800)
im_to_post1 = PIL_processes.grayscale(im_to_post1)
final_image.paste(im_to_post1, (0,0))

left = random.randint(0,400)
top = random.randint(0,400)
im_to_post2 = images[random.randint(0, len(images)-1)].crop((left, top, left+800, top+600))
im_to_post2 = PIL_processes.grayscale(im_to_post2)
final_image2.paste(im_to_post2, (0,0))

im_to_post3 = PIL_processes.resize_image(images[random.randint(0, len(images)-1)], 600, 800)
im_to_post3 = PIL_processes.grayscale(im_to_post3)
final_image3.paste(im_to_post3, (0,0))

left = random.randint(0,400)
top = random.randint(0,400)
im_to_post4 = images[random.randint(0, len(images)-1)].crop((left, top, left+800, top+600))
im_to_post4 = PIL_processes.grayscale(im_to_post4)
final_image4.paste(im_to_post4, (0,0))

final_image.save("public/image1.png")
final_image2.save("public/image2.png")

final_image.save("public/image3.png")
final_image4.save("public/image4.png")

repo = git.Repo('.git')
# repo.index.commit("Is this on?")
repo.git.commit('-am', 'test commit')
repo.git.push()