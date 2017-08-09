#!/usr/bin/env python3
import speech_recognition as sr

recognizer = sr.Recognizer();

with sr.Microphone() as mic:
	print("Go say something! I'm listening...");
	audio = recognizer.listen(mic);

try:
	print("You said: '" + recognizer.recognize_sphinx(audio));
except sr.UnknownValueError:
	print("Sorry. I can't understand ya.");
except sr.RequestError as e:
	print("Sphinx error: {0}".format(e))

