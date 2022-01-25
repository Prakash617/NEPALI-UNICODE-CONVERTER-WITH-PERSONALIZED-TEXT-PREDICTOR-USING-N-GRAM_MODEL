from pynput import keyboard
from PyQt5.QtCore import QThread, pyqtSignal

class MyThread(QThread):

    signal = pyqtSignal(object)
    
    def __init__(self):
        super().__init__()
        self.cnt=0
        self.listener = keyboard.Listener(on_release=self.on_release)
        self.listener2 = keyboard.Listener(on_release=self.toggle_listener)

    def run(self):
        self.listener.start()
        self.listener2.start()
        self.cnt+=1

    def toggle_listener(self,key):
        if key == keyboard.Key.esc:
            if self.cnt:
                self.listener.stop()
                self.cnt =(self.cnt+1) %2
                self.signal.emit("stop")
            else:
                self.listener = keyboard.Listener(on_release=self.on_release)
                self.listener.start()
                self.signal.emit("start")
                self.cnt+=1
                       

    def on_release(self, key):

        if key == keyboard.Key.backspace:
            self.signal.emit("back")
        elif key == keyboard.Key.enter:
            self.signal.emit('ent')
        elif key == keyboard.Key.space:
            self.signal.emit("space")
        else:
            try:
                key.char
            except(AttributeError):
                pass
            else:     
                if(32<ord(key.char)<=126):
                    self.signal.emit(key.char)
               