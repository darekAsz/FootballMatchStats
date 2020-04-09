from .models import Team, Match
from sqlalchemy import or_, and_


def get_id_of_team(team):
    return Team.query.filter(Team.name == team).first().id


def get_matches_for_teams(team1, team2):
    first_team_id = get_id_of_team(team1)
    second_team_id = get_id_of_team(team2)
    records = Match.query.filter(or_((and_(Match.home_team == first_team_id, Match.away_team == second_team_id)),
                                     (and_(Match.home_team == second_team_id, Match.away_team == first_team_id)))).all()
    return records


def select_matches_scores_for_teams(team1, team2):
    first_team_id = get_id_of_team(team1)
    second_team_id = get_id_of_team(team2)
    results = []
    matches = get_matches_for_teams(team1, team2)
    for match in matches:
        results.append((team1 if match.home_team == first_team_id else team2,
                        team1 if match.away_team == first_team_id else team2, match.FTHG, match.FTAG, match.date))
    return results
