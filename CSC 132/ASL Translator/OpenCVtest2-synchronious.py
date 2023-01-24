#import required libraries
from cvzone.HandTrackingModule import HandDetector
import cv2  
from time import monotonic, perf_counter_ns
import numpy as np
import keyboard as kb

#Global Variables
#hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)
#Measuremnt Matrix to record measurements
measurementMatrix = []
#Debug Variable
DEBUG = True
##Timer Related Variables
delayTimerEndTime = 0
preformanceTimer = False
elapsedTime = 0
#Variable to determine Type of recognition 
plot = True
comparison = False
#Calibaration offset list, shares order with measurement pairs
offsetList = []

#List of point pairs to measure
measurementPairs = [
    
    #Connect Neighbors
    (4, 8), #Thumb tip to index tip
    (8, 12), #Index tip to middle tip
    (12, 16), #Middle tip to ring tip
    (16, 20), #Ring tip to pinky tip
   
    #Connect tips to bottom of hand
    (4, 0), #Thumb to bottom of hand
    (8, 0), #Index to bottom of hand
    (12, 0), #Middle to bottom of hand
    (16, 0), #Ring to bottom of hand
    (20, 0), #Pinky to bottom of hand
   
    #Connect thumb tip to other tips
    (4, 12), #Thumb to middle
    (4, 16), #Thumb to ring
    (4, 20) #Thumb to pinky

]

#Dictionary of letters represented by their corresponding 
#measurement range list
alphaDictRange = {
    
    "A" : [(65,75), (15,25), (20,30), (20,30), (170,180), (90,100), (75,85), (70,80), (70,80), (90,100), (105,115), (120,130), (-20,20)]
    
}

#Dictionary of letters represented by their corresponding
#measurement value list
alphaDictPoint = {
    "A" : [55, 20, 20, 20, 125, 70, 60, 50, 55, 65, 85, 100, -30]
}
            
#function that finds the angle of the hand
def findAngle(hand, img = None):
    
    #base and center landmarks
    baseX, baseY, z = hand["lmList"][0]
    middleFingerX, middleFingerY, z = hand["lmList"][9]
    
    #define vertical line
    vert = (baseX, 0)
    
    #create vectors
    baseToPalm = np.array([middleFingerX, middleFingerY]) - np.array([baseX, baseY])
    baseToTop = np.array(vert) - np.array([baseX, baseY])
    
    #calculate angle
    angle = np.degrees(np.math.atan2(np.linalg.det([baseToPalm, baseToTop]), np.dot(baseToPalm, baseToTop)))
    
    #if image is passed, print the vectors and return value
    if img is not None:
        cv2.line(img, (baseX,baseY), (middleFingerX, middleFingerY), (225,225,0), 3)
        cv2.line(img, (baseX,baseY), (vert[0],vert[1]), (225,225,0), 3)
        return angle, img
    
    #otherwise just return value
    else:
        return angle                

#Function that checks the input timer
def inputDelayTimer():
    if monotonic() > delayTimerEndTime:
        return True
    else:
        return False

#Function that sets the input delay timer
def startInputDelayTimer(delayTime):
    global delayTimerEndTime
    delayTimerEndTime = monotonic() + delayTime

#Function to get mesurements (defined by measurementPairs)
#and angle
def getMeasurements(hand, img = None):
    #reset measurement array
    measurements = []
                
    #measure distances
    for x, y in measurementPairs:
        measurement, info = detector.findDistance(hand["lmList"][x], hand["lmList"][y])
        measurements.append(measurement)
    
    #if debug is on, print values and display angle lines
    if DEBUG and img is not None:
        angle, img = findAngle(hand, img)
        measurements.append(angle)      
        #print all measurements
        print (f"measurements:{measurements}\nangle{angle}")
        return measurements, img
    
    else:
        #Calculate angle of hand and add to measurement list
        angle = findAngle(hand)
        measurements.append(angle)
        return measurements

#Function to record measurements into a global list
def recordMeasurements(list):
    global measurementMatrix
    measurementMatrix.append(list)

#Function that uses a set of points to determine the nearest point to the 
#recorded measurements
def detectLetterPlot(measurements, dict):
    #minimum margin for letter to be detected
    margin = 20
    
    #initialize local variables
    mostLikelyLetter = None
    distances = [0 for x in dict]
    
    
    for i, letter in enumerate(dict):
        for index, measurement in enumerate(measurements):
            
            #Sum (terminal - initial)^2
            distances[i] += (dict[letter][index] - measurement) ** 2
        
        #Square root to find distance
        distances[i] = distances[i] ** 0.5
        
        #Debug Print
        if DEBUG:
            print(distances[i])
        
        #if new found distance is less than the margin, save as the new 
        #most likely letter
        if distances[i] < margin:
            margin = distances[i]
            mostLikelyLetter = letter
        
        #print and return
        if mostLikelyLetter:
            print(f"{mostLikelyLetter}\tmargin:{margin}")
            startInputDelayTimer(4)
            return mostLikelyLetter

#Function that uses a dictionary of measuements to detect a letter in asl
def detectLetterCompare(measurements, dict):
    if preformanceTimer:
        t1_start = perf_counter_ns()
    try:
    #for each letter in the letter list
        for letter in dict:
            #for each value in measurements
            for index, val in enumerate(measurements):
                #unpack dictionary value max and min
                min,max = dict[letter][index]
                            
                #check if the value is less than the value 
                #in the matching position in the letter
                if val < (min*offsetList[index]) or val > (max*offsetList[index]):
                    break
                        
                #if the last check passes print the letter 
                #and delay input for 10 seconds
                elif index == len(measurements) - 1:
                    print(letter)
                    startInputDelayTimer(4)
                                
                    #break loop
                    raise StopIteration
                            
    except StopIteration:
        if preformanceTimer:
            printTimer(t1_start, perf_counter_ns())
        return letter
    if preformanceTimer:
        printTimer(t1_start, perf_counter_ns())
        
#Function that prints the preformance timer
def printTimer(start, stop):
    print(f"preformance elapsed time: {stop - start}ns")
    
#Function that receives a matrix and returns a list of tuples 
#with the maximum and minimum values of each index
def createMeasurementRange(matrix, returnType = "Plot" or "Range"):
    
    #initialize output list and fill with values from the first 2 measurement sets
    outputList = []
    for i in range(len(matrix[0])):
        x = matrix[0][i]
        y = matrix[1][i]
        if x > y:
            val = (x,y)
        else:
            val = (y,x)
        outputList.append(val)
    #Itterte through each measurement set in the matrix and compare 
    #to the tuple in the output list to define the maximums and minimums at that index
    for measurementSet in matrix:
        for index, measurement in enumerate(measurementSet):
            min, max = outputList[index]
            if measurement > max:
                max = measurement
            elif measurement < min:
                min = measurement
            outputList[index] = (min,max)
    
    #Print the maximum and minimum values and the difference between them
    if DEBUG:
        for min, max in outputList:
            print(f"max:{max}\tmin:{min}\trange:{max-min}")
        
        #Print the list
        print (outputList)
    
    #return the output list
    if returnType == "Plot":
        return [(min+max)/2 for min, max in outputList]
    
    if returnType == "Range":
        return outputList

#Calibrate measurement offsets by comparing an average measurement set to an ideal case and finding precent difference
def calibration():
 
    ideal = []
    calibrationMatrix = []
    global offsetList
    
    input(
        "Hold your right hand near your chest, plam facing camera with fingers outstretched and touching.\n\
        Press any key when hand is in position\n\
        Please hold position for 1 second."
            )
    
    print("HOLD")
    startInputDelayTimer(1)
    while not inputDelayTimer():
        calibrationMatrix.append(getMeasurements(hand))
    print("DONE")
    
    actual = createMeasurementRange(calibrationMatrix)
    
    for index, measurement in enumerate(actual):
        offsetList.append(measurement / ideal[index])
    
#Main function
def main():
    #initialize the video capture
    cap = cv2.VideoCapture(0)
    
    #Operational Loop
    while not kb.is_pressed("tab"):
    
        #Capture video and find hands
        success, img = cap.read()
        hands, img = detector.findHands(img, draw=True)
    
        #If hand is detected
        if hands:
        
            #Check if it is the right hand
            if hands[0]["type"] == "Right":
            
                #Define hand and landmarks
                rightHand = hands[0]
            
                #check input delay timer
                if inputDelayTimer():
                   
                    #measure hand, print if debug
                    if not DEBUG:
                        measurements = getMeasurements(rightHand)
                    else:
                        measurements, img = getMeasurements(rightHand, img)
                    
                    #Record Mesurements if space is pressed
                    if kb.is_pressed('space'):
                        recordMeasurements(measurements)
                    
                    else:
                        if comparison is True:
                            #Detect hand sign letter using comparison
                            detectLetterCompare(measurements, alphaDictRange)
                        elif plot is True:
                            #Detect hand sign letter using plotting
                            detectLetterPlot(measurements, alphaDictPoint)

        #Show image
        cv2.imshow("Image", img)
        cv2.waitKey(1)

    createMeasurementRange(measurementMatrix)
#if ran as a program, run main
if __name__ == "__main__":
    main()
