
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, \
    QHBoxLayout, QMainWindow, QVBoxLayout, QWidget, QPushButton,QSizePolicy,\
    QDialog
from PyQt5 import QtGui
import sys

from pynput import keyboard
controller= keyboard.Controller()

from integrate import get_three_suggestions
from ListenerThread import MyThread
from Typer import switch_program, delete_and_type
from user_map import save_new_word
from pre_model import pre_make
from user_model import user_make
from model import generate_model
from new_word_window import Ui_MainWindow2
from helpwindow import Ui_MainWindow


class MyWindow(QMainWindow):
    def closeEvent(self,event):
            win.thread.toggle_listener(keyboard.Key.esc)
            try:
                win.ui.dg.close()
            except:pass


    
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.threadstatus=False
        self.setWindowTitle("Nepali UCP")
        self.setWindowIcon(QtGui.QIcon("ico.png"))
        self.setGeometry(1100,500,400,200)
        
        self.word=''
        self.unicode=''
        self.total_text=''
        self.dotcount=0
        self.spc=False
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hboxhelp=QHBoxLayout()

        self.btn1 = QPushButton("",self)
        self.btn2 = QPushButton("",self)
        self.btn3 = QPushButton("",self)

        self.addbtn = QPushButton("+",self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # sizePolicy.setHeightForWidth(self.helpButton.sizePolicy().hasHeightForWidth())
        self.addbtn.setSizePolicy(sizePolicy)
        self.addbtn.setMinimumSize(QtCore.QSize(41, 41))

        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)

        self.addbtn.setFont(font)
        self.addbtn.setStyleSheet("background:rgb(202, 198, 212);color:rgb(66, 77, 223);border-radius: 20px;padding-bottom:4px")
        hboxhelp.addWidget(self.addbtn,0, QtCore.Qt.AlignHCenter)

        self.helpButton = QPushButton("?",self)
        self.helpButton.setSizePolicy(sizePolicy)
        self.helpButton.setMinimumSize(QtCore.QSize(41, 41))

        self.helpButton.setFont(font)
        self.helpButton.setStyleSheet("background:rgb(202, 198, 212);color:rgb(66, 77, 223);border-radius: 20px;padding-bottom:4px")
        hboxhelp.addWidget(self.helpButton,0, QtCore.Qt.AlignHCenter)

        self.addbtn.clicked.connect(self.addnewcustom)
        self.helpButton.clicked.connect(self.helpdiag)
        # hboxhelp.addWidget(self.addbtn)
        hbox.addWidget(self.btn1)
        hbox.addWidget(self.btn2)
        hbox.addWidget(self.btn3)

       
        vbox.addLayout(hbox) 
        vbox.addLayout(hboxhelp)
        self.setLayout(vbox)
        # self.addbtn = QPushButton("+",self)

        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.btn1.clicked.connect(lambda: self.button_insert(self.btn1.text()))
        self.btn2.clicked.connect(lambda: self.button_insert(self.btn2.text()))
        self.btn3.clicked.connect(lambda: self.button_insert(self.btn3.text()))
        self.threadStart()
    
    def addnewcustom(self):
        self.thread.toggle_listener(keyboard.Key.esc)
        self.dg = MyWindow(self)
        self.ui = Ui_MainWindow2()
        self.ui.setupUi(self.dg)
        self.dg.show()

    def threadStart(self):
        if not self.threadstatus:
            self.threadstatus=True
            self.thread = MyThread()
            self.thread.signal.connect(self.suggestWord)
            self.thread.start()

    def button_insert(self,val):
        self.dotcount=val.count('.')
        switch_program(delay=.2)
        delete_and_type(self.word,val)
        save_new_word(self.word,val)
        self.total_text+=val+" "
        self.word=''
        self.unicode=''

    def get_word(self, val):
        if isinstance(val,str):
            if val=='back':
                if not self.word:
                    return ''
                self.word=self.word[:-1]
                if not self.word:
                    self.set_null()
                    return ''
                return self.word
            elif val in ('space','ent'): 
                if  self.unicode:
                    self.dotcount=self.unicode.count('.')
                    if val=='ent':
                        if not self.spc:
                            delete_and_type(self.word,self.unicode,'\n',offset=1)
                            if self.unicode =="।":
                                self.total_text+=self.unicode+" "
                            else: self.total_text+=self.unicode+"।"+" "
                        else:self.total_text+="।"+"\n"
                        
                    else: 
                        delete_and_type(self.word,self.unicode, offset=1)
                        self.total_text+=self.unicode+" "
                        self.spc=True
                    self.unicode=''
                else:
                    g=user_make(self.total_text)
                    x=pre_make(self.total_text)
                    t = g+[i for i in x if i not in g]
                    self.unicode=t[0] if t else ''
                    self.fill_buttons(t)
                self.word=''
                return None
            else: 
                if self.spc:self.spc=False
                self.word+=val
                return self.word
        else: 
            print('error')
            return ''

    def set_null(self):
        self.word=''
        self.unicode=''
        self.fill_buttons(['','',''])

    def stop_listening(self):
        self.set_null()
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
    
    def start_listening(self):
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.show()
    
    def fill_buttons(self, z):
        z+=['']*(3-len(z))
        self.btn1.setText(z[0])
        self.btn2.setText(z[1])
        self.btn3.setText(z[2])

    def suggestWord(self,val):
                
        if val=='stop':
            self.stop_listening()
            return
        elif val=='start':
            self.start_listening()
            return
        if self.dotcount and val=='.':
            print('ii')
            self.dotcount-=1
            return
        wd = self.get_word(val)
        if not wd: 
            return
        
        z=get_three_suggestions(wd)
        self.unicode=z[0]
        self.fill_buttons(z)

    

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.total_text :
            
            with open(r'map\userdata.txt','a', encoding='utf-8') as f:
                f.write(self.total_text)
            generate_model(r'map\userdata.txt')
        return super().closeEvent(a0)
    
    def helpdiag(self):
        self.dg = QMainWindow(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.dg)
        self.dg.show()
        

if __name__ == "__main__":
    App = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(App.exec()) 

    