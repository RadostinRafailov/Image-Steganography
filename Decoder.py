from PIL import Image

# Open with a check for the existence of the stego file with the secret message 
stegoFile = input("Input BMP stego file name without extension: ")
stegoFile = stegoFile + ".bmp"

try:
        img = Image.open(stegoFile)
        pixels = img.load()
        l_pixels = []
except FileNotFoundError:
        print("Stego file not exist!")
        quit()  

def Getsymbol(octet):
	bnr = ""
	for each in range(0,len(octet)):
		bnr += str(format(octet[each],'08b'))[7]

	return chr(int(bnr,2)) 	

def PixelMatrixToList(pixels):
	for i in range(0,img.size[0]):
		for j in range(0,img.size[1]):
			b,g,r = pixels[i,j]
			l_pixels.append(b)
			l_pixels.append(g)
			l_pixels.append(r)

	return l_pixels



PixelMatrixToList(pixels)

stegoText = ""
for i in range(0,len(l_pixels),8):
	symbol = Getsymbol(l_pixels[i:i+8])
	if symbol == '~':
		break
	else:	
		stegoText += symbol

f = open("stego.txt",'w')
f.write(stegoText)
f.close()
print(stegoText)



img.close()
