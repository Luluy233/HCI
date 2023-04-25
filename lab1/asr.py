from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtCore import QThread

from asrInterface import Ui_MainWindow
import sys
import win32api

import speech_recognition as sr

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_sphinx(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

class myWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

class Thread(QThread):

    def __init__(self):
        super(Thread, self).__init__()

    def run(self):
        # create recognizer and mic instances
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        PlayMusic=['ink','ake','pl','music']
        OpenNotepad=['open','oh','pa','ad']

        while 1:
            print("speaking")
            command = recognize_speech_from_mic(recognizer, microphone)
            print("You said: {}".format(command["transcription"]))

            if any(word in command["transcription"] for word in PlayMusic):
                # 播放音乐
                win32api.ShellExecute(0, 'open', '一荤一素.mp3', '', '', 1)
            elif any(word in command["transcription"] for word in OpenNotepad):
                win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', 1)

        Thread.quit()  # 退出线程


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = myWindow()
    application.show()
    thread = Thread()  # 创建线程对象
    thread.start()  # 启动线程
    sys.exit(app.exec())
