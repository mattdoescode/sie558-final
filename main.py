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


while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill((255, 255, 255))

    red1, blue1, red2, blue2, red3, blue3, red4, blue4, pot, photo, mic, distance = arduino1.readline().decode('ascii').split(",")

    messageDisplay("Station 1:", 48, textPositionSensor1[0], textPositionSensor1[1])
    messageDisplay("Blue Button: " + blue1, 36, textPositionSensor1[0], textPositionSensor1[1] + 35)
    messageDisplay("Red Button: " + red1, 36, textPositionSensor1[0], textPositionSensor1[1] + 70)
    messageDisplay("Potentiometer: " + mic, 36, textPositionSensor1[0], textPositionSensor1[1] + 105)

    #0 update display arduino2
    messageDisplay("Station 2:", 48, textPositionSensor2[0], textPositionSensor2[1])
    messageDisplay("Blue Button: " + blue2, 36, textPositionSensor2[0], textPositionSensor2[1] + 35)
    messageDisplay("Red Button: " + red2, 36, textPositionSensor2[0], textPositionSensor2[1] + 70)
    distance = distance.rstrip()
    messageDisplay("Potentiometer: " + distance, 36, textPositionSensor2[0], textPositionSensor2[1] + 105)



    # try:
    #     sensorData1Blue, sensorData1Red, sensorData1 = arduino1.readline().decode('ascii').split(",")
    #
    #     # update display arduino1
    #     messageDisplay("Station 1:", 48, textPositionSensor1[0], textPositionSensor1[1])
    #     # remove \n
    #     sensorData1 = sensorData1.rstrip()
    #     messageDisplay("Blue Button: " + sensorData1Blue, 36, textPositionSensor1[0], textPositionSensor1[1] + 35)
    #     messageDisplay("Red Button: " + sensorData1Red, 36, textPositionSensor1[0], textPositionSensor1[1] + 70)
    #     messageDisplay("Potentiometer: " + sensorData1, 36, textPositionSensor1[0], textPositionSensor1[1] + 105)
    #
    #     # update display arduino2
    #     messageDisplay("Station 2:", 48, textPositionSensor2[0], textPositionSensor2[1])
    # except:
    #     print("error reading sensor 1")

    # print(arduino1.readline().decode('ascii').split(","), "      ", arduino2.readline().decode('ascii').split(","),  "      ", arduino4.readline().decode('ascii').split(","), )



    # print(arduino1.readline().decode('ascii').split(","), "    ", arduino2.readline().decode('ascii').split(","), "     ", arduino3.readline().decode('ascii').split(",")
    #     , "        ", arduino4.readline().decode('ascii').split(","))

    # try:
    #     sensorData2Blue, sensorData2Red, sensorData2 = arduino2.readline().decode('ascii').split(",")
    #     # # remove \n
    #     sensorData2 = sensorData2.rstrip()
    #     messageDisplay("Blue Button: " + sensorData2Blue, 36, textPositionSensor2[0], textPositionSensor2[1] + 35)
    #     messageDisplay("Red Button: " + sensorData2Red, 36, textPositionSensor2[0], textPositionSensor2[1] + 70)
    #     messageDisplay("Potentiometer: " + sensorData2, 36, textPositionSensor2[0], textPositionSensor2[1] + 105)
    # except:
    #     print("error reading sensor 2")

    # update display arduino3


    # update display arduino4


    # print(type(arduino1.readline().decode('ascii')))
    # print(arduino2.readline().decode('ascii'))

    pygame.display.update()

pygame.quit()
quit()