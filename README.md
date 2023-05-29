# TournamentSimulator
"""

The tournament simulator is designed to generate possible outcomes of seeded tournaments submitted by the user. 

I was inspired to build the tournament simulator after watching the NCAA March Madness tournament in 2023 alongside taking a probability and statistics class at my college. While watching the tournament, it was fascinating for me to try and figure out who was going to beat who only to be shocked after watching the games. There are so many ways that things can pan out and I wanted to build something that would help me visualize that by combining my passions for probability and programming.

The tournament simulator begins by asking the user to enter the total number of teams to be included in the bracket to be, choosing from the numbers 2, 4, 8, 16, 32, 64, 128, and 256, all of which would result in an evenly distributed bracket. If the user were to enter a different value, it would be disregarded via input validation and the user would be re-prompted. After one of the number listed is entered by the user, the user is prompted to enter the lowest seed in the bracket. The lowest seed is defined as the number farthest from 1 that is given to a team in the bracket, designating them as the "worst team." The lowest seed must be greater than 1 and go into the total number of teams evenly, so the user is re-prompted via input validation should they enter an improper value.

After the total number of teams and lowest seed have been confirmed, the user is asked to enter the name of the file containing the teams and their seeds in a specified format and order. Using an exception handler, the program checks to confirm that the file exists. If it does, the program opens the file and verifies (again through a loop validation structure) that there are enough teams, no overused seeds, no duplicate teams, and that all seeds and names are in proper format. The user is re-prompted if any of the above conditions fail. If all of these conditions are met, the user is asked to choose from 4 levels of "randomness" for the tournament:

                                                 - 1: The better seeded teams are heavily favored
                                                 - 2: The better seeded teams are moderately favored
                                                 - 3: The better seeded teams are slightly favored
                                                 - 4: Every game is a 50/50 shot
                            
After it has been confirmed that the user entered 1, 2, 3, or 4, the bracket is generated. Round by round, game by game, the results of each matchup are displayed for the user to see all the way up to the championship game. This is done through a process where the teams and seeds from the user's file are entered into an OrderedDict and two teams at a time are sent to a game simulator funtion that uses the specified 1-4 option alongside a weighted seed difference to determine individual probabilities (referred to as scale factors in the program). A random number 1-100 is then generated and if it is less than or equal to the scale factor, the favorite team advances. If the random number is greater (less likely), the underdog advances.            

After all games including the championship have been simulated and printed, the programs prints the champion, runner up (second placer), and reveals how many different brackets results could've been generated using the same teams in the same initial setup.

Additional comments and explanations are available to read in the BracketFiller file.

"""
