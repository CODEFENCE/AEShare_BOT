import urllib
import requests
from bs4 import BeautifulSoup
import os
import glob
import shutil
from moviepy.editor import *
from lxml import html
import string
from random import choice,randint
from urllib import request
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from time import sleep
from datetime import datetime
import colorama
from colorama import Fore,Back,Style
#-----------------------------------------------------------------
colorama.init(autoreset=True)
main_file_path = str(os.getcwd()).replace("\\",'/')
today = datetime.now().strftime("%d %b %Y")
def Getfirst4():
    global links,VideoHiveLinks,TitleDict,LinksToDownload,pagenum
    pagenum = int(input('Page Number > '))
    VideoHiveLinks = []
    links=[]
    
    TitleDict ={}
    LinksToDownload=[]
    src = requests.get("https://shareae.com/after-effects-project/page/2/").text
    soup = BeautifulSoup(src,'lxml')
    titles = soup.find_all('h2',class_='contenthead')

    for num,title in enumerate(titles):
        if num ==0 :
            continue
        if num < 5:
            if str(title.a.text).split('Videohive')[0] == '':
                t = str(title.a.text).split('Videohive')[1]
                result = (''.join([i for i in t if not i.isdigit()])).replace(' |',"").replace('|','').replace(' After Effects','')
                TitleDict[f'vid{num}'] = f'{result} - After Effects Template'
                
            links.append(title.a["href"])

        else:
            sort_orders = sorted(TitleDict.items(), key=lambda x: x[1])
            new_TitleDict = {}
            for num,order in enumerate(sort_orders):
                new_TitleDict[f'vid{num+1}']=order[1]
            print(f'{Back.GREEN}{Style.DIM}{Fore.BLACK}1 ==> Titles Scraped ')
            break
def GetDesc():
    global DescDict
    DescDict = {}
    global links
    d0 =''
    d1 =''
    d2 =''
    d3 =''
    for i in range(4):
        src = requests.get(links[i]).content
        soup = BeautifulSoup(src,'html.parser')
        descri = soup.find('div',attrs={'style':'display:inline;'})
        if i == 0:
            for z in descri:
                d0 += f'{str(z.string)}\n'
            DescDict['vid1']= d0
        if i == 1:
            for z in descri:
                d1 += f'{str(z.string)}\n'
            DescDict['vid2']= d1
        if i == 2:
            for z in descri:
                d2 += f'{str(z.string)}\n'
            DescDict['vid3']= d2
        if i == 3:
            for z in descri:
                d3 += f'{str(z.string)}\n'
            DescDict['vid4']= d3



def VisitInfoPage():
    for link in links:
        src = requests.get(link).text
        soup = BeautifulSoup(src,'lxml')
        downloadlinks = soup.find_all('div',class_='buttondownload1')
        for dl in downloadlinks:
            VideoHiveLinks.append(dl.a["href"])
def GetDownlink():
    global dwnl
    global ToShort
    ToShort =[]
    for link in links:
        src = requests.get(link).text
        soup = BeautifulSoup(src,'lxml')
        dwnl = soup.find_all("a",attrs={"target":"_blank"})
        for linnk in dwnl:

            if linnk['href'].split('/')[2] == 'fileblade.com':
                ToShort.append(linnk['href'])
    
def shortlink():
    global alias
    global Shortned
    Shortned = {}
    alias = []             
    Alias1 = ''
    Alias2 = ''
    Alias3 = ''
    Alias4 = ''
    letter = string.ascii_letters
    for letterr in range(6):
        Alias1 += choice(letter)

    for letterr in range(6):
        Alias2 += choice(letter)

    for letterr in range(6):
        Alias3 += choice(letter)

    for letterr in range(6):
        Alias4 += choice(letter)


    alias.append(Alias1)
    alias.append(Alias2)
    alias.append(Alias3)
    alias.append(Alias4)

    itershort = dict(zip(ToShort,alias))
    for num ,(link , alis) in enumerate(itershort.items()):
        response = requests.get(f"https://cut8url.com/api?api=2ca59b03413f2e7977675659d2162016e795fdf1&url={link}&alias={alis}").json()
        if response['status']=='success':
            Shortned[f'vid{num+1}'] = response['shortenedUrl']
    print(f'{Back.GREEN}{Style.DIM}{Fore.BLACK}URLs Shortned')
DETAILEd = {}
def SetUpDesc():
    with open(f'{main_file_path}/Output/Desc.txt','w') as fd:
        for i in range(4):
            DETAILEd[f'vid{1+i}'] = f'{TitleDict[f"vid{i+1}"]} :\n{DescDict[f"vid{i+1}"]}\nDownload Link : {Shortned[f"vid{i+1}"]}\n\n' 
            fd.write(DETAILEd[f'vid{1+i}']) 
        print(f'{Back.GREEN}{Style.DIM}{Fore.BLACK}Description Setted Up')

def DownloadFunc(AFileName,t):
    global filename
    
    # extract file name from AFileName
    filename = AFileName.split("/")[-1] 
    # download image using GET
    rawImage = requests.get(AFileName, stream=True)
    # save the image recieved into the file
    with open(f'{main_file_path}/{t.strip()}.mp4', 'wb') as fd:
        for num,chunk in enumerate(rawImage.iter_content(chunk_size=1024)):
            fd.write(chunk)
            
    return

def VideoHiveDownload():
    for num,link in enumerate(VideoHiveLinks):
        src = requests.get(link).text
        soup = BeautifulSoup(src,'lxml')
        downloadlinks = soup.find_all('div',class_='video-preview-wrapper')
        for link in downloadlinks:
            LinksToDownload.append(link.a['href'])
        
def VidDownload():
    print(f'{Back.GREEN}{Style.DIM}{Fore.BLACK}\nStarting Download ...')
    print(f'{Back.GREEN}{Style.DIM}{Fore.BLACK}Download Started !!')
    for num,link in enumerate(LinksToDownload):
        DownloadFunc(link,TitleDict[f'vid{num+1}'])
        left = (4-(num+1))
        Rndm_Fact()
        if left == 0:
            print(f'{Back.GREEN}{Style.DIM}{Fore.BLACK}All videos Downloaded')
        else:
            print(f'{Back.GREEN}{Style.DIM}{Fore.BLACK}Downloading Done ! \n{left} videos left !')
def editVid():
    """
    Make Vid 2x Faster and Composite a NoCopyright Music and Rename it to article Title
    """

        # loading video gfg 
        # 

        # getting subclip from it 
        #clip = clip.subclip(0, 9)
         #applying speed effect

    for num, video in enumerate(glob.glob('*.mp4')):
        os.chdir(main_file_path)
        clip = VideoFileClip(f"{video}")
        final = clip.fx(vfx.speedx, 2)
        
        os.chdir(f'Output/Videos/{today}')
        final.write_videofile(f"{video}",audio=False) # don't render audio.'''
        
        sleep(5)

#    for vid in glob.glob('*.mp4'):
#        shutil.move(f'C:/Users/Med Amine/Desktop/BOT/Output/Videos/Pending/{vid}',f'C:/Users/Med Amine/Desktop/BOT/Output/Videos/Final/{vid}')

    print(f'{Back.GREEN}{Style.DIM}{Fore.BLACK}All vids Edited')
    Rndm_Fact()

def initFiles():
    if not(os.path.exists(f'Output/Videos/{today}')):
        os.mkdir(f'Output/Videos/{today}')
    if not(os.path.exists(f'Output/Thumbnails/{today}')):
        os.mkdir(f'Output/Thumbnails/{today}')
jpgs = glob.glob('*.jpg')
def MakeThumb():
    os.chdir(main_file_path)
    print(f'{Back.GREEN}{Style.DIM}{Fore.BLACK} Making thumbnails started ...')
    for (vidnum,Title) in TitleDict.items():
        Title = Title.replace('- After Effects Template','').replace('After Effects','').replace('|','').split()
        if len(Title) > 2:
            f_slice = ''
            for i in Title[:2]:
                f_slice += (i+' ')
            s_slice = ''
            for i in Title[2:]:
                s_slice += (i+' ')
        if len(Title)<2:
            f_slice= Title[0]
            s_slice= Title[1]
        else:
            f_slice = ''
            for i in Title:
                f_slice += (i+' ')
            s_slice = ''
        im = Image.open(choice(jpgs))
        print(f'{Back.GREEN}{Style.DIM}{Fore.BLACK} The {vidnum} thumbnail making ... \nPlease Wait ...')
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype('Output/coolvetica rg.ttf',87)
    #    draw.text((700, 100),"Photo Gallery in an Aband''è'èف'èف'è'è'ف'èèف''èف'èففففففففففèف'èè'ففèفف'ف'ففففففففففففففففففففففففففففففففففففف'èèèèèèèèèèèè'è'èèقق+''ققè''''oned House غغغè'",(0,0,0),font= font)
        draw.text((650,150),f'{f_slice}\n{s_slice}',choice([(0,0,0),(255, 255, 255)]),font=font)
        im.save(f'Output/Thumbnails/{today}/{TitleDict[f"{vidnum}"]}.jpg')
    Rndm_Fact()
    print(f'{Back.GREEN}{Style.DIM}{Fore.BLACK}All thumbnails are READY ')


def Rndm_Fact():
    """
    docstring
    """
    apis = ['https://api.adviceslip.com/advice','https://breaking-bad-quotes.herokuapp.com/v1/quotes','https://official-joke-api.appspot.com/jokes/programming/random']
    r = randint(0,2)
    rndmapi = apis[r]
    if r == 0:
        response = requests.get(rndmapi).json()
        print(f'{Back.BLACK}{Style.BRIGHT}{Fore.YELLOW}{response["slip"]["advice"]}')
    if r == 1:
        response = requests.get(rndmapi).json()
        quote = response[0]['quote']
        author = response[0]['author']
        print(f'{Back.BLACK}{Style.BRIGHT}{Fore.YELLOW}{quote} - {author}')
    if r == 2:
        response = requests.get(rndmapi).json()
        setup = response[0]['setup']
        Pl = response[0]['punchline']
        print(f'{Back.BLACK}{Style.BRIGHT}{Fore.YELLOW}{setup} > {Pl}')


def Upload_To_YT():

    pass


def Closing():
    os.chdir(main_file_path)
    for vid in glob.glob('*.mp4'):
        os.remove(vid)
    print(f'{Back.GREEN}{Style.DIM}{Fore.BLACK}All Done Successfully !!\nNow Upload To Youtube')
