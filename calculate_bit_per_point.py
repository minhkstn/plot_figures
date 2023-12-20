import os
import glob
import open3d as o3d
import pandas as pd

keys = ['positions bitstream size', 'colors bitstream size']

videos = ['BlueSpin', 'CasualSquat', 'FlowerDance', 'ReadyForWinter']
codecs = ['vpcc', 'octree-predlift', 'trisoup-raht']
qualities = ['r01', 'r02', 'r03', 'r04', 'r05']
bpp_df = pd.DataFrame(columns=['video', 'codec', 'quality', 'bpp'])

for video in videos:
    for codec in codecs:
        qualities = ['r01', 'r02', 'r03', 'r04', 'r05']
        encoded_root_path = 'gpcc/{}'.format(codec)

        if codec == 'trisoup-raht':
            qualities = ['r01', 'r02', 'r03', 'r04']
        if codec == 'vpcc':
            encoded_root_path = 'vpcc'
                

        for quality in qualities:
            # get # of points in origin frames
            path = '/local/home/shared2/spirit/subjective_test/raw_data/UVG-VPC/vpcc/{}/ply_vox10/ply_xyz_rgb/*.ply'.format(video)
            files = glob.glob(path)
            num_points = 0

            for file in files:
                f = o3d.io.read_point_cloud(file)

                num_points += int(str(f).split(' ')[2])
                # print(int(str(f).split(' ')[2]))
            # get # of bits in bitstream files
            path = '/local/home/shared2/spirit/subjective_test/raw_data/UVG-VPC/{}/{}/{}/*.bin'.format(encoded_root_path, video, quality)
            files = glob.glob(path)

            num_bytes = 0

            for file in files:
                file_size_bytes = os.path.getsize(file)
                # print("# of bytes: ", file_size_bytes)
                num_bytes += file_size_bytes

            bpp = num_bytes * 8 / num_points
            bpp_df.loc[len(bpp_df.index)] = [video, codec, quality, bpp]
            print('{}\t{}\t{}: {} bpp'.format(video, codec, quality, bpp))

bpp_df.to_csv('./bpp.csv')