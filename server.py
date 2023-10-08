import json
from flask import Flask, render_template, request, redirect, flash, url_for
import datetime


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html', club=club, competitions=competitions)
    except IndexError:
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]

    error_messages = []
    if foundClub and foundCompetition:
        current_date = datetime.date.today()
        competition_date = datetime.datetime.strptime(foundCompetition['date'], "%Y-%m-%d %H:%M:%S").date()

        if competition_date >= current_date:

            return render_template('booking.html', club=foundClub, competition=foundCompetition)

        else:
            error_message = "Ce concours est dans le passé"
            error_messages.append(error_message)

    else:
        flash("Something went wrong-please try again")

    return render_template('welcome.html', club=foundClub, competitions=competitions, error_messages=error_messages)


def update_club(current_club, new_points, file_path='clubs.json'):
    # Enregistrement dans le fichier clubs.json
    with open(file_path, 'r') as c:
        clubs = json.load(c)
    updated_clubs = []
    for club in clubs['clubs']:
        if club['name'] == current_club['name']:
            club['points'] = int(new_points)
        updated_clubs.append(club)

    with open(file_path, 'w') as c:
        json.dump({'clubs': updated_clubs}, c, indent=4)


def update_competition(current_competition, file_path='competitions.json'):
    # Enregistrement dans le fichier competitions.json
    with open(file_path, 'r') as comps:
        listOfCompetitions = json.load(comps)
    updated_competitions = []
    for compet in listOfCompetitions['competitions']:
        if compet["name"] == current_competition["name"]:
            compet["numberOfPlaces"] = str(current_competition["numberOfPlaces"])
        updated_competitions.append(compet)

    with open(file_path, 'w') as c:
        json.dump({'competitions': updated_competitions}, c, indent=3)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired

    """Calcul du nombre de points restant"""
    new_points = int(club['points']) - placesRequired

    """Vérification si le nombre de points du club est supérieur à la commande"""
    error_messages = []
    if int(request.form['places']) < 0:
        error_message = "Vous ne pouvez pas saisir une quantité négative"
        error_messages.append(error_message)
    if new_points < 0:
        error_message = "Vous n'avez pas assez de points pour inscrire le nombre demandé"
        error_messages.append(error_message)
    if placesRequired > 12:
        error_message = "Vous ne pouvez pas commander plus de 12 places"
        error_messages.append(error_message)
    if not error_messages:
        update_club(club, new_points)
        update_competition(competition)
        club['points'] = new_points

        flash('Great-booking complete!')

    return render_template('welcome.html', club=club,
                           competitions=competitions,
                           error_messages=error_messages)


# TODO: Add route for points display
@app.route('/board')
def board():
    points_club = []
    for club in clubs:
        points_club.append({'name': club['name'], 'points': club['points']})

    return render_template('board.html', points_club=points_club)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
