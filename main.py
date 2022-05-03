"""
Author: David Moore
Course: Python 87B
Date: 3/27/22
Purpose: To write a script that takes a photo, edits its colors and resizes it.  My goal is to
edit the image vai quadrants.  The 3 quadrants will be edited using the mapping, grayscale, and
negative features we have learned and the final quadrant will be left unedited for reference.  Once
edited it will double the size of the image(Expanding from a 512x512 grid to 1024x1024 grid).
"""
from image import *
import math

def doublesize(image):
    old = image
    width = old.getWidth()
    height = old.getHeight()

    doubled = EmptyImage(width * 2, height * 2)

    for row in range(height):
        for col in range(width):
            oldP = old.getPixel(col, row)

            doubled.setPixel(2 * col, 2 * row, oldP)
            doubled.setPixel(2 * col + 1, 2 * row, oldP)
            doubled.setPixel(2 * col, 2 * row + 1, oldP)
            doubled.setPixel(2 * col + 1, 2 * row + 1, oldP)

    return doubled

def make_gray(image):
    intSum = image.getRed() + image.getGreen() + image.getBlue()
    aveRGB = intSum // 3
    newPixel = Pixel(aveRGB, aveRGB, aveRGB)
    return newPixel

def gray_scale(image, width, height):
    gray = image

    for row in range(height):
        for col in range(width):
            pic = gray.getPixel(col, row)
            newPixel = make_gray(pic)
            gray.setPixel(col, row, newPixel)

    return gray

def neg(image):
    red = 255 - image.getRed()
    green = 255 - image.getGreen()
    blue = 255 - image.getBlue()
    newPixel = Pixel(red, green, blue)

    return newPixel

def negative(image, widthStart, widthEnd, heightStart, heightEnd):
    negative = image
    for row in range(heightStart, heightEnd):
        for col in range(widthStart, widthEnd):
            inverse = negative.getPixel(col, row)
            newPixel = neg(inverse)
            negative.setPixel(col, row, newPixel)

    return negative

def vertFlip(image):
    oldW = image.getWidth()
    oldH = image.getHeight()

    newIm = EmptyImage(oldW, oldH)
    maxP = oldW - 1
    for row in range(oldH):
        for col in range(oldW):
            oldPixel = image.getPixel(maxP - col, row)
            newIm.setPixel(col, row, oldPixel)

    return newIm

def convolve(image, pRow, pCol, kernel):
    kernelColumnBase = pCol - 1
    kernelRowBase = pRow - 1
    sum = 0
    for row in range(kernelRowBase, kernelRowBase + 3):
        for col in range(kernelColumnBase, kernelColumnBase + 3):
            kColIndex = col - kernelColumnBase
            kRowIndex = row - kernelRowBase
            aPixel = image.getPixel(col, row)
            intensity = aPixel.getRed()
            sum = sum + intensity * kernel[kRowIndex][kColIndex]
    return sum

def edgeDetect(image,width, height):
    """
    The instructional document notes that 175 is a good threshold value, however I found that through
    increasing the number significantly, the result in the quadrant had higher accuracy.
    """
    graySection = gray_scale(image,width, height)
    newIM = image
    black = Pixel(0,0,0)
    white = Pixel(255, 255, 255)
    XMask = [[-1,-2,-1], [0,0,0], [1,2,1]]
    YMask = [[1,0,-1], [2,0,-2], [1,0,-1]]

    for row in range(1, width):
        for col in range(1, height):
            gX = convolve(graySection, row, col, XMask)
            gY = convolve(graySection, row, col, YMask)
            g = math.sqrt(gX**2 + gY**2)

            if g > 650:
                newIM.setPixel(col, row, black)
            else:
                newIM.setPixel(col,row, white)

    return newIM

def printImage(image):
    width = image.getWidth()
    height = image.getHeight()
    win = ImageWin(height, width, "Check It Out!")
    image.draw(win)
    print("Please click anywhere on the image to exit.")
    win.exitonclick()
    image.save("EditedBrule.gif")

def recolor(image):
    new_color = image
    width = new_color.getWidth()
    height = new_color.getHeight()

    second_quad_h = int(height * .5)
    second_quad_w = int(width * .5)

    gray_scale(new_color, second_quad_w, second_quad_h)
    negative(new_color, second_quad_w, width, second_quad_h, height)
    flip1 = vertFlip(new_color)
    edgeDetect(flip1, second_quad_w, second_quad_h)
    final_image = vertFlip(flip1)

    return final_image

def main():
    #Please feel free to change it to any jpg
    bringo = FileImage("Brule.jpg")
    new_color = recolor(bringo)
    new_size = doublesize(new_color)
    printImage(new_size)

if __name__ == "__main__":
    main()