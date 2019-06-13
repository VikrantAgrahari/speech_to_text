from django.shortcuts import render , get_object_or_404 ,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.contrib import  messages
from os import path
from pydub import AudioSegment
import time
import speech_recognition as sr
import matplotlib.pyplot as plt
import numpy as np
import sys
import wave

# Create your views here.
r= sr.Recognizer()
def index(request):
    print('Index page is working')
    return  render(request,'voicetext/index.html')

def upload(request):
    if request.method =='POST':
        file= request.FILES['audio']
        fs = FileSystemStorage()
        name=file.name #Got file name

        # Splitting Function
        spl= name.split('.')
        if(spl[1]=='wav'):
            har = sr.AudioFile(file)
            #plot_it(file)
            name= file.name
            size =round(((file.size)/1000),2)
            with har as source:
                r.adjust_for_ambient_noise(source)
                audio = r.record(source)
            mic_text = r.recognize_google(audio)
            data = []
            dataum = {'mic': mic_text,'name':name, 'size':size}
            data.append(dataum)
            return render(request, 'voicetext/upload.html', {'data': data})
        else:
            messages.error(request, ('The uploaded file format is not supported!'))
            return render(request, 'voicetext/index.html', {})
    else:
        return render(request, 'voicetext/index.html',{})


def convert_mp3(file):
    sound= AudioSegment.from_mp3(file)
    return sound.export('cnvt.wav',format='wav')

def conver_ogg(file):
    sound= AudioSegment.from_ogg(file)
    return sound.export('cnvt.wav',format='wav')

def to_text(request,file):
    print('Converting to text')
    har = sr.AudioFile(file)
    with har as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
    mic_text = r.recognize_google(audio)
    data=[]
    dataum={'mic':mic_text}
    data.append(dataum)
    print(mic_text)
    return render(request, 'voicetext/upload.html',{'data':data})

def plot_it(file):
    voice= wave.open(file,'r')
    signal = voice.readframes(-1)
    signal = np.fromstring(signal, 'Int16')

    # If Stereo
    if voice.getnchannels() == 2:
        print('Mono Files')
    plt.figure(1)
    plt.title('Signal Wave...')
    plt.plot(signal)
    plt.show()

