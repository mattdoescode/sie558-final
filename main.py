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

screenX = screenY = 1000

gameDisplay = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption('Matthew Loewen - SIE 558 Final')

crashed = False

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface


def messageDisplay(text, size, xPos, Ypos):
    largeText = pygame.font.SysFont("C:\Windows\Fonts\Arial.ttf", size)
    textSurf = text_objects(text, largeText)
    gameDisplay.blit(textSurf, (xPos, Ypos))

# # Function from:
# https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
def translateValueRange(value, oldMin, oldMax, newMin, newMax):
   newValue = (((value - oldMin) * (newMax - newMin)) / (oldMax - oldMin)) + newMin
   return newValue;

micIdeal = 24
# determine error ranges
idealLight = 630
distanceIdeal = 10.1;

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill((255, 255, 255))

    red1, blue1, red2, blue2, red3, blue3, red4, blue4, pot, photo, mic, distance = arduino1.readline().decode(
        'ascii').split(",")

    # microphone color square
    mic = int(mic)
    if mic == micIdeal:
        pygame.draw.rect(gameDisplay, (0, 255, 0), (0, 0, screenX/2, screenY/2))
    elif mic == micIdeal + 1 or mic == micIdeal - 1 or mic == micIdeal - 2:
        pygame.draw.rect(gameDisplay, (125, 130, 0), (0, 0, screenX/2, screenY/2))
    else:
        pygame.draw.rect(gameDisplay, (255, 0, 0), (0, 0, screenX/2, screenY/2))

    # display grid 1
    messageDisplay("Station 1:", 48, textPositionSensor1[0], textPositionSensor1[1])
    messageDisplay("Blue Button: " + blue1, 36, textPositionSensor1[0], textPositionSensor1[1] + 35)
    messageDisplay("Red Button: " + red1, 36, textPositionSensor1[0], textPositionSensor1[1] + 70)
    messageDisplay("Microphone: " + str(mic), 36, textPositionSensor1[0], textPositionSensor1[1] + 105)

    # removed ascii characters
    distance = distance.rstrip()

    if float(distance) > 20:
        changeColor = 255
    elif float(distance) < 10:
        changeColor = 255
    else:
        changeColor = translateValueRange(float(distance), 10, 20, 0, 255)

    pygame.draw.rect(gameDisplay, (changeColor, 255 - changeColor, 0), (screenX/2, 0, screenX/2, screenY/2))


    # display grid 2
    messageDisplay("Station 2:", 48, textPositionSensor2[0], textPositionSensor2[1])
    messageDisplay("Blue Button: " + blue2, 36, textPositionSensor2[0], textPositionSensor2[1] + 35)
    messageDisplay("Red Button: " + red2, 36, textPositionSensor2[0], textPositionSensor2[1] + 70)
    messageDisplay("Distance : " + distance, 36, textPositionSensor2[0], textPositionSensor2[1] + 105)

    lightError = abs(idealLight - int(photo))
    if lightError > 255:
        lightError = 255

    pygame.draw.rect(gameDisplay, (lightError, 255 - lightError, 0), (screenX/2, screenY/2, screenX/2, screenY/2))

    # display grid 3
    messageDisplay("Station 3:", 48, textPositionSensor3[0], textPositionSensor3[1])
    messageDisplay("Blue Button: " + blue3, 36, textPositionSensor3[0], textPositionSensor3[1] + 35)
    messageDisplay("Red Button: " + red3, 36, textPositionSensor3[0], textPositionSensor3[1] + 70)
    messageDisplay("Light Level: " + photo, 36, textPositionSensor3[0], textPositionSensor3[1] + 105)

    if int(pot) <= 300:
        potError = 255
        pygame.draw.rect(gameDisplay, (255, 0, 0), (0, screenY / 2, screenX / 2, screenY / 2))
    else:
        potError = translateValueRange(int(pot), 300, 1024, 0, 255)
        pygame.draw.rect(gameDisplay, (255 - potError, potError, 0), (0, screenY / 2, screenX / 2, screenY / 2))

    print(potError)

    # display grid 4
    messageDisplay("Station 4:", 48, textPositionSensor4[0], textPositionSensor4[1])
    messageDisplay("Blue Button: " + blue4, 36, textPositionSensor4[0], textPositionSensor4[1] + 35)
    messageDisplay("Red Button: " + red4, 36, textPositionSensor4[0], textPositionSensor4[1] + 70)
    messageDisplay("Resistance: " + pot, 36, textPositionSensor4[0], textPositionSensor4[1] + 105)

    pygame.display.update()

pygame.quit()
quit()
