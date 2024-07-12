import aiohttp
import asyncio
import aiofiles
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor
from utils import timer, async_timer, merge_video_clips
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

        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as pool:
            await loop.run_in_executor(pool, merge_video_clips, segment_files, fpath)
        # merge_video_clips(segment_files, fpath)

        # fl = os.path.join(_getAbsPath("tmp_ts_list.txt"))
        # async with aiofiles.open(fl, "w") as f:
        #     await f.write(
        #         "\n".join(
        #             [f"file '{segment_file}'" for segment_file in segment_files]
        #         )
        #     )

        # os.system(f"ffmpeg -f concat -safe 0 -i {fl} -c copy -bsf:a aac_adtstoasc {fpath}")


async def main():
    l = await read_tslist(_getAbsPath("ts_urls"))
    # print(l)
    headers = {
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "Windows",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }
    await async_download_merge(l, headers, _getAbsPath("output_file2.mp4"))


if __name__ == "__main__":
    asyncio.run(main())
