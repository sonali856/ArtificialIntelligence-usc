from collections import OrderedDict
import collections


DEBUG = True
SORTBYID = True

def dPrintf(arg):
    if DEBUG:
        print str(arg)


class applicant:
     def __init__(self,applicantId,gender,age,pets,medicalCondition,car,drivingLicense,days):
        self.applicantId = applicantId
        self.gender=gender
        self.age = age
        self.pets = pets
        self.medicalCondition= medicalCondition
        self.car=car
        self.drivingLicense=drivingLicense
        self.days = [x for x in days]

     def __str__(self):
         result = "ID = " + self.applicantId + " Gender = "+self.gender+" Age =  "+self.age+" Pets = "+self.pets+" Medical Conditions = "+self.medicalCondition + " Car = "+self.car+" DL = "+self.drivingLicense + " Days = "+"".join(self.days)
         return result

     def checkForSPLA(self):
        if self.car == 'Y' and self.drivingLicense == 'Y' and self.medicalCondition == 'N':
            return True
        else:
            return False

     def checkForLAHSA(self):
        if self.gender =='F' and self.age > 17 and self.pets=='N':
            return True
        else:
            return False




#MiniMax Function

def callMiniMax(noOfSpacesWeekly,noOfBedsWeekly,orderedApplicants,maxCurrentSpla,maxCurrentLahsa,currentId,countOfCommon,player):

    dPrintf("***********************************************************************")

    #TODO : Check if nthy is compliant :,

    #SPLA
    if player==1:
        dPrintf("Player: SPLA")
        localMaxSpla = -1
        localMaxLahsa = -1
        localMaxId = ""

        dPrintf("Applicants : ")
        dPrintf(orderedApplicants)

        dPrintf("Spla Applicants: " +",".join(str(k) for k,v in orderedApplicants.items()
                                                if applicantsDict[k].checkForSPLA() and not applicantsDict[k].checkForLAHSA()))

        dPrintf("Lahsa Applicants: "+",".join(str(k) for k,v in orderedApplicants.items()
                                                if applicantsDict[k].checkForLAHSA() and not applicantsDict[k].checkForSPLA()))

        dPrintf("Common Applicants : "+",".join(str(k) for k,v in orderedApplicants.items()
                                                if applicantsDict[k].checkForLAHSA() and applicantsDict[k].checkForSPLA()))

        dPrintf("Parent : "+currentId)


        if checkIfAllApplicantsDone(orderedApplicants,1):
            return maxCurrentSpla,maxCurrentLahsa,currentId

            #do it for when no applicants can be taken

        countOfApplicantsPossSpla = 0;
        for applicantChild ,status in orderedApplicants.items():

            if status and applicantsDict[applicantChild].checkForSPLA():
                if(applicantsDict[applicantChild].checkForLAHSA()):
                    countOfCommon-=1

                if checkIfApplicantPoss(noOfSpacesWeekly,applicantsDict[applicantChild]):

                    countOfApplicantsPossSpla+=1
                    #Remove
                    for i in xrange(len(noOfSpacesWeekly)):
                        noOfSpacesWeekly[i] = noOfSpacesWeekly[i] - int(applicantsDict[applicantChild].days[i])

                    dPrintf("Beds Weekly  : " + str(noOfBedsWeekly))
                    dPrintf("Spaces Weekly : " + str(noOfSpacesWeekly))


                    #maxCurrentSpla = calculateCurrentMax(noOfSpacesWeekly,1)

                    dPrintf("Max Current SPLA " +str(calculateCurrentMax(noOfSpacesWeekly,1)))

                    dPrintf("Max Current LAHSA: ")
                    dPrintf(maxCurrentLahsa)

                    dPrintf("SPLA REMOVES Applicant : " + "".join(applicantChild))
                    orderedApplicants[applicantChild] = False

                    maxSpla, maxLahsa, maxId = callMiniMax(noOfSpacesWeekly,
                                                                 noOfBedsWeekly,
                                                                 orderedApplicants,
                                                                 calculateCurrentMax(noOfSpacesWeekly, 1),
                                                                 maxCurrentLahsa,
                                                                 applicantChild,
                                                                 countOfCommon,
                                                                 0);


                    dPrintf("MAX ID "+str(maxId)+"\n"+"Max Spla"+str(maxSpla)+"\n"+"Max Lahsa"+str(maxLahsa));


                    # reversing back the states

                    dPrintf("SPLA ADDING Applicant : "+"".join(applicantChild))
                    for i in xrange(len(noOfSpacesWeekly)):
                        noOfSpacesWeekly[i] = noOfSpacesWeekly[i] + int(applicantsDict[applicantChild].days[i])

                    orderedApplicants[applicantChild] = True

                    #maxCurrentSpla = calculateCurrentMax(noOfSpacesWeekly, 1)


                    if(localMaxSpla<maxSpla):
                        localMaxSpla = maxSpla
                        localMaxLahsa = maxLahsa
                        localMaxId = str(maxId)+","+str(currentId)
                        dPrintf("Local Max ID  " +str(localMaxId))


                    elif(localMaxSpla == maxSpla):
                        if(localMaxId[::-1]>maxId[::-1]):
                            dPrintf("Local Max Id ------ SPLA "+str(localMaxId) + " Max ID "+str(maxId))
                            localMaxSpla =maxSpla
                            localMaxLahsa =maxLahsa
                            localMaxId = str(maxId)+","+str(currentId)
                            dPrintf("Local Max ID  " + str(localMaxId))


        if(countOfApplicantsPossSpla==0):
            return maxCurrentSpla, maxCurrentLahsa, currentId


        dPrintf("Spla Node : "+str(currentId))
        dPrintf(" Local Max Id  "+str(localMaxId)+"\nLocal Max Spla "+str(localMaxSpla)+"\nLocal Max Lahsa "+str(localMaxLahsa))


         #check for the lowest index applicant store those values

         # check for local max and maxSpla n according to that change if greater // problem where to get another max forom (wont it get overridden)



        #if end of loop , or no applicants can be picked
            #update maxSpla, maxLahsa


        #for loop for common+spla
        #if applicant can be taken :
            #change state(noSpaces,noBeds)
            #remove this applicant from the common/spla list

            #callMiniMax again ()
            # change maxCurrentSpla,maxCurrentLahsa



    #LAHSA Player
    if player==0:

        dPrintf("LAHSA Player")
        localMaxSpla = -1
        localMaxLahsa = -1
        localMaxId = ""

        dPrintf("Applicants : ")
        dPrintf(orderedApplicants)

        dPrintf("Spla Applicants: " + ",".join(str(k) for k, v in orderedApplicants.items()
                                             if applicantsDict[k].checkForSPLA() and not applicantsDict[k].checkForLAHSA()))

        dPrintf("Lahsa Applicants: " + ",".join(str(k) for k, v in orderedApplicants.items()
                                              if applicantsDict[k].checkForLAHSA() and not applicantsDict[k].checkForSPLA()))

        dPrintf("Common Applicants : " + ",".join(str(k) for k, v in orderedApplicants.items()
                                                 if applicantsDict[k].checkForLAHSA() and applicantsDict[k].checkForSPLA()))

        dPrintf("Parent : " + currentId)

        if checkIfAllApplicantsDone(orderedApplicants,0):
            if not checkIfAllApplicantsDone(orderedApplicants,1):
                maxSpla, maxLahsa, maxId = callMiniMax(noOfSpacesWeekly,
                                                       noOfBedsWeekly,
                                                       orderedApplicants,
                                                       maxCurrentSpla,
                                                       maxCurrentLahsa,
                                                       currentId,
                                                       countOfCommon,
                                                       1);
                return maxSpla,maxLahsa,maxId
            else:
                return maxCurrentSpla,maxCurrentLahsa,currentId


            # do it for when no applicants can be taken

        countOfApplicantsPossLahsa = 0;

        for applicantChild, status in orderedApplicants.items():

            if status and applicantsDict[applicantChild].checkForLAHSA():

                if (applicantsDict[applicantChild].checkForSPLA()):
                    countOfCommon -=1

                if checkIfApplicantPoss(noOfBedsWeekly, applicantsDict[applicantChild]):

                    countOfApplicantsPossLahsa+=1

                    # changing state beds
                    for i in range(len(noOfBedsWeekly)):
                        noOfBedsWeekly[i] = noOfBedsWeekly[i] - int(applicantsDict[applicantChild].days[i])

                    dPrintf("Beds Weekly  : "+str(noOfBedsWeekly))
                    dPrintf("Spaces Weekly : "+str(noOfSpacesWeekly))

                    #maxCurrentLahsa = calculateCurrentMax(noOfBedsWeekly,0)

                    dPrintf(" Max Current SPLA : ")
                    dPrintf(maxCurrentSpla)

                    dPrintf(" Max Current LAHSA: ")
                    dPrintf(calculateCurrentMax(noOfBedsWeekly, 0))

                    dPrintf(" LAHSA REMOVES Applicant : " + "".join(applicantChild))
                    orderedApplicants[applicantChild] = False

                    maxSpla,maxLahsa,maxId = callMiniMax(noOfSpacesWeekly,
                                                 noOfBedsWeekly,
                                                 orderedApplicants,
                                                 maxCurrentSpla,
                                                 calculateCurrentMax(noOfBedsWeekly, 0),
                                                 applicantChild,
                                                 countOfCommon,
                                                 1);

                    dPrintf("MAX ID " + str(maxId) + "\n" + "Max Spla" + str(maxSpla) + "\n" + "Max Lahsa" + str(maxLahsa));

                    dPrintf(" LAHSA ADDING Applicant: "+ str(applicantChild))
                    orderedApplicants[applicantChild] = True

                    for i in range(len(noOfBedsWeekly)):
                        noOfBedsWeekly[i] = noOfBedsWeekly[i] + int(applicantsDict[applicantChild].days[i])


                    if(localMaxLahsa<maxLahsa):
                        localMaxSpla = maxSpla
                        localMaxLahsa = maxLahsa
                        localMaxId = str(maxId)+","+str(currentId)
                        dPrintf("Local Max ID  " +str(localMaxId))

                    elif(localMaxLahsa == maxLahsa):
                        if(localMaxId[::-1]>maxId[::-1]):
                            dPrintf("Local Max Id     ------ LAHSA "+str(localMaxId) + " Max ID "+str(maxId))
                            localMaxSpla = maxSpla
                            localMaxLahsa = maxLahsa
                            localMaxId = str(maxId)+","+str(currentId)
                            dPrintf("Local Max ID  " + str(localMaxId))

        dPrintf("Lahsa Node : " + str(currentId))
        dPrintf("Local Max Id  " + str(localMaxId) + "\nLocal Max Spla " + str(
            localMaxSpla) + "\nLocal Max Lahsa " + str(localMaxLahsa))

        if countOfApplicantsPossLahsa==0:
            maxSpla, maxLahsa, maxId = callMiniMax(noOfSpacesWeekly,
                                                  noOfBedsWeekly,
                                                  orderedApplicants,
                                                  maxCurrentSpla,
                                                  maxCurrentLahsa,
                                                  currentId,
                                                  countOfCommon,
                                                  1);
            return maxSpla,maxLahsa,maxId

    return localMaxSpla,localMaxLahsa,localMaxId

def checkIfApplicantPoss(weeklyApplicants,a):
    for x in range(len(weeklyApplicants)):
        if (weeklyApplicants[x] - int(a.days[x])) < 0:
            return False

    return True


def calculateCurrentMax(weeklyApplicants,player):
    sum = 0
    if player == 0 :
        total = beds*7
    else:
        total = spaces*7

    for x in range(len(weeklyApplicants)):
        sum+=weeklyApplicants[x]

    return total-sum


def checkIfAllApplicantsDone(orderedApplicants,player):

    if player==1:
        for key,value in orderedApplicants.items():
            if applicantsDict[key].checkForSPLA():
                if value==True:
                    return False

    if player==0:
        for key,value in orderedApplicants.items():
            if applicantsDict[key].checkForLAHSA():
                if value==True:
                    return False

    return True


if __name__ == '__main__':


    #Inputing File
    input = open("input1.txt", "r")
    beds = int(input.readline())
    spaces = int(input.readline())

    noOfBedsWeekly = [beds for i in range(7)]
    noOfSpacesWeekly = [spaces for i in range(7)]

    noOfLAHSA = int(input.readline())
    lahsaAssigned = ["" for x in range(noOfLAHSA)]
    for i in range(noOfLAHSA):
        lahsaAssigned[i] = input.readline().rstrip()

    noOfSPLA = int(input.readline())
    splaAssigned = ["" for x in range(noOfSPLA)]
    for i in range(noOfSPLA):
        splaAssigned[i] = input.readline().rstrip()

    noOfApplicants = int(input.readline())

    applicantsDict = {}
    applicants = []
    countOfCommon = 0

    for i in range(noOfApplicants):
        app = input.readline().rstrip();
        temp = applicant(app[:5], app[5:6], app[6:9], app[9:10], app[10:11], app[11:12], app[12:13], app[13:])
        applicantsDict[temp.applicantId] = temp


    input.close()

    #player 1 - SPLA
    #player 0 - LAHSA

    #removing already assigned applicants

    for i in range(len(lahsaAssigned)):
        if lahsaAssigned[i] in applicantsDict:
            applicant = applicantsDict.get(lahsaAssigned[i])
            for x in range(len(noOfBedsWeekly)):
                noOfBedsWeekly[x] = noOfBedsWeekly[x]-int(applicant.days[x])
            del applicantsDict[lahsaAssigned[i]]


    for i in range(len(splaAssigned)):
        if splaAssigned[i] in applicantsDict:
            applicant = applicantsDict.get(splaAssigned[i])
            for x in range(len(noOfSpacesWeekly)):
                noOfSpacesWeekly[x]=noOfSpacesWeekly[x]-int(applicant.days[x])
            del applicantsDict[splaAssigned[i]]


    for key,value in applicantsDict.iteritems():
        applicants.append(value)

    dPrintf(noOfSpacesWeekly)
    dPrintf(noOfBedsWeekly)

     #Creating sets for all applicants left

    orderedApplicants = OrderedDict()

    for i in xrange(len(applicants)):
        if applicants[i].checkForSPLA() and applicants[i].checkForLAHSA():
            #print(" BOTH " +str(applicants[i].applicantId))
            orderedApplicants[applicants[i].applicantId] = True
            countOfCommon += 1

    for i in xrange(len(applicants)):
        if applicants[i].checkForSPLA() and not applicants[i].checkForLAHSA():

            #print(" SPLA ONLY " + str(applicants[i].applicantId))
            orderedApplicants[applicants[i].applicantId] = True

    for i in xrange(len(applicants)):
        if not applicants[i].checkForSPLA() and applicants[i].checkForLAHSA():

            #print(" LAHSA ONLY  " + str(applicants[i].applicantId))
            orderedApplicants[applicants[i].applicantId] = True




    #print(orderedApplicants)
    #print(countOfCommon)

    if(SORTBYID):
        orderedApplicants = OrderedDict(sorted(orderedApplicants.items(), key=lambda t: t[0]))

    #print(orderedApplicants)

    #start Game Play

    #initialise

    maxCurrentSpla = 0
    maxCurrentLahsa = 0

    maxSpla = 0
    maxLahsa = 0
    currentId = ""

    if len(orderedApplicants) == 0 :
        outputFile = open("output.txt", "w")
        outputFile.write(str(""))
        outputFile.close()

    #call MiniMax

    MaxSpla, MaxLahsa, MaxId = callMiniMax(noOfSpacesWeekly,
                                          noOfBedsWeekly,
                                          orderedApplicants,
                                          maxCurrentSpla,
                                          maxCurrentLahsa,
                                          currentId,
                                          countOfCommon,
                                          1)

    dPrintf(MaxSpla)
    dPrintf(MaxLahsa)
    dPrintf(MaxId)
    #print (MaxId.split(",")[-2])
    outputFile = open("output1.txt", "a")
    if(len(MaxId)==0 or MaxId == None):
        outputFile.write("NA | " + "0\n")

    outputFile.write(str(MaxId.split(",")[-2]) +" | "+str(MaxSpla)+"\n")
    outputFile.close()







