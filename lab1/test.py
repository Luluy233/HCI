import speech_recognition as sr
r = sr.Recognizer()
speech=sr.AudioFile('f1lcapae.wav')
with speech as source:
    audio=r.record(source)
print(r.recognize_sphinx(audio))
