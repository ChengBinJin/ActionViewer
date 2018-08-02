import os
import argparse

from ICVL_data_reader import ICVL
from write2excel import Writer

parser = argparse.ArgumentParser(description='')
parser.add_argument('--resize_ratio', dest='resize_ratio', type=float, default=1.0,
                    help='resize ratio for input frame')
parser.add_argument('--interval_time', dest='interval_time', type=int, default=20,
                    help='interval time between two frames')

args = parser.parse_args()


def main(video_list):
    writer = Writer()
    video_id = 1

    for video_path in video_list:
        video_reader(video_id, video_path, writer)
        video_id += 1


def video_reader(video_id, path, writer):
    reader = ICVL(video_id, path=path, resize_ratio=args.resize_ratio, interval_time=args.interval_time)
    reader.read_gt()
    writer.write2excel(path, video_id, reader.GT, reader.videoTime)
    reader.show()


if __name__ == '__main__':
    path = './DB'
    video_types = ['.avi', '.mkv']

    filenames = []
    for video_type in video_types:
        filenames.extend([os.path.join(path, fname) for fname in os.listdir(path) if fname.endswith(video_type)])

    print(filenames)

    main(filenames)

