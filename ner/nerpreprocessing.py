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
        prevclass=bol
        prev2class=bol

        i=0
        while(i<length):

            word = linedata[i]

            pos = word.rfind("/")
            classname = word[pos+1:]
            word = word[:pos]
            pos = word.rfind("/")
            postag = word[pos+1:]
            crnt = word[:pos]


            if(i==length-1):
                nextword= eol
                nextpos = eol
            else:
                nextdata = linedata[i+1]
                rpos = nextdata.rfind("/")
                nextdata = nextdata[:rpos]
                rpos = nextdata.rfind("/")
                nextpos = nextdata[rpos+1:]
                nextword = nextdata[:rpos]

            if not(classname in clData):
                clData.append(classname)



            wshape = wordshape(crnt)
            nextshape = wordshape(nextword)
            suffix = suffixes(crnt)

            outputData += classname
            outputData += " crnt|"+crnt
            outputData += " crntpos|"+postag
            outputData += " prevpos|"+prevpos
            outputData += " prevcls|"+prevclass
            outputData += " prev2pos|"+prev2pos
            outputData += " prev2cls|"+prev2class
            outputData += " next|"+nextword
            outputData += " nextpos|"+nextpos
            outputData += " wshape|"+wshape
            outputData += " suffix|"+suffix
            outputData += os.linesep


            prev2pos = prevpos
            prevpos = postag
            prev2class = prevclass
            prevclass = classname

            i+=1

with open(outputPath,'w',encoding = "ISO-8859-1") as outFilepointer:
    outFilepointer.write(" ".join(clData)+os.linesep+outputData)

