import requests
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor


_getAbsPath = lambda p: os.path.join(os.path.dirname(__file__), p)


def read_tslist(fpath):
    with open(fpath, "r") as f:
        lines = [line.strip("\n") for line in f.readlines()]

    return lines


def download_ts_segment(url, index, headers, output_dir):
    print(index)
    segment_filename = os.path.join(output_dir, f"{index}.ts")
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        with open(segment_filename, "wb") as f:
            f.write(resp.content)
    return segment_filename


def chunks_then_merge(ts_urls, headers, fpath):

    with ThreadPoolExecutor(
        max_workers=8
    ) as executor, tempfile.TemporaryDirectory() as tmp_frag_dir:
        futures = [
            executor.submit(download_ts_segment, url, idx, headers, tmp_frag_dir)
            for idx, url in enumerate(ts_urls)
        ]
        fl = os.path.join(tmp_frag_dir, "tmp_ts_list.txt")

        with open(file=fl, mode="w") as f:
            f.write("\n".join(["file '" + future.result() + "'" for future in futures]))
        print([future.result() for future in futures])
        
        os.system(f"ffmpeg -f concat -safe 0 -i {fl} -c copy -bsf:a aac_adtstoasc {fpath}")


if __name__ == "__main__":
    l = read_tslist(_getAbsPath("./ts_filelist"))[:10]
    print(l)
    # chunks_then_merge()
