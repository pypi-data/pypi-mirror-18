import os.path
# import urllib.request

import ituneslibrarian.utils as utils
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3


def library(library):

    for track in library:

        title = track["Name"]
        tokens = []
        # location = urllib.request.unquote(
        #    track["Location"][7:].replace("%20", " "))

        location = track["Location"][7:].replace("%20", " ")

        filename, file_extension = os.path.splitext(location)

        utils.notice_print(title)

        if os.path.exists(location):
            if file_extension == ".mp3":

                audio = MP3(location, ID3=EasyID3)

                audio["artistsort"] = ['']
                audio["titlesort"] = ['']
                audio["albumsort"] = ['']

                if "title" in audio.keys():
                    if audio["title"][0] != title:

                        utils.warning_print('different titles\n\tTitle: ' +
                                            str(audio["title"]) + "\n" + '\tName: ' + title)

                        title_selection = utils.prompt(
                            'Which one would you like to keep? ', ["1", "2", "s"], 0)

                        if title_selection == "2":
                            audio["title"] = [title]
                        elif title_selection == "1":
                            title = audio["title"][0]

                else:
                    utils.warning_print("no title")

                    title_duplication = utils.prompt(
                        'Would you like to clone the name? ', ["1", "2"], 0)

                    if title_duplication == "1":
                        audio["title"] = [title]
                    elif title_duplication == "2":
                        audio["title"] = []

                if "artist" in audio.keys():
                    if "albumartist" in audio.keys():

                        if audio["artist"] != audio["albumartist"]:

                            utils.warning_print('different artists\n\tArtist: ' + str(
                                audio["artist"]) + "\n" + '\tAlbum artist: ' + str(audio["albumartist"]))

                            artist_selection = utils.prompt(
                                'Which one would you like to keep? ', ["1", "2", "s"], 2)

                            if artist_selection == "1":
                                audio["albumartist"] = audio["artist"]
                            elif artist_selection == "2":
                                audio["artist"] = audio["albumartist"]

                    else:
                        utils.warning_print("no album artist")

                        artist_duplication = utils.prompt(
                            'Would you like to substitute < no album artist > with < ' + audio["artist"][0] + ' >? ', ["1", "2", "s"], 1)

                        if artist_duplication == "1":
                            audio["albumartist"] = audio["artist"]
                        elif artist_duplication == "2":
                            audio["albumartist"] = []

                else:
                    utils.warning_print("no artist")

                title_components = title.split("-")
                title_components_dir = {}

                i = 0

                noconflicts = {"title": False, "artist": False}

                if len(title_components) > 1:

                    utils.warning_print("splittable name")

                    for comp in title_components:

                        comp = comp.strip()
                        title_components_dir[i] = comp

                        if "title" in audio.keys() and len(audio["title"]) > 0 and comp.lower() == audio["title"][0].lower():
                            noconflicts["title"] = comp
                            del title_components_dir[i]

                        if "artist" in audio.keys() and len(audio["artist"]) > 0 and comp.lower() == audio["artist"][0].lower():
                            noconflicts["artist"] = comp
                            del title_components_dir[i]

                        print("\t" + str(i) + " - " + comp)
                        i += 1

                    print (len(title_components_dir))

                    if len(title_components_dir) == 1:
                        suggestion = 0
                    else:
                        suggestion = False

                    if noconflicts["title"] is False:

                        newtitle = utils.prompt(
                            'Which term is the title? ', [str(val) for val in list(title_components_dir.keys())] + ["s"], suggestion)

                        if newtitle != "s":
                            audio["title"] = title_components[
                                int(newtitle)].strip()

                    if noconflicts["artist"] is False:

                        newartist = utils.prompt(
                            'Which term is the artist? ', [str(val) for val in list(title_components_dir.keys())] + ["s"], suggestion)

                        if newartist != "s":
                            audio["artist"] = title_components[
                                int(newartist)].strip()

                audio.save()

            else:
                utils.error_print(
                    "Wrong file extension. Extension: " + file_extension)
        else:
            utils.error_print("File not found. Location: " + location)

        utils.notice_print("All done.\n\n")
