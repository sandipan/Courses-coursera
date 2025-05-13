import os
from PIL import Image, ImageDraw, ImageFont
for dirname, dirnames, filenames in os.walk('.'):
	
	for filename in filenames:
		
		filename = dirname + '/' + filename
		print (filename)

		main = Image.open(filename).convert('RGB')
		watermark = Image.new("RGBA", main.size)
		waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")
		#fnt = ImageFont.truetype("./Verdana.ttf",20)
		waterdraw.text((10, 10), "Sandipan Dey (UMBC)", fill=(255,0,0,200))  #, font=fnt
		watermask = watermark.convert("L").point(lambda x: max(x, 50))
		watermark.putalpha(watermask)
		main.paste(watermark, None, watermark)
		main.save(filename, "PNG")
