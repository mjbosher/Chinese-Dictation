import sys
from PyQt5.QtWidgets import (QWidget, QGridLayout, QPushButton, QApplication,QLabel,QRadioButton,QComboBox,QSpinBox)
from PyQt5 import QtGui,QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QObject
import numpy as np
import pandas as pd
from google_speech import Speech
import time
import os
from googletrans import Translator
import random
import sys

global config_file
global repeat_file
config_file = 'config'
repeat_file = 'repeated'
#dont forget to change output csv path
class Main(QWidget): 
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		grid = QGridLayout()
		
		title = QLabel('<h1 align="center">Chinese Dictation</h1>')
		title.setFont(QtGui.QFont("Ubuntu", 20, QtGui.QFont.Bold))
		title.setStyleSheet("color: rgb(85,170,255);background-color:rgb(28,33,39)")
		grid.addWidget(title, 1,0)

		text = ['START','SETTINGS','CLEAR WORDS','EXIT']
		button1 = QPushButton()
		button1.setFont(QtGui.QFont("Ubuntu", 20, QtGui.QFont.Bold))
		button1.clicked.connect(self.dictate_)
		button1.setStyleSheet("color: rgb(154,205,50);")
		button1.setText(text[0])
		grid.addWidget(button1, 2,0)

		button2 = QPushButton(text[1])
		button2.setFont(QtGui.QFont("Ubuntu", 20, QtGui.QFont.Bold))
		button2.setStyleSheet("color: rgb(154,205,50)")
		button2.clicked.connect(self.settings_)
		grid.addWidget(button2, 3,0)


		button3 = QPushButton(text[2])
		button3.setFont(QtGui.QFont("Ubuntu", 20, QtGui.QFont.Bold))
		button3.setStyleSheet("color: rgb(154,205,50)")
		button3.clicked.connect(self.clear)
		grid.addWidget(button3, 4,0)


		button4 = QPushButton(text[3])
		button4.setFont(QtGui.QFont("Ubuntu", 20, QtGui.QFont.Bold))
		button4.setStyleSheet("color: rgb(154,205,50)")
		button4.clicked.connect(self.exit)
		grid.addWidget(button4, 5,0)

		self.setStyleSheet('background-color: rgb(22,26,31)')
		self.move(300, 150)
		self.setLayout(grid) 
		self.setGeometry(300, 300, 350, 100)
		self.setWindowTitle('Dictation')
		self.setWindowIcon(QIcon('icon.jpg'))
		self.show()
	def dictate_(self,name):
		self.dictate = Dictate()
		self.close()
		self.dictate.show()
	def settings_(self,name):
		self.settings = Settings()
		self.close()
		self.settings.show()
	def exit(self):
		QApplication.quit()
	def clear(self):
		Config.Clear_repeat(repeat_file)
		name = 'Repeated words have been cleared'
		self.exPopup = examplePopup(name)
		self.exPopup.setGeometry(400, 400, 200, 100)
		self.exPopup.show()

class examplePopup(QWidget):
	def __init__(self, name):
		super().__init__()

		self.name = name
		self.initUI()
	def initUI(self):
		grid = QGridLayout()
		self.setLayout(grid)
		self.move(500, 150) 
		self.setGeometry(500, 500, 500, 500)
		lblName = QLabel(self.name, self)
		lblName.setStyleSheet("color: rgb(85,170,255)")
		grid.addWidget(lblName, 1,0)
		button4 = QPushButton('OK')
		button4.setFont(QtGui.QFont("Ubuntu", 20, QtGui.QFont.Bold))
		button4.setStyleSheet("color: rgb(154,205,50)")
		button4.clicked.connect(self.close)
		grid.addWidget(button4, 5,0)
		self.setWindowTitle('Dictation')
		self.setWindowIcon(QIcon('icon.jpg'))
class Settings(QWidget): 
	switch_window = QtCore.pyqtSignal()
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		try:
			config=Config.Read(config_file)
			random_words_=config['random_words']
			timeout_=config['timeout']
			language_=config['language']
			repeat_words_ = config['repeat_word']
		except:
			config=Config.Read(config_file)
			random_words_=config['random_words']
			timeout_=config['timeout']
			language_=config['language']
			repeat_words_ = config['repeat_word']
		self.b1_res=random_words_
		self.b2_res=repeat_words_
		self.b3_res=language_
		self.b4_res=timeout_
		self.config_file =config_file

		if language_ == 'zh':
			language_ = 'Chinese'
		elif language_ == 'en':
			language_ = 'English'
		elif language_ == 'ru':
			language_ = 'Russian'
		elif language_ == 'mixed':
			language_ = 'Mixed'
		timeout_=int(timeout_)
 
		grid = QGridLayout()
		self.setLayout(grid)
		random_words = QLabel('<b align="center">Random Words</b>')
		random_words.setFont(QtGui.QFont("Ubuntu", 20, QtGui.QFont.Bold))
		random_words.setStyleSheet("color: rgb(85,170,255);background-color:rgb(22,26,31)")
		grid.addWidget(random_words, 0,0)
		self.b1_1 = QRadioButton("On")
		self.b1_1.toggled.connect(lambda:self.btnstate1(self.b1_1))
		self.b1_2 = QRadioButton("Off")
		self.b1_2.toggled.connect(lambda:self.btnstate1(self.b1_2))
		if random_words_ == 'True':
			self.b1_1.setChecked(True)
		elif random_words_ == 'False':
			self.b1_2.setChecked(True)
		grid.addWidget(self.b1_1,0,1)
		grid.addWidget(self.b1_2,0,2)

		random_words_help = QLabel('<b align="center">When turned on, the program well choose<br>random words from the start of the wordlist to a point that you specify</b>')
		random_words_help.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
		random_words_help.setFont(QtGui.QFont("Ubuntu", 10, QtGui.QFont.Bold))
		random_words_help.setStyleSheet("color: rgb(154,205,50);background-color:rgb(22,26,31)")
		grid.addWidget(random_words_help, 1,0,1,1)

		repeat_words = QLabel('<b align="center">Repeat Words</b>')
		repeat_words.setFont(QtGui.QFont("Ubuntu", 20, QtGui.QFont.Bold))
		repeat_words.setStyleSheet("color: rgb(85,170,255);background-color:rgb(22,26,31)")
		
		grid.addWidget(repeat_words, 2,0)
		self.b2_1 = QRadioButton("On")
		self.b2_1.toggled.connect(lambda:self.btnstate2(self.b1_1))
		self.b2_2 = QRadioButton("Off")
		self.b2_2.toggled.connect(lambda:self.btnstate2(self.b1_2))
		if repeat_words_ == 'True':
			self.b2_1.setChecked(True)
		elif repeat_words_ == 'False':
			self.b2_2.setChecked(True)
		grid.addWidget(self.b2_1,2,1)
		grid.addWidget(self.b2_2,2,2)
		repeat_words_help = QLabel('<b align="center">Only valid if <u color = "red">"repeat_words" </u> is turned on.<br> This option stores completed words in a file when turned on <br> The words stored in the file will not be spoken again by the computer until the file is cleared</b>')
		repeat_words_help.setFont(QtGui.QFont("Ubuntu", 10, QtGui.QFont.Bold))
		repeat_words_help.setStyleSheet("text-align:center;color: rgb(154,205,50);background-color:rgb(22,26,31)")
		repeat_words_help.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)		
		grid.addWidget(repeat_words_help, 3,0,1,1)
		
		language = QLabel('<b align="center">Select the speakers language</b>')
		language.setFont(QtGui.QFont("Ubuntu", 20, QtGui.QFont.Bold))
		language.setStyleSheet("color: rgb(85,170,255);background-color:rgb(22,26,31)")
		grid.addWidget(language, 4,0)
		b3 = QComboBox(self)
		b3.addItem("Chinese")
		b3.addItem("English")
		b3.addItem("Russian")
		b3.addItem("Mixed")
		b3.setCurrentText(language_)
		grid.addWidget(b3,4,1,1,2)
		b3.activated[str].connect(self.onChanged)

		language_help = QLabel('<b align="center">Select the language that you want the speaker to use<br><u>Mixed</u> creates audios in random languages from the languuage selection</b>')
		language_help.setFont(QtGui.QFont("Ubuntu", 10, QtGui.QFont.Bold))
		language_help.setStyleSheet("text-align:center;color: rgb(154,205,50);background-color:rgb(22,26,31)")
		language_help.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)	
		grid.addWidget(language_help, 5,0,1,1)
		
		timeout = QLabel('<b align="center">Time between words</b>')
		timeout.setFont(QtGui.QFont("Ubuntu", 20, QtGui.QFont.Bold))
		timeout.setStyleSheet("color: rgb(85,170,255);;background-color:rgb(22,26,31)")
		
		grid.addWidget(timeout, 6,0)
		b4 = QSpinBox()
		b4.valueChanged.connect(self.valuechange)
		b4.setValue(timeout_)
		grid.addWidget(b4,6,1,1,2)
		
		timeout_help = QLabel('<b align="center">Time between spoken words (seconds) </b>')
		timeout_help.setFont(QtGui.QFont("Ubuntu", 10, QtGui.QFont.Bold))
		timeout_help.setStyleSheet("color: rgb(154,205,50);background-color:rgb(22,26,31)")
		timeout_help.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
		grid.addWidget(timeout_help,7,0,1,1)

		button1 = QPushButton()
		button1.setFont(QtGui.QFont("Ubuntu", 15, QtGui.QFont.Bold))
		button1.clicked.connect(self.log)
		button1.setStyleSheet("color: rgb(154,205,50);")
		button1.setText('OK')
		grid.addWidget(button1, 8,2)
		
		button2 = QPushButton()
		button2.setFont(QtGui.QFont("Ubuntu", 15, QtGui.QFont.Bold))
		button2.clicked.connect(self.exit)
		button2.setStyleSheet("color: rgb(154,205,50);")
		button2.setText('BACK')
		grid.addWidget(button2, 8,1)
		
		self.setGeometry(300, 300,350, 100)
		self.setWindowTitle('Settings')
		self.setStyleSheet('background-color: rgb(22,26,31)')
		self.setWindowIcon(QIcon('icon.jpg'))
		self.show()

	def valuechange(self,b):
		self.b4_res = b
	def btnstate1(self,b):
		self.b1_res = b.text()
	def btnstate2(self,b):
		self.b2_res = b.text()
	def onChanged(self,text):
		self.b3_res = text
	def log(self):
		if self.b1_res == 'On':
			self.b1_res = 'True'
		elif self.b1_res == 'Off':
			self.b1_res = 'False'

		if self.b2_res == 'On':
			self.b2_res = 'True'
		elif self.b2_res == 'Off':
			self.b2_res = 'False'

		if self.b3_res == 'English':
			self.b3_res = 'en'
		elif self.b3_res == 'Chinese':
			self.b3_res = 'zh'
		elif self.b3_res == 'Russian':
			self.b3_res = 'ru'
		elif self.b3_res == 'Mixed':
			self.b3_res = 'mixed'
		config=dict(
				random_words=self.b1_res,
				timeout=self.b4_res,
				language=self.b3_res,
				repeat_word=self.b2_res)
		Config.Write(config,self.config_file)
		self.main = Main()
		self.close()
		self.main.show()

	def exit(self):
		self.main = Main()
		self.close()
		self.main.show()
class Dictate(QWidget): 
	switch_window = QtCore.pyqtSignal()
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		self.grid = QGridLayout()
		self.setStyleSheet('background-color: rgb(22,26,31)')
		file = 'output.csv'
		try:
			self.config=Config.Read(config_file)
		except:
			self.config=Config.Read(config_file)
		self.table = Table.Get(file)
		#sample = Table.Sample(table,config,repeat_file)
		self.b1_res = 0
		self.b2_res = 100
		self.start = QLabel('<b align="center">Starting index</b>')
		self.start.setFont(QtGui.QFont("Ubuntu", 20, QtGui.QFont.Bold))
		self.start.setStyleSheet("color: rgb(85,170,255);;background-color:rgb(22,26,31)")
		
		self.grid.addWidget(self.start, 0,0)
		self.b1 = QSpinBox()
		self.b1.valueChanged.connect(self.get_b1)
		self.b1.setValue(1)
		self.b1.setMinimum(1)
		self.b1.setMaximum(len(self.table)-1)
		self.grid.addWidget(self.b1,0,1,1,2)
		
		self.start_help = QLabel('<b align="center">The number of the word in the wordlist<br>which the program should start reading from</b>')
		self.start_help.setFont(QtGui.QFont("Ubuntu", 10, QtGui.QFont.Bold))
		self.start_help.setStyleSheet("color: rgb(154,205,50);background-color:rgb(22,26,31)")
		self.start_help.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
		self.grid.addWidget(self.start_help,1,0,1,1)

		self.max_words = QLabel('<b align="center">End index</b>')
		self.max_words.setFont(QtGui.QFont("Ubuntu", 20, QtGui.QFont.Bold))
		self.max_words.setStyleSheet("color: rgb(85,170,255);;background-color:rgb(22,26,31)")
		
		self.grid.addWidget(self.max_words, 2,0)
		self.b2 = QSpinBox()
		self.b2.setMaximum(len(self.table))
		self.b2.valueChanged.connect(self.get_b2)
		self.b2.setValue(100)
		self.grid.addWidget(self.b2,2,1,1,2)
		
		self.end_help = QLabel('<b align="center">The number of the word in the wordlist<br>which the program should end at</b>')
		self.end_help.setFont(QtGui.QFont("Ubuntu", 10, QtGui.QFont.Bold))
		self.end_help.setStyleSheet("color: rgb(154,205,50);background-color:rgb(22,26,31)")
		self.end_help.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
		self.grid.addWidget(self.end_help,3,0,1,1)
		
		self.button1 = QPushButton()
		self.button1.setFont(QtGui.QFont("Ubuntu", 15, QtGui.QFont.Bold))
		self.button1.clicked.connect(self.get_number)
		self.button1.setStyleSheet("color: rgb(154,205,50);")
		self.button1.setText('OK')
		self.grid.addWidget(self.button1, 8,2)
		
		self.button2 = QPushButton()
		self.button2.setFont(QtGui.QFont("Ubuntu", 15, QtGui.QFont.Bold))
		self.button2.clicked.connect(self.exit)
		self.button2.setStyleSheet("color: rgb(154,205,50);")
		self.button2.setText('BACK')
		self.grid.addWidget(self.button2, 8,1)
			
		self.setLayout(self.grid) 
		self.setGeometry(300, 300, 350, 100)
		self.setWindowTitle('Dictate')
		self.setWindowIcon(QIcon('icon.jpg'))
		self.show()

	def get_b1(self,b):
		self.b1_res = b
	def get_b2(self,b):
		self.b2_res = b
	def get_number(self):
		self.b3_res = self.b2_res - self.b1_res
		while self.grid.count():
			item = self.grid.takeAt(0)
			widget = item.widget()
			widget.deleteLater()
		
		self.number = QLabel('<b align="center">Number of words</b>')
		self.number.setFont(QtGui.QFont("Ubuntu", 20, QtGui.QFont.Bold))
		self.number.setStyleSheet("color: rgb(85,170,255);;background-color:rgb(22,26,31)")
		
		self.grid.addWidget(self.number, 0,0)
		self.b3 = QSpinBox()
		self.b3.setMaximum(self.b3_res)
		self.b3.valueChanged.connect(self.get_b3)
		self.b3.setValue(30)
		self.grid.addWidget(self.b3,0,1,1,2)
	
		self.number_help = QLabel('<b align="center">The number of the word to be tested on</b>')
		self.number_help.setFont(QtGui.QFont("Ubuntu", 10, QtGui.QFont.Bold))
		self.number_help.setStyleSheet("color: rgb(154,205,50);background-color:rgb(22,26,31)")
		self.number_help.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
		self.grid.addWidget(self.number_help,1,0,1,3)
		
		self.button1 = QPushButton()
		self.button1.setFont(QtGui.QFont("Ubuntu", 15, QtGui.QFont.Bold))
		self.button1.clicked.connect(self.test)
		self.button1.setStyleSheet("color: rgb(154,205,50);")
		self.button1.setText('OK')
		self.grid.addWidget(self.button1, 2,2)
		
		self.button2 = QPushButton()
		self.button2.setFont(QtGui.QFont("Ubuntu", 15, QtGui.QFont.Bold))
		self.button2.clicked.connect(self.exit)
		self.button2.setStyleSheet("color: rgb(154,205,50);")
		self.button2.setText('BACK')
		self.grid.addWidget(self.button2, 2,1)
	def get_b3(self,b):
		self.b3_res = b
	def test(self):
		self.move(0, 0)
		while self.grid.count():
			item = self.grid.takeAt(0)
			widget = item.widget()
			widget.deleteLater()
		time.sleep(1)
		print(self.b3_res)
		speech = [f'You will now hear {self.b3_res} words, get your pen ready','1','2','3','go']
		for i in speech:
				Audio.Play(i,'en')

		if self.config['random_words'] == 'True':
			sample = self.table.iloc[self.b1_res-1:self.b2_res+1]
			sample = sample.sample(self.b3_res)
			for i in sample:
				if i in repeat_file and self.config['repeat_word'] == 'True':
					sample = sample.sample(self.b3_res)
				else:
					pass
					
		elif self.config['random_words'] == 'False':
			start=self.b1_res-1
			sample = self.table.iloc[start:self.b2_res+1]
			sample=sample.head(self.b3_res)
		
		self.answers = []
		if self.config['language'].lower() == 'zh':
			for i in sample.Word:
				Audio.Play(i,self.config['language'])
				time.sleep(int(self.config['timeout']))
				self.Log(i)
		elif self.config['language'].lower() == 'ru':
			for i in sample.Russian:
				Audio.Play(i,self.config['language'])
				time.sleep(int(self.config['timeout']))
				i=sample['Russian'==i].Word.items()
				self.Log(i)
		elif self.config['language'].lower() == 'en':
			translator = Translator()
			for i in sample.Word:
				x=translator.translate(i,src='zh-CN',dest='en')
				Audio.Play(x.text,self.config['language'])
				time.sleep(int(self.config['timeout']))
				self.Log(i)
		elif self.config['language'].lower() == 'mixed':
			translator = Translator()
			langs=('en','ru','zh')
			for i in sample.Word:
				choice = random.choice(langs)
				if choice != 'zh':
					x=translator.translate(i,src='zh-CN',dest=choice)
					Audio.Play(x.text,choice)
					time.sleep(int(self.config['timeout']))
				else:
					Audio.Play(i,'zh')
					time.sleep(int(self.config['timeout']))
				self.Log(i)
		self.Answers()
		self.move(0, 0)
	def Answers(self):
		column=0
		row=0 
		rows = []
		cols = [0]
		for j,i in enumerate(self.answers):
			j=j+1
			translator = Translator()
			russian=translator.translate(i,src='zh-CN',dest='ru').text
			pinyin=translator.translate(i,src='zh-CN',dest='zh-CN').pronunciation
			i=f'[{j}]<sup>{pinyin}</sup><br><b>{i}</b><br><sub>{russian}</sub>'
			#self.test_res.append(i)
			self.test_res = QLabel(i)
			self.test_res.setFont(QtGui.QFont("Ubuntu", 20, QtGui.QFont.Bold))
			self.test_res.setStyleSheet("color:black;background-color:rgb(192,192,192);")
			self.test_res.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
			self.grid.addWidget(self.test_res,column,row)
			rows.append(row)			
			row = row+1
			if row >= 11:
				column = column+1
				cols.append(column)
				row = 0
		self.button2 = QPushButton()
		self.button2.setFont(QtGui.QFont("Ubuntu", 15, QtGui.QFont.Bold))
		self.button2.clicked.connect(self.exit)
		self.button2.setStyleSheet("color: rgb(154,205,50);")
		self.button2.setText('Ok')
		self.grid.addWidget(self.button2, max(cols)+1,max(rows))
		print(max(cols)+1)
		print(max(rows)+1)
	def Log(self,word):
		answer=word
		word = f'{word}\n'
		if os.path.exists(repeat_file) == True and self.config['repeat_word'] == 'False' and self.config['random_words'] == 'False':
			f = open(repeat_file,'a')
			f.write(word)
			f.close()
		elif os.path.exists(repeat_file) == False and self.config['repeat_word'] == 'False' and self.config['random_words'] == 'False':
			os.mknod(repeat_file)
			f = open(repeat_file,'a')
			f.write(word)
			f.close()
		self.answers.append(answer)
	def exit(self):
		self.main = Main()
		self.close()
		self.main.show()
	
	def login(self):
		self.switch_window.emit()
class Config():
	def Configure():
		config=dict(
				random_words='False',
				timeout=3,
				language='zh',
				repeat_word='False')
		return(Config.Write(config,config_file))
	def Read(config_file):
		config = {}
		try:
			config_file = open(config_file,'r')
			for i in config_file:
				i=i.split('=')
				config[i[0]] = i[1].replace('\n','')
		except:
			Config.Configure()
		return(config)
	def Clear_repeat(file):
		if os.path.exists(file) == True:
			os.remove(file)
			os.mknod(file)
		else:
			os.mknod(file)
	def Write(config,config_file):
		if os.path.exists(config_file) == True:
			os.remove(config_file)
			os.mknod(config_file)
		else:
			os.mknod(config_file)
		config_file = open(config_file,'a')
		for key,item in config.items():
			item = f'{key}={item}\n'
			config_file.write(item)

class Table():
	def Get(file):
		table = pd.read_csv(file)
		table.dropna(subset=['Number','Word','Example'],inplace=True)
		table.set_index('Number',drop=True,inplace=True)
		return(table)
	
	def Sample(table,config,repeated):
		pass

class Audio():
	def Play(text,lang):
		speech = Speech(text, lang)
		speech.play()

def main():
	app = QApplication(sys.argv)
	controller = Main()
	controller.initUI()
	sys.exit(app.exec_())
'''FAILS ON START BECAUSE INPUT NEEDS TO BE TAKEN OUT OF THE TABLE SECTION '''

if __name__ == '__main__':
    main()
