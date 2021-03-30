from PIL import Image
from termcolor import colored
import os

# Open with a check for the existence of the file with the secret message 
try:
	f_secret = open("secret.txt",'r')
	secretText = f_secret.read() + '~'
	f_secret.close()
except FileNotFoundError:
	print("Stego message file not exist!")
	quit()	

# Open with a check for the existence of the carrier file
coverFile = input("Input BMP cover file name without extension: ")
coverFile = coverFile + ".bmp"

try:
	img = Image.open(coverFile)
except FileNotFoundError:
	print("Cover file not exist!")
	quit()

# Function for colored display of RGB values of the image 
def PrintImage(pixels):
	for i in range(0,img.size[0]):
		for j in range(0,img.size[1]):
			b,g,r = pixels[i,j]
			print(colored(b,'blue'),colored(g,'green'),colored(r,'red'), end=',')
		print()	

# Function for converting the hidden message into a binary record 
def StrToBin(secret):
	string = ""
	for symbol in secret:
		string += str(format(ord(symbol),'08b'))
	return string	

# Function for check if number is even
def even(color):
	if color % 2 == 0:
		return True
	else:
		return False	

# Function to change the least significant bit 
def change(color,bit):
	if bit == '0' and even(color):
		return color, 0
	if bit == '0' and not even(color):
		return color - 1, 1
	if bit == '1' and even(color):
		return color + 1, 1
	if bit == '1' and not even(color):
		return color, 0			

# Function for inserting a secret message in the image
def Embedding():
	# Writing in a variable the secret message in binary record
	binSecretText = StrToBin(secretText)
	# Write to variable length binary record 
	numberBytes = len(binSecretText)
	# Variable to count each insert 
	br = 0
	# Тaking the pixel matrix of the carrier file 
	pixels = img.load()
	PrintImage(pixels)
	changes = 0
	# Performing LSB modification in the image
	for i in range(0,img.size[0]):
		for j in range(0,img.size[1]):
			b,g,r = pixels[i,j]
			if br < numberBytes:
				b,ch = change(b,binSecretText[br])
				br += 1
				changes += ch 
			if br < numberBytes:
				g,ch = change(g,binSecretText[br])
				br += 1
				changes += ch
			if br < numberBytes:
				r,ch = change(r,binSecretText[br])
				br += 1
				changes += ch
			pixels[i,j] = b,g,r		
	print("--------------------------------------------------------")
	PrintImage(pixels)
	print("Total changes:",changes)			

	img.save("stego2.bmp")
	img.close()

maxByteImage = img.size[0]*img.size[1]*3
lengthSecretText = len(secretText)*8

print("Maximum number of bytes in cover image:",maxByteImage)
print("Required bytes for the secret message:",lengthSecretText)

if lengthSecretText > maxByteImage:
	print("The secret message is too big for the cover file!")
	quit()

Embedding()
