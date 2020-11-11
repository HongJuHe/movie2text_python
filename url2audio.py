import sys
import os
from pytube import YouTube
import moviepy.editor as mp
from bs4 import BeautifulSoup
from pydub import AudioSegment
import urllib.request
import glob
import re

class YouTubeDownloader(object): #youtube에서 동영상 다운 받기
    def __init__(self, youtube_rul):
        self.path = './movie'
        self.youtube_url = youtube_rul

    def downloader(self):
        yt = YouTube(self.youtube_url)
        os.makedirs(self.path, exist_ok=True) #영상 파일을 저장할 하위 디렉터리 생성
        try:
            source = urllib.request.urlopen(self.youtube_url).read()
        except ValueError as er:
            print("잘못된 url 입니다")
            return 0
        soup = BeautifulSoup(source, "html.parser")
        title = soup.find('title').text #페이지 크롤링하여 영상 제목 가져오기
        title = re.sub("[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'》]", "", title) #영상 제목에서 특수 문자 제외하기
        print(self.path)
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(self.path) #영상 다운 받기
        if os.path.isfile(self.path+'Unknown YouTube Video Title.mp4'):
            os.rename(self.path+'Unknown YouTube Video Title.mp4', self.path+title+'.mp4') #영상 제목 바꾸기
        else:
            other_file = glob.glob(self.path+title[0:3]+"*.mp4")
            other_title = os.path.basename(other_file[0])
            os.rename(self.path+other_title, self.path+title+".mp4")
        return title

    def pathvalue(self):
        self.path += '/'
        return self.path

class ChangeMovie(object):
    def __init__(self, path, filename):
        self.path = path
        self.filename = filename

    def MovieToAudio(self):
        clip = mp.VideoFileClip(self.path+self.filename+".mp4")
        clip.audio.write_audiofile(self.path + self.filename + ".mp3") #영상을 음원 파일로 바꾸기

        filedir = str(os.getcwd() + "/movie/" + self.filename)
        src = filedir + ".mp3"
        print(src)
        sound = AudioSegment.from_mp3(src)
        sound.export(filedir + ".wav", format="wav") #wav로 형식 바꾸기

url = input(); #arvg[0]으로 바꿀 예정
y = YouTubeDownloader(url)
yp = y.pathvalue()
yt = y.downloader()

if yt != 0:
    c = ChangeMovie(yp, yt)
    num = c.MovieToAudio()
