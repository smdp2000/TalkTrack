from flask import Flask, render_template, request
import speech_recognition as sr
import makePloty as mp
from os import path
from pydub import AudioSegment
import paralleldots
import json
import os
paralleldots.set_api_key("4hIabinTFcXDOCwsykbDyxiQRfoVNdM8r4RGGK1EXVc")
app = Flask(__name__)

@app.route('/')
def my_form():
   return render_template('hp.html')

@app.route('/result',methods = ['POST'])
def my_form_post():
   sentiment_data = {}
   taxonomy_data = {}
   intent_data = {}
   abuse_data = {}
   if request.method == 'POST':
      result = request.form['impath']
      files = os.listdir(result)
      for item in files:
        nm=item
        if item.split('.')[1]=='mp3':
            sound = AudioSegment.from_mp3(os.getcwd() + '/'+'data/'+ str(nm))
            nm=item.split('.')[0]+".wav"
            sound.export(result+ str(nm), format="wav")
        AUDIO_FILE = result+ str(nm)
        #AUDIO_FILE = result + str(item)
        #name = item.split('.')
        ##print(name[0])
        #fh = open("recognized.txt", "w+")
        #AUDIO_FILE = "/home/samroadie/Desktop/codebreak/audios/data/preamble1.wav"
        r = sr.Recognizer()
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # read the entire audio file
        text=r.recognize_google(audio)
        lang_code="en"
        #######################################
        response=paralleldots.sentiment(text,lang_code)
        sentiment_data.update ({item : response ["sentiment"]})
        #######################################
        response=paralleldots.taxonomy(text)
        #print(response)
        taxonomy_data.update ({item : response ["taxonomy"]})
        #######################################
        response=paralleldots.intent(text)
        intent_data.update ({item : response ["intent"]})
        #############################################
        response=paralleldots.abuse(text)
        abuse_data.update ({item : response})
        ###########################################
        mp.plot_sentiment (sentiment_data)
        mp.plot_abuse (abuse_data)
        mp.plot_intent (intent_data)
        mp.plot_taxonomy (taxonomy_data)

      return render_template ('output.html')

if __name__ == '__main__':
   app.run(debug = True)
