from PIL import Image, ImageDraw

# US Letter at 72dpi: 612 pixels x 792 pixels
# US Letter at 300dpi: 2550 pixels x 3300 pixels

WIDTH, HEIGHT = (612, 792)

img = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))
img.save('Image.png')