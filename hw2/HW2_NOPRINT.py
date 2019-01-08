from collections import OrderedDict
import collections

SORTBYID = True

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

    # SPLA
    if player == 1:

       #Assigning current value to the local Max Values
        localMaxSpla = maxCurrentSpla
        localMaxLahsa = maxCurrentLahsa
        localMaxId = "1000000"
        splaUnEligibleApplicants = set()

        splaOver = True

        #iterate through the eligible list
        for applicantChildId in splaEligible.copy():

            if applicantChildId in visitedSet:
                continue

            if checkIfApplicantPoss(noOfSpacesWeekly, applicantsDict[applicantChildId], 1):

                splaOver = False

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



                maxSpla, maxLahsa, maxId = callMiniMax(noOfSpacesWeekly,
                                                       noOfBedsWeekly,
                                                       visitedSet,
                                                       maxCurrentSpla,
                                                       maxCurrentLahsa,
                                                       applicantChildId,
                                                       0,
                                                       visitedPath+","+applicantChildId);



                #checking for higher spla value and checking if same then lower id


                if localMaxSpla < maxSpla  or (localMaxSpla == maxSpla  and localMaxId>maxId) :
                    localMaxSpla = maxSpla
                    localMaxLahsa = maxLahsa
                    localMaxId = maxId

                #Removing applicant and updating values

                visitedSet.remove(applicantChildId)
                spacesRequired = applicantsDict[applicantChildId]
                maxCurrentSpla=0
                for i in xrange(7):
                    noOfSpacesWeekly[i] = noOfSpacesWeekly[i] - spacesRequired[i]
                    maxCurrentSpla += noOfSpacesWeekly[i]



            else:
                #Remove from eligible set and add in unviable set
                splaEligible.remove(applicantChildId)
                splaUnEligibleApplicants.add(applicantChildId)


        if splaOver and len(lahsaEligible)>0:

            totalEfficiency , lowerId = checkAllApplicantsFit(noOfBedsWeekly,visitedSet,0)

            if totalEfficiency>-1:
                splaEligible.update(splaUnEligibleApplicants)
                return localMaxSpla,totalEfficiency,lowerId
            else:
                maxSpla,maxLahsa,maxId = callMiniMax(noOfSpacesWeekly,
                                        noOfBedsWeekly,
                                        visitedSet,
                                        maxCurrentSpla,
                                        maxCurrentLahsa,
                                        currentId,
                                        0, visitedPath + "," + "Dummy");
                splaEligible.update(splaUnEligibleApplicants)
                return maxSpla,maxLahsa,maxId

         #Adding back all unviable applicants as recursion done
        splaEligible.update(splaUnEligibleApplicants)
        return localMaxSpla, localMaxLahsa, localMaxId

        # LAHSA Player
    if player == 0:

        # Assigning current value to the local Max Values
        localMaxSpla = maxCurrentSpla
        localMaxLahsa = maxCurrentLahsa
        localMaxId = "10000000"
        lashaOver = True
        lahsaUnEligibleApplicants = set()

        for applicantChildId in lahsaEligible.copy():

            if applicantChildId in visitedSet:
                continue

            if checkIfApplicantPoss(noOfBedsWeekly,applicantsDict[applicantChildId],0):

                lashaOver = False

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


                maxSpla, maxLahsa, maxId = callMiniMax(noOfSpacesWeekly,
                                                       noOfBedsWeekly,
                                                       visitedSet,
                                                       maxCurrentSpla,
                                                       maxCurrentLahsa,
                                                       applicantChildId,
                                                       1, visitedPath + "," + applicantChildId);


                # checking for higher lahsa value and checking if same then lower id
                if localMaxLahsa < maxLahsa or (localMaxLahsa == maxLahsa and localMaxId > maxId):
                    localMaxSpla = maxSpla
                    localMaxLahsa = maxLahsa
                    localMaxId = maxId


                visitedSet.remove(applicantChildId)

                maxCurrentLahsa = 0
                bedsRequired = applicantsDict[applicantChildId]
                for i in xrange(7):
                    noOfBedsWeekly[i] = noOfBedsWeekly[i] - bedsRequired[i]
                    maxCurrentLahsa += noOfBedsWeekly[i]



            else:
                lahsaEligible.remove(applicantChildId)
                lahsaUnEligibleApplicants.add(applicantChildId)

        if lashaOver and len(splaEligible)>0:

            totalEfficiency , lowerId = checkAllApplicantsFit(noOfSpacesWeekly,visitedSet,1)
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
                lahsaEligible.update(lahsaUnEligibleApplicants)
                return maxSpla,maxLahsa,maxId

        lahsaEligible.update(lahsaUnEligibleApplicants)


        return localMaxSpla, localMaxLahsa, localMaxId


def checkAllApplicantsFit(weeklyApplicants,visitedSet,player):

    totalEfficiency = 0

    tempApplicants = [0]*7

    for i in xrange(7):
        tempApplicants[i] = weeklyApplicants[i]
        totalEfficiency+=tempApplicants[i]


    #SPLA
    if player==1:

        for applicantID in splaEligible:

            lowerId = "10000000"

            if applicantID in visitedSet:
                continue

            if checkIfApplicantPoss(tempApplicants, applicantsDict[applicantID], 1):
                # totalEfficiency = 0
                spacesRequired = applicantsDict[applicantID]
                for i in xrange(7):
                    tempApplicants[i] += spacesRequired[i]
                    totalEfficiency += spacesRequired[i]
                if applicantID < lowerId:
                    lowerId = applicantID
            else:

                return -1, "NA"

        return totalEfficiency, lowerId


    #LAHSA
    if player==0:

        for applicantID in lahsaEligible:

            lowerId = "10000000"

            if applicantID in visitedSet:
                continue

            if checkIfApplicantPoss(tempApplicants, applicantsDict[applicantID], 0):
                # totalEfficiency = 0
                spacesRequired = applicantsDict[applicantID]
                for i in xrange(7):
                    tempApplicants[i] += spacesRequired[i]
                    totalEfficiency += spacesRequired[i]
                if applicantID < lowerId:
                    lowerId = applicantID
            else:

                return -1, "NA"

        return totalEfficiency, lowerId



def firstChoiceApplicant(noOfSpacesWeekly,noOfBedsWeekly,vistedSet,maxCurrentSpla,maxCurrentLahsa):



    maxFinalSpla = 0
    maxFinalLahsa = 0
    startApplicant = ""

    for i in xrange(7):
        maxCurrentLahsa+=noOfBedsWeekly[i]



    #iterate through all applicants
    for applicantID,daysRequired in applicantsDict.items():
        if applicantID in visitedSet:

            continue
        if applicantID in splaEligible and checkIfApplicantPoss(noOfSpacesWeekly,daysRequired,1):



            #Adding applicant to visited set
            visitedSet.add(applicantID)



            maxCurrentSpla = 0
            #Add days and add to current max
            for i in xrange(7):
                noOfSpacesWeekly[i] = noOfSpacesWeekly[i] + daysRequired[i]
                maxCurrentSpla += noOfSpacesWeekly[i]




            #Call MiniMax
            maxSpla,maxLahsa,maxId = callMiniMax(noOfSpacesWeekly,
                                                 noOfBedsWeekly,
                                                 vistedSet,
                                                 maxCurrentSpla,
                                                 maxCurrentLahsa,
                                                 applicantID,
                                                 0,str(applicantID))



            #Check if efficiency is greater then current efficiency
            if maxSpla>maxFinalSpla:
                maxFinalSpla = maxSpla
                maxFinalLahsa = maxLahsa
                startApplicant = applicantID
            #Removing from visited
            visitedSet.remove(applicantID)

            #Removing days and remove from current max
            maxCurrentSpla = 0

            for i in xrange(len(noOfSpacesWeekly)):
                noOfSpacesWeekly[i] = noOfSpacesWeekly[i] - daysRequired[i]
                maxCurrentSpla +=noOfSpacesWeekly[i]


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


if __name__ == '__main__':

    # Inputing File
    input = open("input.txt", "r")
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



    if (SORTBYID):
        applicantsDict = OrderedDict(sorted(applicantsDict.items(),key=lambda t: t[0]))



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


