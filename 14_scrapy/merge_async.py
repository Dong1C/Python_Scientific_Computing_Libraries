import aiohttp
import asyncio
import aiofiles
import os
import tempfile
from utils import timer, async_timer
from tqdm.asyncio import tqdm

_getAbsPath = lambda p: os.path.join(os.path.dirname(__file__), p)


async def read_tslist(fpath):
    async with aiofiles.open(fpath, "r") as f:
        lines = [line.strip("\n") for line in await f.readlines()]

    return lines


async def download_ts_segment(session, url, index, headers, output_dir):
    segment_filename = os.path.join(output_dir, f"{index}.ts")
    async with session.get(url, headers=headers) as resp:
        if resp.status == 200:
            content = await resp.read()
            async with aiofiles.open(segment_filename, "wb") as f:
                await f.write(content)
    return segment_filename


@async_timer
async def async_download_merge(ts_urls, headers, fpath):
    with tempfile.TemporaryDirectory() as tmp_frag_dir:
        async with aiohttp.ClientSession() as session:
            tasks = [
                download_ts_segment(session, url, idx, headers, tmp_frag_dir)
                for idx, url in enumerate(ts_urls)
            ]
            segment_files = await tqdm.gather(*tasks)

            fl = os.path.join(_getAbsPath("tmp_ts_list.txt"))
            async with aiofiles.open(fl, "w") as f:
                await f.write(
                    "\n".join(
                        [f"file '{segment_file}'" for segment_file in segment_files]
                    )
                )

        # os.system(f"ffmpeg -f concat -safe 0 -i {fl} -c copy -bsf:a aac_adtstoasc {fpath}")


async def main():
    l = await read_tslist(_getAbsPath("./ts_filelist"))
    # print(l)
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
    await async_download_merge(l[:500], headers, "output_file.mp4")


if __name__ == "__main__":
    asyncio.run(main())
