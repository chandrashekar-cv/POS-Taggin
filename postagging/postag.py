import sys,re, os, io
from _collections import defaultdict


def loadModelfile():
    modelfile = sys.argv[1]
    features = defaultdict()

    #load model file into features
    with open(modelfile,"r", encoding = "ISO-8859-1") as modelhandler:
        model = modelhandler.readlines()
        for cldata in model:
            cldata = cldata.strip()
            cldata = cldata.split(" ")
            clname = cldata[0]
            cldata = cldata[1:]
            weights = defaultdict(float)
            for ft in cldata:
                ft = ft.split("=|")
                weights[ft[0]] = float(ft[1])
            features[clname] = weights




    input_stream = io.TextIOWrapper(sys.stdin.buffer,encoding = "ISO-8859-1")
    calculate_accuracy(input_stream,features)


def calculate_accuracy(lines,features):

    for line in lines:
        output=""
        line = line.strip()

        line = " ".join(line.split())

        data = line.split(" ")
        length = len(data)

        bos = "*BOS*"
        eos = "*EOS*"

        prev = bos
        prev2= bos

        i=0
        while(i<length):

            crnt = data[i]

            if(i==length-1):
                next =eos
            else:
                next = data[i+1]

            wshape = wordshape(crnt)

            ftarray = ["crnt|"+crnt, "prev|"+prev, "2prev|"+prev2, "next|"+next, "wshape|"+wshape]


            scores = defaultdict()
            for key in features.keys():
                score = calculateScore(ftarray,features[key])
                scores[key]=score

            predClass = max(scores.keys(), key=(lambda key: scores[key] ))

            prev2 = prev
            prev = predClass
            i+=1
            output+=crnt+"/"+predClass+" "
        output=output.strip() + os.linesep
        sys.stdout.write(output)
        sys.stdout.flush()

def wordshape(word):
    wshape = word
    wshape = re.sub("[A-Z]+","A",wshape)
    wshape = re.sub("[a-z]+","a",wshape)
    wshape = re.sub("[0-9]+","0",wshape)
    wshape = re.sub("[^A-Za-z0-9]+","_",wshape)
    return wshape

def calculateScore(data,weightVector):
    score = 0.0
    for ft in data:
        if(ft in weightVector.keys()):
            score+=weightVector[ft]
    return score


loadModelfile()
