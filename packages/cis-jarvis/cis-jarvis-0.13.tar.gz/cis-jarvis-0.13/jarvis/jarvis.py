#!/usr/bin/env python3
# Requires PyAudio and PySpeech.
 
import speech_recognition as sr
import pyttsx
import webbrowser
import os

class jarvis():
	def __init__(self):
		pass

	def do_action(self, audio):
		if audio == 'Firefox':
			webbrowser.get('firefox').open_new_tab('http://www.cisin.com/')
		if audio == 'sublime':
			os.system('subl')
		if audio == 'Skype':
			os.system('skype')
		if audio == 'Thunderbird':
			os.system('thunderbird')

	def speech_to_text(self): 
		# Record Audio
		engine = pyttsx.init()
		# engine.say("Hello")
		r = sr.Recognizer()
		with sr.Microphone() as source:
		    engine.say("Say something!")
		    engine.runAndWait()
		    audio = r.listen(source)	 	
		try:
			print("You said: " + r.recognize_google(audio))
			engine.say("You said: " + r.recognize_google(audio))
			self.do_action(str(r.recognize_google(audio)))
			engine.runAndWait()
			fss = open('speech.txt', 'w')
			fss.write(str(r.recognize_google(audio)))
			fss.close()
		except sr.UnknownValueError:
		    print("Jarvis could not understand audio")
		except sr.RequestError as e:
		    print("Could not request results from Jarvis; {0}".format(e))

jarvis().speech_to_text()