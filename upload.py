#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, math
from PyQt4 import QtGui, QtCore
from PyDictionary import PyDictionary
import upload_ui
import argparse
import uploadvideo as uv



# Shows the preview window showcasing the changes made in the editor window
class Upload(QtGui.QWizard) :

    closeApp = QtCore.pyqtSignal() #signal , slot to be with caller

    def __init__(self, ui):
        super(Upload, self).__init__()
        self.ui = ui
        

    def setup_connections(self) :
        self.ui.seedTagBtn.clicked.connect( self.populateTextBoxWithSynonyms )
        self.ui.youtubeBtn.clicked.connect( self.authenticateYoutube )
        

    def getSynonyms( self, seedTag ):
        dictionary=PyDictionary()
        list_of_syn = dictionary.synonym(str(seedTag))
        return list_of_syn
        
    def populateTextBoxWithSynonyms( self ) :
        seedTag = self.ui.seedTagTextBox.text()
        list_of_syn = self.getSynonyms( seedTag )
        string_of_syn = ",".join( list_of_syn )
        self.ui.textEdit.setText( string_of_syn )

    def authenticateYoutube( self ):
        args = argparse.Namespace(file="",title="",description="",keywords="",category="",privacyStatus="",auth_host_name='localhost', auth_host_port=[8080, 8090],logging_level='ERROR', noauth_local_webserver=False)
        self.youtubeObj = uv.authenticateWithYoutube(args)
        if self.youtubeObj is not None :
            self.ui.youtubeBtn.setText("Auth successful")

                


    def accept(self):  # gets triggered on exiting the wizard
        print "yo"

    def closeEvent(self, event) :
        self.closeWidget()

    def closeWidget(self) :
        self.closeApp.emit()
        self.close()



def showUpload( caller  ) :
    ui = upload_ui.Ui_Wizard()
    widget = Upload( ui )
    ui.setupUi(widget)
    widget.setup_connections()
    widget.caller = caller
    widget.show()
    return widget



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    widget = showUpload(app)
    sys.exit(app.exec_())


     
