import base64
import os
import sys
import string
import random
import uuid
import time

import validators
import youtube_dl
import argparse

import re

VIDEO_DL_DIR = "./downloads/"
VIDEO_FILE_PREFIX = 'awsec2_'
FINISHED_PATTERN = 'awsec2OK'


def get_random_str(length=7):
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=length))
    return res


def get_title(url):
    title = re.compile('[^a-zA-Z0-9]') \
        .sub('_', youtube_dl.YoutubeDL().extract_info(url, download=False)['title']) \
        .replace('__', '_').replace('__', '_').replace('__', '_') \
        .replace('__', '_').replace('__', '_')
    return title


def ytdl_config(video_file, dl_proxy=''):
    ffmpeg_cmd = "ffmpeg -i {} -acodec aac -ac 1 " \
                 + "-ar 48000 -b:a 128k -vcodec libx264 -b:v 4000k -pix_fmt yuv420p -video_size hd720 " \
                 + "-framerate 30 -g 60 -f flv " + video_file

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': VIDEO_DL_DIR + '%(id)s',
        # Workaround for https://github.com/rg3/youtube-dl/issues/11348
        # 'postprocessor_args': ['-bsf:a', 'aac_adtstoasc'],
        'postprocessors': [{
            'key': 'ExecAfterDownload',
            # see https://ffmpeg.org/ffmpeg-filters.html#scale
            # for explanation on -2 choice for scale filter
            'exec_cmd': ffmpeg_cmd
        }],
        'addmetadata': True,
        'xattrs': True,
        'proxy': dl_proxy,
        'geo_bypass': True,
        'continuedl': True,
        'fragment_retries': 10,
        'verbose': True
    }

    return ydl_opts


def get_finished_name(filename):
    name, ext = os.path.splitext(filename)
    return "{name}_{ok}{ext}".format(name=name, ok=FINISHED_PATTERN, ext=ext)


def ytdl_download(url, video_file, ydl_opts):
    ret = ''
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Downloading video from ' + url)
        ydl.extract_info(url, download=True)
        print('Video successfully downloaded to ' + video_file)
        final_name = get_finished_name(video_file)
        os.rename(video_file, final_name)
        print('Video file renamed to ' + final_name)
    return ret


def download_and_convert_url(url, output_type='flv'):
    ret = ''
    if not validators.url(url):
        print('Please, stop sending shit.')
        return ret
    video_file = VIDEO_DL_DIR + VIDEO_FILE_PREFIX + get_title(url) + '.' + output_type
    try:
        ydl_opts = ytdl_config(video_file)
        ret = ytdl_download(url, video_file=video_file, ydl_opts=ydl_opts)
    except Exception as e:
        error_msg = 'Sorry, download failed due to error : ' + str(e)
        print(error_msg)
    return ret


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Download and Convert Youtube videos for facebook live with ffmpeg.')

    parser.add_argument('-url', '--url', help='Youtube video link', required=True)
    parser.add_argument('-format', '--format', help='Output video format', default='flv', required=False)

    args = vars(parser.parse_args())

    youtube_url = args['url']
    output_format = None
    if args['format']:
        output_format = args['format']

    start = time.time()
    download_and_convert_url(url=youtube_url)
    end = time.time()
    print("Time elapsed: ", end - start, " Secs.")
