import sys
from PyQt4 import QtCore, QtGui
import b
from vispy import app, gloo
from vispy.util.transforms import perspective, translate, rotate
from vispy.geometry import meshdata as md
from vispy.geometry import generation as gen

import numpy as np

from vispy.gloo import Program, VertexBuffer, IndexBuffer
from vispy.util.transforms import perspective, translate, rotate
from vispy.geometry import create_cube

import cv2
import math

import threading

vertex = """
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform sampler2D texture;

attribute vec3 position;
attribute vec2 texcoord;
attribute vec3 normal;
attribute vec4 color;

varying vec2 v_texcoord;
void main()
{
    gl_Position = projection * view * model*  vec4(position,1.0);
    v_texcoord = texcoord;
}
"""

fragment = """
uniform sampler2D texture;
varying vec2 v_texcoord;
void main()
{
    gl_FragColor = texture2D(texture, v_texcoord);
}
"""

def checkerboard(grid_num=8, grid_size=32):
    row_even = grid_num // 2 * [0, 1]
    row_odd = grid_num // 2 * [1, 0]
    Z = np.row_stack(grid_num // 2 * (row_even, row_odd)).astype(np.uint8)
    return 255 * Z.repeat(grid_size, axis=0).repeat(grid_size, axis=1)



class Canvas(app.Canvas):

	def __init__(self,):		
		app.Canvas.__init__(self)
		print "Canvas init..."
		self.xcolor=0.0
		self.size = 300,300
		self.fid=0
#		self._timer=app.Timer(1.0/60.0)
		self._timer=app.Timer('auto')
#		self.cap = cv2.VideoCapture('c.mp4')
#		self.ret,self.frame= self.cap.read()
		self._timer.connect(self.on_timer)

		# Build cube data
		V, I, _ = create_cube()
		vertices = VertexBuffer(V)
		self.indices = IndexBuffer(I)

		# Build program
		self.program = Program(vertex, fragment)
		self.program.bind(vertices)

		# Build view, model, projection & normal
		view = translate((0, 0, -4))
		model = np.eye(4, dtype=np.float32)
		self.program['model'] = model
		self.program['view'] = view
		self.program['texture'] = rt[self.fid].frame
		self.program['texture'] = checkerboard()

		self.activate_zoom()

		self.phi, self.theta = 0, 0

		# OpenGL initalization
		gloo.set_state(clear_color=(0.30, 0.30, 0.35, 1.00), depth_test=True)



		self._timer.start()
		self.show()
#		gloo.set_clear_color((1, 1, 1, 1))
#		gloo.set_state('opaque')
#		gloo.set_polygon_offset(1, 1)
		


	def on_timer(self,event):
		#print "timer..."
#		self.ret,self.frame= self.cap.read()
#        	if not self.ret:
#                	self.cap.set(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO, 0);
#        		self.program['texture'] = self.frame
#		else:
#        		self.program['texture'] = self.frame
		self.program['texture'] = gloo.Texture2D(rt[self.fid].frame)
		if self.xcolor > 1.0:
			self.xcolor = 0.0
		#gloo.set_clear_color((self.xcolor,1.0,1.0-self.xcolor, 1.0))
		self.theta += .5
        	self.phi += 1*self.xcolor
        	self.program['model'] = np.dot(rotate(self.theta, (0, 0, 1)),
                                       rotate(self.phi, (0, 1, 0)))

		self.update()
	
	def on_resize(self,event):
		self.activate_zoom()
		#self.size=event.size

	def activate_zoom(self):
        	gloo.set_viewport(0, 0, *self.physical_size)
        	projection = perspective(45.0, self.size[0] / float(self.size[1]),2.0, 10.0)
       		self.program['projection'] = projection


	def on_draw(self,event):
		gloo.clear(color=True, depth=True)
	        self.program.draw('triangles', self.indices)
		#gloo.clear()

	def set_data(self,v,f,o):
		self.update()

	def set_color(self,c):
		self.xcolor=float(c)/100.0
		self.update()
		
	def on_mouse_move(self, event):
		x, y = event.pos
		ui.verticalSlider.setValue(x)
		#print x," ",y

	def on_mouse_press(self, event):
		print event

	def set_footage(self,x):
		self.fid=x


class ReaderThread ( threading.Thread ):

   def __init__ ( self, footage,fid ):
      print "Reading: ",footage
      self.footage = footage
      self.fid = fid
      self.frame=[]
      self.cap = cv2.VideoCapture(self.footage)
      self.ret,self.frame= self.cap.read()

      threading.Thread.__init__ ( self )

   def run ( self ):
	while True:
		ret,self.x= self.cap.read()
		#print ret
		if not ret:
			print "rewind...."
			self.cap.set(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO, 0);
			ret,self.x= self.cap.read()
		b,g,r=cv2.split(self.x)
		self.frame=cv2.merge([r,g,b])
		#cv2.cvtColor(self.frame,self.frame,cv2.COLOR_RGB2BGR)
		#cv2.waitKey(0)
		#print "read..."
		#canvas.program['texture'] = self.frame
		

def xxx():
	print "x"

def blubb(data):
	print data

def scon():
	ui.verticalSlider.valueChanged.connect(ui.lcdNumber.display)
	ui.verticalSlider.valueChanged.connect(canvas.set_color)
	#ui.verticalSlider.valueChanged.connect(canvas2.set_color)
	#ui.verticalSlider.valueChanged.connect(blubb)


appi = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = b.Ui_MainWindow()
ui.setupUi(MainWindow)

rt=[None]*10

rt[0]=ReaderThread ('cc.mp4', 1 )
rt[0].start()

#rt[1]=ReaderThread ('cc.mp4', 2 )
#rt[1].start()


canvas = Canvas()
canvas.set_footage(0);
canvas.create_native()
canvas.native.setParent(MainWindow)
canvas.measure_fps()

#canvas2 = Canvas()
#canvas.set_footage(0);
#canvas2.create_native()
#canvas2.native.setParent(MainWindow)
#canvas2.measure_fps()

#use("pyqt4")

ui.hl.addWidget(canvas.native)
ui.hl.addWidget(canvas.native)


scon()
MainWindow.show()
appi.exec_()
sys.exit(appi.exec_())

