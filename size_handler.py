#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore


class Widget(QtGui.QWidget) :

    

    def __init__(self):
        super(Widget, self).__init__()
        self.initUI()
        self.setMouseTracking(True)  #mouse move will always be called, unlike earlier when it meant drag
        

    def initUI(self, sizeHandler = None):      
        self.setGeometry(300, 500, 350, 300)
        self.setWindowTitle('Colours')
        self.sizeHandler = sizeHandler
        self.bounds = QtCore.QRect(50, 100, 250, 200)
        self.label = self.bannerLabel = QtGui.QLabel(self)
        self.label.setText("Hello welcome to sajjanpur")
        self.label.move(50,50)
        self.show()

    def paintEvent(self, event):

        if self.sizeHandler is not None :
            self.bounds = self.sizeHandler.bounds

        qp = QtGui.QPainter()
        qp.begin(self)
        color = QtGui.QColor(0, 0, 0)
        color.setNamedColor('#d4d4d4')
        qp.setPen(color)
        qp.setBrush(QtGui.QColor("Red"))
        qp.drawRect(  self.bounds )
        qp.end()

        if self.sizeHandler is not None :
            self.sizeHandler.paintEvent( event)

        
    def mousePressEvent(self, event):
        if self.sizeHandler is not None :
            self.sizeHandler.mousePressEvent(event)
        else: #size handler is  none
            print "handler added"
            if self.bounds.contains( event.pos()) :
                self.sizeHandler = SizeHandler(self, "rectangle", self.bounds)
                self.repaint()


    def mouseReleaseEvent(self, event):
        if self.sizeHandler is not None :
            self.sizeHandler.mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.sizeHandler is not None :
            self.sizeHandler.mouseMoveEvent(event)
            if self.sizeHandler.can_Hresize is True or \
                self.sizeHandler.can_Vresize is True or \
                self.sizeHandler.can_move is True:

                self.repaint()
        

class SizeHandler :

    def __init__(self, widget, obj, bounds=None) :
        self.object = obj  # could be any QPainter shape or Qlabel
        self.widget = widget
        if bounds is not None :
            self.bounds = bounds #in case of QPainter rectangle
        else :
            self.bounds = obj.boundingRect() # incase of QLabel

        self.can_Hresize = self.can_Vresize = self.can_move = False
        self.VBounds = QtCore.QRect( self.bounds.x() + self.bounds.width()/2 - 4, self.bounds.y() - 4, 8, 8)
        self.HBounds = QtCore.QRect( self.bounds.x() + self.bounds.width() - 4, self.bounds.y() + self.bounds.height()/2 - 4, 8, 8)
        self.CBounds = QtCore.QRect( self.bounds.x() + self.bounds.width()/2 - 4, self.bounds.y() + self.bounds.height()/2 - 4, 8, 8)


    def paintEvent( self, event ) :
        if self.object == "rectangle" : 
            qp = QtGui.QPainter()
            qp.begin(self.widget)
            
            color = QtGui.QColor(0, 0, 0)
            color.setNamedColor('#d4d4d4')
            qp.setPen(color)
            # vertical  handle 
            self.VBounds = QtCore.QRect( self.bounds.x() + self.bounds.width()/2 - 4, self.bounds.y() - 4, 8, 8)
            qp.setBrush(QtGui.QColor("Black"))
            qp.drawRect(  self.VBounds )


            # horizontal  handle 
            self.HBounds = QtCore.QRect( self.bounds.x() + self.bounds.width() - 4, self.bounds.y() + self.bounds.height()/2 - 4, 8, 8)
            qp.setBrush(QtGui.QColor("Black"))
            qp.drawRect( self.HBounds ) 


            # central  handle 
            self.CBounds = QtCore.QRect( self.bounds.x() + self.bounds.width()/2 - 4, self.bounds.y() + self.bounds.height()/2 - 4, 8, 8)
            qp.setBrush(QtGui.QColor("Black"))
            qp.drawRect( self.CBounds ) 


            qp.end()    

    def mousePressEvent(self, event):
        #horizontal
        if self.HBounds.contains( event.pos()) :
                self.can_Hresize = True
        #vertical
        elif self.VBounds.contains( event.pos()) :
                self.can_Vresize = True
                
        elif self.CBounds.contains( event.pos()) :
                self.can_move = True

                

    def mouseReleaseEvent(self, event):
        if self.can_Hresize == True :
            self.can_Hresize  = False

        elif self.can_Vresize == True :
            self.can_Vresize  = False
        
        elif self.can_move == True :
            self.can_move  = False

    def mouseMoveEvent(self, event):
        if self.can_Hresize == True:
            if self.object == "rectangle" :
                self.bounds.setRight(event.pos().x()) #change width of rectangle being drawn using these values

        elif self.can_Vresize == True:
            if self.object == "rectangle" :
                self.bounds.setTop(event.pos().y())  #change height Qt is awesome for giving these functions
        
        elif self.can_move == True:
            if self.object == "rectangle" :
                self.bounds = QtCore.QRect(event.pos().x() - self.bounds.width() / 2, \
                                            event.pos().y() - self.bounds.height() / 2, \
                                            self.bounds.width(), self.bounds.height()) 
        
        else : #when mouse is simply moving and hovers over handlers, change mouse cursor momentarily
            if self.HBounds.contains( event.pos()) :
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor ))

            elif self.VBounds.contains( event.pos()) :
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor ))

            elif self.CBounds.contains( event.pos()) :
                QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor ))
            else:
                QtGui.QApplication.restoreOverrideCursor() #normal cursor mode


        #repaint to be called by the caller

def main():
    
    app = QtGui.QApplication(sys.argv)
    widget = Widget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()