from app import db
from csv_reader import get_list_of_teams
import os
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
import datetime

##########
# Date = Date of match
# FTHG = Full Time Home Team Goals
# FTAG = Full Time Away Team Goals
# FTR = Full Time Result (H=Home Win, D=Draw, A=Away Win)
# HTHG = Half Time Home Team Goals
# HTAG = Half Time Away Team Goals
# HTR = Half Time Result
# HS = Home Team Shots
# AwS = Away Team Shots
# HST = Home Team Shots on Target
# AST = Away Team Shots on Target
# HF = Home Team Fouls Committed
# AF = Away Team Fouls Committed
# HC = Home Team Corners
# AC = Away Team Corners
# HY = Home Team Yellow Cards
# AY = Away Team Yellow Cards
# HR = Home Team Red Cards
# AR = Away Team Red Cards


match_columns = {
    "Date": "Date of match",
    "FTHG": "Full Time Home Team Goals",
    "FTAG": "Full Time Away Team Goals",
    "FTR": "Full Time Result (H=Home Win, D=Draw, A=Away Win)",
    "HTHG": "Half Time Home Team Goals",
    "HTAG": "Half Time Away Team Goals",
    "HTR": "Half Time Result",
    "HS": "Home Team Shots",
    "AwS": "Away Team Shots",
    "HST": "Home Team Shots on Target",
    "AST": "Away Team Shots on Target",
    "HF": "Home Team Fouls Committed",
    "AF": "Away Team Fouls Committed",
    "HC": "Home Team Corners",
    "AC": "Away Team Corners",
    "HY": "Home Team Yellow Cards",
    "AY": "Away Team Yellow Cards",
    "HR": "Home Team Red Cards",
    "AR": "Away Team Red Cards"
}


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    home = db.relationship('Match', backref='home', lazy='dynamic', foreign_keys='Match.home_team')
    away = db.relationship('Match', backref='away', lazy='dynamic', foreign_keys='Match.away_team')

    def __repr__(self):
        return '<Team {}>'.format(self.name)


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.String(64))
    start_date = db.Column(db.String(64))
    end_date = db.Column(db.String(64))

    def __repr__(self):
        return '<Season {}>'.format(self.season)

    def __init__(self, season, start, end):
        self.season = season
        self.start_date = start
        self.end_date = end


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)  # TODO: make date type date
    home_team = db.Column(db.Integer, db.ForeignKey('team.id'))
    away_team = db.Column(db.Integer, db.ForeignKey('team.id'))
    FTHG = db.Column(db.Integer)
    FTAG = db.Column(db.Integer)
    FTR = db.Column(db.CHAR(1))
    HTHG = db.Column(db.Integer)
    HTAG = db.Column(db.Integer)
    HTR = db.Column(db.CHAR(1))
    Referee = db.Column(db.String(64))
    HS = db.Column(db.Integer)
    AwS = db.Column(db.Integer)
    HST = db.Column(db.Integer)
    AST = db.Column(db.Integer)
    HF = db.Column(db.Integer)
    AF = db.Column(db.Integer)
    HC = db.Column(db.Integer)
    AC = db.Column(db.Integer)
    HY = db.Column(db.Integer)
    AY = db.Column(db.Integer)
    HR = db.Column(db.Integer)
    AR = db.Column(db.Integer)

    def __repr__(self):
        return '<Match {}>'.format(self.season)  # TODO: change format

    # TODO: check if all should be none
    def __init__(self, date, home_team, away_team, fthg=None, ftag=None, ftr=None, hthg=None, htag=None, htr=None,
                 referee=None, hs=None, aws=None, hst=None, ast=None, hc=None, ac=None, hf=None, af=None, hy=None,
                 ay=None, hr=None, ar=None):
        self.date = date
        self.home_team = home_team
        self.away_team = away_team
        self.FTHG = fthg
        self.FTAG = ftag
        self.FTR = ftr
        self.HTHG = hthg
        self.HTAG = htag
        self.HTR = htr
        self.Referee = referee
        self.HS = hs
        self.AwS = aws
        self.HST = hst
        self.AST = ast
        self.HC = hc
        self.AC = ac
        self.HF = hf
        self.AF = af
        self.HY = hy
        self.AY = ay
        self.HR = hr
        self.AR = ar


def fill_teams_table():
    teams_list = get_list_of_teams()
    for team in teams_list:
        db.session.add(Team(name=team))
    db.session.commit()


def fill_season_table():
    seasons = [
        Season('08/09', '16/08/08', '24/05/09'),
        Season('09/10', '15/08/09', '09/05/10'),
        Season('10/11', '14/08/10', '22/05/11'),
        Season('11/12', '13/08/11', '13/05/12'),
        Season('12/13', '18/08/12', '19/05/13'),
        Season('13/14', '17/08/13', '11/05/14'),
        Season('14/15', '16/08/14', '24/05/15'),
        Season('15/16', '08/08/15', '17/05/16'),
        Season('16/17', '13/08/16', '21/05/17'),
        Season('17/18', '11/08/17', '13/05/18'),
        Season('18/19', '10/08/18', '12/05/19'),
        Season('19/20', '09/08/19', '09/03/20')
    ]
    for season in seasons:
        db.session.add(Season(season.season, season.start_date, season.end_date))
    db.session.commit()


def fill_match_table():
    csv_directory = os.path.join(os.getcwd(), 'csv_files')
    csv_files = os.listdir(csv_directory)
    for file in csv_files:
        reader = pd.read_csv(os.path.join(csv_directory, file))
        for index, row in reader.iterrows():
            try:
                home_team_id = Team.query.filter_by(name=row["HomeTeam"]).first().id
                away_team_id = Team.query.filter_by(name=row["AwayTeam"]).first().id
                date = row["Date"][:6] + '20' + row["Date"][6:]
                time = datetime.datetime.strptime(date, "%d/%m/%Y")
                record = Match(time, home_team_id, away_team_id, row["FTHG"], row["FTAG"], row["FTR"], row["HTHG"],
                               row["HTAG"], row["HTR"], row["Referee"], row["HS"], row["AS"], row["HST"], row["AST"],
                               row["HF"], row["AF"], row["HC"], row["AC"], row["HY"], row["AY"], row["HR"], row["AR"])
                db.session.add(record)
            except KeyError:
                db.session.rollback()
                print("Cannot add record - invalid key")
            except SQLAlchemyError as e:
                db.session.rollback()
                error = str(e.__dict__['orig'])
                print("Database error: ", error)
        db.session.commit()


def init_db(db_uri):
    if not os.path.isfile(db_uri):
        db.create_all()
        # TODO: check if table exist
        fill_teams_table()
        fill_season_table()
        fill_match_table()
