
from pathlib import Path


def main():

    database = loadDatabase()
    username = input(
        "Enter your name (put a $ symbol after your name if you wish your preferences to remain private): "
    )
    if username not in database:
        database[username] = enterPreferences()

    while True:
        option = input(
            """Enter a letter to choose an option:
e - Enter preferences
r - Get recommendations
p - Show most popular artists
h - How popular is the most popular
m - Which user has the most likes
q - Save and quit
s - Show Preferences"""
        )

        if option == "e":
            database[username] = enterPreferences()
        elif option == "r":
            recommendations(username, database)
        elif option == "p":
            print(mostPopular(database))
        elif option == "h":
            print(highestPopularity(database))
        elif option == "m":
            mostLikesUser(database)
        elif option == "q":
            saveDatabase(database, "musicrecplus.txt")
            break
        elif option == "s":
            showPreferences(username, database)
        else:
            print("That is not an option.")


def loadDatabase(filename: str = "musicrecplus.txt") -> dict:
    """loads the database from the file named musicrecplus.txt,
    if it exists. Otherwise it creates the file. Checks if user is
    in the database, if not it adds to database along with their preferences"""
    filename = Path(filename)
    filename.touch(exist_ok=True)  # will create file, if it exists will do nothing
    database = {}
    with open(filename, "r") as file:
        for line in file:
            [userName, artists] = line.strip().split(":")
            # seperates contents of file into userName list and artists list
            artistList = artists.split(",")
            # creates an artistList of each artist that are seperated by commas
            artistList.sort()
            database[userName] = artistList
            # assigns username as key and artistlist as value in the database dictionary
    return database


def recommendations(username: str, database: dict) -> tuple:
    """
    Takes in username and database dict.
    Returns a tuple of artist names.
    """
    # gets the users artist
    user_artists = database[username]
    # initates best_user
    best_user = ["", 0]

    # iterates through other users
    for other_user in database:
        # skips user and names with $
        if other_user == username or "$" in other_user:
            continue
        similar_artists = 0
        # iterates through the preferred artists of other users
        for other_artist in database[other_user]:
            # iterates through users preferred artists
            for user_artist in user_artists:
                # adds 1 to similar artist if artists of user and other match
                if other_artist == user_artist:
                    similar_artists += 1
        # makes best_user the most similar user that has reccomendations to give
        if similar_artists > best_user[1] and similar_artists != len(
            database[other_user]
        ):
            best_user = [other_user, similar_artists]

    # print(best_user)
    if best_user[0] == "":
        print("No recommendations available at this time.")
    else:
        # iterates through artists of the most similar user
        for rec_artist in database[best_user[0]]:
            # if rec_artist is not part of the user_artist print it
            if rec_artist not in user_artists:
                print(rec_artist)


def mostPopularHelper(userDict):
    """returns the artist that occurs in users preferences the most. Is a helper for
    most popular function"""
    artistPopularity = {}
    for x in userDict:
        if x[-1] != "$":
            # excludes users who are private
            for i in userDict[x]:
                if i not in artistPopularity:
                    artistPopularity[i] = 1
                    # if artist is not in the dictionary, it adds one instance to the new dictionary
                else:
                    artistPopularity[i] += 1
                    # if artist is already in dictionary, value of 1 is added to the artist count
    return sorted(artistPopularity.items(), key=lambda x: x[1], reverse=True)
    # returns a list sorted by value from greatest to least, so most popular artist will be at index 0, least will be at the end


def mostPopular(userDict):
    """returns the top 3 artists that appear in users preferences."""
    mostPop = mostPopularHelper(userDict)[:3]
    a = ""
    # takes the top 3 most popular artists
    for x in mostPop:
        if x == "":
            a = "Sorry, no artists found"
        a += str(x[0]) + "\n"
    return a


def highestPopularity(userDict):
    """returns how popular the most popular artist is."""
    x = mostPopularHelper(userDict)[0]
    a = ""
    if x == "":
        a = "Sorry, no artists found"
    a = str(x[1])
    return a


def enterPreferences() -> tuple:
    """
    Takes in nothing.
    Returns the tuple of the entered preferences.
    """
    preferences = []
    while (artist := input("Enter an artist that you like (Enter to finish):\n")) != "":
        if artist.title() not in preferences:
            preferences.append(artist.title())
        else:
            print(f"You already added {artist} to your likes.")
    preferences.sort()
    return tuple(preferences)


def mostLikesUser(database: dict) -> str:
    """
    Takes in a database dict.
    Returns the name of the user that has liked the most artists.
    """
    # makes an empty dictionary to append values to
    user_likes = {}
    # iterates through database
    for user in database:
        # if user has $ dont do this
        if "$" in user:
            continue
        # appends number of liked songs to dictionary with username as key
        user_likes[user] = len(database[user])
    # iterates through user_likes
    for user in user_likes:
        # if user_likes value is the number of likes and does not include $, print it
        if user_likes[user] == max(user_likes.values()):
            print(user)


def saveDatabase(database: dict, filename: str) -> None:
    """
    Takes in a database dict and file name.
    Saves the database dict to the file according to the spec.
    """
    word = ''
    for key in database:
        word = word + key + ":"
        for value in database[key]:
            if value == database[key][-1]:
                word = word + value
                continue
            word = word + value + ','
        word += '\n'

    text_file = open(filename, "w")
    n = text_file.write(word)
    text_file.close()


def showPreferences(userName, userDict):
    """
    Extra credit, shows current users preferences 
    """
    [print(x) for x in userDict[userName]]


"""
DATABASE SPEC

Each user is on their own line
Format is “UserName:Artist1,Artist2,Artist3, . . .”
Because we load the entire database every run,
overwrite the existing database instead of appending when saving.
"""

if __name__ == "__main__":
    main()
