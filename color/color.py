from PIL import Image, ImageDraw
import math
import colorsys

def step (r,g,b, repetitions=1):
    # Credit goes to Alan Zucconi
    # https://www.alanzucconi.com/2015/09/30/colour-sorting/
    lum = math.sqrt( .241 * r + .691 * g + .068 * b )
 
    h, s, v = colorsys.rgb_to_hsv(r,g,b)
 
    h2 = int(h * repetitions)
    lum2 = int(lum * repetitions)
    v2 = int(v * repetitions)
 
    if h2 % 2 == 1:
        v2 = repetitions - v2
        lum = repetitions - lum
 
    return (h2, lum, v2)

def get_colors(infile, outline_width, palette_length_div, outline_color, numcolors=10):
    original_image = Image.open(infile)
    image = Image.open(infile)
    image = image.resize((80, 80))
    result = image.convert('P', palette=Image.ADAPTIVE, colors=numcolors)   # image with only 10 dominating colors
    result.putalpha(0)
    colors = result.getcolors(80*80)      # array of colors in the image

    width = original_image.size[0]
    height = original_image.size[1]
    palette_height = int(height/palette_length_div)
    background = Image.new("RGB", (width, height+palette_height))   # blank canvas(original image + palette)
    pal = Image.new("RGB", (width, palette_height))
    draw = ImageDraw.Draw(pal)
    posx = 0
    swatchsize = width/10
    
    colors.sort(key=lambda x: step(x[1][0], x[1][0], x[1][0],8)	)
       
    # making the palette
    for count, col in colors:
        draw.rectangle([posx, 0, posx+swatchsize, palette_height], fill=col, width=outline_width, outline=outline_color)
        posx = posx + swatchsize

    del draw
    box = (0, height, width, height+palette_height)

    # pasting image and palette on the canvas
    background.paste(original_image)
    background.paste(pal, box)

    return background
