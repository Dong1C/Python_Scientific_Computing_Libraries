import json
import urllib.parse
import requests
import os
import unittest
from concurrent.futures import ThreadPoolExecutor

"""
    1. store all ts_urls into a specific file 
    2. download ts files and compress them into the video chunks
        1. ffmpeg merge 100 ts files one time
        2. chunks merge last
    3. 
    
    
"""


_getAbsPath = lambda p: os.path.join(os.path.dirname(__file__), p)

# set the headers
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Host": "ikcdn01.ikzybf.com",
    "Origin": "https://www.7qhb.com",
    "Referer": "https://www.7qhb.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}


# read the json_data and extract the url
def extract_m3u8_url(raw_str: str):
    # transform the data to json data
    json_data = json.loads(raw_str)
    url_encoded = json_data["url"].split("url=")[-1]
    m3u8_url = urllib.parse.unquote(url_encoded)

    # rearrang the path
    m3u8_url = urllib.parse.urlparse(m3u8_url)
    url_path = m3u8_url.path.split("/")
    url_path.insert(-1, "2000kb")
    url_path.insert(-1, "hls")

    return urllib.parse.urljoin(m3u8_url.geturl(), "/".join(url_path))


# download all ts segments
def download_ts_segment(url, session, output_dir):
    response = session.get(url, stream=True)
    segment_filename = os.path.join(output_dir, url.split("/")[-1])
    with open(segment_filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return segment_filename


# get the ts files' urls and store them
def fetch_m3u8_ts_urls(m3u8_url, fpath="ts_filelist"):
    # set the session and get the response
    session = requests.Session()
    response = session.get(m3u8_url, headers=headers)

    # strip and get the urls
    ts_urls = [
        urllib.parse.urljoin(m3u8_url, line.strip())
        for line in response.text.splitlines()
        if line and not line.startswith("#")
    ]

    fpath = _getAbsPath(fpath)
    with open(file=fpath, mode="w") as f:
        for line in ts_urls:
            f.write(line+'\n')

    return fpath


def merge_ts_files(ts_files, output_file):
    with open("file_list.txt", "w") as file_list:
        for ts_file in ts_files:
            file_list.write(f"file '{ts_file}'\n")
    os.system(f"ffmpeg -f concat -safe 0 -i file_list.txt -c copy {output_file}")
    os.remove("file_list.txt")

def ffmpeg_merge_chunks(chunks, file_path):
    # just reduce the chunks using the merge function
    pass


if __name__ == "__main__":
    # json_str = '{"link":"/vod/wuyizhidi/1-1.html","link_next":null,"link_pre":null,"url":"/m3u8/player/?vod=51509&pid=1&no=1&url=https%3A%2F%2Fikcdn01.ikzybf.com%2F20221008%2FXRC0vaXI%2Findex.m3u8","url_next":null,"poster":"https://webp.ykjljdcss.com/upload/movie/c/c6034bb52169e608.webp","adUrl":null,"no":"1","vod":51509}'
    # m3u8_url = extract_m3u8_url(json_str)
    # print(m3u8_url)

    # fpath = fetch_m3u8_ts_urls(m3u8_url)
    # print(fpath)

    urls = [
        "https://ikcdn01.ikzybf.com/20221008/XRC0vaXI/2000kb/hls/uW7t9XEy.ts",
        "https://ikcdn01.ikzybf.com/20221008/XRC0vaXI/2000kb/hls/M4meCSLs.ts"
    ]
    for idx, url in enumerate(urls):
        resp = requests.get(url, headers=headers)
        paths = []
        if resp.status_code == 200:
            paths.append(_getAbsPath(f"{idx}.ts"))
            with open(paths[-1], 'wb') as f:
                f.write(resp.content)
    
    import ffmpeg
    
    ffmpeg.input(urls).output(_getAbsPath("output.mp4"))
   
   
    
    # output_dir = "downloaded_segments"
    # output_file = "output_movie.mp4"

    # ts_files = download_m3u8_playlist(m3u8_url, output_dir)
    # merge_ts_files(ts_files, output_file)
    # print(f"Downloaded and merged video saved as {output_file}")
