import sys
import argparse
from itertools import izip


class comparator:
    def __init__(self,output,ratioLoc,countLoc,CHH):
        # ratio loc is the column location of the methylation ratio, countLOC is the column location of the methylation count
        self.out = open(output,"w")
        self.start = -1
        self.end = -1
        self.chromosome = ""
        self.notDMR = False
        self.ratioLoc = ratioLoc
        self.countLoc = countLoc
        self.CHH=CHH
    def analyze(self,line1,line2):
        if(self.start != -1): # if there is a start region (continuous region)
            if(self.chromosome != line1[0]): # make sure the current region is on the same chromosome as the continuous region
                self.out.write(self.chromosome+ "\t" + str(self.start) + "\t" + str(self.end) + "\n") 
                self.start = -1
                self.end = -1
                self.notDMR=False # if it is on different chromosome, output the previous continuous region as dmr and check if the current region is a dmr
                if(self.isDMR(float(line1[self.ratioLoc]),float(line2[self.ratioLoc]),int(line1[self.countLoc]),int(line2[self.countLoc]))):
                    # check if the current region is dmr, if it is, then start a new continuous region
                    self.chromosome = line1[0]
                    self.start = int(line1[1])
                    self.end = int(line1[2])
                    self.notDMR = False
            else:
                if(self.isDMR(float(line1[self.ratioLoc]),float(line2[self.ratioLoc]),int(line1[self.countLoc]),int(line2[self.countLoc]))):
                    # if it is on a chromosome and the current region is a dmr, then append it to the continous region
                    self.end = int(line1[2])
                    self.notDMR = False
                elif(self.notDMR):
                    # if the current region is not dmr, and the previous region is also not dmr, then the region is discontinued 
                    self.out.write(self.chromosome + "\t" + str(self.start) + "\t" + str(self.end) + "\n")
                    self.start = -1
                    self.end = -1
                    self.notDMR = False
                else:
                    # if the current region isn't dmr and the previous region is, make note that the current region is not dmr
                    self.notDMR = True
        elif(self.isDMR(float(line1[self.ratioLoc]),float(line2[self.ratioLoc]),int(line1[self.countLoc]),int(line2[self.countLoc]))):
                # check if region is dmr, if it is, then start a new continuous region
                self.chromosome = line1[0]
                self.start = int(line1[1])
                self.end = int(line1[2])
                self.notDMR = False

    def theEnd(self):
        # this function will output any continuous region just in case there is one at the end of the file
        if(self.start != -1):
            self.out.write(self.chromosome + "\t" + str(self.start) + "\t" + str(self.end) + "\n")
        self.out.close()
    def isDMR(self,ratio1,ratio2,count1,count2):
        # check if a region is dmr given the ratio and count
        ## criteria is different for different methylations 
        if(self.CHH):
            return (count1>=6 and count2>= 6) and ((ratio1 < 0.05 and ratio2> 0.25) or (ratio1>0.25 and ratio2<0.05))
        return ((count1>=3 and count2>= 3) and (abs(ratio1 - ratio2) >= 0.6))
    
        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a',required = True,help="First file for comparison")
    parser.add_argument('-b',required = True,help="Second File for comparison")
    parser.add_argument('-o',required = True,help="The Output Name")
    args = parser.parse_args()
    inputFile1 = args.a
    inputFile2 = args.b
    outputFile = args.o
    content1 = open(inputFile1,"r")
    content2 = open(inputFile2,"r")
    next(content1)
    next(content2)
    CG = comparator(outputFile+"_CG.bed",3,5,False)
    CHG = comparator(outputFile+"_CHG.bed",6,8,False)
    CHH = comparator(outputFile+"_CHH.bed",9,11,True)
    #counter = 0
    for line1,line2 in izip(content1,content2):
        line1 = line1.rstrip('\n')
        arr1 = line1.split("\t")
        line2 = line2.rstrip('\n')
        arr2 = line2.split("\t")
        if(arr1[0] != arr2[0] or arr1[1] != arr2[1] or arr1[2] != arr2[2]):
            print "Comparison Mismatch" # If the chromosome and/or chromosome location is not properly aligned by line between the two comparison files
            continue
        #print '\r'+arr1[1],   -- progress report... sort of by printing out the location on chromosome the program is reading
        #counter +=1
        #print '\r'+str(counter), a better progress report based on the number of lines (wc -l to get the # number lines)
        CG.analyze(arr1,arr2)
        CHG.analyze(arr1,arr2)
        CHH.analyze(arr1,arr2)
    CG.theEnd()
    CHG.theEnd()
    CHH.theEnd()
if __name__ == "__main__":
    main()
