# author = matthew loewen
# date = 12/11/2019
# description = sie 558 final
# this project reads data from 4 Arduinos with sensors and makes a visual display of their readings

import serial
import pygame

arduino1 = serial.Serial('COM13', 9600, timeout=1)
# arduino2 = serial.Serial('COM11', 9600, timeout=1)
# arduino3 = serial.Serial('COM9', 9600, timeout=1)
# arduino4 = serial.Serial('COM12', 9600, timeout=1)

textPositionSensor1 = [25, 25]
textPositionSensor2 = [600, 25]
textPositionSensor3 = [600, 600]
textPositionSensor4 = [25, 600]

pygame.init()
white = (0, 0, 0)

gameDisplay = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption('Matthew Loewen - SIE 558 Final')

crashed = False

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface

def messageDisplay(text, size, xPos, Ypos):
    largeText = pygame.font.SysFont("C:\Windows\Fonts\Arial.ttf", size)
    textSurf = text_objects(text, largeText)
    gameDisplay.blit(textSurf, (xPos, Ypos))

#
# Function from:
# https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
def translateValueRange(value, oldMin, oldMax, newMin, newMax):
    newValue = (((value - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin
    return newValue;


while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill((255, 255, 255))

    red1, blue1, red2, blue2, red3, blue3, red4, blue4, pot, photo, mic, distance = arduino1.readline().decode('ascii').split(",")

    # draw 4 squares 1 for each sensor.
    pygame.draw.rect(gameDisplay, (255, 0, 0), (0, 0, 300, 300))

    # display grid 1
    messageDisplay("Station 1:", 48, textPositionSensor1[0], textPositionSensor1[1])
    messageDisplay("Blue Button: " + blue1, 36, textPositionSensor1[0], textPositionSensor1[1] + 35)
    messageDisplay("Red Button: " + red1, 36, textPositionSensor1[0], textPositionSensor1[1] + 70)
    messageDisplay("Microphone: " + mic, 36, textPositionSensor1[0], textPositionSensor1[1] + 105)

    # value of mic is 24ish
    # we have noise if it gets above 24
    

    # display grid 2
    messageDisplay("Station 2:", 48, textPositionSensor2[0], textPositionSensor2[1])
    messageDisplay("Blue Button: " + blue2, 36, textPositionSensor2[0], textPositionSensor2[1] + 35)
    messageDisplay("Red Button: " + red2, 36, textPositionSensor2[0], textPositionSensor2[1] + 70)
    distance = distance.rstrip()
    messageDisplay("Distance : " + distance, 36, textPositionSensor2[0], textPositionSensor2[1] + 105)

    #display grid 3
    messageDisplay("Station 3:", 48, textPositionSensor3[0], textPositionSensor3[1])
    messageDisplay("Blue Button: " + blue3, 36, textPositionSensor3[0], textPositionSensor3[1] + 35)
    messageDisplay("Red Button: " + red3, 36, textPositionSensor3[0], textPositionSensor3[1] + 70)
    messageDisplay("Light Level: " + photo, 36, textPositionSensor3[0], textPositionSensor3[1] + 105)

    #display grid 4
    messageDisplay("Station 4:", 48, textPositionSensor4[0], textPositionSensor4[1])
    messageDisplay("Blue Button: " + blue4, 36, textPositionSensor4[0], textPositionSensor4[1] + 35)
    messageDisplay("Red Button: " + red4, 36, textPositionSensor4[0], textPositionSensor4[1] + 70)
    messageDisplay("Resistance: " + pot, 36, textPositionSensor4[0], textPositionSensor4[1] + 105)

    pygame.display.update()

pygame.quit()
quit()