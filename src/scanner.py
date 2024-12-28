import argparse
import os
import json
import time
from pathlib import PurePosixPath
from dotenv import load_dotenv
import requests
# from io import StringIO


API_KEY = ''

def check_ip(ip):
    url = 'https://api.abuseipdb.com/api/v2/check'

    querystring = {
        'ipAddress': ip,
        'maxAgeInDays': '90'
    }

    headers = {
        'Accept': 'application/json',
        # 'Key': 'deb8df47db633683bd8542685d5ea8a2d173e8c24ba6f8ed55a113b1f3bf05ccb8f4955c10d43b6f'
        'Key': API_KEY
    }

    response = requests.request(method='GET', url=url, headers=headers, params=querystring)

    decodedResponse = json.loads(response.text)
    return json.dumps(decodedResponse, sort_keys=True, indent=4)

def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(description="A simple command-line tool")
    parser.add_argument('-f', '--file', type=str, help="file to process relative to root dir", required=True)
    args = parser.parse_args()

    # init env
    load_dotenv()
    global API_KEY 
    API_KEY = os.getenv('API_KEY')
    
    path = PurePosixPath(__file__)
    path = PurePosixPath(path.parents[1])
    path = path.joinpath(PurePosixPath(args.file))
    with open(str(path), 'r') as f:
        list = f.readlines()
        list = [line.strip().strip('"') for line in list if line.strip()]
        total = len(list)
        if total:
            num_dashes = 80
            new_file = path.with_name(f"{path.name}_done")
            with open(new_file, 'w') as maliciuos:
                for idx, ip in enumerate(list, start=1):
                    maliciuos.write(check_ip(ip))
                    dashes = int((idx / total) * num_dashes)
                    progress = f'Processing.. [{"-" * dashes}{" " * (num_dashes - dashes)}]'
                    print(progress, end='\r')
                    time.sleep(1)
    print("\ndone")

if __name__ == "__main__":
    main()
