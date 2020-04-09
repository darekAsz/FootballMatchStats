import os
import pandas as pd


# read every csv file, get teams name and return list of them
def get_list_of_teams():
    csv_directory = os.path.join(os.getcwd(), 'csv_files')
    csv_files = os.listdir(csv_directory)
    reading_lines_number = 21  # read 21 rows to avoid missing team because moving date of match

    teams_list = []
    for file in csv_files:
        your_file = pd.read_csv(os.path.join(csv_directory, file), nrows=reading_lines_number)
        # read home and away teams to avoid missing team because playing 2 matches in row as home/away team
        teams = your_file["HomeTeam"]
        teams_list.extend(teams.array)
        teams = your_file["AwayTeam"]
        teams_list.extend(teams.array)

    # get list with unique names
    names = []
    for team in teams_list:
        if team not in names:
            names.append(team)
    names.sort()
    return names
