#coding:utf-8
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTextEdit, QGridLayout, QMainWindow
# from PyQt5.QtWebKitWidgets import QWebView
# from PyQt5.QtCore import QUrl, QThread, pyqtSignal
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from PyQt4.QtCore import *
import re
import markdown
import time
import threading

class Thread(QThread):
	trigger = pyqtSignal(int)

	def __init__(self, parent=None):
		super(Thread,self).__init__(parent)
		# self.browser = browser

	# def setup(self, say):
	# 	self.say = say

	def run(self):
		while 1:
			# self.browser.reload()
			time.sleep(1)
			self.trigger.emit(1)


class Md(QWidget):

	def __init__(self, parent=None):
		super(Md,self).__init__(parent)

		self.initUI()

	# def print_(self):
	# 	text = self.textedit1.toPlainText().toUtf8()
	# 	print(text)
	# 	with open('/tmp/md.html','w') as f:
	# 		f.write(markdown.markdown(text))
		
		# self.browser.load(QUrl('file:///tmp/md.html'))
		# self.browser.load(QUrl('file:///home/biebergong/Documents/%E5%A6%82%E4%BD%95%E5%91%8A%E5%88%AB%E7%99%BE%E5%BA%A6/%E5%A6%82%E4%BD%95%E5%91%8A%E5%88%AB%E7%99%BE%E5%BA%A6.html'))
		# self.textedit2.clean()
		# self.textedit2.append(text)

	def auto_save_(self):
		# self.textedit1.append(open(sys.argv[1]).read())
		while 1:
			# text = unicode( self.textedit1.toPlainText() )
			text = self.textedit1.toPlainText()
			p = re.compile('\n')
			text = p.sub('  \n', text)
			pp = re.compile(' +\n')
			text = pp.sub('  \n', text)
			# print(text)
			with open(self.file, 'w') as f:
				f.write(text)
			with open(self.filename+'.html','w') as f:
				f.write(markdown.markdown(text))
			# self.browser.load(QUrl('file:///tmp/md.html'))
			time.sleep(2)
			# self.browser.reload()

	def auto_save(self):
		t = threading.Thread(target=self.auto_save_)
		t.setDaemon(True)
		t.start()

	def browser_reload(self, i):
		self.browser.reload()

	def output_pdf(self):
		p = QPrinter()
		p.setOutputFormat(QPrinter.PdfFormat)
		p.setOutputFileName(self.filename+'.pdf')
		self.browser.print(p)
		self.show_message('PDF已保存到工作目录')

	def show_message_(self, string):
		self.message.setText(string)
		time.sleep(4)
		self.message.setText('')

	def show_message(self, string):
		# print(string)
		t = threading.Thread( target=self.show_message_,args=(string,) )
		t.setDaemon(True)
		t.start()		

	def initUI(self):
		# okbutton = QPushButton('Ok')
		# okbutton.clicked.connect(self.print_)
		# cancelbutton = QPushButton('Cancel')
		self.file = sys.argv[1]
		self.filename = '.'.join( self.file.split('.')[:-1] )

		# self.textedit1 = QTextEdit()
		self.textedit1 = QPlainTextEdit()
		# self.textedit1.zoomIn(2)
		self.textedit1.setFont(QFont('黑体',12))
		# self.textedit1.setTextFormat(QtextEdit.PlainText)
		# self.textedit1.resize(800,600)
		self.textedit1.setMinimumWidth(500)
		t = open(self.file).read()
		print(t)
		self.textedit1.appendPlainText(open(self.file).read())
		self.auto_save()
		# self.textedit2 = QTextEdit()

		self.browser = QWebView()
		self.browser.showMaximized()
		self.browser.coding = self.browser.settings()
		self.browser.coding.setDefaultTextEncoding('utf-8')
		# self.browser = QWebView()
		# self.browser.resize(100,100)
		self.browser.load( QUrl(self.filename+'.html') )
		thread = Thread(self)
		thread.trigger.connect(self.browser_reload)
		thread.start()
		# self.browser.load(QUrl('http://h.nimingban.com'))

		self.message = QLabel('')
		self.show_message('v0.1.0 written by BJ')
		# self.message.setText('a')

		hbox = QHBoxLayout()
		# grid = QGridLayout()
		# grid.setSpacing(0)
		hbox.setSpacing(0)
		vbox = QVBoxLayout()
		vbox.setSpacing(0)
		# vbox.addStretch()
		# hbox.addWidget(okbutton)
		hbox.addWidget(self.textedit1)
		hbox.addWidget(self.browser)
		vbox.addLayout(hbox)
		vbox.addWidget(self.message)
		# grid.addWidget(self.textedit2, 1, 1, 1, 2)
		# hbox.addLayout(vbox)
		# hbox.addWidget(self.browser)

		# vbox.addStretch()
		# vbox.addLayout(hbox)

		self.setLayout(vbox)
		# self.setLayout(vbox)


class mainWindow(QMainWindow):
	def __init__(self):
		super().__init__()

		md = Md()

		outputAction = QAction( QIcon(), '输出PDF', self )
		# outputAction.set
		outputAction.triggered.connect(md.output_pdf)
		self.toolbar = self.addToolBar('output')
		self.toolbar.addAction(outputAction)


		self.setGeometry(100, 100, 1100, 640)
		self.setWindowTitle('Toyoung')
		self.setCentralWidget(md)
		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	mainwindow = mainWindow()
	sys.exit(app.exec_())