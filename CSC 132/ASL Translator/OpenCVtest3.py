#Import modules and libraries
from cvzone.HandTrackingModule import HandDetector
import cv2 
from keyboard import is_pressed as pressed
import numpy as np
from time import monotonic
import abc

#Video Class that initializes a OpenCV video feed and updates it
class Video():
    def __init__(self, name = "Image"):
        #connect to default camera
        self.capture = cv2.VideoCapture(0)
        #capture name (Deault = "Image")
        self.name = name
        #Grab frame
        self.update()

    #function that updates frame from video feed and displays
    def update(self):
        #Grab frame
        self.success, self.img = self.capture.read()
    
    def display(self):
        #display frame
        cv2.imshow(self.name, self.img)
        cv2.waitKey(1)      

#American Sign Language Detector Superclass
#Includes functions to calibrate, get measurements, and calculate other values based on video feed 
class ASLDetector(metaclass = abc.ABCMeta):
    
    #Initilization, passes a default generic videofeed
    #Initializes other varibles
    def __init__(self, videoFeed = Video()):
        self.handDetector = HandDetector(detectionCon=0.8, maxHands=1)
        self.measurements = []
        self.delayTimerEndTime = 0
        self.DEBUG = True
        self.anglearray = []
        self.videoFeed = videoFeed
        self.measurementPairs = [
            
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
        self.distanceFromCamera = 1
        self.width = 46
        self.focalLength = 1
    
    #Function that detects the right hand from video feed
    def findHands(self, d = False):
        self.hands = self.handDetector.findHands(self.videoFeed.img, draw=d) 
        if self.hands:
            if self.hands[0]["type"] == "Right":
                self.hand = self.hands[0]
            else:
                self.hand = None
        else:
            self.hand = None

    #Function to calibrate the focal length of the camera in order to find distance between hand and camera
    def calibrate(self):
        
        #initialize calibration list and actual value
        calibrationMatrix = []
        actual = 0
        
        #print instructions for user
        print("Hold your right hand near your chest, palm facing the camera with fingers outstreched and touching")
        print("Please hold position for approximately 1 second")
        print("Press space when ready")
        
        #Wait for user to press Space
        while not pressed("space"):
            self.videoFeed.update()
        
        #Print hold and dots while 20 measurements are being taken
        #measurement is between base of hand and base of thumb
        print("Hold")
        while len(calibrationMatrix) < 20:
            self.videoFeed.update
            #calibrationMatrix.append((self.handDetector.findDistance(self.hand["lmList"][0], self.hand["lmList"][1]), self.handDetector.findDistance(self.hand["lmList"][0],self.hand["center"])))
            self.findHands()
            if self.hands:
                calibrationMatrix.append(self.handDetector.findDistance(self.hand["lmList"][0], self.hand["lmList"][1]))
            print(".")
        
        #Notify user when done
        print ("DONE")
        
        #Average the measurements
        for horizontalMeasurement, info in calibrationMatrix:
            horizontalAverage = actual
            actual = ((horizontalAverage + horizontalMeasurement)/2)
        
        #calculate focal length
        self.focalLength = (actual * self.distanceFromCamera)/self.width

    #Use distance formula (D = (known width * focal length) / measured width)
    def findDistanceFromCamera(self):
        measurement, info = self.handDetector.findDistance(self.hand["lmList"][0], self.hand["lmList"][1])
        self.distanceFromCamera = (self.width * self.focalLength)/measurement

    #Get measurement set defined by measurement pairs in __init__ and angle of hand
    def getMeasurements(self):

        self.findHands()
        self.measurements = []
        if self.hand:
            for index, pair in enumerate(self.measurementPairs):
                x, y = pair
                measurement, info = self.handDetector.findDistance(self.hand["lmList"][x], self.hand["lmList"][y])
                self.findDistanceFromCamera()
                self.measurements.append(measurement * self.distanceFromCamera)

            if len(self.anglearray) < 20:
                self.anglearray.append(self.findAngle())
            else:
                self.anglearray.pop(0)
                self.anglearray.append(self.findAngle())
                
            self.measurements.append(self.findAngle())
            return self.measurements
    
    #find angle between vertical line and line drawn between base of hand and base of middle finger  
    def findAngle(self):
        #unpack base and middle finger landmarks
        baseX, baseY, z = self.hand['lmList'][0] #base of hand coodinates
        middleFingerX, middleFingerY, z = self.hand["lmList"][9] #base of middle finger coodinates
        
        #define vertical line
        vertical = (baseX, 0)
        
        #create vectors
        baseToPalm = np.array([middleFingerX, middleFingerY]) - np.array([baseX, baseY])
        baseToTop = np.array(vertical) - np.array([baseX, baseY])
             
        #calculate angle
        self.angle = np.degrees(np.math.atan2(np.linalg.det([baseToPalm, baseToTop]), np.dot(baseToPalm, baseToTop)))
        return self.angle
    
    #Set input timer end time by adding a delay to the current time reading
    def startInputTimer(self, delayTime = 1.0):
        self.delayTimerEndTime = monotonic() + delayTime
    
    #check if current time is greater than the generated time by startInpuDelayTimer: return False if greater
    def inputTimer(self):
        if monotonic() > self.delayTimerEndTime:
            return False
        else:
            return True
    
    #Function that takes in a matrix and creates a list of pairs or averages from the matrix 
    def createMeasurementRange(self, matrix, pairs = True):
        outputList = []
        
        for i in range(len(matrix[0])):
            x = matrix[0][i]
            y = matrix[1][i]
            
            if x > y:
                val = (x,y)
            else:
                val = (y,x)
            outputList.append(val)
            
        for measurementSet in matrix:
            for index, measurement in enumerate(measurementSet):
                min, max = outputList[index]
                if measurement> max:
                    max = measurement
                elif measurement < min:
                    min = measurement
                outputList[index] = (min,max)
                
        if self.DEBUG:
            for min, max in outputList:
                print(f"max:{max}\tmin{min}\trange:{max-min}")
                
            print(outputList)
        
        if pairs:
            return outputList
        else:
            return [(min+max)/2 for min, max in outputList]
    
    #method to be defined by the detection method
    @abc.abstractmethod
    def detectLetter(self):
        raise NotImplementedError("Not Supported")

#ASL detector that uses a dictionary of measurement ranges to detect letter
#Reads measurements and checks if each value falls between range for each measurement range for each letter
class ComparisonDetector(ASLDetector):
    def __init__(self):
        super().__init__()
        self.dictionary = {
                    "A" : [(48.33572535931633, 72.1527767966223), (19.23222436947584, 27.400115637890664), (20.24103623156961, 25.084424328550067), (17.716875543422436, 26.096569353842614), (135.52995107460407, 159.88524933113874), (85.08344459470437, 89.82872406316697), (71.68744187781107, 76.66642468171716), (62.84163120397823, 69.09554878595311), (70.20644818554202, 76.51028421403441), (63.87910321282352, 90.57648464651405), (81.05820521380075, 111.79694160124535), (94.3847003949833, 128.19910266749878), (-17.771320822908752, -15.255118703057787)],
                    "B" : [(146.92075048200178, 162.12882571550685), (24.53871153859172, 32.50101744646942), (25.72158575104016, 28.380114711252457), (31.73689785675333, 43.11699231218389), (69.85058683614652, 95.69819314343444), (221.9007597843073, 244.6994632757363), (228.19777373909017, 259.75820257811387), (223.9560832447865, 245.34219589852685), (191.70191828277353, 218.71097818320106), (158.41612513196486, 171.57302705670355), (142.44191648501925, 156.48734619934987), (119.50394080232401, 125.18630972283056), (-18.43494882292202, -14.500166766552564)],    
                    "C" : [(33.49810351502698, 36.71864460827378), (2.935591585347991, 5.189441791984329), (3.113665075190598, 5.589199861373405), (7.8275714589470615, 9.791419190297233), (130.16278578670148, 138.76921124736214), (150.66022405909044, 159.8628669006658), (148.93891500647055, 156.1701594640708), (145.12524454807163, 154.4624750675807), (138.49382110936497, 146.80308006244667), (33.040608524403176, 37.45683817893415), (34.42534795879357, 39.10882530926666), (37.60823948316257, 42.04825527158643), (-9.19665589162891, -5.04245106917091)],
                    "D" : [(156.79215774126286, 175.9734158684031), (134.10145102478643, 151.48026837760372), (26.655847880984574, 29.75533110387032), (21.588613722717668, 24.92700395588074), (113.28541289457839, 128.97240885362044), (267.7828913746357, 299.7748490658276), (134.2587394585101, 150.54132464318516), (121.98675151584237, 137.92664025232332), (123.39870711677263, 138.37322147109361), (21.4453453647957, 25.501595177523477), (31.333679872954836, 38.366977695387426), (52.79787604050321, 59.31025836776032), (-15.642246457208735, -14.574216198038735)],   
                    "E" : [(69.09152169878733, 74.7933007958651), (20.731180442633008, 24.120114754491496), (20.826643021695006, 24.96176583686186), (20.37732514786834, 25.211555882526728), (91.43439528838401, 99.97582007180237), (113.91820598517354, 120.1559818584818), (110.02322039286969, 117.45115986477127), (105.87704921539304, 113.38194774349822), (97.2316659794301, 105.08801703879377), (48.171997897273656, 53.756591732258755), (26.894760299796307, 33.95788190818141), (4.673733194674399, 14.636588346941375), (-18.434948822922014, -16.699244233993642)],     
                    "F" : [(30.168398010786994, 36.461029066114385), (148.80831511427047, 181.14517707854608), (61.220793473593865, 66.01259547670092), (76.65492385538822, 88.55109114451051), (136.52812220611096, 144.25463754751232), (164.61908473068974, 176.34207566326953), (294.98417686636657, 327.31265787943835), (278.8291597595957, 305.32199254941196), (237.75992536205138, 261.0543058075561), (181.57057285426137, 212.60250652106927), (189.97331626584892, 216.01088890619252), (189.21379971641787, 215.73325470300347), (-15.945395900922849, -15.300845572449985)],
                    "G" : [(23.45816131854543, 26.083292983285766), (76.31036566494696, 79.49467421352567), (15.811357828741425, 19.07759141623674), (14.566431944401785, 16.124484421030115), (131.57893157672987, 136.71721745907195), (152.88635574755568, 158.56724772349187), (77.91093830714723, 82.95273495566926), (61.62407278158385, 66.10986428373708), (48.480830649960474, 52.66677311715534), (56.93514990036309, 59.78213333353313), (70.23657547000616, 74.23787116882437), (82.13962716246168, 86.27441887585131), (-17.671050361992005, -15.124007308310576)],        
                    "H" : [(65.14407150901697, 75.55431873354401), (25.81310777168469, 28.9289170693955), (111.35979474751797, 119.20547482528852), (16.14433972275355, 19.324219276382024), (129.411348984358, 135.1556741455122), (195.8923509430534, 208.72425666473808), (206.76209530811576, 218.06482108344642), (95.38490924204912, 101.27881133003885), (84.21409805913113, 90.16008004049743), (82.44595107274597, 91.0941516054897), (32.140220459339474, 38.44938947721465), (47.378849633798104, 56.09816948577192), (-37.933270283598915, -33.11134196037205)],
                    "I" : [(29.84048346775511, 39.23889045332213), (16.064423726003, 27.400541713837182), (36.063124828380275, 46.8936397224304), (122.59857771402568, 157.21031073836147), (115.11203196599966, 138.43479538826693), (101.88286544731416, 122.91934772693959), (104.67842297207025, 129.73738897183415), (76.9344079894182, 90.58328176938035), (193.75143324048008, 239.92704914324324), (10.712851284419894, 14.693755818459584), (41.14313732486183, 52.15871768927946), (104.89178514808404, 130.95807807446752), (-18.799885158652643, -16.975499467929733)],     
                    "K" : [(75.81383194894212, 88.81616203765158), (89.04370763537061, 99.4779575477738), (156.2543925046318, 169.98800837294354), (21.64071202847797, 23.743257390718984), (140.8013409762514, 153.4744180087881), (213.31247133627687, 235.1983278013734), (219.59612443836298, 238.34948082953272), (62.75876509585744, 68.61625688595666), (59.302593162125966, 63.71181574167483), (88.66107638691489, 96.4203515444817), (78.89094001794676, 86.56771796062195), (92.75773244091005, 103.04042187686655), (-0.6030911943805327, 1.2319774026397279)],
                    "L" : [(138.6383504355192, 157.38424301883757), (151.3424835654466, 173.83581350923973), (24.405880831684396, 27.090343797830887), (22.403545114129386, 25.98159251675303), (163.67045333407432, 177.91338373414885), (217.63947416232392, 240.31724595398282), (65.88187631040248, 70.29815066154246), (53.60014204831305, 57.58585771656561), (56.75343133704248, 61.70908738556869), (110.76984363262936, 125.04119005941826), (135.28503019339786, 150.5584947455246), (157.343592768519, 175.72467676234507), (0.0, 2.436648246810132)],
                    "M" : [(74.4072824285767, 85.0410026084277), (15.932051484181695, 18.36745799096776), (22.403545114129386, 25.607915615269686), (33.95847597622468, 42.835083901080054), (114.62139680680404, 124.32520610645166), (84.79179298806471, 92.54419376086395), (75.02182098674317, 82.93044691205382), (78.3475059091081, 85.24821542994809), (49.79709174099396, 58.61533420561116), (61.67899849770127, 72.38412745039886), (42.073599932538905, 49.274946789088055), (61.06882774344245, 72.60215299603686), (-18.904575842611642, -16.348171547351246)],
                    "N" : [(68.31204076916292, 74.48392563071167), (14.537671590761757, 17.5015713333019), (46.20645127238705, 50.7820288477009), (21.26025065210692, 23.679611719308536), (131.3776959337681, 140.12097635016713), (90.97444889468332, 96.5776273870648), (91.00189275161433, 95.95665388530115), (44.70401850336615, 49.142738446131354), (44.61334944789342, 48.37704969192665), (54.817963360245585, 61.21954528843833), (84.90343281879754, 92.84084309949661), (90.23829830144766, 97.03638765514114), (-15.321510074864799, -12.771242564901456)],
                    "O" : [(15.403752552771856, 19.659776798422033), (1.6094247095304164, 4.6922390298236145), (7.458589330763151, 8.66701730549587), (9.175132511769496, 11.198916055027412), (137.1815352648456, 146.63290705746243), (145.00717607794897, 153.663232384885), (142.91840228187652, 152.5322548948589), (138.90041325724744, 148.22245732801193), (131.15577103197617, 140.19370532444486), (16.929563546758484, 20.99695565622355), (22.785679450095433, 26.46778453274545), (28.510438435222667, 33.355825519682135), (0.0, 1.888188006740931)],
                    "P" : [(40.62764527297752, 44.03172003323524), (78.84711202631144, 84.34578132987876), (53.80871174991918, 60.22160916028986), (8.778658044155712, 10.686629983166064), (116.8650540150196, 122.40121455761864), (155.62337485721633, 161.910982881589), (100.31533428261766, 106.2366258840509), (46.13978605057356, 48.59718813537893), (36.67059636182521, 38.80079753574153), (64.7358840788501, 70.33283036473571), (75.19497728053643, 81.87878377820924), (83.11620879765277, 90.0583793331145), (3.1798301198642327, 5.815626529491238)],
                    "Q" : [(37.55527287619149, 50.932948881744224), (24.60432782078293, 96.46883491947004), (17.4000166883279, 25.245502349435842), (14.429965922003774, 23.727847048553958), (141.45603738765723, 158.02272492418825), (96.6363737102988, 192.10162617992506), (80.3363285531141, 98.32790981831849), (57.83413445059116, 74.10135280886928), (43.72181522084538, 55.226474737808594), (64.88438774298781, 75.37886709597849), (80.3421158650753, 93.42449970031402), (91.95580529638839, 105.90397136903906), (-62.949402992913896, -34.74318015830361)],
                    "R" : [(74.23602989678041, 82.87343219597558), (10.110238640558386, 24.232557391230635), (146.9931622227393, 157.76080465087483), (18.413609660691936, 22.001298211351465), (130.81993621804, 153.38436442348515), (203.60549102737244, 229.77460995707327), (213.39258118321948, 239.16123042610243), (66.63485209859375, 81.58542890231584), (55.08264260583354, 74.37034208810613), (77.932476264979, 89.25741810164304), (64.68895733259939, 71.81911818397288), (76.81087859402578, 84.55626391560774), (-31.879596847022746, -13.760785111791241)],
                    "U" : [(134.24174303113048, 179.01853509512486), (27.148396429191667, 31.52897646690817), (170.5375226848469, 203.6386704067198), (19.098621141278418, 33.29677119389729), (128.08297007851294, 138.79840757726936), (260.0325849878913, 310.85037079443316), (275.5854901490763, 315.88934398396805), (104.66460718808956, 112.93844493984291), (97.84464323683828, 108.9019012637705), (146.37383705041498, 180.15380587120552), (24.078392951630462, 29.386336676934818), (40.25895476153107, 46.19109357380216), (-11.888658039627968, -10.06906269888941)],    
                    "V" : [(147.15893473560524, 164.14776162590618), (64.58193726067151, 72.41447824599734), (154.9714622600704, 175.14054879670493), (19.161775780353338, 22.109953171009664), (110.23927846275838, 123.47663882101754), (246.65142876164174, 273.9829965020134), (252.5357727503403, 280.13473763503754), (98.00491303014495, 108.4029640996163), (90.20126592138345, 98.5167664538441), (142.6916358868225, 159.0983083375983), (12.303067272558598, 17.45501795932135), (26.199044396336237, 32.72477509312457), (-12.355359865083528, -10.587321318237132)],       
                    "W" : [(180.18428965366164, 197.09413439633684), (61.022964206205536, 69.49130316600444), (49.253042639436245, 57.565574732186086), (157.11696188562246, 168.47282557149498), (124.2658492516003, 133.80787676177917), (280.9512974951682, 301.4535614796457), (287.7479866616621, 307.4808540088645), (271.5824550585058, 290.39121020559213), (114.70482076933449, 126.29734168787431), (170.3012930447592, 183.75708827182262), (147.85539020432418, 159.4553605749226), (6.086792055245878, 11.9198140541451), (-8.94538183353896, -7.31901937559043)],
                    "X" : [(51.35444567814311, 57.35375761971527), (65.39003548013758, 69.12468467328303), (16.17211963388187, 19.58661614388814), (14.28062576994972, 17.671801432207467), (106.18770373203213, 113.88579530616232), (149.67467515872676, 156.7178137799328), (85.98621903847442, 91.57231044620215), (67.15900065927673, 75.05899202521191), (52.66799914240088, 58.77827261776591), (22.938397890460188, 25.795000498072362), (37.28755265573857, 40.63940233086473), (51.29889122353767, 56.07867582181027), (-1.5074357587749687, 0.0)],
                    "Y" : [(89.1877086685367, 97.0323171341075), (23.40760011589728, 30.221651240014022), (19.435523132136833, 22.481648350885948), (108.01565764310803, 127.49752803023213), (167.60272444980896, 183.3509596197819), (101.76567276330191, 111.84405472986154), (85.0410026084277, 90.73170690213055), (89.2960557933241, 93.94788048109082), (191.44464205568704, 213.66287472752887), (111.74091854405131, 125.17262118753702), (128.64036947134116, 144.27888375750464), (193.28432215437135, 219.06651942647903), (-2.489552921999156, -0.5846305207051781)]           
                        }
    
    def detectLetter(self):
        try:
            for letter in self.dictionary:
                for index, val in enumerate(self.measurements):
                    min, max = self.dictionary[letter][index]
                    
                    if val < (min) or val > (max):
                        break
                    
                    elif index == len(self.measurements) - 1:
                        if letter == "i":
                            changeInAngle = self.anglearray[-1] - self.anglearray[0]
                            self.anglearray=[]
                            if changeInAngle >= 30:
                                letter = "J"
                        print (letter)
                        self.startInputTimer(4)
                        raise StopIteration
        
        except StopIteration:
                return letter 

class TouchDetector(ASLDetector):
    def __init__(self):
        super().__init__()
        
        #[8-12][12-16][16-20][point 4 touches]
        self.dictionary ={
            0xE6 : "A", # 1 1 1 00110
            0xF5 : "B", # 1 1 1 10101
            0xE0 : "C", # 1 1 1 00000
            0x68 : "D", # 0 1 1 01000
            0xF4 : "E", # 1 1 1 10100
        }
    def detectLetter(self):
        pass

def main():
    #initialize the measurement storage matrix
    measurementMatrix = []
    
    #initalize the ASL Detector using the comparison detection method
    detector = ComparisonDetector()
    
    #Calibrate the detector
    detector.calibrate()
    
    #Run main loop until tab is pressed
    while not pressed("tab"):
        
        #get frame
        detector.videoFeed.update()
        
        #Get measurement list from new frame
        detector.getMeasurements()
        
        #Try to detect letter
        detector.detectLetter()
        
        #display
        detector.videoFeed.display()
        
        #If R is pressed record measuremnt to measurement storage
        if pressed("R"):
            measurementMatrix.append(detector.measurements)
            
    #Once main loop is exited if there are values stored, convert matrix into a range list and print
    list = detector.createMeasurementRange(measurementMatrix)
    print (list)
    
if __name__ == "__main__":
    main()