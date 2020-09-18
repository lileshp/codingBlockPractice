import json
import os
# import boto3 #
# import pyttsx3 #
#from comtypes.client import CreateObject #
# from google.cloud import texttospeech
# from pydub import AudioSegment
# import time
# from mergee import mergeAudio
import glob

class objectCreation():
    objectlist = []
    CharDict = {}
    genderDict={}
    actionPause={}

    def __init__(self):
        self.scene = ''
        self.charDial = {}
        self.actionLine = {}
        self.seq = {}
        self.location=''
        self.time=''

    def openFile(self, fileName):
        with open(r'fileName') as f:
            data = json.load(f)

    def loadData(self, data):
        for char in data:
            if char != 'Characters':
                fileObj = objectCreation()
                fileObj.scene = char
                if "Narration" in data[char]:
                    for i in data[char]['Narration']:
                        fileObj.actionLine[i] = data[char]['Narration'][i]
                if 'Dialogue' in data[char]:
                    for j in data[char]["Dialogue"]:
                        fileObj.charDial[j] = data[char]['Dialogue'][j]
                for k in data[char]['Sequence']:
                    fileObj.seq[k] = data[char]['Sequence'][k]
                fileObj.location=data[char]["Set"]["Location"] 
                fileObj.time=data[char]["Set"]["Time"]   
                objectCreation.objectlist.append(fileObj)
            else:
                for l in data[char]:
                    objectCreation.CharDict[l] = data[char][l]
    @staticmethod
    def googleCloud(dialText, Gender, nameOfFile,sceneName):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"C:\Users\Lenovo\Downloads\attach\NoveltoScr-f6132bf13013.json"
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.types.SynthesisInput(text=dialText)
        if Gender =="F":
            voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            name='en-US-Wavenet-C',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
        elif Gender == "M":
            voice = texttospeech.types.VoiceSelectionParams(
            language_code='en-US',
            name='en-US-Wavenet-D',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
        else:
            raise Exception        
        audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)
        response = client.synthesize_speech(synthesis_input, voice, audio_config)
        with open(r'C:\Users\Lenovo\Downloads\attach\{}_{}.mp3'.format(sceneName,nameOfFile), 'wb') as out:
            out.write(response.audio_content)  
    @staticmethod
    def genderDeter():
        for obj in range(len(objectCreation.objectlist)):
           objectCreation.genderDict[objectCreation.objectlist[obj].scene]={}
           for i in (objectCreation.objectlist[obj].charDial):
               name=objectCreation.objectlist[obj].charDial[i]['Dialgoue_Character']
               for j in (objectCreation.CharDict):
                   if name == objectCreation.CharDict[j]["Name"]:
                       objectCreation.genderDict[objectCreation.objectlist[obj].scene][i]=objectCreation.CharDict[j]["Gender"]
    @staticmethod
    def countWords():
        for obj in range(len(objectCreation.objectlist)):
            objectCreation.actionPause[objectCreation.objectlist[obj].scene]={}
            # path=f"/{obj}"##
            # os.makedirs(path)##
            for i in (objectCreation.objectlist[obj].actionLine):
                string=objectCreation.objectlist[obj].actionLine[i]['Narration_Words']
                StrLength=len(string)
                pauseLength=round(StrLength/56)
                objectCreation.actionPause[objectCreation.objectlist[obj].scene][i]=pauseLength
    @staticmethod
    def pauseSound(sceneLocation):
        song = AudioSegment.from_mp3(r"C:\Users\Lenovo\Downloads\attach\{}.mp3".format(sceneLocation))
        for i in (objectCreation.actionPause):
            for j in (objectCreation.actionPause[i]):
                if objectCreation.actionPause[i][j]!=0:
                    repeat_file=song * objectCreation.actionPause[i][j]
                    repeat_file.export(fr"C:\Users\Lenovo\Downloads\attach\{i}_{j}.mp3", format="mp3")
                else:
                    repeat_file=song * 1
                    repeat_file.export(fr"C:\Users\Lenovo\Downloads\attach\{i}_{j}.mp3", format="mp3")
                    
                # CODE TO USE DEFAULT AUDIO    

    def audioIntegSceneBased(Scene,Sequence):
        pass        
    def audioIntegAll(scene,titleOfStory):
        pass








# Pl TEST
with open(r"D:\MNF\test\Script.json") as f:
    data = json.load(f)
for char in data:
    if char != 'Characters':
        f = objectCreation()
        f.scene = char
        if "Narration" in data[char]:
            for i in data[char]['Narration']:
                f.actionLine[i] = data[char]['Narration'][i]
        if 'Dialogue' in data[char]:
            for j in data[char]["Dialogue"]:
                f.charDial[j] = data[char]['Dialogue'][j]
        for k in data[char]['Sequence']:
            f.seq[k] = data[char]['Sequence'][k]
        objectCreation.objectlist.append(f)
    else:
        for l in data[char]:
            objectCreation.CharDict[l] = data[char][l]

# print(objectCreation.CharDict)
for i in range(len(objectCreation.objectlist)):
    print(objectCreation.objectlist[i].scene)
    # print(objectCreation.objectlist[i].charDial)
#     print(objectCreation.objectlist[i].actionLine)
    print(objectCreation.objectlist[i].seq)
    print(i)

# objectCreation.genderDeter()
# print(objectCreation.genderDict)

# objectCreation.countWords()
# print(objectCreation.actionPause)

# objectCreation.pauseSound("forest")

# filename="Male"
# objectCreation.googleCloud("Hello,i am spandan","M", filename)
# filename='female'
# objectCreation.googleCloud("Hello,i am spandan","F", filename)

# for i in range(len(objectCreation.objectlist)):
#     for j in (objectCreation.genderDict):
#         testScene=objectCreation.objectlist[i].scene
#         if (testScene == j):
#             for k in (objectCreation.objectlist[i].charDial):
#                 objectCreation.googleCloud(objectCreation.objectlist[i].charDial[k]["Dialogue_Words"],objectCreation.genderDict[j][k],k,j)

songList=[]
ind=0
allFiles = glob.iglob(r'D:\MNF\test\\**/*.mp3',recursive=True)
fi=open(r"D:\MNF\test\naudio.txt","w")
for i in allFiles:
    fi.write("file "+i+"\n")


def createFile():
    global fi
    for i in range(len(objectCreation.objectlist)):
        for j in (objectCreation.objectlist[i].seq):
            scene=objectCreation.objectlist[i].scene
            seq=objectCreation.objectlist[i].seq[j]["Dialogue/Narration"]
            # song=AudioSegment.from_mp3(r"C:\Users\Lenovo\Downloads\attach\{}_{}.mp3".format(scene,seq))
            # songList.append(song)
            fi.write("file '{}{}_{}.mp3'\n".format("D:\MNF\test\\",scene,seq))
    return fi

def merger(inputFile):
    os.system("ffmpeg -f concat -safe 0 -i "+inputFile+" -c copy out3.mp3")  

# path=createFile()
# print(path)
# foll=open(r"D:\MNF\test\mylist.txt","r")
# print(foll)
path = "D:\MNF\test\\naudio.txt"
merger(path)          
 
         


