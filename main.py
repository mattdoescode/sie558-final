# author = matthew loewen
# date = 12/11/2019
# description = sie 558 final
# this project reads data from 4 Arduinos with sensors and makes a visual display of their readings

import serial
import pygame
import mysql.connector
import time

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="558-final"
)

mycursor = cnx.cursor()

arduino1 = serial.Serial('COM13', 9600, timeout=1)
# arduino2 = serial.Serial('COM11', 9600, timeout=1)
# arduino3 = serial.Serial('COM9', 9600, timeout=1)
# arduino4 = serial.Serial('COM12', 9600, timeout=1)

currentTime = time.time()
timeToRefresh = currentTime + 5
timeToRefreshSensor = currentTime + 2

textPositionSensor1 = [25, 25]
textPositionSensor2 = [600, 25]
textPositionSensor3 = [600, 600]
textPositionSensor4 = [25, 600]

activeBluePess = [0, 0, 0, 0]
blueButton = [-1, -1, -1, -1]
activeRedPess = [0, 0, 0, 0]
redButton = [-1, -1, -1, -1]

red5Minute = [0,0,0,0]
blue5Minute = [0,0,0,0]

red10Minute = [0,0,0,0]
blue10Minute = [0,0,0,0]

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


def recordButtonPress(buttonName):
    sql = "INSERT INTO button (name) VALUE ('" + buttonName + "')"
    mycursor.execute(sql)
    cnx.commit()


def checkRecordCount(buttonName, timeFrame):
    sql = "SELECT COUNT(name) FROM button WHERE time >= NOW() - INTERVAL " + timeFrame + " MINUTE AND name = '" + buttonName + "'"
    print(sql)
    mycursor = cnx.cursor(buffered=True)
    mycursor.execute(sql)
    cnx.commit()
    myresult = mycursor.fetchall()
    for x in myresult:
        return x[0]


def recordSensorValue(sensorName, sensorValue):
    sql = "INSERT INTO sensordata (name, value) VALUE (" + str(sensorName) + " , " + str(sensorValue) + ")"
    mycursor.execute(sql)
    cnx.commit()


# refactor
def checkButtonPress(red1, blue1, red2, blue2, red3, blue3, red4, blue4):
    if red1 == 1 and activeRedPess[0] == 0:
        redButton[0] = redButton[0] + 1
        activeRedPess[0] = 1
        recordButtonPress("red1")
    elif red1 == 0 and activeRedPess[0] == 1:
        activeRedPess[0] = 0
    if red2 == 1 and activeRedPess[1] == 0:
        redButton[1] = redButton[1] + 1
        activeRedPess[1] = 1
        recordButtonPress("red2")
    elif red2 == 0 and activeRedPess[1] == 1:
        activeRedPess[1] = 0
    if red3 == 1 and activeRedPess[2] == 0:
        redButton[2] = redButton[2] + 1
        activeRedPess[2] = 1
        recordButtonPress("red3")
    elif red3 == 0 and activeRedPess[2] == 1:
        activeRedPess[2] = 0
    if red4 == 1 and activeRedPess[3] == 0:
        redButton[3] = redButton[3] + 1
        activeRedPess[3] = 1
        recordButtonPress("red4")
    elif red4 == 0 and activeRedPess[0] == 1:
        activeRedPess[3] = 0

    if blue1 == 1 and activeBluePess[0] == 0:
        blueButton[0] = blueButton[0] + 1
        activeBluePess[0] = 1
        recordButtonPress("blue1")
    elif blue1 == 0 and activeBluePess[0] == 1:
        activeBluePess[0] = 0
    if blue2 == 1 and activeBluePess[1] == 0:
        blueButton[1] = blueButton[1] + 1
        activeBluePess[1] = 1
        recordButtonPress("blue2")
    elif blue2 == 0 and activeBluePess[1] == 1:
        activeBluePess[1] = 0
    if blue3 == 1 and activeBluePess[2] == 0:
        blueButton[2] = blueButton[2] + 1
        activeBluePess[2] = 1
        recordButtonPress("blue3")
    elif blue3 == 0 and activeBluePess[2] == 1:
        activeBluePess[2] = 0
    if blue4 == 1 and activeBluePess[3] == 0:
        blueButton[3] = blueButton[3] + 1
        activeBluePess[3] = 1
        recordButtonPress("blue4")
    elif blue4 == 0 and activeBluePess[0] == 1:
        activeBluePess[3] = 0


micIdeal = 24
# determine error ranges
idealLight = 720
distanceIdeal = 10.1;

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    gameDisplay.fill((255, 255, 255))


    try:
        red1, blue1, red2, blue2, red3, blue3, red4, blue4, pot, photo, mic, distance = arduino1.readline().decode('ascii').split(",")
    except:
        continue

    checkButtonPress(int(red1), int(blue1), int(red2), int(blue2), int(red3), int(blue3), int(red4), int(blue4));

    # microphone color square
    mic = int(mic)
    if mic == micIdeal:
        pygame.draw.rect(gameDisplay, (0, 255, 0), (0, 0, screenX / 2, screenY / 2))
        error = ""
    elif mic == micIdeal + 1 or mic == micIdeal - 1 or mic == micIdeal - 2:
        pygame.draw.rect(gameDisplay, (125, 130, 0), (0, 0, screenX / 2, screenY / 2))
        error = ""
    else:
        pygame.draw.rect(gameDisplay, (255, 0, 0), (0, 0, screenX / 2, screenY / 2))
        error = "ERROR!"

    # display grid 1
    messageDisplay("Station 1: " + error, 48, textPositionSensor1[0], textPositionSensor1[1])
    messageDisplay("Blue Button: " + blue1, 36, textPositionSensor1[0], textPositionSensor1[1] + 35)
    messageDisplay("Red Button: " + red1, 36, textPositionSensor1[0], textPositionSensor1[1] + 70)
    messageDisplay("Microphone: " + str(mic), 36, textPositionSensor1[0], textPositionSensor1[1] + 105)
    messageDisplay("Accepted: " + str(blueButton[0]), 36, textPositionSensor1[0], textPositionSensor1[1] + 135)
    messageDisplay("Rejected: " + str(redButton[0]), 36, textPositionSensor1[0], textPositionSensor1[1] + 165)
    messageDisplay("Rejected 5 Minutes: " + str(red5Minute[0]), 36, textPositionSensor1[0], textPositionSensor1[1] + 195)
    messageDisplay("Rejected 10 Minutes: " + str(red10Minute[0]), 36, textPositionSensor1[0],textPositionSensor1[1] + 225)
    messageDisplay("Accepted 5 Minutes: " + str(blue5Minute[0]), 36, textPositionSensor1[0], textPositionSensor1[1] + 255)
    messageDisplay("Accepted 10 Minutes: " + str(blue10Minute[0]), 36, textPositionSensor1[0],textPositionSensor1[1] + 285)

    # removed ascii characters
    distance = distance.rstrip()

    if float(distance) > 20:
        changeColor = 255
    elif float(distance) < 9.5:
        changeColor = 255
    else:
        changeColor = translateValueRange(float(distance), 9.5, 20, 0, 255)

    pygame.draw.rect(gameDisplay, (changeColor, 255 - changeColor, 0), (screenX / 2, 0, screenX / 2, screenY / 2))

    if changeColor == 255:
        error = "ERROR!"
    else:
        error = ""

    # display grid 2
    messageDisplay("Station 2: " + error, 48, textPositionSensor2[0], textPositionSensor2[1])
    messageDisplay("Blue Button: " + blue2, 36, textPositionSensor2[0], textPositionSensor2[1] + 35)
    messageDisplay("Red Button: " + red2, 36, textPositionSensor2[0], textPositionSensor2[1] + 70)
    messageDisplay("Distance : " + distance, 36, textPositionSensor2[0], textPositionSensor2[1] + 105)
    messageDisplay("Accepted: " + str(blueButton[1]), 36, textPositionSensor2[0], textPositionSensor2[1] + 135)
    messageDisplay("Rejected: " + str(redButton[1]), 36, textPositionSensor2[0], textPositionSensor2[1] + 165)
    messageDisplay("Rejected 5 Minutes: " + str(red5Minute[1]), 36, textPositionSensor2[0], textPositionSensor2[1] + 195)
    messageDisplay("Rejected 10 Minutes: " + str(red10Minute[1]), 36, textPositionSensor2[0],textPositionSensor2[1] + 225)
    messageDisplay("Accepted 5 Minutes: " + str(blue5Minute[1]), 36, textPositionSensor2[0], textPositionSensor2[1] + 255)
    messageDisplay("Accepted 10 Minutes: " + str(blue10Minute[1]), 36, textPositionSensor2[0],textPositionSensor2[1] + 285)

    lightError = abs(idealLight - int(photo))
    if lightError > 255:
        lightError = 255

    pygame.draw.rect(gameDisplay, (lightError, 255 - lightError, 0),
                     (screenX / 2, screenY / 2, screenX / 2, screenY / 2))

    if lightError == 255:
        error = "ERROR!"
    else:
        error = ""

    # display grid 3
    messageDisplay("Station 3: " + error, 48, textPositionSensor3[0], textPositionSensor3[1])
    messageDisplay("Blue Button: " + blue3, 36, textPositionSensor3[0], textPositionSensor3[1] + 35)
    messageDisplay("Red Button: " + red3, 36, textPositionSensor3[0], textPositionSensor3[1] + 70)
    messageDisplay("Light Level: " + photo, 36, textPositionSensor3[0], textPositionSensor3[1] + 105)
    messageDisplay("Accepted: " + str(blueButton[2]), 36, textPositionSensor3[0], textPositionSensor3[1] + 135)
    messageDisplay("Rejected: " + str(redButton[2]), 36, textPositionSensor3[0], textPositionSensor3[1] + 165)
    messageDisplay("Rejected 5 Minutes: " + str(red5Minute[2]), 36, textPositionSensor3[0], textPositionSensor3[1] + 195)
    messageDisplay("Rejected 10 Minutes: " + str(red10Minute[2]), 36, textPositionSensor3[0],textPositionSensor3[1] + 225)
    messageDisplay("Accepted 5 Minutes: " + str(blue5Minute[2]), 36, textPositionSensor3[0], textPositionSensor3[1] + 255)
    messageDisplay("Accepted 10 Minutes: " + str(blue10Minute[2]), 36, textPositionSensor3[0],textPositionSensor3[1] + 285)

    if int(pot) <= 300:
        potError = 255
        pygame.draw.rect(gameDisplay, (255, 0, 0), (0, screenY / 2, screenX / 2, screenY / 2))
    else:
        potError = translateValueRange(int(pot), 300, 1024, 0, 255)
        pygame.draw.rect(gameDisplay, (255 - potError, potError, 0), (0, screenY / 2, screenX / 2, screenY / 2))

    if potError == 255:
        error = "ERROR!"
    else:
        error = ""

    # display grid 4
    messageDisplay("Station 4: " + error, 48, textPositionSensor4[0], textPositionSensor4[1])
    messageDisplay("Blue Button: " + blue4, 36, textPositionSensor4[0], textPositionSensor4[1] + 35)
    messageDisplay("Red Button: " + red4, 36, textPositionSensor4[0], textPositionSensor4[1] + 70)
    messageDisplay("Resistance: " + pot, 36, textPositionSensor4[0], textPositionSensor4[1] + 105)
    messageDisplay("Accepted: " + str(blueButton[3]), 36, textPositionSensor4[0], textPositionSensor4[1] + 135)
    messageDisplay("Rejected: " + str(redButton[3]), 36, textPositionSensor4[0], textPositionSensor4[1] + 165)
    messageDisplay("Rejected 5 Minutes: " + str(red5Minute[3]), 36, textPositionSensor4[0], textPositionSensor4[1] + 195)
    messageDisplay("Rejected 10 Minutes: " + str(red10Minute[3]), 36, textPositionSensor4[0],textPositionSensor4[1] + 225)
    messageDisplay("Accepted 5 Minutes: " + str(blue5Minute[3]), 36, textPositionSensor4[0], textPositionSensor4[1] + 255)
    messageDisplay("Accepted 10 Minutes: " + str(blue10Minute[3]), 36, textPositionSensor4[0],textPositionSensor4[1] + 285)

    if timeToRefresh < time.time():
        timeToRefresh = time.time()+10

        red5Minute[0] = checkRecordCount("red1", "5")
        red5Minute[1] = checkRecordCount("red2", "5")
        red5Minute[2] = checkRecordCount("red3", "5")
        red5Minute[3] = checkRecordCount("red4", "5")

        red10Minute[0] = checkRecordCount("red1", "10")
        red10Minute[1] = checkRecordCount("red2", "10")
        red10Minute[2] = checkRecordCount("red3", "10")
        red10Minute[3] = checkRecordCount("red4", "10")

        blue5Minute[0] = checkRecordCount("blue1", "5")
        blue5Minute[1] = checkRecordCount("blue2", "5")
        blue5Minute[2] = checkRecordCount("blue3", "5")
        blue5Minute[3] = checkRecordCount("blue4", "5")

        blue10Minute[0] = checkRecordCount("blue1", "10")
        blue10Minute[1] = checkRecordCount("blue2", "10")
        blue10Minute[2] = checkRecordCount("blue3", "10")
        blue10Minute[3] = checkRecordCount("blue4", "10")
    pygame.display.update()

    # if timeToRefreshSensor < time.time():
    #     timeToRefreshSensor = time.time()+2
    #
    #     recordSensorValue("mic", int(mic))
    #     recordSensorValue("distance", float(mic))
    #     recordSensorValue("photo", float(photo))
    #     recordSensorValue("resistance", int(pot))


pygame.quit()
quit()
