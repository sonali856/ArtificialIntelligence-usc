from collections import OrderedDict
import collections


SORTBYID = True


debug = True
debugFileHandle = open('debug.txt', 'w')

def dPrintf(arg):
  if debug:
      debugFileHandle.write(arg)
      debugFileHandle.write("\n")
      print(arg)



class applicant:
    def __init__(self, applicantId, gender, age, pets, medicalCondition, car, drivingLicense, days):
        self.applicantId = applicantId
        self.gender = gender
        self.age = age
        self.pets = pets
        self.medicalCondition = medicalCondition
        self.car = car
        self.drivingLicense = drivingLicense
        self.days = []
        for x in days:
            self.days.append(int(x))
        if self.car == 'Y' and self.drivingLicense == 'Y' and self.medicalCondition == 'N':
            self.splaViable = True
        else:
            self.splaViable = False
        if self.gender == 'F' and self.age > 17 and self.pets == 'N':
            self.lahsaViable = True
        else:
            self.lahsaViable = False

    def __str__(self):
        result = "ID = " + self.applicantId + " Gender = " + self.gender + " Age =  " + self.age + " Pets = " + self.pets + " Medical Conditions = " + self.medicalCondition + " Car = " + self.car + " DL = " + self.drivingLicense + " Days = " + "".join(
            self.days)
        return result


# MiniMax Function

def callMiniMax(noOfSpacesWeekly, noOfBedsWeekly, visitedSet, maxCurrentSpla, maxCurrentLahsa, currentId,
                player,visitedPath):

    dPrintf("**********************************************************************************************")
    # SPLA
    if player == 1:

        dPrintf("Player: SPLA ")

        #Assigning current value to the local Max Values
        localMaxSpla = maxCurrentSpla
        localMaxLahsa = maxCurrentLahsa
        localMaxId = "1000000"

        dPrintf("Local Max SPLA Assignment "+str(localMaxSpla))
        dPrintf("Local Max LAHSA Assignment "+str(localMaxLahsa))

        dPrintf("Till Now Visited "+str(visitedSet))

        dPrintf("Spla Eligible "+str(splaEligible))

        dPrintf("Lahsa Eligible "+str(lahsaEligible))

        dPrintf("Parent : " + currentId)

        # if checkIfAllApplicantsDone(orderedApplicants, 1):
        #     return maxCurrentSpla, maxCurrentLahsa, currentId

        splaOver = True

        splaUnEligibleApplicants = set()

        #iterate through the eligible list
        for applicantChildId in splaEligible.copy():

            if applicantChildId in visitedSet:
                continue

            if checkIfApplicantPoss(noOfSpacesWeekly, applicantsDict[applicantChildId], 1):

                splaOver = False

                dPrintf("SPLA ADDS APPLICANT ********************** "+str(applicantChildId))
                #Adding to visited set
                visitedSet.add(applicantChildId)

                #Assigning id to localMax
                localMaxId = applicantChildId


                maxCurrentSpla = 0

                # changing spaces
                spacesRequired=applicantsDict[applicantChildId]
                for i in xrange(7):
                    noOfSpacesWeekly[i] = noOfSpacesWeekly[i] + spacesRequired[i]
                    maxCurrentSpla += noOfSpacesWeekly[i]


                dPrintf("SPACES FILLED "+str(noOfSpacesWeekly))
                dPrintf("BEDS FILLED "+str(noOfBedsWeekly))


                dPrintf("Max Current SPLA : ")
                dPrintf(str(maxCurrentSpla))

                dPrintf("Max Current LAHSA: ")
                dPrintf(str(maxCurrentLahsa))

                maxSpla, maxLahsa, maxId = callMiniMax(noOfSpacesWeekly,
                                                       noOfBedsWeekly,
                                                       visitedSet,
                                                       maxCurrentSpla,
                                                       maxCurrentLahsa,
                                                       applicantChildId,
                                                       0,
                                                       visitedPath+","+applicantChildId);

                dPrintf(" CALL RETURNED IN SPLA Max Spla"+str(maxSpla)+"Max Lahsa"+str(maxLahsa)+"Max Id"+str(maxId))

                #checking for higher spla value and checking if same then lower id

                dPrintf("LOCAL MAX "+str(localMaxSpla)+ " Max SPLA "+str(maxSpla)+" LOCAL MAX ID COMPARES " + str(localMaxId) + " MAX ID " + str(maxId))
                if localMaxSpla < maxSpla  or (localMaxSpla == maxSpla  and localMaxId>maxId) :
                    dPrintf("Replacing id "+str(localMaxId)+" WITH "+str(maxId))
                    localMaxSpla = maxSpla
                    localMaxLahsa = maxLahsa
                    localMaxId = maxId



                dPrintf("LOCAL MAX LAHSA "+str(localMaxLahsa)+"LOCAL MAX SPLA "+str(localMaxSpla)+" LOCAL MAX "+str(localMaxId))
                #Removing applicant and updating values

                dPrintf("SPLA REMOVES APPLICANT " + str(applicantChildId))

                visitedSet.remove(applicantChildId)

                spacesRequired = applicantsDict[applicantChildId]
                maxCurrentSpla=0
                for i in xrange(7):
                    noOfSpacesWeekly[i] = noOfSpacesWeekly[i] - spacesRequired[i]
                    maxCurrentSpla += noOfSpacesWeekly[i]

                dPrintf("SPACES AFTER REMOVAL " + str(noOfSpacesWeekly))
                dPrintf("BEDS AFTER REMOVAL " + str(noOfBedsWeekly))

            else:
                #Remove from eligible set and add in unviable set
                splaEligible.remove(applicantChildId)
                splaUnEligibleApplicants.add(applicantChildId)

        if splaOver and len(lahsaEligible)>0:

            dPrintf("SPLA IS OVER ")
            dPrintf(" No of Spaces" +str(noOfSpacesWeekly))
            dPrintf("CURRENT SPLA "+str(maxCurrentSpla))
            dPrintf("VISITED SET "+str(visitedSet))

            maxSpla,maxLahsa,maxId = callMiniMax(noOfSpacesWeekly,
                                    noOfBedsWeekly,
                                    visitedSet,
                                    maxCurrentSpla,
                                    maxCurrentLahsa,
                                    currentId,
                                    0, visitedPath + "," + "Dummy");

            dPrintf(" Return when SPLA IS OVER MAX SPLA :"+str(maxSpla)+" Max Lahsa:"+str(maxLahsa)+" Max id"+str(maxId))
            splaEligible.update(splaUnEligibleApplicants)
            return maxSpla,maxLahsa,maxId

         #Adding back all unviable applicants as recursion done
        splaEligible.update(splaUnEligibleApplicants)
        return localMaxSpla, localMaxLahsa, localMaxId

        # LAHSA Player
    if player == 0:

        dPrintf("LAHSA Player")

        # Assigning current value to the local Max Values
        localMaxSpla = maxCurrentSpla
        localMaxLahsa = maxCurrentLahsa
        localMaxId = "10000000"

        dPrintf("Local Max SPLA Assignment" + str(localMaxSpla))
        dPrintf("Local Max LAHSA Assignment" + str(localMaxLahsa))

        lashaOver = True

        lahsaUnEligibleApplicants = set()

        dPrintf("Till Now Visited " + str(visitedSet))

        dPrintf("Spla Eligible " + str(splaEligible))

        dPrintf("Lahsa Eligible " + str(lahsaEligible))

        dPrintf("Parent : " + currentId)


        for applicantChildId in lahsaEligible.copy():
            #print (lahsaEligible.copy())
            if applicantChildId in visitedSet:
                continue

            if checkIfApplicantPoss(noOfBedsWeekly,applicantsDict[applicantChildId],0):

                lashaOver = False

                dPrintf("LAHSA ADDS APPLICANT " + str(applicantChildId))
                # Adding to visited set
                visitedSet.add(applicantChildId)

                # Assigning id to localMax
                localMaxId = applicantChildId

                maxCurrentLahsa=0
                # changing state beds
                bedsRequired = applicantsDict[applicantChildId]
                for i in xrange(7):
                    noOfBedsWeekly[i] = noOfBedsWeekly[i] + bedsRequired[i]
                    maxCurrentLahsa += noOfBedsWeekly[i]


                dPrintf("SPACES FILLED " + str(noOfSpacesWeekly))
                dPrintf("BEDS FILLED " + str(noOfBedsWeekly))

                dPrintf("Max Current SPLA : ")
                dPrintf(str(maxCurrentSpla))

                dPrintf("Max Current LAHSA: ")
                dPrintf(str(maxCurrentLahsa))

                maxSpla, maxLahsa, maxId = callMiniMax(noOfSpacesWeekly,
                                                       noOfBedsWeekly,
                                                       visitedSet,
                                                       maxCurrentSpla,
                                                       maxCurrentLahsa,
                                                       applicantChildId,
                                                       1, visitedPath + "," + applicantChildId);

                dPrintf("CALL RETURNED IN LAHSA Max Spla " + str(maxSpla) + "Max Lahsa " + str(maxLahsa) + "Max Id " + str(maxId))

                # checking for higher lahsa value and checking if same then lower id
                dPrintf("LOCAL MAX "+str(localMaxLahsa)+ " Max LAHSA "+str(maxLahsa) +" LOCAL MAX ID COMPARES " + str(localMaxId) + " MAX ID " + str(maxId))
                if localMaxLahsa < maxLahsa or (localMaxLahsa == maxLahsa and localMaxId > maxId):
                    dPrintf("Replacing id " + str(localMaxId) + " WITH " + str(maxId))
                    localMaxSpla = maxSpla
                    localMaxLahsa = maxLahsa
                    localMaxId = maxId


                dPrintf("LOCAL MAX LAHSA "+str(localMaxLahsa)+"LOCAL MAX SPLA "+str(localMaxSpla)+" LOCAL MAX "+str(localMaxId))

                dPrintf("LAHSA REMOVES APPLICANT " + str(applicantChildId))

                visitedSet.remove(applicantChildId)

                maxCurrentLahsa = 0
                bedsRequired = applicantsDict[applicantChildId]
                for i in xrange(7):
                    noOfBedsWeekly[i] = noOfBedsWeekly[i] - bedsRequired[i]
                    maxCurrentLahsa += noOfBedsWeekly[i]

                dPrintf("SPACES AFTER REMOVAL " + str(noOfSpacesWeekly))
                dPrintf("BEDS AFTER REMOVAL " + str(noOfBedsWeekly))

            else:
                #print (lahsaEligible)
                #print (applicantChildId)
                lahsaEligible.remove(applicantChildId)
                lahsaUnEligibleApplicants.add(applicantChildId)

        if lashaOver and len(splaEligible)>0:

            dPrintf("LAHSA IS OVER ")
            dPrintf(" No of Spaces" +str(noOfSpacesWeekly))
            dPrintf("CURRENT SPLA "+str(maxCurrentSpla))
            dPrintf("VISITED SET "+str(visitedSet))

            totalEfficiency , lowerId = checkAllSPLAApplicantsFit(noOfSpacesWeekly,visitedSet)

            dPrintf("TOTAL EFFICIENCY : " +str(totalEfficiency)+" LOWER ID "+lowerId)
            if totalEfficiency>-1:

                lahsaEligible.update(lahsaUnEligibleApplicants)
                return totalEfficiency,localMaxLahsa,lowerId

            else:

                maxSpla,maxLahsa,maxId = callMiniMax(noOfSpacesWeekly,
                                        noOfBedsWeekly,
                                        visitedSet,
                                        maxCurrentSpla,
                                        maxCurrentLahsa,
                                        currentId,
                                        1, visitedPath + "," + "Dummy");

                dPrintf(" Return when LAHSA IS OVER MAX SPLA :"+str(maxSpla)+" Max Lahsa:"+str(maxLahsa)+" Max id"+str(maxId))
                lahsaEligible.update(lahsaUnEligibleApplicants)
                return maxSpla,maxLahsa,maxId

        lahsaEligible.update(lahsaUnEligibleApplicants)
        dPrintf("LAHSA AFTER UPDATING" + str(splaEligible))

        return localMaxSpla, localMaxLahsa, localMaxId


def checkAllSPLAApplicantsFit(noOfSpacesWeekly,visitedSet):

    dPrintf(" INSIDE CHECK ALL APPLICANTS FOR SPLA")
    totalEfficiency = 0

    for x in xrange(7):
        totalEfficiency+=noOfSpacesWeekly[x]

    dPrintf(" noOfSpaces"+str(noOfSpacesWeekly))

    for applicantID in splaEligible:

        lowerId = "10000000"

        if applicantID in visitedSet:
            continue


        if checkIfApplicantPoss(noOfSpacesWeekly,applicantsDict[applicantID],1):

            dPrintf("Adding Applicant ID "+applicantID)

            #totalEfficiency = 0
            spacesRequired = applicantsDict[applicantID]
            for i in xrange(7):
                totalEfficiency+=spacesRequired[i]

            if applicantID < lowerId:
                lowerId = applicantID

            dPrintf("Lower ID"+str(lowerId))
            dPrintf("Total Efficiency "+str(totalEfficiency))

        else:

            return -1,"NA"

        dPrintf(" Returning"+str(totalEfficiency)+"id"+str(lowerId))
    return totalEfficiency,lowerId



def firstChoiceApplicant(noOfSpacesWeekly,noOfBedsWeekly,vistedSet,maxCurrentSpla,maxCurrentLahsa):

    dPrintf("****************************************************  FIRST")

    dPrintf("FIRST APPLICANT ")
    dPrintf("SPLA Eligible : "+str(splaEligible))
    dPrintf("LAHSA Eligible : "+str(lahsaEligible))

    dPrintf("SPACES  "+str(noOfSpacesWeekly))
    dPrintf("BEDS "+str(noOfBedsWeekly))

    dPrintf("Visted"+str(visitedSet))

    maxFinalSpla = 0
    maxFinalLahsa = 0
    startApplicant = ""

    for i in xrange(7):
        maxCurrentLahsa+=noOfBedsWeekly[i]

    dPrintf(str(applicantsDict))

    #iterate through all applicants
    for applicantID,daysRequired in applicantsDict.items():
        if applicantID in visitedSet:
            dPrintf("Skip Applicant"+str(applicantID))
            continue
        if applicantID in splaEligible and checkIfApplicantPoss(noOfSpacesWeekly,daysRequired,1):

            dPrintf("**************************************************** FIRST")

            #Adding applicant to visited set
            visitedSet.add(applicantID)

            dPrintf("Adding First Applicant    "+str(applicantID))

            maxCurrentSpla = 0
            #Add days and add to current max
            for i in xrange(7):
                noOfSpacesWeekly[i] = noOfSpacesWeekly[i] + daysRequired[i]
                maxCurrentSpla += noOfSpacesWeekly[i]

            dPrintf("SPACES "+str(noOfSpacesWeekly))

            dPrintf("MAX CURRENT SPLA"+str(maxCurrentSpla)+"MAX CURRENT LAHS"+str(maxCurrentLahsa))
            #Call MiniMax
            maxSpla,maxLahsa,maxId = callMiniMax(noOfSpacesWeekly,
                                                 noOfBedsWeekly,
                                                 vistedSet,
                                                 maxCurrentSpla,
                                                 maxCurrentLahsa,
                                                 applicantID,
                                                 0,str(applicantID))

            dPrintf("------------------------------------------------------------------------------------------------------------")
            #dPrintf("MAX FINAL"+str(startApplicant))
            dPrintf("MAX SPLA FIRST APPLICANT "+str(maxSpla))
            dPrintf("APPLICANT "+maxId)


            #Check if efficiency is greater then current efficiency
            if maxSpla>maxFinalSpla:
                maxFinalSpla = maxSpla
                maxFinalLahsa = maxLahsa
                startApplicant = applicantID
            #Removing from visited
            visitedSet.remove(applicantID)
            dPrintf("SPLA CURRENT FINAL " + str(maxFinalSpla) + " LAHSA FINAL " + str(maxFinalLahsa) + " FINAL APPLICANT " + str(
                    startApplicant))
            #Removing days and remove from current max
            dPrintf("Removing First Applicant : " + "".join(applicantID))

            maxCurrentSpla = 0

            for i in xrange(len(noOfSpacesWeekly)):
                noOfSpacesWeekly[i] = noOfSpacesWeekly[i] - daysRequired[i]
                maxCurrentSpla +=noOfSpacesWeekly[i]

            dPrintf("SPACES AFTER REMOVAL " + str(noOfSpacesWeekly))

    print ("SPLA FINAL "+str(maxFinalSpla) +" LAHSA FINAL "+str(maxFinalLahsa)+" FINAL APPLICANT "+str(startApplicant))

    return maxFinalSpla,startApplicant






def checkIfApplicantPoss(weeklyApplicants,days,player):
    if player == 0:
        max = beds
    else:
        max = spaces

    for x in xrange(7):
        if (weeklyApplicants[x] + days[x]) > max:
            return False

    return True


# def checkIfAllApplicantsDone(orderedApplicants, player):
#     if player == 1:
#         for key, value in orderedApplicants.items():
#             if applicantsDict[key].checkForSPLA():
#                 if value == True:
#                     return False
#
#     if player == 0:
#         for key, value in orderedApplicants.items():
#             if applicantsDict[key].checkForLAHSA():
#                 if value == True:
#                     return False
#
#     return True


if __name__ == '__main__':

    # Inputing File
    input = open("input1.txt", "r")
    beds = int(input.readline())
    spaces = int(input.readline())

    noOfBedsWeekly = [0]*7
    noOfSpacesWeekly = [0]*7

    noOfLAHSA = int(input.readline())
    lahsaAssigned = ["" for x in xrange(noOfLAHSA)]
    for i in xrange(noOfLAHSA):
        lahsaAssigned[i] = input.readline().rstrip()

    noOfSPLA = int(input.readline())
    splaAssigned = ["" for x in xrange(noOfSPLA)]
    for i in xrange(noOfSPLA):
        splaAssigned[i] = input.readline().rstrip()

    noOfApplicants = int(input.readline())

    applicantsDict = OrderedDict()
    splaEligible = set()
    lahsaEligible = set()
    commonEligible = set() #just for easy access , can remove later
    visitedSet = set()
    applicants = []
    countOfCommon = 0

    for i in xrange(noOfApplicants):
        app = input.readline().rstrip();
        temp = applicant(app[:5], app[5:6], app[6:9], app[9:10], app[10:11], app[11:12], app[12:13], app[13:])
        applicantsDict[temp.applicantId] = temp.days
        if temp.splaViable:
            splaEligible.add(temp.applicantId)
        if temp.lahsaViable:
            lahsaEligible.add(temp.applicantId)
        if temp.splaViable and temp.lahsaViable:
            commonEligible.add(temp.applicantId)


    input.close()

    # player 1 - SPLA
    # player 0 - LAHSA

    # removing already assigned applicants

    for i in xrange(len(lahsaAssigned)):
        if lahsaAssigned[i] in applicantsDict:
            daysLahsa = applicantsDict.get(lahsaAssigned[i])
            for x in xrange(7):
                noOfBedsWeekly[x] = noOfBedsWeekly[x] + int(daysLahsa[x])
            del applicantsDict[lahsaAssigned[i]]

            splaEligible.discard(lahsaAssigned[i])
            lahsaEligible.discard(lahsaAssigned[i])
            commonEligible.discard(lahsaAssigned[i])

    for i in xrange(len(splaAssigned)):
        if splaAssigned[i] in applicantsDict:
            daysSpla = applicantsDict.get(splaAssigned[i])
            for x in xrange(7):
                noOfSpacesWeekly[x] = noOfSpacesWeekly[x] + int(daysSpla[x])
            del applicantsDict[splaAssigned[i]]

            splaEligible.discard(splaAssigned[i])
            lahsaEligible.discard(splaAssigned[i])
            commonEligible.discard(splaAssigned[i])

    dPrintf( "SPLA After removal  " + str(splaEligible))
    dPrintf( "LAHSA After removal  " + str(lahsaEligible))
    dPrintf( "BOTH After removal  " + str(commonEligible))

    dPrintf(str(applicantsDict))

    if (SORTBYID):
        applicantsDict = OrderedDict(sorted(applicantsDict.items(),key=lambda t: t[0]))

    dPrintf("Applicants Dict  " +str(applicantsDict))

    # start Game Play
    # initialise

    maxCurrentSpla = 0
    maxCurrentLahsa = 0
    currentId =""

    if len(commonEligible) and len(lahsaEligible) and len(splaEligible) == 0:
        outputFile = open("output1.txt", "a")
        outputFile.write(str(""))
        outputFile.close()

    # call MiniMax

    MaxSpla,MaxId = firstChoiceApplicant(noOfSpacesWeekly,
                                noOfBedsWeekly,
                                visitedSet,
                                maxCurrentSpla,
                                maxCurrentLahsa)


    outputFile = open("output1.txt", "a")
    outputFile.write(str(MaxId) +" | "+str(MaxSpla)+"\n")
    outputFile.close()





#Data Structures to be improved - sets ( applicant & days )
#String Comparsion Fucked Up :
# Keep First Value Outside
#O(1) implementation
