from django.shortcuts import render , get_object_or_404 ,redirect
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.contrib import  messages
from os import path
#from pydub import AudioSegment
import time
import speech_recognition as sr
#import matplotlib.pyplot as plt
#import numpy as np
import sys
#import wave
#import simpleaudio as sa
from reportlab.pdfgen import canvas
#import docx
import os

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
        print('Saved!')
        # Splitting Function
        spl= name.split('.')
        if(spl[1]=='wav'):
            har = sr.AudioFile(file)
            #plot_it(file)
            name= file.name
            size =round(((file.size)/1000),2)
            if size>1024:
                size=round((size/1000),2)
                we=str(size)+" MB"
            else:
                we=str(size)+" KB"
            with har as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.record(source)
            try:
                mic_text = r.recognize_google(audio, language='en-US')
            except sr.UnknownValueError:
                mic_text="I couldn't undestand. It's too much noise :( "
            except sr.RequestError:
                mic_text="Sorry, Service is not Avaiable right now!"
            #fs.save(file.name,file)
            #doc=to_doc(mic_text)
            data = []
            dataum = {'mic': mic_text,'name':name, 'size':we, 'file_name':file.name}
            data.append(dataum)
            return render(request, 'voicetext/upload.html', {'data': data} )
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

'''
def to_doc(text):
    doc=docx.Document()
    os.remove('voicetext/static/tmp.docx')
    doc.add_paragraph(text)
    doc.save('voicetext/static/tmp.docx')
    return doc

'''