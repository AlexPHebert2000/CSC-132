#Dictionary Generator
import OpenCVtest3 as M
from keyboard import is_pressed as pressed


outputMatrix = []
detector = M.ComparisonDetector()

detector.calibrate()
    

for letter in detector.dictionary:
    print(f"Make {letter} then press space")
    while not pressed("space"):
        detector.videoFeed.update()
    measurementTEMP = []
    print("HOLD")
    while len(measurementTEMP) < 20:
        detector.videoFeed.update()
        detector.getMeasurements()
        measurementTEMP.append(detector.measurements)
        print(".")
    outputMatrix.append(f"{letter} : {detector.createMeasurementRange(measurementTEMP, pairs = True)},")

for entry in outputMatrix:
    print(entry)