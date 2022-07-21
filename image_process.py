# aim is to create a large image that is split up into smaller images which are displayed on the kindle
# files: kindle1.png, kindle2.png etc., a large_image.png
# all black and white, no alpha channels
# I will then need to push the change to github to ensure the change registers
# 
# Aesthetics: smaller shapes blown up, a dense background image with smaller light 'clear'/transparent layers on top

from PIL import Image, ImageDraw
import git

current_image = Image.new('L', (600, 800))

draw = ImageDraw.Draw(current_image)
draw.line((0, 0) + current_image.size, fill=248)
# draw.line((600/3, 800/2) + current_image.size, fill=248)
draw.line((0, current_image.size[1], current_image.size[0], 0), fill=248)

current_image.save("public/image1.png")

repo = git.Repo('.git')
# repo.index.commit("Is this on?")
repo.git.commit('-am', 'test commit')
repo.git.push()