from collections import OrderedDict

spla_eligible=set()
lahsa_eligible=set()

debug = True
debugFileHandle = open('debug.txt', 'w')

def dprintf(arg):
  if debug:
      debugFileHandle.write(arg)
      debugFileHandle.write("\n")
      print(arg)

class Person:
    # global lahsa_viable
    # global spla_viable

    def __init__(self, applicant_id, gender, age, pets, medical_condition, car, license, needy_days_string):
        self.applicant_id=applicant_id
        self.gender = gender
        self.age = age
        self.pets = pets
        self.medical_condition = medical_condition
        self.car = car
        self.license = license
        self.needy_days=list()
        for x in needy_days_string:
            self.needy_days.append(int(x))
        if medical_condition == "N" and car== "Y" and license =="Y":
            self.spla_eligible= True
            spla_eligible.add(applicant_id)
        else:
            self.spla_eligible = False
        if gender == "F" and pets == "N" and age > 17:
            self.lahsa_eligible = True
            lahsa_eligible.add(applicant_id)
        else:
            self.lahsa_eligible = False

    def __repr__(self):
        result= "Applicant ID : " + self.applicant_id + "  Days Needed : " + str(self.needy_days) +"\n"
        return str(result)


def readInput():

    inputFileHandle = open('input1Den.txt', 'r')
    beds=int(inputFileHandle.readline())
    parking_spaces=int(inputFileHandle.readline())

    initial_lahsa_applicant_count=int(inputFileHandle.readline())
    initial_lahsa_applicants=list()
    for x in xrange(initial_lahsa_applicant_count):
        initial_lahsa_applicants.append(inputFileHandle.readline().rstrip())

    initial_spla_applicant_count = int(inputFileHandle.readline())
    initial_spla_applicants = list()
    for x in xrange(initial_spla_applicant_count):
        initial_spla_applicants.append(inputFileHandle.readline().rstrip())

    #{i: True for i in initial_spla_applicants}

    total_application_count=int(inputFileHandle.readline())
    total_applicants_list=list()
    for x in xrange(total_application_count):
        stringIp=inputFileHandle.readline()
        total_applicants_list.append(Person(stringIp[0:5], stringIp[5:6], int(stringIp[6:9]), stringIp[9:10], stringIp[10:11], stringIp[11:12], stringIp[12:13],stringIp[13:20]))

    total_applicants= OrderedDict()
    for x in total_applicants_list:
        total_applicants[x.applicant_id]=x.needy_days
    startGame(total_applicants, initial_lahsa_applicant_count, initial_lahsa_applicants, initial_spla_applicant_count,
              initial_spla_applicants, beds, parking_spaces)
    dprintf("*************************")
    dprintf(str(total_applicants))
    dprintf(str(total_applicants_list))
    dprintf(str(spla_eligible))
    dprintf(str(lahsa_eligible))


def startGame(total_applicants,initial_lahsa_applicant_count,initial_lahsa_applicants,initial_spla_applicant_count,initial_spla_applicants,beds,parking_spaces):


    dprintf(str(spla_eligible))
    dprintf(str(lahsa_eligible))

    firstApplicant=0
    max_efficiency_spla=0
    visited=set()
    visited.update(initial_lahsa_applicants)
    visited.update(initial_spla_applicants)
    dprintf("Initial spla Visited: " + str(initial_spla_applicants))
    dprintf("Initial lahsa Visited: " + str(initial_lahsa_applicants))
    dprintf("Initial State of Visited: "+ str(visited))

    spla_parking_status= [parking_spaces]*7
    lahsa_bed_status= [beds]*7

    spla_occupied_beds=initializeSplaParkingSpots(initial_spla_applicants,spla_parking_status,total_applicants)
    lahsa_occupied_beds=initializeSplaParkingSpots(initial_lahsa_applicants,lahsa_bed_status,total_applicants)
    dprintf("*****************")
    dprintf("Initial spla parking spot status: " + str(spla_parking_status))
    dprintf("spla occupied parking spots " + str(spla_occupied_beds))
    dprintf("*****************")
    dprintf("Initial lahsa bed status: " + str(lahsa_bed_status))
    dprintf("lahsa occupied beds " + str(lahsa_occupied_beds))
    dprintf("*****************")
    for person_id,needy_days in total_applicants.items():
        if person_id in visited:
            dprintf("*************************************************")
            dprintf("Skipping Person  " + str(person_id))
            dprintf("*************************************************")
            continue
        if person_id in spla_eligible and checkSplaViability(spla_parking_status,needy_days):
            visited.add(person_id)
            spla_occupied_beds += updateSplaParkingSpots(spla_parking_status, needy_days)
            dprintf("*************************************************")
            dprintf("First Pick:"+str(person_id))
            dprintf("Visited Status:" + str(visited))
            dprintf("Parking status" + str(spla_parking_status))
            temp_max_efficiency_spla,temp,person_idtempperson=runGame(total_applicants, initial_lahsa_applicant_count, initial_lahsa_applicants,
                    initial_spla_applicant_count, initial_spla_applicants, beds, parking_spaces, visited,
                    spla_parking_status, lahsa_bed_status,spla_occupied_beds,lahsa_occupied_beds, False, str(person_id),0)
            if temp_max_efficiency_spla > max_efficiency_spla :
                dprintf("Max efficiency changed to "+ str(temp_max_efficiency_spla))
                max_efficiency_spla=temp_max_efficiency_spla
                firstApplicant=person_id
                dprintf("Applicant ID is  " + str(firstApplicant))
            visited.remove(person_id)
            spla_occupied_beds -= resetSplaParkingSpots(spla_parking_status,needy_days)
            dprintf("*************************************************")

    print("RESULT:  " + str(max_efficiency_spla) + " : " + str(firstApplicant))
    writeOutput(firstApplicant)

def initializeSplaParkingSpots(initial_spla_applicants,spla_parking_status,total_applicants):
    beds_occupied=0
    for applicant_id in initial_spla_applicants:
        beds_occupied+=updateSplaParkingSpots(spla_parking_status,total_applicants[applicant_id])
    return beds_occupied

def runGame(total_applicants, initial_lahsa_applicant_count, initial_lahsa_applicants, initial_spla_applicant_count,
            initial_spla_applicants, beds, parking_spaces, visited, spla_parking_status, lahsa_bed_status,
            spla_occupied_parkings, lahsa_occupied_beds, chance,visited_path,depth):

    if chance:
        max_efficiency_spla=spla_occupied_parkings
        max_efficiency_lahsa=lahsa_occupied_beds
        best_applicant=10000000;
        spla_unviable_people=set()
        #spla plays
        for person_id in spla_eligible.copy():
            if person_id in visited:
                continue
            if checkSplaViability(spla_parking_status,total_applicants[person_id]):
                best_applicant = person_id
                visited.add(person_id)
                spla_occupied_parkings+=updateSplaParkingSpots(spla_parking_status, total_applicants[person_id])
                dprintf("****** SPLA TO PLAY ***********")
                dprintf("SPLA picked: "+ str(person_id)+ " With efficiency: " + str(spla_occupied_parkings))
                dprintf("Current Path :" + visited_path + " | "+str(person_id))
                dprintf("Visited Status:" + str(visited))
                dprintf("Parking status" + str(spla_parking_status))

                temp_max_efficiency_spla,temp_lahsa_occupied_beds, temp_best_applicant=runGame(total_applicants, initial_lahsa_applicant_count, initial_lahsa_applicants,
                                                                initial_spla_applicant_count, initial_spla_applicants, beds, parking_spaces, visited,
                                                                spla_parking_status, lahsa_bed_status, spla_occupied_parkings, lahsa_occupied_beds, not chance,visited_path + " | "+str(person_id),depth)


                dprintf("call  Returned in spla: " + str(temp_best_applicant) + " With efficiency: " + str(temp_max_efficiency_spla) + "with opponent efficiency: "+ str(temp_lahsa_occupied_beds))

                if temp_max_efficiency_spla > max_efficiency_spla or (temp_max_efficiency_spla==max_efficiency_spla and best_applicant>temp_best_applicant):
                    max_efficiency_spla=temp_max_efficiency_spla
                    max_efficiency_lahsa=temp_lahsa_occupied_beds
                    best_applicant=temp_best_applicant

                visited.remove(person_id)
                spla_occupied_parkings -=resetSplaParkingSpots(spla_parking_status, total_applicants[person_id])
            else:
                spla_eligible.remove(person_id)
                spla_unviable_people.add(person_id)
        spla_eligible.update(spla_unviable_people)
        dprintf("Returning Max from spla at "+visited_path +" as: " + str(max_efficiency_spla))
        dprintf("bestApplicant"+str(best_applicant))
        return max_efficiency_spla,max_efficiency_lahsa,best_applicant

    else:
        lahsaExhausted=True
        max_efficiency_lahsa = lahsa_occupied_beds
        max_efficiency_spla=spla_occupied_parkings
        best_applicant=10000000
        lahsa_unviable_people=set()
        for person_id in lahsa_eligible.copy():
            if person_id in visited:
                continue
            if checkSplaViability(lahsa_bed_status,total_applicants[person_id]):
                lahsaExhausted=False
                best_applicant = person_id
                visited.add(person_id)
                lahsa_occupied_beds+=updateSplaParkingSpots(lahsa_bed_status, total_applicants[person_id])
                dprintf("LAHSA picked:" + str(person_id))
                temp_spla_occupied_parkings,temp_max_efficiency_lahsa,temp_best_applicant=runGame(total_applicants, initial_lahsa_applicant_count, initial_lahsa_applicants,
                        initial_spla_applicant_count, initial_spla_applicants, beds, parking_spaces, visited,
                        spla_parking_status, lahsa_bed_status, spla_occupied_parkings, lahsa_occupied_beds, not chance,visited_path + " | "+str(person_id),depth)
                dprintf("call  Returned in lahsa: " + str(temp_best_applicant) + " With efficiency: " + str(
                    temp_max_efficiency_lahsa) + "with opponent efficiency: " + str(temp_spla_occupied_parkings))
                if temp_max_efficiency_lahsa > max_efficiency_lahsa or (temp_max_efficiency_lahsa==max_efficiency_lahsa and best_applicant>temp_best_applicant):
                    dprintf("Bettering applicant ID from: "+str(best_applicant) +"  to: "+ str(temp_best_applicant))
                    max_efficiency_lahsa=temp_max_efficiency_lahsa
                    max_efficiency_spla=temp_spla_occupied_parkings
                    best_applicant=temp_best_applicant

                visited.remove(person_id)
                lahsa_occupied_beds-=resetSplaParkingSpots(lahsa_bed_status, total_applicants[person_id])
            else:
                lahsa_unviable_people.add(person_id)
                lahsa_eligible.remove(person_id)

        if lahsaExhausted:
            # temp1,temp2,temp3=runGame(total_applicants, initial_lahsa_applicant_count, initial_lahsa_applicants,
            #                            initial_spla_applicant_count, initial_spla_applicants, beds, parking_spaces, visited,
            #                            spla_parking_status, lahsa_bed_status, spla_occupied_parkings, lahsa_occupied_beds, not chance,visited_path + " | Lahsa None ",depth+1)
            # if depth==0:
            #     print ("Can Fit all Spla remaining is : " + str(temp1))
            # return temp1,temp2,temp3

            # return runGame(total_applicants, initial_lahsa_applicant_count, initial_lahsa_applicants,
            #                            initial_spla_applicant_count, initial_spla_applicants, beds, parking_spaces, visited,
            #                            spla_parking_status, lahsa_bed_status, spla_occupied_parkings, lahsa_occupied_beds, not chance,visited_path + " | Lahsa None ",depth)


            can_spla_fit_remaining = canSplaFitAllRemaining(total_applicants,spla_occupied_parkings,spla_parking_status,visited)
            # print ("Can Fit all Spla remaining is : "+ str(can_spla_fit_remaining))
            if can_spla_fit_remaining > -1:
                return can_spla_fit_remaining,max_efficiency_lahsa,spla_eligible.pop
            else:
                return runGame(total_applicants, initial_lahsa_applicant_count, initial_lahsa_applicants,
                    initial_spla_applicant_count, initial_spla_applicants, beds, parking_spaces, visited,
                    spla_parking_status, lahsa_bed_status, spla_occupied_parkings, lahsa_occupied_beds, not chance,visited_path + " | Lahsa None ",depth)
        lahsa_eligible.update(lahsa_unviable_people)
        dprintf("Returning Max from Lahsa at " + visited_path + " as: " + str(max_efficiency_lahsa))
        #printf("AAA" + str(best_applicant))
        return max_efficiency_spla,max_efficiency_lahsa,best_applicant

def canSplaFitAllRemaining(total_applicants,spla_occupied_parkings,spla_parking_status,visited):
    for person_id in spla_eligible:
        if person_id in visited:
            continue
        if checkSplaViability(spla_parking_status, total_applicants[person_id]):
            spla_occupied_parkings += getPeopleinParkingSpots(spla_parking_status, total_applicants[person_id])
        else:
            return -1
    return spla_occupied_parkings



def getPeopleinParkingSpots(spla_parking_status,needy_days):
    new_beds_filled = 0
    for x in xrange(7):
        if needy_days[x] == 1:
            new_beds_filled += 1
    return new_beds_filled

def checkSplaViability(spla_parking_status,needy_days):

    for x in xrange(7):
        if needy_days[x]==1 and spla_parking_status[x] == 0:
            return False
    return True

def updateSplaParkingSpots(spla_parking_status,needy_days):
    new_beds_filled=0
    for x in xrange(7):
        if needy_days[x]==1:
            new_beds_filled+=1
            spla_parking_status[x]-=1
    return new_beds_filled

def resetSplaParkingSpots(spla_parking_status,needy_days):
    new_beds_filled = 0
    for x in xrange(7):
        if needy_days[x]==1:
            new_beds_filled += 1
            spla_parking_status[x]+=1
    return new_beds_filled

def writeOutput(result):
    outputFileHandle = open('output.txt', 'w')
    outputFileHandle.write(str(result))

readInput()
# Convert total applicants to a Dict??
# Repeated Scans of total applicants??