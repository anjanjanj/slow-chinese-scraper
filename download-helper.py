import requests

from sys import argv
import sys

try:
    filename = argv[1]
except IndexError:
    print("No file name provided...")
    sys.exit()

def download_file(url):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return local_filename

print("*** File list: " + filename)

lines = [line.strip() for line in open(filename)]
lines = lines[::-1]

for link in lines:
	localname = download_file(link)
	print ("File saved to " + localname)