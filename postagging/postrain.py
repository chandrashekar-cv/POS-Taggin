import os,sys,random,copy,re
from _collections import defaultdict


def main():
    inputpath= sys.argv[1]
    outputpath = sys.argv[2]

    devPath=""
    if(len(sys.argv)>3 and sys.argv[3]=="-h"):
        if(len(sys.argv)==5):
            devPath=sys.argv[4]

    counter = 0
    
    features =  defaultdict()
    scoresum = defaultdict()
    
    with open(inputpath,'r',encoding = "ISO-8859-1") as inputPointer:
        lines = inputPointer.readlines()
        
        clData = lines[0].strip()
        clData = clData.split(" ")


        #load all the class names (POS tags) found in training data.
        for cl in clData:
            if not(cl in features.keys()):
                    weights= defaultdict(float)
                    
                    features[cl] =weights
        
        lines = lines[1:]
        
        while(counter < 20):
        #multiple interation to improve efficiency
            counter+=1
            random.shuffle(lines)
            for line in lines:
            #for each training data entry. 
                line = line.strip()
                data = line.split(" ")
                
                classname = data[0] #actual class name
                
                data=data[1:]
                
                for ft in data:
                    if not(ft in (features[classname]).keys()):
                        addNewFeatureData(ft,features) 
                        #add new feature to all classes with weight 0 to that vector.
                
                
                #calculate score for each class (POS tag)
                scores = defaultdict()
                for key in features.keys():
                    score = calculateScore(data,features[key])
                    scores[key] = score



                predClass = max(scores.keys(), key=(lambda key: scores[key] ))

                #get the name of the class with the max score as the predicted class.
                #it might happen that scores might be same for 2 or more classes, but 
                #over the course of many iterations the scores get updated to give a fairly 
                #accurate prediction. Number of iterations can be reduced.
                
                if not(classname==predClass):
                #if predicted class is not the same as class name in training data.
                #reduce the weights in weightVector if the predicted class and increase the
                #weights in the actual class.
                
                    manipulatescore(data,features[predClass],-1)
                    manipulatescore(data,features[classname],+1)
            
            if(counter==1):
                for key in features.keys():
                    scoresum[key] = copy.deepcopy(features[key])
            else:
                addscores(scoresum,features)
            
            if not(devPath==""):
                calculate_accuracy(features,counter,devPath)
            
        #calculate average weights for features - Avgperceptron
        for key in scoresum.keys():
            for ft in scoresum[key].keys():
                (scoresum[key])[ft] = (scoresum[key])[ft] / (counter * len(lines))         

        if not(devPath == ""):
            calculate_accuracy(scoresum," average perceptron ",devPath)
        
        with open(outputpath,"w", encoding = "ISO-8859-1") as outputHandler:
            outdata=""
            for key in scoresum.keys():
                outdata+=key+" "
                for ft in (scoresum[key]).keys():
                    outdata+=ft+"=|"+str((scoresum[key])[ft])+" "
                outdata+=os.linesep
            outputHandler.write(outdata)

def calculate_accuracy(features,counter,devPath):

    total =0
    with open(devPath,"r", encoding = "ISO-8859-1") as devHandler:
        lines = devHandler.readlines()

        accuracy=0.0
        for line in lines:
            line = line.strip()

            line = " ".join(line.split())

            data = line.split(" ")
            length = len(data)

            bos = "*BOS*"
            eos = "*EOS*"

            prev = bos
            prev2= bos

            i=0

            total+=length
            while(i<length):

                word = data[i]

                #actual classname
                classname = word.rsplit("/",1)[1]


                crnt =  word.rsplit("/",1)[0]

                if(i==length-1):
                    next =eos
                else:
                    next = data[i+1].rsplit("/",1)[0]

                wshape = wordshape(crnt)
                suf = suffixes(crnt)

                ftarray = ["crnt|"+crnt, "prev|"+prev, "2prev|"+prev2, "next|"+next, "wshape|"+wshape, "suffix|"+suf]


                scores = defaultdict()
                for key in features.keys():
                    score = calculateScore(ftarray,features[key])
                    scores[key]=score

                predClass = max(scores.keys(), key=(lambda key: scores[key] ))

                if(classname==predClass):
                    accuracy+=1.0

                if(next == eos):
                    prev2 = bos
                    prev= bos
                else:
                    prev2 = prev
                    prev = predClass
                i+=1
                
    print("accuracy for iteration "+str(counter)+" = "+str((accuracy/total)*100))


def addscores(scoresum,features):
    for key in scoresum.keys():
        for ft in (scoresum[key]).keys():
            (scoresum[key])[ft] += (features[key])[ft]

def manipulatescore(data,weightVector,val):          
    for ft in data:
        weightVector[ft] +=val

def calculateScore(data,weightVector):
    score = 0.0
    for ft in data:
        if(ft in weightVector.keys()):
            score+=weightVector[ft]
    return score

def addNewFeatureData(ft,features):
    for key in features.keys():
        weightVector = features[key]
        if not(ft in weightVector.keys()):
            weightVector[ft] = 0.0

def wordshape(word):
    wshape = word
    wshape = re.sub("[A-Z]+","A",wshape)
    wshape = re.sub("[a-z]+","a",wshape)
    wshape = re.sub("[0-9]+","0",wshape)
    wshape = re.sub("[^A-Za-z0-9]+","_",wshape)
    return wshape

def suffixes(word):
    suf=""
    if(len(word)>3):
        suf = word[len(word)-3:]
    else:
        suf = "*N*"
    return suf



#calling main function
main()   
        
        
        
