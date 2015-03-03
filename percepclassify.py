import sys,re, os, io
from _collections import defaultdict


def loadModelfile():
    modelfile = sys.argv[1]
    features = defaultdict()

    #load model file into features
    with open(modelfile,"r", encoding = "ISO-8859-1") as devHandler:
        model = devHandler.readlines()
        for cldata in model:
            cldata = cldata.strip()
            cldata = cldata.split(" ")
            clname = cldata[0]
            cldata = cldata[1:]
            weights = defaultdict(float)
            features[clname] = weights
            for ft in cldata:
                ft = ft.split("==")
                weights[ft[0]] = ft[1]

        input_stream = io.TextIOWrapper(sys.stdin.buffer,encoding = "ISO-8859-1")
        calculate_accuracy(input_stream,features)
        sys.stdout.flush()

def calculate_accuracy(lines,features):
    for line in lines:
        line = line.strip()
        line = " ".join(line.split())

        data = line.split(" ")
        bos = "*BOS*"
        eos = "*EOS*"


        if(len(sys.argv)>2):
            data=data[1:]

        scores = defaultdict()



        for key in features.keys():
            i=0
            score=0
            prev = bos
            prev2= bos

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
            scores[score]=key
        predClass = max(scores.keys(), key=(lambda key: scores[key] ))
        sys.stdout.write(predClass+os.linesep)
        sys.stdout.flush()

def calculateScore(data,weightVector):
    score = 0.0
    for ft in data:
        if(ft in weightVector.keys()):
            score+=weightVector[ft]
    return score

def wordshape(word):
    wshape = word
    wshape = re.sub("[A-Z]+","A",wshape)
    wshape = re.sub("[a-z]+","a",wshape)
    wshape = re.sub("[0-9]+","0",wshape)
    wshape = re.sub("[^A-Za-z0-9]+","_",wshape)
    return wshape


loadModelfile()