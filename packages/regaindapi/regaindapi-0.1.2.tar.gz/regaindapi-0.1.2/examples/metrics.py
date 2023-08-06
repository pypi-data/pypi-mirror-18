import pprint
import os
import argparse

from regaindapi import Client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", type=str, required=True)
    parser.add_argument("--client-secret", type=str, required=True)
    parser.add_argument("files", type=str, nargs="+")
    args = parser.parse_args()

    client = Client(args.client_id, args.client_secret)

    call_options = ["saliency", "sharpness", "exposure", "faceanalysis", "hue", "aesthetics", "labels"]

    print("Sending metrics request...")
    if len(args.files) == 1:
        call_ids = [client.metrics(args.files[0], call_options, async=True)["id"]]
    else:
        for f in args.files:
            assert (not os.path.lexists(f)), "Only remote URLs can be specified to make multiple metrics requests at once."
        call_ids = client.metrics(args.files, call_options)["entries"]

    print("Fetching reply of calls")
    while True:
        resp = client.metrics_result(call_ids)
        for x in resp:
            if resp[x]["status"] == "work-in-progress":
                break
        else:
            pprint.pprint(resp)
            break
