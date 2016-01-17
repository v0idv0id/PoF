import sys
from PyQt4 import QtCore, QtGui
import b
from vispy import app, gloo
from vispy.util.transforms import perspective, translate, rotate
from vispy.geometry import meshdata as md
from vispy.geometry import generation as gen

import numpy as np

class Canvas(app.Canvas):

	def __init__(self,):		
		app.Canvas.__init__(self)
		print "Canvas init..."
		self.xcolor=0
		self.size = 50,50
		self._timer=app.Timer(1.0/60.0)
		self._timer.connect(self.on_timer)
		self._timer.start()
#		gloo.set_clear_color((1, 1, 1, 1))
#		gloo.set_state('opaque')
#		gloo.set_polygon_offset(1, 1)
		


	def on_timer(self,event):
		#print "timer..."
		if self.xcolor > 1.0:
			self.xcolor = 0
		gloo.set_clear_color((self.xcolor,1.0,1.0-self.xcolor, 1.0))
		self.update()
	
	def on_resize(self,event):
		self.size=event.size

	def on_draw(self,event):
		gloo.clear()

	def set_data(self,v,f,o):
		self.update()

	def set_color(self,c):
		self.xcolor=float(c)/100.0
		self.update()
		
	def on_mouse_move(self, event):
		x, y = event.pos
		ui.verticalSlider.setValue(x)
		print x," ",y

	def on_mouse_press(self, event):
		print event


def xxx():
	print "x"

def blubb(data):
	print data

def scon():
	ui.verticalSlider.valueChanged.connect(ui.lcdNumber.display)
	ui.verticalSlider.valueChanged.connect(canvas.set_color)
	#ui.verticalSlider.valueChanged.connect(blubb)


appi = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = b.Ui_MainWindow()
ui.setupUi(MainWindow)
canvas = Canvas()
canvas.create_native()
canvas.native.setParent(MainWindow)
canvas.measure_fps()
#use("pyqt4")
c2=canvas.native
ui.hl.addWidget(canvas.native)
ui.hl.addWidget(c2)


scon()
MainWindow.show()
appi.exec_()
sys.exit(appi.exec_())

