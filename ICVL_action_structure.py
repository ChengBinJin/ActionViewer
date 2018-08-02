import cv2


# noinspection PyPep8Naming
def int2stringLabel(gt):
    postureLayer = {
        "0": "Sitting",
        "1": "Standing",
        "2": "Lying",
        "3": "Bending"
    }
                      
    locomotionLayer = {
        "0": "Stationary",
        "1": "Walking",
        "2": "Running",
        "3": "Bicycling"
    }
                       
    gestureLayer = {
        "0": "Nothing",
        "1": "Texting",
        "2": "Smoking",
        "3": "Phoning",
        "9": "Others"}
    
    interactionLayer = {
        "0": "Nothing",
        "1": "Littering",
        "2": "Falling"}
                  
    firstLabel = ""
    secondLabel = ""
    thirdLabel = ""
    fourthLabel = ""
    
    try:
        firstLabel = postureLayer[str(gt[7])]
    except KeyError:
        print("There are wrong lable in the posture layer!")
    
    try:
        secondLabel = locomotionLayer[str(gt[8])]
    except KeyError:
        print("There are wrong label in the locomotion layer!")
    
    try:
        thirdLabel = gestureLayer[str(gt[9])]
    except KeyError:
        print("There are wrong label in the gesture layer!")

    try:
        fourthLabel = interactionLayer[str(gt[10])]
    except KeyError:
        print("There are wrong label in the interaction layer!")
        
    return [firstLabel, secondLabel, thirdLabel, fourthLabel]


# noinspection PyPep8Naming
def readIcon():
    SIZE = 64
    
    sittingImg = cv2.imread("./Icon/Sitting.bmp")
    sittingImg = cv2.resize(sittingImg, (SIZE, SIZE))
    
    standingImg = cv2.imread("./Icon/Standing.bmp")
    standingImg = cv2.resize(standingImg, (SIZE, SIZE))
    
    lyingImg = cv2. imread("./Icon/Lying.bmp")
    lyingImg = cv2.resize(lyingImg, (SIZE, SIZE))

    bendingImg = cv2.imread("./Icon/Bending.bmp")
    bendingImg = cv2.resize(bendingImg, (SIZE, SIZE))
    
    stationaryImg = cv2.imread("./Icon/Stationary.bmp")
    stationaryImg = cv2.resize(stationaryImg, (SIZE, SIZE))
    
    walkingImg = cv2.imread("./Icon/Walking.bmp")
    walkingImg = cv2.resize(walkingImg, (SIZE, SIZE))
    
    runningImg = cv2.imread("./Icon/Running.bmp")
    runningImg = cv2.resize(runningImg, (SIZE, SIZE))
    
    bicyclingImg = cv2.imread("./Icon/Bicycling.bmp")
    bicyclingImg = cv2.resize(bicyclingImg, (SIZE, SIZE))
    
    fallingImg = cv2.imread("./Icon/Falling.bmp")
    fallingImg = cv2.resize(fallingImg, (SIZE, SIZE))
    
    nothingImg = cv2.imread("./Icon/Nothing.bmp")
    nothingImg = cv2.resize(nothingImg, (SIZE, SIZE))
    
    textingImg = cv2.imread("./Icon/Texting.bmp")
    textingImg = cv2.resize(textingImg, (SIZE, SIZE))
    
    smokingImg = cv2.imread("./Icon/Smoking.bmp")
    smokingImg = cv2.resize(smokingImg, (SIZE, SIZE))
    
    phoningImg = cv2.imread("./Icon/Phoning.bmp")
    phoningImg = cv2.resize(phoningImg, (SIZE, SIZE))
    
    othersImg = cv2.imread("./Icon/Others.bmp")
    othersImg = cv2.resize(othersImg, (SIZE, SIZE))
    
    litteringImg = cv2.imread("./Icon/Littering.bmp")
    litteringImg = cv2.resize(litteringImg, (SIZE, SIZE))
    
    return {"Sitting": sittingImg,
            "Standing": standingImg,
            "Lying": lyingImg,
            "Bending": bendingImg,
            "Stationary": stationaryImg,
            "Walking": walkingImg,
            "Running": runningImg,
            "Bicycling": bicyclingImg,
            "Falling": fallingImg,
            "Nothing": nothingImg,
            "Texting": textingImg,
            "Smoking": smokingImg,
            "Phoning": phoningImg,
            "Others": othersImg,
            "Littering": litteringImg
            }
