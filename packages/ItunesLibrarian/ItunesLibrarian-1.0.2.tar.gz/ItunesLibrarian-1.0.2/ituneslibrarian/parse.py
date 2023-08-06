import untangle
import csv

def to_dict(input):
    obj = untangle.parse(input)

    tracklist = obj.plist.dict.dict

    library = []
    track = {}
    sampletrack = {}

    maxparam = 0
    maxtrack = 0

    for xmltrack in tracklist.dict:

        track = {}
        lastdata = ""

        for data in xmltrack.children:

            if data._name == "key":
                lastdata = data.cdata
                sampletrack[lastdata] = ""
            else:
                track[lastdata] = data.cdata

        library.append(track)

    finallibrary = []
    finaltrack = sampletrack.copy()

    for dicttrack in library:
        for key in dicttrack:
            finaltrack[key] = dicttrack[key]
        finallibrary.append(finaltrack)
        finaltrack = sampletrack.copy()

    return finallibrary


def to_csv(input, output):

    library = to_dict(input)

    with open(output, 'w') as csvfile:
        fieldnames = library[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for track in library:
            writer.writerow(track)
