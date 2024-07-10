import json
import urllib.parse
import requests
import os
from concurrent.futures import ThreadPoolExecutor

# read the json_data and extract the url
def extract_m3u8_url(json_data):
    url_encoded = json_data['url']
    m3u8_url = urllib.parse.unquote(url_encoded.split('&url=')[1])
    return m3u8_url

# download all ts segments
def download_ts_segment(url, session, output_dir):
    response = session.get(url, stream=True)
    segment_filename = os.path.join(output_dir, url.split('/')[-1])
    with open(segment_filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return segment_filename

def download_m3u8_playlist(m3u8_url, output_dir):
    session = requests.Session()
    response = session.get(m3u8_url)
    ts_urls = [[line.strip() for line in response.text.splitlines() if line and not line.startswith("#")]
    ]
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(download_ts_segment, url, session, output_dir) for url in ts_urls]
        ts_files = [future.result() for future in futures]

    return ts_files

def merge_ts_files(ts_files, output_file):
    with open("file_list.txt", "w") as file_list:
        for ts_file in ts_files:
            file_list.write(f"file '{ts_file}'\n")
    os.system(f"ffmpeg -f concat -safe 0 -i file_list.txt -c copy {output_file}")
    os.remove("file_list.txt")

json_str = '{"link":"/vod/wuyizhidi/1-1.html","link_next":null,"link_pre":null,"url":"/m3u8/player/?vod=51509&pid=1&no=1&url=https%3A%2F%2Fikcdn01.ikzybf.com%2F20221008%2FXRC0vaXI%2Findex.m3u8","url_next":null,"poster":"https://webp.ykjljdcss.com/upload/movie/c/c6034bb52169e608.webp","adUrl":null,"no":"1","vod":51509}'
json_data = json.loads(json_str)
m3u8_url = extract_m3u8_url(json_data)
print(m3u8_url)

output_dir = "downloaded_segments"
output_file = "output_movie.mp4"

ts_files = download_m3u8_playlist(m3u8_url, output_dir)
merge_ts_files(ts_files, output_file)
print(f"Downloaded and merged video saved as {output_file}")
