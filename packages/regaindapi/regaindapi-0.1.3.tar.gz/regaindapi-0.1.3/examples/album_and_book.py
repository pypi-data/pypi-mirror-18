import pprint
import argparse

from regaindapi import Client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", type=str, required=True)
    parser.add_argument("--client-secret", type=str, required=True)
    parser.add_argument("directory", type=str)
    args = parser.parse_args()

    client = Client(args.client_id, args.client_secret)

    # Uploading a collection from a local directory
    album_id, pic_ids = client.make_album(args.directory)
    print("Uploaded album {}".format(album_id))

    print("Getting back metadata one by one...")
    # Fetch album pictures metadata one by one
    for pic in pic_ids:
        while True:
            resp = client.metadata(album_id, pic)
            if resp["status"] != "work-in-progress":
                pprint.pprint(resp)
                break

    print("Getting back metadata all at once...")
    # Fetch all album pictures metadata at once
    pprint.pprint(client.metadata(album_id, pic_ids))

    # Getting some sane selection counts suggestions: low (minimum # of
    # pictures required to tell the story), best (optimal number), high (no
    # duplicate pictures, but possibly redundant)
    print("Getting selection size suggestions...")
    suggestion = client.suggest(album_id)
    count = suggestion["best"]

    print("Suggested thresholds:")
    pprint.pprint(suggestion)

    # Getting the selection for a given number of pictures
    print("Getting a narrative selection...")
    selection = client.summary_narrative(album_id, count)
    pprint.pprint(selection)

    # Generate a photobook for this selection
    # Only works if there are enough pictures in the album!
    if count >= 26:
        print("Building book...")
        book = client.book(album_id, selection)
        pprint.pprint(book)
    else:
        print("Insufficient number of pictures in selection to build a photobook.")
