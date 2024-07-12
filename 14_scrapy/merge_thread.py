import requests
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from utils import timer, merge_video_clips

_getAbsPath = lambda p: os.path.join(os.path.dirname(__file__), p)


def read_tslist(fpath):
    with open(fpath, "r") as f:
        lines = [line.strip("\n") for line in f.readlines()]

    return lines


def download_ts_segment(url, index, headers, output_dir):
    # print(index)
    segment_filename = os.path.join(output_dir, f"{index}.ts")
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        with open(segment_filename, "wb") as f:
            f.write(resp.content)
    return segment_filename


@timer
def thread_download_merge(ts_urls, headers, fpath):

    # create the threadpool then submit the tasks
    # open the tmpfiledir and store all file into it
    with ThreadPoolExecutor(
        max_workers=8
    ) as executor, tempfile.TemporaryDirectory() as tmp_frag_dir:
        
        # submit the tasks
        futures_to_url = {
            executor.submit(download_ts_segment, url, idx, headers, tmp_frag_dir): url
            for idx, url in enumerate(ts_urls)
        }

        # moviepy
        # get segment files' path
        downloaded_segments = []
        for future in tqdm(as_completed(futures_to_url), total=len(ts_urls)):
            downloaded_segments.append(future.result())
        # merge
        merge_video_clips(downloaded_segments, fpath)

        # version: ffmpeg
        # fl = os.path.join(_getAbsPath("tmp_ts_list.txt"))
        # with open(file=fl, mode="w") as f:
        #     segment_filenames = []
        #     for future in tqdm(as_completed(futures_to_url), total=len(ts_urls)):
        #         segment_filenames.append(future.result())
        #     f.write("\n".join(["file '" + fname + "'" for fname in segment_filenames]))
        # os.system(f"ffmpeg -f concat -safe 0 -i {fl} -c copy -bsf:a aac_adtstoasc {fpath}")


def main():
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
    l = read_tslist(_getAbsPath("./ts_filelist"))
    # print(l)
    thread_download_merge(l, headers, _getAbsPath("output_file.mp4"))


if __name__ == "__main__":
    main()
