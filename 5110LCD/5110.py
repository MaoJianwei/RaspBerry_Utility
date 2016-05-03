# coding=utf-8
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

import Image
import ImageDraw
import ImageFont


DC = 25
RST = 22
SPI_PORT = 0
SPI_DEVICE = 0

First_Line = -2
Line = 6


# image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
# draw = ImageDraw.Draw(image)
# draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
# font = ImageFont.load_default()
# font = ImageFont.truetype('5110.ttf', 10)
# draw.text((0,First_Line), 'jGPS=40.046,116.466', font=font)
# draw.text((0,First_Line + 1*Line), 'QWERTYUIOP', font=font)
# draw.text((0,First_Line + 2*Line), 'ASDFGHJKL;', font=font)
# draw.text((0,First_Line + 3*Line), 'ZXCVBNM,.?', font=font)
# draw.text((0,First_Line + 4*Line), '0123456789', font=font)
# draw.text((0,First_Line + 5*Line), '1123456789', font=font)
# draw.text((0,First_Line + 6*Line), '2123456789', font=font)
# draw.text((0,First_Line + 7*Line), '666666666666678', font=font)
# draw.text((0,First_Line + 8*Line), '4123456789', font=font)
# disp.image(image)
# disp.display()

def getNewImage():
    image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, LCD.LCDWIDTH, LCD.LCDHEIGHT), outline=255, fill=255)
    addOneLine(draw, "Mao Cloud v0.6", 0, True)
    return (image, draw)

def addOneLine(draw, txt, lineNum, isInit=False):
    font = ImageFont.truetype('5110.ttf', 10)
    if(isInit):
        draw.text((0, First_Line), txt, font=font)
    else:
        draw.text((0, First_Line + 3 + lineNum * Line), txt, font=font)
    return

def clearLCD(screen):
    screen.clear()
    screen.display()
    return

def showLCD(screen, image):
    screen.image(image)
    screen.display()
    return


def getCharWidth(char):
    if(char == '1'):
        return 2+1
    elif(char == 'i' or char == 'I'):
        return 1+1
    elif(char == ';' or char == ',' or char == '.'):
        return 1+1
    elif(char == '\n'):
        return 0;
    else:
        return 5+1

def showStringNew(screen, text):

    (image, draw) = getNewImage()

    lineCounter = 1
    charCounter = 0

    subLen = 0
    subStr = ""
    while(charCounter < len(text)):
        charLen = getCharWidth(text[charCounter])
        if(charLen == 0):
            addOneLine(draw, subStr, lineCounter)
            charCounter = charCounter + 1
            lineCounter = lineCounter + 1
            subLen = 0
            subStr = ""
        elif(subLen + charLen > 84):
            addOneLine(draw, subStr, lineCounter)
            lineCounter = lineCounter + 1
            subLen = 0
            subStr = ""
        else:
            subStr = subStr + text[charCounter]
            subLen = subLen + charLen
            charCounter = charCounter + 1

    addOneLine(draw, subStr, lineCounter)
    showLCD(screen, image)
    return

screen = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))
screen.begin(contrast=60)
clearLCD(screen)
showStringNew(screen, "HU7181,\ncontact beijing tower on 118.5,\ngood day!")