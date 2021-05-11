# Hier kommen alle Befehle rein, die etwas mit dem Spieleabend zutun haben
from random import randrange
import datetime


async def gamelist(cursor, message):
    cursor.execute("SELECT * FROM games")
    results = cursor.fetchall()

    if not results:
        await message.channel.send("Keine Einträge gefunden!")
    else:
        msg = ""

        for row in results:
            msg = msg + "- " + row[1] + "\n"

        await message.channel.send(msg)


def get_games(cursor):
    cursor.execute("SELECT * FROM games")
    results = cursor.fetchall()

    if not results:
        return

    games = []

    for row in results:
        games.append(row[1])

    return games


async def add_games(message, cursor, db):
    game = message.content.replace('!game add ', '')

    try:
        cursor.execute(f"INSERT INTO games (name) VALUES ('{game}')")
        db.commit()
    except:
        db.rollback()

    await message.channel.send("\"" + game + "\" wurde erfolgreich in die Liste aufgenommen")


# def del_games():


async def next_game(message, cursor):
    msg = ""

    # today = datetime.date.today() + datetime.timedelta(6) # Heute +6 Tage simuliert
    today = datetime.date.today()
    wednesday = today + datetime.timedelta((1 - today.weekday()) % 7 + 1)
    msg = msg + "Nächster Spielabend ist am: " + wednesday.strftime("%d.%m.%Y") + "\n"

    games = get_games(cursor)

    if not games:
        await message.channel.send("Keine Liste mit Spielen in der Datenbank vorhanden!")

    rng_game = games[randrange(len(games))]
    msg = msg + "Folgendes Spiel wird gespielt: " + rng_game

    await message.channel.send(msg)
