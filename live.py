import os
import time
import argparse
import subprocess


def get_cmd_output(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8')


def fb_live(video_link, strem_link):
    fb_live_url = "rtmps://live-api-s.facebook.com:443/rtmp/" + strem_link
    cmd_new = 'ffmpeg -re -i \"' + video_link + '\" -c copy -f flv \"' + fb_live_url + '\"'
    msg = ''
    msg = get_cmd_output(cmd_new)
    if len(msg) > 0:
        print(msg)
    print('CMD Finished.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Broadcast video to Facebook live with ffmpeg.')

    parser.add_argument('-video',
                        '--video',
                        help='Video link or flv encoded video file',
                        required=True)

    parser.add_argument('-key',
                        '--key',
                        help='Facebook live stream key',
                        required=True)

    args = vars(parser.parse_args())

    video = args['video']
    key = args['key']

    start = time.time()
    fb_live(video_link=video, strem_link=key)
    end = time.time()
    print("Time elapsed: ", end - start, " Secs.")
