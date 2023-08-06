import pprint
import os
import uuid
import argparse

from regaindapi import Client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", type=str, required=True)
    parser.add_argument("--client-secret", type=str, required=True)
    parser.add_argument("urls", type=str, nargs="+")
    args = parser.parse_args()

    client = Client(args.client_id, args.client_secret)

    # Uploading a collection from remote urls
    print("Creating album...")
    album_id = client.new_album()

    print("Sending batch of urls to add to album...")
    entries = [{"filename": os.path.basename(url),
                "id": uuid.uuid4().hex,
                "url": url,
                }
               for url in args.urls]
    out = client.uploads(album_id, entries)

    print("Getting back metadata one by one...")
    # Fetch album pictures metadata one by one
    for p in out["entries"]:
        pic = p["id"]
        while True:
            resp = client.metadata(album_id, pic)
            if resp["status"] != "work-in-progress":
                pprint.pprint(resp)
                break

    print("Getting back metadata all at once...")
    # Fetch all album pictures metadata at once
    pprint.pprint(client.metadata(album_id, [p["id"] for p in out["entries"]]))

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
