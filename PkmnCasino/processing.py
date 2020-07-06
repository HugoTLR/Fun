from cv2 import calcHist,convertScaleAbs

def auto_constrast(gray):
    histSize = 256
    #alpha,beta
    #minGray = 0, maxGray = 0
    clipHistPercent = 1

    hist = calcHist([gray],[0],None,[256],[0,256])
    
    accumulator = []
    accumulator.append(hist[0])

    for i in range(1,256):
        accumulator.append(accumulator[i-1] + hist[i])
        #print(accumulator[i])

    maxVal = accumulator[-1]
    clipHistPercent = clipHistPercent * (maxVal / 100.0)
    clipHistPercent = clipHistPercent / 2.0

    minGray = 0
    while accumulator[minGray] < clipHistPercent:
        minGray = minGray + 1

    maxGray = 255

    while accumulator[maxGray] >= (maxVal - clipHistPercent):
        maxGray = maxGray - 1


    inputRange = maxGray - minGray
    alpha = 255 / inputRange
    beta = -minGray *alpha
    #print("Alpha: {}\tBeta: {}".format(alpha,beta))
    adjusted = convertScaleAbs(gray,alpha=alpha,beta=beta)
    return adjusted