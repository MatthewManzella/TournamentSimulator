import random
import sys
from collections import OrderedDict


def main():
    """
    Prompts the user to enter the number of total teams in the bracket, the lowest seed, and the file containing
    the teams. The teams and seeds are then read into dict_teams for storage and correlation in the format
    team_name: seed. The user is then asked to pick option 1, 2, 3, or 4 for randomization and then bracket_simulator
    is called to play the tournament.
    """
    print("\nWELCOME TO THE TOURNAMENT SIMULATOR!\n")
    dict_teams = OrderedDict()
    # num_of_teams = total number of teams to be put into bracket.
    num_of_teams = get_teams()
    # lowest_seed = the seed of the worst team(s) listed.
    lowest_seed = get_lowest_seed(num_of_teams)
    # file_path = absolute path to file with teams inside.
    file_path = get_file(num_of_teams, lowest_seed)
    file = open(file_path, 'r')
    # Starts dict_teams (see comment below).
    line = file.readline().split(":")
    dict_teams[line[1].strip()] = line[0]
    # Adds key(team name)/value(seed) pairs to dict_teams by manipulating each individual line in the file using
    # .split(":") to separate the team name and seed as well as .strip('\n') to get rid of newline characters.
    while len(line) != 0:
        try:
            line = file.readline().split(":")
            dict_teams[line[1].strip()] = line[0]
        except IndexError:
            break
    file.close()
    # Asks user to pick option 1, 2, 3, or 4 for randomization.
    user_pick = 0
    while user_pick not in ["1", "2", "3", "4"]:
        print("\nOPTIONS:\n- 1: The better seeded teams are heavily favored\n- 2: The better seeded teams are"
              " moderately favored\n- 3: The better seeded teams are slightly favored\n- 4: Every game is a 50/50 shot")
        user_pick = input("\nPick your level of randomization (1, 2, 3, or 4): ")
        if user_pick not in ["1", "2", "3", "4"]:
            print("\nERROR. Please type 1, 2, 3, or 4")
    # Sends dict_teams to the options function chosen by the user.
    bracket_simulator(dict_teams, int(user_pick), lowest_seed)
    print(f"\nThis is one of {2 ** (num_of_teams-1)} possible brackets that could've been generated with these"
          f" teams!")


def get_teams():
    """
    Asks user for number of teams to be put into bracket and verifies that the number
    is valid (number must be in total_teams_list) via input validation.

    :return: num_of_teams: Total number of teams to be put into the bracket.
    :rtype: int
    """
    num_of_teams = 0
    total_teams_list = (2, 4, 8, 16, 32, 64, 128, 256)
    # Will ask user to re-enter value until a number from total_teams_list is entered.
    while num_of_teams not in total_teams_list:
        print("\nOPTIONS: 2, 4, 8, 16, 32, 64, 128, 256")
        num_of_teams = input("How many teams total in the bracket? (Pick a number from above): ")
        if not num_of_teams.isdigit():
            print("\nERROR. Please give a number from the options list.")
        elif int(num_of_teams) not in total_teams_list:
            print("\nERROR. Please give a number from the options list.")
        else:
            num_of_teams = int(num_of_teams)
    return num_of_teams


def get_lowest_seed(num_of_teams):
    """
    Asks user for the lowest seed in the bracket so that teams can be ordered properly.
    Ex: A bracket of 64 in March Madness format has a "lowest seed" of 16 - the four lowest ranked
    teams are seeded 16.

    :param: num_of_teams: Total number of teams to be put into the bracket.

    :return: lowest_seed: The seed of the worst team(s) listed.
    :rtype: int
    """
    lowest_seed = 1
    # Will ask user to re-enter value until a number that num_of_teams is divisible by is entered.
    while num_of_teams % int(lowest_seed) != 0 or int(lowest_seed) == 1:
        print(f"\nNUMBER OF TEAMS: {num_of_teams}")
        lowest_seed = input("What is the lowest (worst) seed in your bracket? ")
        if not lowest_seed.isdigit() or lowest_seed == "0":
            print("\nERROR. Please give a proper number.")
            # lowest_seed set to 1 so that loop is re-entered/no type conversion errors arise.
            lowest_seed = 1
        elif num_of_teams % int(lowest_seed) != 0 or int(lowest_seed) == 1:
            print("\nERROR. Please give a number greater than 1 that goes into the number of teams evenly.")
    return int(lowest_seed)


def get_file(num_of_teams, lowest_seed):
    """
    Asks user for the absolute path to the file containing the list of bracket teams in it and verifies that
    there are enough teams in the file, that the seeds are within the range given, that there
    are no duplicate teams, and that each line is formatted properly.

    :param: num_of_teams: Total number of teams to be put into the bracket.
    :param: lowest_seed: The seed of the worst team(s) listed.

    :return: file_path: Absolute path to the file with teams in it.
    :rtype: str
    """
    file_path = None
    print(
        "\nTIP: Make sure your teams in the file are listed one team to a line (starting from line 1, no empty lines) "
        "and in \norder of when they play the first round so that the bracket is constructed properly.\nList each"
        " team as [insert seed]: team name."
        "\n\nEXAMPLE: \n1: First Team to Play\n16: First Team to Play's Opponent\n8: Second Team to Play\n"
        "9: Second Team to Play's Opponent")
    print("\n\nNOTE: The winner of each of the two games above will face each other in the next round.")
    # Asks user for file path.
    while file_path is None:
        print("\nHINT: Find the absolute path by going to your File Explorer, single-clicking\non the file you "
              "are using, and holding Ctrl + Shift + C at the same time.\nRemove the quotation marks before "
              "submitting it to the Tournament Simulator.")
        file_path = input("\n\nEnter the absolute path to the text file (without quotation marks)"
                          " with your teams listed in it or enter 'no' to quit: ")
        # Exits the program should the user type no.
        if file_path == 'no':
            sys.exit(0)
        # Attempts to open the file and repeatedly prompts the user to re-enter a file path until one with proper
        # format is given (valid file, correct number of teams, correct format on each line, and proper seeding).
        try:
            file = open(file_path, 'r')
            length = calc_length(file)
            file.close()
            if length != num_of_teams:
                print(f"\nERROR. Your file has {length} teams. You previously specified {num_of_teams} teams.")
                print("Please re-enter a new or modified file.")
                file_path = None
            # Checks for correct format on each line and proper seeding.
            elif check_format(file_path, num_of_teams, lowest_seed):
                file_path = None
            else:
                return file_path
        except OSError or Exception:
            print("ERROR. Enter a valid file name.")
            file_path = None


def calc_length(file):
    """
    Calculates the number of non-empty lines in the file being measured.

    :param: file: The file path of the file being measured.

    :return: length: The number of non-empty lines in the file.
    :rtype: int
    """
    length = 0
    line = file.readline()
    while len(line) != 0:
        # Strips the line of any leading/trailing whitespace.
        line = line.strip()
        # Verifies that the line isn't blank.
        if len(line) != 0:
            length += 1
        line = file.readline()
    return length


def check_format(file_path, num_of_teams, lowest_seed):
    """
    Verifies that the seeds are within the range given, that each line is
    formatted properly ([insert seed]: team name), and that there are no
    duplicate teams.

    :param: file_path: The path to the file being checked.
    :param: num_of_teams: Total number of teams to be put into the bracket.
    :param: lowest_seed: The seed of the worst team(s) listed.

    :return: False/True: False if the format is proper, True if it is not.
    :rtype: bool
    """
    # Opens the file and creates a list for all seeds to be stored in.
    file = open(file_path, 'r')
    line = file.readline()
    seed_list = []
    team_list = []
    while len(line) != 0:
        # Strips the line of any leading/trailing whitespace.
        line = line.strip()
        # Verifies that the line isn't blank.
        if len(line) != 0:
            if ":" in line:
                # Returns True/exits function if ":" is the last character in the line (indicates no name is present)
                if ":" == line[-1]:
                    print("ERROR. Make sure every team has a name.")
                    return True
                else:
                    # Adds the team name from each line to team_list if it is not already in there. If it is already
                    # in there, the function returns True because duplicate names are not allowed.
                    if line[line.index(":"): -1] not in team_list:
                        team_list.append(line[line.index(":"):])
                    else:
                        print(line[line.index(":"):])
                        print("ERROR. Make sure every team has a different name.")
                        return True
                seed = line[0: line.index(":")]
                # Attempts to add the seed to seed_list, returns True/ exits function if the seed is improper.
                try:
                    if 1 <= int(seed) <= lowest_seed:
                        seed_list.append(int(seed))
                except ValueError:
                    print("ERROR. Make sure your teams are in the format [insert seed]: team name.")
                    return True
        line = file.readline()
    # Checks to make sure that the length of the seed_list equals the number of teams and that no seed is used too
    # often.
    file.close()
    if len(seed_list) == num_of_teams and sorted(seed_list) == sorted(
            list(range(1, lowest_seed + 1)) * int(num_of_teams / lowest_seed)):
        return False
    else:
        print(f"ERROR. Make sure your teams are in the format [insert seed]: team name and that your lowest seed is "
              f"{lowest_seed} as previously specified.")
        return True


def bracket_simulator(dict_teams, option, lowest_seed):
    """
    Simulates the bracket by putting teams from team_list against each other in select matchups and
    subsequently deleting the loser. This is done until one team remains.

    :param: dict_teams: Dictionary in the format {team_name : seed #}.
    :param: option: The option (1, 2, 3, or 4) picked by the user.
    :param: lowest_seed: The seed of the worst team(s) in the bracket.
    """
    # Creates a list of the teams in dict_teams as well as a list of the seeds of the teams in dict_teams.
    team_list = list(dict_teams.keys())
    seed_list = list(dict_teams.values())
    # Prints which round of the tournament is being played.
    if len(team_list) >= 16:
        print(f"\n\nROUND OF {len(team_list)}: ")
    elif len(team_list) == 8:
        print("\n\nQUARTERFINALS: ")
    elif len(team_list) == 4:
        print("\n\nSEMIFINALS: ")
    elif len(team_list) == 2:
        print("\n\nCHAMPIONSHIP: ")
    # Simulates each individual game for the round.
    for i in range(0, len(team_list) - 1, 2):
        # Decides which team lost the individual game being simulated via the game_simulator function.
        knocked_out = game_simulator(team_list[i], team_list[i + 1], option, int(seed_list[i]), int(seed_list[i + 1]),
                                     int(lowest_seed))
        # Declares winner of the individual game being simulated as the team not stored in knocked_out.
        if team_list[i] == knocked_out:
            winner = team_list[i + 1]
        else:
            winner = team_list[i]
        # Prints both teams from the game in a bracket shell with the winner included in the next round.
        print(f"\n\n{seed_list[i]}: {team_list[i]}")
        bracket_shell_printer(winner, dict_teams[winner])
        print(f"{seed_list[i + 1]}: {team_list[i + 1]}")
        # Prints the champion and runner-up after the final game.
        if len(team_list) == 2:
            print(f"\n\nCHAMPION: {dict_teams[winner]}: {winner}")
            print(f"RUNNER-UP: {dict_teams[knocked_out]}: {knocked_out}")
        # Deletes the team that was knocked out from dict_teams.
        del (dict_teams[knocked_out])
    # Recursively calls bracket_simulator with the updated dictionary until only one team still stands in the
    # tournament.
    if len(dict_teams) != 1:
        bracket_simulator(dict_teams, option, lowest_seed)


def bracket_shell_printer(winner, seed):
    """
    Prints the rectangular bracket shell for each individual game with the winner and their seed printed
    on a line to the right of the shell.

    :param: winner: The winner of the individual game.
    :param: seed: The seed of the winner of the individual game.
    """
    print(f"--------------------|\n\t\t\t\t\t|\n\t\t\t\t\t|\t{seed}: {winner}\n\t\t\t\t\t|--------------------"
          f"\n\t\t\t\t\t|\n--------------------|")


def game_simulator(team1, team2, option, team1_seed, team2_seed, lowest_seed):
    """
    Simulates each individual game in the tournament using weighted seeding differences and a generated scale
    factor

    :param: team1/team2: The names of the two teams playing.
    :param: option: The option the user picked in the previous menu.
    :param: team1_seed/team2_seed: The seeds of the two teams playing.
    :param: lowest_seed: The seed of the worst team(s) in the bracket.

    :return: team1/team2: The name of the team deemed loser in the simulation.
    :rtype: str
    """
    # Information about team1 stored for later reference.
    team1_contents = [team1, team1_seed]
    # Calculates the percent difference in seeds of the two teams playing (used for generating scale factor).
    weighted_seed_diff = abs(team2_seed - team1_seed) / lowest_seed
    # Figures out which of the two seeds is better (closer to 1).
    better_seed = min(team1_seed, team2_seed)
    # If option 1, 2, or 3 was chosen by the user, a scale factor is generated alongside a random number
    # used for picking a winner based on weighted_seed_diff.
    if option in [1, 2, 3]:
        sf = scale_factor(weighted_seed_diff, option, lowest_seed)
        rand_num = random.randint(1, 100)
        # If the random number (between 1 and 100 inclusive) is less than the scale factor, the team that
        # has the worse seed of the two teams is returned.
        if rand_num <= sf:
            if better_seed in team1_contents:
                return team2
            else:
                return team1
        # If the random number (between 1 and 100 inclusive) is more than the scale factor, the team that
        # has the better seed of the two teams is returned. This is considered an "upset."
        else:
            if better_seed in team1_contents:
                return team1
            else:
                return team2
    # If the user picked option 4 (every game is a 50/50 shot) then either int 1 or 2 is randomly generated and
    # the team (team1 or team2) with that number is returned.
    elif option == 4:
        if random.randint(1, 2) == 1:
            return team1
        else:
            return team2


def scale_factor(difference, option, lowest_seed):
    """
    Determines a scale factor used for deciding which team will win the game being simulated. If the randomly
    generated number (1-100) in game_simulator is below sf, the favorite (better seed) will win but if it is above sf,
    the underdog (lower seed) will win.

    :param: difference: The percent difference in seeds of the two teams playing.
            - Equation = (worse seed - better seed) / lowest seed
    :param: option: The option the user picked in the previous menu.
    :param: lowest_seed: The seed of the worst team(s) in the bracket.

    :return: sf: Scale factor used for deciding who will win the game in game_simulator.
    :rtype: int
    """
    # Determines scale factor based on option and weighted difference. This can be thought of as assigning the
    # better seed a [sf] % chance of winning the individual match-up.
    if option == 1:
        if difference >= .75:
            sf = 99
        elif 0.5 <= difference < 0.75:
            sf = 90
        elif 0.25 <= difference < 0.5:
            sf = 82
        else:
            sf = 75
    elif option == 2:
        if difference >= .75:
            sf = 88
        elif 0.5 <= difference < 0.75:
            sf = 80
        elif 0.25 <= difference < 0.5:
            sf = 72
        else:
            sf = 68
    else:
        if difference >= .75:
            sf = 80
        elif 0.5 <= difference < 0.75:
            sf = 70
        elif 0.25 <= difference < 0.5:
            sf = 55
        else:
            sf = 50
    # Adds 10 to the scale factor if the lowest seed is a 32 or higher. This is to ensure that with a higher variability
    # of teams, the top teams still have a distinct advantage.
    if lowest_seed >= 32:
        sf += 10
    # Subtracts 5 from the scale factor if the option is 1 or 2 and the lowest seed is 8 or smaller. This is to
    # ensure that top teams aren't given a vastly disproportionate advantage.
    elif lowest_seed <= 8:
        if option in [1, 2]:
            sf -= 5
    return sf


if __name__ == '__main__':
    main()

