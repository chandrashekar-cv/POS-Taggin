import os,sys,random,copy,re
from _collections import defaultdict


def main():
    inputpath= sys.argv[1]
    outputpath = sys.argv[2]
    devpath=""
    if(len(sys.argv)>3):
        devpath=sys.argv[3]

        with open(devpath,'r',encoding = "ISO-8859-1") as devPointer:
            devlines = devPointer.readlines()
            #print(len(devlines))

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
                scores = defaultdict(list)
                for key in features.keys():
                    score = calculateScore(data,features[key])
                    scores[score].append(key)

                predClass = scores[max(scores.keys())][0]
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

            if not(devpath==""):
                calculate_accuracy(devlines,features,counter)

        #calculate average weights for features - Avgperceptron
        for key in scoresum.keys():
            for ft in scoresum[key].keys():
                (scoresum[key])[ft] = (scoresum[key])[ft] / (counter * len(lines))


        with open(outputpath,"w", encoding = "ISO-8859-1") as outputHandler:
            outdata=""
            for key in scoresum.keys():
                outdata+=key+" "
                for ft in (scoresum[key]).keys():
                    outdata+=ft+"=|"+str((scoresum[key]).get(ft))+" "
                outdata+=os.linesep
            outputHandler.write(outdata)
        if not(devpath==""):
            calculate_accuracy(devlines,scoresum,"Average perceptron")


def calculate_accuracy(devlines,features,counter):
    length = len(devlines)

    accuracy=0.0
    for line in devlines:
        line = line.strip()
        line = " ".join(line.split())

        data = line.split(" ")
        bos = "*BOS*"
        eos = "*EOS*"

        classname = data[0]
        data = data[1:]

        scores = defaultdict()

        for key in features.keys():
            prev = bos
            prev2= bos

            i=0
            score = 0
            while(i<len(data)):

                word = data[i]
                wshape = wordshape(word)

                crnt = "crnt|"+ word

                if(crnt=="crnt|." or i==len(data)-1):
                    next =eos
                else:
                    next = "next|"+ data[i+1]

                ftarray = [crnt,"prev|"+prev, "2prev|"+prev2, next,"wshape|"+wshape]

                score += calculateScore(ftarray,features[key])

                if(next == eos):
                    prev2 = bos
                    prev= bos
                else:
                    prev2 = prev
                    prev = crnt
                i+=1
            #end of while loop interating through all the words of sentence and calculating the score

            scores[score]=key
        #end of for loop iterating through all the feature classes to find the score
        predClass = max(scores.keys(), key=(lambda key: scores[key] ))

        if(classname==predClass):
            accuracy+=1.0
    #        print(classname+" "+predClass)

    #End of for loop iterating through all the lines (dev examples)
    print("Iteration" +str(counter)+" accuracy = "+str(accuracy)+" / "+str(length))


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

#calling main function
main()



