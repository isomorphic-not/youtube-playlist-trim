import argparse
import pathlib
from typing import Optional

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pytubefix import Playlist


def trim_playlist(
    playlist: Playlist, output_path: str, start: int, end: Optional[int] = None
) -> None:
    tmp_filename = "tmp.mp4"
    pl_path = pathlib.Path(output_path)
    for index, vid in enumerate(playlist.videos):
        vid.streams.first().download(filename=tmp_filename)
        if "\\" in vid.vid_info['videoDetails']['title']:
            vid_title = vid.vid_info['videoDetails']['title'].replace('\\', '-')
        elif "/" in vid.vid_info['videoDetails']['title']:
            vid_title = vid.vid_info['videoDetails']['title'].replace('/', '-')
        else:
            vid_title = vid.vid_info['videoDetails']['title']
        full_output_path = str(pl_path / f"{index + 1}_{vid_title}.mp4")
        end_time = end or int(vid.vid_info["videoDetails"]["lengthSeconds"])
        ffmpeg_extract_subclip(
            tmp_filename, start, end_time, targetname=full_output_path
        )

    pathlib.Path.unlink(pathlib.Path(tmp_filename))


def main() -> None:
    parser = argparse.ArgumentParser(description="Get playlist info")
    parser.add_argument(
        "--playlist", type=Playlist, action="store", help="URL of Youtube playlist."
    )
    parser.add_argument("--output-path", action="store", help="Output path of video")
    parser.add_argument(
        "--start", type=float, action="store", help="Beginning timestamp to clip in seconds."
    )
    parser.add_argument(
        "--end",
        type=float,
        action="store",
        help="End timestamp to clip in seconds. "
        "if none is provided then will default to normal video end time.",
    )
    args = parser.parse_args()
    trim_playlist(
        playlist=args.playlist,
        output_path=args.output_path,
        start=args.start,
        end=args.end,
    )


if __name__ == "__main__":
    main()
