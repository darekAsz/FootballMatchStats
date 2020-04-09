from flask import render_template, flash, redirect, url_for, request

from app import app
from csv_reader import get_list_of_teams
from .queries import select_matches_scores_for_teams
from .models import match_columns


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    teams_list = get_list_of_teams()
    title = 'One team statistics'
    if request.method == 'GET':
        return render_template('index.html', title=title, teams=teams_list,
                               columns=match_columns, active="index")
    elif request.method == 'POST':
        team = request.form.get('selected_team')
        c = request.form.getlist('selected_columns')
        text = request.form.get('matches_count')
        return render_template('index.html', title=title, teams=teams_list,
                               columns=match_columns, active="index")


@app.route('/teams', methods=['GET', 'POST'])
def teams():
    teams_list = get_list_of_teams()
    if request.method == 'GET':
        return render_template('teams.html', title='Teams', teams=teams_list, active="teams")
    elif request.method == 'POST':
        select_first = request.form.get('selected_team1')
        select_second = request.form.get('selected_team2')
        matches = select_matches_scores_for_teams(select_first, select_second)
        return render_template('teams.html', title='Teams', teams=teams_list, matches=matches, active="teams")
