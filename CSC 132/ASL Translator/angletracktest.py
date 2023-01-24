import OpenCVtest3 as ASLDetector
from keyboard import is_pressed as pressed


outputMatrix = []
detector = ASLDetector.ComparisonDetector()
detector.measurementPairs = []
matrix = []
detector.calibrate()
while not pressed("space"):
    detector.videoFeed.update()
    detector.findAngle()
    if pressed("r"):
        matrix.append(detector.getMeasurements())
print(detector.createMeasurementRange(matrix))
