#Nicholas Mohammad
#12/7/2018
#Raytracer

from PIL import Image
import sys
import numpy as np
from random import uniform

in_file,out_file,filename = 0,0,0
pixels,red,green,blue,light = [],[],[],[],[]

def hue(r,g,b):
	V = max(r,g,b)
	d = round(V - min(r,g,b),5)
	if d == 0:
		H = 0
	elif V == r:
		H = (g-b)/(6*d) if round((g-b)/(6*d),5) >= 0 else (g-b)/(6*d) + 1
	elif V == g:
		H = (b-r)/(6*d) + (1/3)
	elif V == b:
		H = (r-g)/(6*d) + (2/3)
	return H

def saturation(r,g,b):
	V = max(r,g,b)
	d = V - min(r,g,b)
	if V != 0:
		return d/V
	return 0

def lightness(r,g,b):
	return .299*r + .587*g + .114*b

def rgb(h,s,v):
	r = v*((1-s)+s*clamp((6*h+3)%6))
	g = v*((1-s)+s*clamp((6*h+1)%6))
	b = v*((1-s)+s*clamp((6*h+5)%6))
	return (r,g,b)

def clamp(x):
	return min(max(2 - abs(3-x),0),1)

def command(line):
	global pixels
	draw = False
	words=[]
	line=(line.strip()).split(" ")
	if len(line) >= 1:
		for word in line:
			if(word!= "" and word!= " "):
				words.append(word)
	if len(words) == 0:
		words.append("")
	if words[0] == "monochrome":
		if words[1] == "hue":
			H=0
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					H = hue(pixels[x,y][0],pixels[x,y][1],pixels[x,y][2])
					pixels[x,y][0],pixels[x,y][1],pixels[x,y][2] = H,H,H
		if words[1] == "saturation":
			S = 0
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					S = saturation(pixels[x,y][0],pixels[x,y][1],pixels[x,y][2])
					pixels[x,y][0],pixels[x,y][1],pixels[x,y][2] = S,S,S
		if words[1] == "lightness":
			L = 0
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					L = lightness(pixels[x,y][0],pixels[x,y][1],pixels[x,y][2])
					pixels[x,y][0],pixels[x,y][1],pixels[x,y][2] = L,L,L
		if words[1] == "red":
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					pixels[x,y][1],pixels[x,y][2] = pixels[x,y][0],pixels[x,y][0]
		if words[1] == "green":
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					pixels[x,y][0],pixels[x,y][2] = pixels[x,y][1],pixels[x,y][1]
		if words[1] == "blue":
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					pixels[x,y][0],pixels[x,y][1] = pixels[x,y][2],pixels[x,y][2]
		if words[1] == "alpha":
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					pixels[x,y][0],pixels[x,y][1],pixels[x,y][2] = pixels[x,y][3],pixels[x,y][3],pixels[x,y][3]

		out_file.save(filename)
	if words[0] == "equalize":
		if words[1] == "red":
			maximum = -1
			minimum = 256
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					maximum = max(maximum, pixels[x,y][0])
					minimum = min(minimum, pixels[x,y][0])

			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					pixels[x,y][0]= (pixels[x,y][0]-minimum)/(maximum - minimum)
			#pixels[:pixels.shape[0],:pixels.shape[1]][0] = (pixels[:pixels.shape[0],:pixels.shape[1]][0] - minimum )/(maximum - minimum)
		
		if words[1] == "green":
			maximum = -1
			minimum = 256
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					maximum = max(maximum, pixels[x,y][1])
					minimum = min(minimum, pixels[x,y][1])
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					pixels[x,y][1]= (pixels[x,y][1]-minimum)/(maximum - minimum)
			#pixels[:pixels.shape[0],:pixels.shape[1]][1] = (pixels[:pixels.shape[0],:pixels.shape[1]][1] - minimum )/(maximum - minimum)


		if words[1] == "blue":
			maximum = -1
			minimum = 256
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					maximum = max(maximum, pixels[x,y][2])
					minimum = min(minimum, pixels[x,y][2])

			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					pixels[x,y][2]= (pixels[x,y][2]-minimum)/(maximum - minimum)
			#pixels[:pixels.shape[0],:pixels.shape[1]][2] = (pixels[:pixels.shape[0],:pixels.shape[1]][2] - minimum )/(maximum - minimum)
	if words[0] == "posterize":
		if words[1] == "red":
			n = float(words[2])
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					i = round(pixels[x,y][0]*(n-1),5)
					i = int(i+.5)
					pixels[x,y][0] = i/(n-1)
		if words[1] == "green":
			n = float(words[2])
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					i = round(pixels[x,y][1]*(n-1),5)
					i = int(i+.5)
					pixels[x,y][1] = i/(n-1)
		if words[2] == "blue":
			n = float(words[2])
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					i = round(pixels[x,y][2]*(n-1),5)
					i = int(i+.5)
					pixels[x,y][2] = i/(n-1)
		draw = True
	if words[0] == "rehue":
		dH = float(words[1])
		for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					H = hue(pixels[x,y][0],pixels[x,y][1],pixels[x,y][2])
					V = max(pixels[x,y][0],pixels[x,y][1],pixels[x,y][2])
					S = saturation(pixels[x,y][0],pixels[x,y][1],pixels[x,y][2])

					if H + dH < 0 or H+dH > 1:
						H = (H+dH)%1
					else:
						H += dH

					vals = rgb(H,S,V)
					pixels[x,y][0],pixels[x,y][1],pixels[x,y][2]=min(max(vals[0],0),1),min(max(vals[1],0),1),min(max(vals[2],0),1)

		draw = True
	if words[0] == "dither":
		if words[1] == "red":
			n = float(words[2])
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					i = pixels[x,y][0]*(n-1)
					dist = abs(i-int(i+1))
					r = uniform(0,1)
					if r <= dist:
						i = int(i)
					else:
						i = int(i+1)
					pixels[x,y][0] = i/(n-1)
		if words[1] == "green":
			n = float(words[2])
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					i = pixels[x,y][1]*(n-1)
					dist = abs(i-int(i+1))
					r = uniform(0,1)
					if r <= dist:
						i = int(i)
					else:
						i = int(i+1)
					pixels[x,y][1] = i/(n-1)
		if words[2] == "blue":
			n = float(words[2])
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					i = pixels[x,y][2]*(n-1)
					dist = abs(i-int(i+1))
					r = uniform(0,1)
					if r <= dist:
						i = int(i)
					else:
						i = int(i+1)
					pixels[x,y][2] = i/(n-1)
		draw = True
	if words[0] == "gradient":
		scharr_y = np.array([[-3,-10,-3],[0,0,0],[3,10,3]])
		scharr_x = np.array([[-3,0,3],[-10,0,10],[-3,0,3]])

		light = np.empty((pixels.shape[0],pixels.shape[1]))
	
		for x in range(0,pixels.shape[0]):
			for y in range(0,pixels.shape[1]):
				light[x,y] = lightness(pixels[x,y,0],pixels[x,y,1],pixels[x,y,2])
		pad_width = ((1,1),(1,1))
		light = np.pad(light,pad_width,'edge')

		for x in range(0,pixels.shape[0]):
			for y in range(0,pixels.shape[1]):
				conv = np.sum((light[x:x+3,y:y+3]*scharr_y))/16
				pixels[x,y,1]= conv

		for x in range(0,pixels.shape[0]):
			for y in range(0,pixels.shape[1]):
				conv = np.sum((light[x:x+3,y:y+3]*scharr_x))/16
				pixels[x,y,0],pixels[x,y,2]= conv,conv
		draw = True
	if words[0] == "sharpen":
		a = float(words[2])
		sharp = np.array([[-.1*a,-.15*a,-.1*a],[-.15*a,1+a,-.15*a],[-.1*a,-.15*a,-.1*a]])
		color_channel = np.empty((pixels.shape[0],pixels.shape[1]))

		if words[1] == "red":
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					color_channel[x,y] = pixels[x,y,0]
			pad_width = ((1,1),(1,1))
			color_channel = np.pad(color_channel,pad_width,'edge')
			
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					pixels[x,y,0] = np.sum((color_channel[x:x+3,y:y+3]*sharp))
		if words[1] == "green":
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					color_channel[x,y] = pixels[x,y,1]
			pad_width = ((1,1),(1,1))
			color_channel = np.pad(color_channel,pad_width,'edge')
			
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					pixels[x,y,1] = np.sum((color_channel[x:x+3,y:y+3]*sharp))
		if words[1] == "blue":
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					color_channel[x,y] = pixels[x,y,2]
			pad_width = ((1,1),(1,1))
			color_channel = np.pad(color_channel,pad_width,'edge')
			
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					pixels[x,y,2] = np.sum((color_channel[x:x+3,y:y+3]*sharp))
		draw = True
	if words[0] == "convolve":
		conv = np.empty((int(words[3]),int(words[2])))
		pad = ((int(words[3])//2,int(words[3])//2),(int(words[2])//2,int(words[2])//2))
		j = 0
		for x in range(0,conv.shape[0]):
			for y in range(0,conv.shape[1]):
				conv[x,y] = words[4+j]
				j+=1
		color_channel = np.empty((pixels.shape[0],pixels.shape[1]))

		if words[1] == "red":
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					color_channel[x,y] = pixels[x,y,0]
			pad_width = pad
			color_channel = np.pad(color_channel,pad_width,'edge')

			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					pixels[x,y,0] = np.sum((color_channel[x:x+conv.shape[0],y:y+conv.shape[1]]*conv))

		if words[1] == "green":
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					color_channel[x,y] = pixels[x,y,1]
			pad_width = pad
			color_channel = np.pad(color_channel,pad_width,'edge')

			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					pixels[x,y,1] = np.sum((color_channel[x:x+conv.shape[0],y:y+conv.shape[1]]*conv))

		if words[1] == "blue":
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					color_channel[x,y] = pixels[x,y,2]
			pad_width = pad
			color_channel = np.pad(color_channel,pad_width,'edge')

			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					pixels[x,y,2] = np.sum((color_channel[x:x+conv.shape[0],y:y+conv.shape[1]]*conv))
		if words[1] == "alpha":
			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					color_channel[x,y] = pixels[x,y,3]
			pad_width = pad
			color_channel = np.pad(color_channel,pad_width,'edge')

			for x in range(0,pixels.shape[0]):
				for y in range(0,pixels.shape[1]):
					pixels[x,y,3] = np.sum((color_channel[x:x+conv.shape[0],y:y+conv.shape[1]]*conv))

for args in sys.argv[1:]:
	file = open(str(args),"r")
	lines = file.readlines()
	file.close()
	words = lines[0].split()
	if words[0] != "input":
		print("Cannot perform operation for ",args,", please put input command at first line.")
		continue
	filename = words[1].strip()
	in_file = Image.open(filename)
	in_pixels = in_file.load()
	size = in_file.size
	words = lines[-1].split()
	if words[0] != "output":
		print("NO OUTPUT FILE FOR ",args)
		continue
	filename = words[1].strip()
	out_file = Image.new("RGBA", size, (0,0,0,0))
	out_file.save(filename)
	pixels = np.array(in_file)
	pixels = pixels / 255

	putpixel = out_file.im.putpixel

	for line in lines:
		command(line)

	pixels = np.clip(pixels,0,1)

	out_file = Image.fromarray(np.uint8(pixels*255))
	out_file.save(filename)