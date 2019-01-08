from collections import OrderedDict

# Global set that holds the applicants who are SPLA compliant
spla_compliant_applicants = set()

# Global set that holds the applicants who are LAHSA compliant
lahsa_compliant_applicants = set()

# Input file name in local directory
INPUT_FILE = "input1.txt"


# This 'Applicant' class holds the parsed information regarding every applicant
class Applicant:

    # The basic constructor function to build the Applicant object and instantialize basic global variables
    def __init__(self, app_info_str):
        self.app_id = app_info_str[0:5]
        self.gender = app_info_str[5:6]
        self.age = int(app_info_str[6:9])
        self.pets = app_info_str[9:10]
        self.med_cond = app_info_str[10:11]
        self.car = app_info_str[11:12]
        self.dl = app_info_str[12:13]
        self.days_reqd = list()

        # Build the required week days list
        for x in app_info_str[13:20]:
            self.days_reqd.append(int(x))

        # Check LAHSA compliance and add applicant IDs to the global set
        if self.gender == "F" and self.pets == "N" and self.age > 17:
            self.lahsa_eligible = True
            lahsa_compliant_applicants.add(self.app_id)
        else:
            self.lahsa_eligible = False

        # Check SPLA compliance and add applicant IDs to the global set
        if self.med_cond == "N" and self.car == "Y" and self.dl == "Y":
            self.spla_eligible = True
            spla_compliant_applicants.add(self.app_id)
        else:
            self.spla_eligible = False

        # Returns the full applicant information string
        def get_full_str(self):
            return self.app_str

        # Returns the ID details substring
        def get_id(self):
            return self.app_str[:5]

        # Returns the gender details substring
        def get_gender(self):
            return self.app_str[5:6]

        # Returns the age details substring
        def get_age(self):
            return int(self.app_str[6:9])

        # Checks if the applicant has pets
        def has_pets(self):
            return "Y" == self.app_str[9:10]

        # Checks if the applicant has medical conditions
        def has_med_cond(self):
            return "Y" == self.app_str[10:11]

        # Checks if the applicant has a car
        def has_car(self):
            return "Y" == self.app_str[11:12]

        # Checks if the applicant has a driving license
        def has_dl(self):
            return "Y" == self.app_str[12:13]

        # Returns the week details substring
        def get_week_str(self):
            return self.app_str[13:20]

        # Util function to get the number of days requested by applicant
        def get_days_count(self):
            return self.app_str[13:20].count("1")

        # Checks if the applicant is compliant with SPLA constraints
        def is_spla_compliant(self):
            return "Y" == self.app_str[11:12] and "Y" == self.app_str[12:13] and "N" == self.app_str[10:11]

        # Checks if the applicant is compliant with LAHSA constraints
        def is_lahsa_compliant(self):
            return "N" == self.app_str[9:10] and "F" == self.app_str[5:6] and int(self.app_str[6:9]) > 17

        # Util function to simply display the compliance type
        def show_compliance(self):
            comp = ""
            if self.spla_compliance:
                comp += "SPLA "
            if self.lahsa_compliance:
                comp += "LAHSA "
            return comp

        # Simple one-liner string notation of all the attributes the applicant object holds
        def to_string_one_liner(self):
            return "[App Str : " + self.get_full_str() + " | ID: " + self.get_id() + " | Gender: " \
                   + self.get_gender() + " | Age: " + str(self.get_age()) + " | Pets: " + str(self.has_pets()) \
                   + " | Medical: " + str(self.has_med_cond()) + " | Car: " + str(self.has_car()) + " | DL : " \
                   + str(self.has_dl()) + " | Days: " + self.get_week_str() + " | DayCount: " + str(
                self.get_days_count()) \
                   + " | Compliance: " + self.show_compliance() + "]"

        # Simple string notation of all the attributes the applicant object holds
        def to_string(self):
            return "\nApp Str : " + self.get_full_str() + "\n\tID: " + self.get_id() + "\n\tGender: " \
                   + self.get_gender() + "\n\tAge: " + str(self.get_age()) + "\n\tPets: " + str(self.has_pets()) \
                   + "\n\tMedical: " + str(self.has_med_cond()) + "\n\tCar: " + str(self.has_car()) + "\n\tDL : " \
                   + str(
                self.has_dl()) + "\n\tDays: " + self.get_week_str() + "\n\tCompliance: " + self.show_compliance()


# This function checks the viability of the applicant, whether an applicant can be fit into the available slots
def is_applicant_viable(available_slots, days_reqd):
    for i in xrange(7):
        if days_reqd[i] == 1 and available_slots[i] == 0:
            return False
    return True


# This function adds a applicant and returns back the number of slots now being added
def add_applicant_slots(available_slots, days_reqd):
    slots_added = 0
    for i in xrange(7):
        slots_added += days_reqd[i]
        available_slots[i] -= days_reqd[i]
    return slots_added


# This function checks if all the remaining applicants are viable (without actually assigning them) and also return
# back the lowest applicant ID of all the unvisited unviable applicants
def all_remaining_applicants_viable(compliant_applicants, appl_days_reqd_dict, assigned_slots_count,
                                    available_slots, visited_applicants):
    available_slots_copy = [0] * 7
    for d in xrange(7):
        available_slots_copy[d] = available_slots[d]

    for app_id in compliant_applicants:
        lowest_app_id = "9999999"

        # If the applicants is already visited
        if app_id in visited_applicants:
            continue

        # Is the applicant able to fit in the current available slots, if yes, simply add the number of 1's to the
        # assigned slots counter
        if is_applicant_viable(available_slots_copy, appl_days_reqd_dict[app_id]):
            assigned_slots_count += appl_days_reqd_dict[app_id].count(1)
            available_slots_copy = [p_i - d_i for p_i, d_i in zip(available_slots_copy, appl_days_reqd_dict[app_id])]
            if app_id < lowest_app_id:
                lowest_app_id = app_id
        else:

            # return -1 if not all the remaining applicants are viable in the available slots
            return -1, "NA"
    return assigned_slots_count, lowest_app_id


# This function reverses the impact of having added a applicant and returns back the number of slots now becoming vacant
def remove_applicant_slots(available_slots, days_reqd):
    slots_removed = 0
    for i in xrange(7):
        slots_removed += days_reqd[i]
        available_slots[i] += days_reqd[i]
    return slots_removed


# This function initializes the parking or the beds available slots for the pre-assigned applicants
def init_pre_assigned_applicants(init_appl_list, curr_slots_status, app_week_dict):
    slots_assigned = 0
    for app_id in init_appl_list:
        slots_assigned += add_applicant_slots(curr_slots_status, app_week_dict[app_id])
    return slots_assigned


# This function simply flips the player from SPLA(max) to LAHSA(min)
def toggle_player(player_state):
    if player_state == 1:
        return -1               # returns LAHSA
    elif player_state == -1:
        return 1                # returns SPLA


# This function reads the input file and parses the input and populates the required variables
def parse_input():

    # Reading from the input file
    input_fh = open(INPUT_FILE, 'r')

    # Setting the beds count
    beds = int(input_fh.readline())

    # Setting the parking count
    parking_spaces = int(input_fh.readline())

    # Reading the pre assigned LAHSA count
    pre_assigned_lahsa_count = int(input_fh.readline())
    pre_assigned_lahsa_applicants = list()

    # Reading and saving pre assigned LAHSA applicants
    for x in xrange(pre_assigned_lahsa_count):
        pre_assigned_lahsa_applicants.append(input_fh.readline().rstrip())

    # Reading the pre assigned SPLA count
    pre_assigned_spla_count = int(input_fh.readline())
    pre_assigned_spla_applicants = list()

    # Reading and saving pre assigned SPLA applicants
    for x in xrange(pre_assigned_spla_count):
        pre_assigned_spla_applicants.append(input_fh.readline().rstrip())

    # Reading the all applicants count
    all_applicants_count = int(input_fh.readline())
    all_applicants_info_list = list()

    # Reading and saving all the applicant information in a list of Applicant objects
    for x in xrange(all_applicants_count):
        appl_info = input_fh.readline()
        all_applicants_info_list.append(Applicant(appl_info))

    # Creating a new dict to hold the applicant IDs and their respective daily requirement list
    appl_days_reqd_dict = OrderedDict()
    for x in all_applicants_info_list:
        appl_days_reqd_dict[x.app_id] = x.days_reqd

    # Calling the game-play initialization function
    best_next_move = init_maximax(
        appl_days_reqd_dict,                # Applicants daily requirements dict
        pre_assigned_lahsa_applicants,      # List of pre-assigned LAHSA applicants
        pre_assigned_spla_applicants,       # List of pre-assigned SPLA applicants
        beds,                               # Beds slots count
        parking_spaces                      # Parking slots count
    )

    # Writing output to file
    f_out = open("./output.txt", "w")
    f_out.write(str(best_next_move))
    f_out.close()


# This function initializes the data structures needed for the recursive mini-max game play function
def init_maximax(appl_days_reqd_dict, pre_assigned_lahsa_applicants,
                pre_assigned_spla_applicants, beds_count, parking_count):

    # Creating an initial state of parking slots
    parking_slots_state = [parking_count] * 7

    # Creating an initial state of beds slots
    bed_slots_state = [beds_count] * 7

    # Setting the initial best move ID
    best_move_id = "NA"

    # Set the initial maximum SPLA utility value
    max_spla_utility = 0

    # Set the initial visited applicants sets as empty
    visited_applicants = set()

    # Add the pre assigned applicants into the visited applicants set
    visited_applicants.update(pre_assigned_lahsa_applicants)
    visited_applicants.update(pre_assigned_spla_applicants)

    # Assigning the pre-assigned candidates and updating the assigned slots counts
    assigned_parking_count = init_pre_assigned_applicants(
                                pre_assigned_spla_applicants,   # List of pre-assigned SPLA applicants
                                parking_slots_state,            # Current parking slots state
                                appl_days_reqd_dict             # Applicants daily requirements dict
                            )
    assigned_beds_count = init_pre_assigned_applicants(
                                pre_assigned_lahsa_applicants,  # List of pre-assigned LAHSA applicants
                                bed_slots_state,                # Current beds slots state
                                appl_days_reqd_dict             # Applicants daily requirements dict
                            )

    # Iterating through all applicants
    for app_id, days_reqd in appl_days_reqd_dict.items():
        # Check if applicant is already visited or not, and skip over if already visited
        if app_id in visited_applicants:
            continue

        # Check if applicant is SPLA complaint and also is assigning this applicant is viable
        if app_id in spla_compliant_applicants and is_applicant_viable(parking_slots_state, days_reqd):

            # Marking applicant as visited
            visited_applicants.add(app_id)

            # Make the recursive call to the next player with the updated parking/beds states and utility values
            unwound_spla_utility, unwound_lahsa_utility, unwound_app_id = run_maximax(
                                appl_days_reqd_dict,            # Applicants daily requirements dict
                                visited_applicants,             # Visited applicants
                                [p_i - d_i for p_i, d_i in zip(parking_slots_state, appl_days_reqd_dict[app_id])],            # The updated state of the parking slots
                                bed_slots_state,                # The updated state of the beds slots
                                assigned_parking_count + appl_days_reqd_dict[app_id].count(1),         # The count of parking slots already assigned
                                assigned_beds_count,            # The count of beds slots already assigned
                                False,                             # Player type
                                str(app_id)                     # Visited path variable track
                            )

            # Update the local maximising variable and the corresponding child applicant ID
            if unwound_spla_utility > max_spla_utility:
                max_spla_utility = unwound_spla_utility
                best_move_id = app_id

            # Mark the applicant as available / not visited
            visited_applicants.remove(app_id)

    print "BEST NEXT MOVE | Gives maximum utility: [ " + str(max_spla_utility) + " ] " \
                    "when [ "+str(best_move_id) + " ] chosen"

    return best_move_id


# This is the primary recursive game playing function
def run_maximax(appl_days_reqd_dict, visited_applicants, parking_slots_state, bed_slots_state,
                assigned_parking_count, assigned_beds_count, player, visited_path):

    # Player is SPLA
    if player:

        # Flag to check whether no more SPLA applicants are viable to fit and compliant
        no_spla_applicant_fit = True

        # Setting the maximum values for the inner iteration
        max_spla_utility = assigned_parking_count
        max_lahsa_utility = assigned_beds_count
        max_app_id = 100000

        # Set to keep track of all unviable applicants every iteration
        unviable_spla_applicants = set()

        # Iterating through all applicants which are SPLA applicants
        for app_id in spla_compliant_applicants.copy():

            # Check if applicant is already visited or not, and skip over if already visited
            if app_id in visited_applicants:
                continue

            # Check if the applicant is viable to be fit in the available slots
            if is_applicant_viable(parking_slots_state, appl_days_reqd_dict[app_id]):

                # Marking applicant as visited
                visited_applicants.add(app_id)

                # Set the flag as false, as LAHSA is not exhausted, there is at least this one applicant who was able to
                # be fit in this turn of recursion
                no_spla_applicant_fit = False

                # Setting the max applicant ID to the ID for this iteration
                max_app_id = app_id

                # Make the recursive call to the next player with the updated parking/beds states and utility values
                unwound_spla_utility, unwound_lahsa_utility, unwound_app_id = run_maximax(
                    appl_days_reqd_dict,                # Applicants daily requirements dict
                    visited_applicants,                 # Visited applicants
                    [p_i - d_i for p_i, d_i in zip(parking_slots_state, appl_days_reqd_dict[app_id])],    # The updated state of the parking slots
                    bed_slots_state,                    # The updated state of the beds slots
                    assigned_parking_count + appl_days_reqd_dict[app_id].count(1),
                    assigned_beds_count,                # The count of beds slots already assigned
                    not player,              # Toggles the player
                    visited_path + " | " + str(app_id)  # Visited path variable track
                )

                # Update the local maximising variable and the corresponding child applicant ID if the recursion
                # returned back a higher value or in case the value returned was equal, but the child applicant ID
                # was smaller than the local child applicant ID
                if unwound_spla_utility > max_spla_utility or \
                        (unwound_spla_utility == max_spla_utility and max_app_id > unwound_app_id):
                    max_spla_utility = unwound_spla_utility
                    max_lahsa_utility = unwound_lahsa_utility
                    max_app_id = unwound_app_id

                # Mark the applicant as available / not visited
                visited_applicants.remove(app_id)

            # If the applicant is not viable
            else:

                # Remove from the global set of compliant applicants while going deeper in the recursion
                spla_compliant_applicants.remove(app_id)

                # Add the applicant ID to the unviable tracking set (at every depth level)
                unviable_spla_applicants.add(app_id)

        # Checks if SPLA applicant are exhausted, that is was even one SPLA applicant who got assigned or not
        # If not, then we need to continue our game play with LAHSA
        if no_spla_applicant_fit and len(lahsa_compliant_applicants) > 0:

            # Fetch the possible utility value gain if all LAHSA compliant applicants can all be fit / are all viable
            potential_utility_gain, lowest_app_id = all_remaining_applicants_viable(
                                                            lahsa_compliant_applicants,
                                                            appl_days_reqd_dict,
                                                            assigned_beds_count,
                                                            bed_slots_state,
                                                            visited_applicants
                                                        )

            # If the gain is some positive value, means all the remaining applicants can be placed, simply return
            # back the new gained value as SPLA's utility and randomly any one of the applicant ID from the global
            # applicant set as the game tree from here below is just going to be permutations
            if potential_utility_gain > -1:

                # Restore the global compliant set post teh deeper recursion call to
                # now begin the outer most sibling call
                spla_compliant_applicants.update(unviable_spla_applicants)

                return max_spla_utility, potential_utility_gain, lowest_app_id

            # If all the remaining applicants cant be fit, simply continue playing the game for SPLA alone
            else:

                # Make the recursive call to the next player with the existing parking/beds states and utility values
                max_spla_utility, max_lahsa_utility, max_app_id = run_maximax(
                    appl_days_reqd_dict,  # Applicants daily requirements dict
                    visited_applicants,  # Visited applicants
                    parking_slots_state,  # The current state of the parking slots
                    bed_slots_state,  # The current state of the beds slots
                    assigned_parking_count,  # The count of parking slots already assigned
                    assigned_beds_count,  # The count of beds slots already assigned
                    not player,  # Toggles the player
                    visited_path + " | " + "DUMMY"  # Visited path variable track
                )

                # Restore the global compliant set post teh deeper recursion call to
                # now begin the outer most sibling call
                spla_compliant_applicants.update(unviable_spla_applicants)

                return max_spla_utility, max_lahsa_utility, max_app_id

        # Restore the global compliant set post teh deeper recursion call to now begin the outer most sibling call
        spla_compliant_applicants.update(unviable_spla_applicants)

        return max_spla_utility, max_lahsa_utility, max_app_id

    # Player is LAHSA
    else:
        # Flag to check whether no more LAHSA applicants are viable to fit and compliant
        no_lahsa_applicant_fit = True

        # Setting the maximum values for the inner iteration
        max_lahsa_utility = assigned_beds_count
        max_spla_utility = assigned_parking_count
        max_app_id = 100000

        # Set to keep track of all unviable applicants every iteration
        unviable_lahsa_applicants = set()

        # Iterating through all applicants which are LAHSA applicants
        for app_id in lahsa_compliant_applicants.copy():

            # Check if applicant is already visited or not, and skip over if already visited
            if app_id in visited_applicants:
                continue

            # Check if the applicant is viable to be fit in the available slots
            if is_applicant_viable(bed_slots_state, appl_days_reqd_dict[app_id]):

                # Set the flag as false, as LAHSA is not exhausted, there is at least this one applicant who was able to
                # be fit in this turn of recursion
                no_lahsa_applicant_fit = False

                # Marking applicant as visited
                visited_applicants.add(app_id)

                # Setting the max applicant ID to the ID for this iteration
                max_app_id = app_id

                # Make the recursive call to the next player with the updated parking/beds states and utility values
                unwound_spla_utility, unwound_lahsa_utility, unwound_app_id = run_maximax(
                    appl_days_reqd_dict,                # Applicants daily requirements dict
                    visited_applicants,                 # Visited applicants
                    parking_slots_state,                # The updated state of the parking slots
                    [b_i - d_i for b_i, d_i in zip(bed_slots_state, appl_days_reqd_dict[app_id])],                    # The updated state of the beds slots
                    assigned_parking_count,             # The count of parking slots already assigned
                    assigned_beds_count + appl_days_reqd_dict[app_id].count(1),                # The count of beds slots already assigned
                    not player,              # Toggles the player
                    visited_path + " | " + str(app_id)  # Visited path variable track
                )

                # Update the local maximising variable and the corresponding child applicant ID if the recursion
                # returned back a higher value or in case the value returned was equal, but the child applicant ID
                # was smaller than the local child applicant ID
                if unwound_lahsa_utility > max_lahsa_utility or \
                        (unwound_lahsa_utility == max_lahsa_utility and max_app_id > unwound_app_id):
                    max_lahsa_utility = unwound_lahsa_utility
                    max_spla_utility = unwound_spla_utility
                    max_app_id = unwound_app_id

                # Mark the applicant as available / not visited
                visited_applicants.remove(app_id)

            # If the applicant is not viable
            else:

                # Add the applicant ID to the unviable tracking set (at every depth level)
                unviable_lahsa_applicants.add(app_id)

                # Remove from the global set of compliant applicants while going deeper in the recursion
                lahsa_compliant_applicants.remove(app_id)

        # Checks if LAHSA applicant are exhausted, that is was even one LAHSA applicant who got assigned or not
        # If not, then we need to continue our game play with SPLA
        if no_lahsa_applicant_fit and len(spla_compliant_applicants) > 0:
            '''
            # Make the recursive call to the next player with the existing parking/beds states and utility values
            return run_maximax(
                        appl_days_reqd_dict,                #
                        visited_applicants,                 #
                        parking_slots_state,                #
                        bed_slots_state,                    #
                        assigned_parking_count,             #
                        assigned_beds_count,                #
                        toggle_player(player),              #
                        visited_path + " | " + str(app_id)  #
                    )
            '''

            # Fetch the possible utility value gain if all SPLA compliant applicants can all be fit / are all viable
            potential_utility_gain, lowest_app_id = all_remaining_applicants_viable(
                                                spla_compliant_applicants,
                                                appl_days_reqd_dict,
                                                assigned_parking_count,
                                                parking_slots_state,
                                                visited_applicants
                                            )

            # If the gain is some positive value, means all the remaining applicants can be placed, simply return
            # back the new gained value as SPLA's utility and randomly any one of the applicant ID from the global
            # applicant set as the game tree from here below is just going to be permutations
            if potential_utility_gain > -1:

                # Restore the global compliant set post teh deeper recursion call to
                # now begin the outer most sibling call
                lahsa_compliant_applicants.update(unviable_lahsa_applicants)

                return potential_utility_gain, max_lahsa_utility, lowest_app_id

            # If all the remaining applicants cant be fit, simply continue playing the game for SPLA alone
            else:

                # Make the recursive call to the next player with the existing parking/beds states and utility values
                max_spla_utility, max_lahsa_utility, max_app_id = run_maximax(
                    appl_days_reqd_dict,            # Applicants daily requirements dict
                    visited_applicants,             # Visited applicants
                    parking_slots_state,            # The current state of the parking slots
                    bed_slots_state,                # The current state of the beds slots
                    assigned_parking_count,         # The count of parking slots already assigned
                    assigned_beds_count,            # The count of beds slots already assigned
                    not player,          # Toggles the player
                    visited_path + " | " + "DUMMY"  # Visited path variable track
                )
                # Restore the global compliant set post teh deeper recursion call to
                # now begin the outer most sibling call
                lahsa_compliant_applicants.update(unviable_lahsa_applicants)

                return max_spla_utility, max_lahsa_utility, max_app_id

        # Restore the global compliant set post teh deeper recursion call to now begin the outer most sibling call
        lahsa_compliant_applicants.update(unviable_lahsa_applicants)

        return max_spla_utility, max_lahsa_utility, max_app_id


# This is where the code begins.... by parsing the input
parse_input()