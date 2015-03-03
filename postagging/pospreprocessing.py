import os,sys,re




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
        length = len(linedata)

        prevpos = bol
        prev2pos = bol

        i=0
        while(i<length):

            word = (linedata[i]).rsplit("/",1)
            classname = word[1]


            if(i==length-1):
                next = eol
            else:
                next= (linedata[i+1]).rsplit("/",1)[0]

            if not(word[1] in clData):
                clData.append(word[1])

            wshape = wordshape(word[0])
            suf = suffixes(word[0])

            outputData+=classname+" crnt|"+word[0]+" prev|"+prevpos+" 2prev|"+prev2pos+" next|"+next+\
                        " wshape|"+wshape+" suffix|"+suf+os.linesep

            prev2pos = prevpos
            prevpos = classname

            i+=1

with open(outputPath,'w',encoding = "ISO-8859-1") as outFilepointer:
    outFilepointer.write(" ".join(clData)+os.linesep+outputData)

