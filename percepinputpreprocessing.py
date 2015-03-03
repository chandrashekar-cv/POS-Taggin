import os,sys,re



def wordshape(word):
    wshape = word
    wshape = re.sub("[A-Z]+","A",wshape)
    wshape = re.sub("[a-z]+","a",wshape)
    wshape = re.sub("[0-9]+","0",wshape)
    wshape = re.sub("[^A-Za-z0-9]+","_",wshape)
    return wshape


inputPath = sys.argv[1]
outputPath = sys.argv[2]
outputData = ""
bol="*BOS*"
eol="*EOS*"
clData=[]
with open(inputPath,'r',encoding = "ISO-8859-1") as inputPointer:
    lines = inputPointer.readlines()
    for line in lines:

        line = line.strip()
        line = " ".join(line.split())
        linedata = line.split(" ")


        prevpos = bol
        prev2pos = bol
        classname = linedata[0]
        linedata = linedata[1:]
        length = len(linedata)
        if not(classname in clData):
            clData.append(classname)
        i=0
        while(i<length):

            word = linedata[i]

            if(word=="." or i==length-1):
                next = eol
            else:
                next= linedata[i+1]

            wshape = wordshape(word)

            outputData+=classname+" crnt|"+word+" prev|"+prevpos+" 2prev|"+prev2pos+" next|"+next+" wshape|"+wshape+os.linesep

            if(next==eol):
                prevpos=bol
                prev2pos=bol
            else:
                prev2pos = prevpos
                prevpos = word

            i+=1

with open(outputPath,'w',encoding = "ISO-8859-1") as outFilepointer:
    outFilepointer.write(" ".join(clData)+os.linesep+outputData)



