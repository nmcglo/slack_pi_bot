from subprocess import call
from PIL import Image


call(["screencapture", "test.jpg"])

im = Image.open("test.jpg")
print(im.format, im.size, im.mode)

test_image = "test.jpg"
original = Image.open(test_image)
# original.show()

width, height = original.size   # Get dimensions
left = 12 * width/14
top = 0
right = width
bottom = height/20
cropped_example = original.crop((left, top, right, bottom))

cropped_example.save("test.jpg", "JPEG")

# cropped_example.show()
