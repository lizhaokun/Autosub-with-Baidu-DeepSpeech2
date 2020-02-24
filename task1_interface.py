from autosub_baidu import generate_subtitle
import subprocess
subprocess.call(["ffmpeg", "-i", "http://tv6.ustc.edu.cn/hls/cctv1hd.m3u8", "-c", "copy", "-bsf:a", "aac_adtstoasc", "./data/cctv/2019-03-19-HH-MM-SS.mp4"])
def extractSubtitlefromVideo(filename):
    featurefilename = generate_subtitle(filename)
    return featurefilename

extractSubtitlefromVideo("./data/cctv/2019-03-19-HH-MM-SS.mp4")