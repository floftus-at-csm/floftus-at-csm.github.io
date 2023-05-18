from time import sleep
from PIL import Image, ImageDraw
import git
from fefe_image_processing import PIL_processes, general, scikit
import random
import time

source_image_folder = "individuals/"

images = general.load_images_in_folder(source_image_folder)

current_image = images[random.randint(0, len(images)-1)]

left = 0
top = 0

# I should add a bit of spacing to account for the gap!
cropped_img = current_image.crop((left, top, left+600, top+800))
cropped_img2 = current_image.crop((left+600, top, left+1200, top+800))

cropped_img3 = current_image.crop((left, top+800, left+600, top+1600))
cropped_img4 = current_image.crop((left+600, top+800, left+1200, top+1600))

final_image = Image.new('L', (600, 800))
final_image2 = Image.new('L', (600, 800))
final_image3 = Image.new('L', (600, 800))
final_image4 = Image.new('L', (600, 800))

final_image.paste(cropped_img, (0,0))
final_image2.paste(cropped_img2, (0,0))
final_image3.paste(cropped_img3, (0,0))
final_image4.paste(cropped_img4, (0,0))

final_image.save("public/image1.png")
final_image2.save("public/image2.png")

final_image3.save("public/image3.png")
final_image4.save("public/image4.png")

repo = git.Repo('.git')
# repo.index.commit("Is this on?")
repo.git.commit('-am', 'test commit')
repo.git.push()