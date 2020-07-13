# -*- coding: utf-8 -*-
"""
Created on May 2020

@author: Alfredo Remon
"""
from mainWindows import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QFileDialog, QInputDialog
import sys
import json
import requests
import BodyPass as BP
import pyperclip


metrics_provided = []
metrics_to_retrieve = []
metricsAll = ["","Age","AnkleGirthAvg","AnkleGirthRight","BackArmpitsContour","BackNeckHeight","BackNeckPointToWaist","BackNeckToKneeHeight","BackShoulderWidth","BustGirth","BustHeight","BustPointWidth","CervicaleToKneeHeight", "CountryCode","DistanceNeckHip","ElbowGirthAvg","ElbowGirthLeft","ElbowGirthRight","ForearmGirthAvg","ForearmGirthLeft","ForearmGirthRight","FrontNeckHeight","FrontalArmpitContour","Gender","HeadGirth","HipBreadth","HipGirth","HipHeight","InsideLegHeight","KneeGirthAvg","KneeGirthLeft","KneeGirthRight","KneeHeight","KneeHeightLeft","KneeHeightRight","LowerArmLengthLeft","LowerArmLengthRight","LowerArmLengthAvg","MaximumHipGirthHeight","MinimumLegGirthAvg","MinimumLegGirthLeft","MinimumLegGirthRight","NeckGirth","NeckShoulderPointToWaistAvg","NeckShoulderPointToWaistLeft","NeckShoulderPointToWaistRight","OuterArmLength","OuterArmLengthLeft","OuterArmLengthRight","ScyeDepth","ShoulderBiacromicalBreadth","ShoulderLengthLeft","ShoulderLengthRight","SideNeckPointToWaistLevelAvg","SideNeckPointToWaistLevelLeft","SideNeckPointToWaistLevelRight","Stature", "ThighGirthAvg","ThighGirthLeft","ThighGirthRight","TopHipGirth","TorsoHeight","UnderBustGirth","UpperArmGirthAvg","UpperArmGirthLeft","UpperArmGirthRight","UpperArmLengthAvg","UpperArmLengthLeft","UpperArmLengthRight","VolumeBody","WaistBreadth","WaistFrontalContour","WaistGirth","WaistHeight","WaistToButtockLength","WaistToKneeHeight","Weight","WristGirthAvg","WristGirthLeft","WristGirthRight"]

class First(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(First, self).__init__(parent)
        self.setupUi(self)
        
        self.setWindowTitle('EasyQuery0_1D3D')
        self.setWindowIcon(QtGui.QIcon('logoIBV_red.png'))

        loadToken = QtWidgets.QAction('&Load Token', self)      
        loadToken.triggered.connect(self.menuLoadToken)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(loadToken)
        
        
        self.loadData( )
        self.setMode( 0 )

        self.statusBar()

        self.butRetrieveAvatar.clicked.connect(self.buttonRetrieveAvatar)
        self.leDataCode.textChanged.connect(self.checkDataCode)        
##        self.butRunQ0.clicked.connect(self.buttonRunQ0Pressed)
        self.butCopyLink.clicked.connect(self.buttonCopyLink)
        self.butCopyMetrics.clicked.connect(self.buttonCopyMetrics)
        self.butAddMetricRet.clicked.connect(self.buttonAddMetricRetPressed)
        self.butMetricsRet.clicked.connect(self.buttonRetrieveMetrics)


    def menuLoadToken(self):
        text, ok = QInputDialog.getText(self, 'Load Token', 'Enter your token:')
        if ok:
            self.JWTToken.setText(text)
            ses, token = BP.initSession( text )
            if( len(token)>0 ):
                name = BP.getDefaultWallet( token )
                if( len(name)>0 ):
                    self.lToken.setText("Current identity:     "+name)
                else:
                    self.lToken.setText( "Warning: Empty Wallet" )
            else:
                self.lToken.setText( "NON VALID TOKEN" )

        
    def checkDataCode(self):
        code = self.leDataCode.text()
        if(len(code)==11):
            self.TellUser('Valid format data code')
            self.setMode(1)
        else:
            self.TellUser('Input a valid data code')
            self.clearResults()
            self.setMode(0)          

    def clearResults(self):
        self.lUrl.setText('-')
        self.listWidget_2.clear()
        self.lvMetricsRetrieved.clear()
        metrics_provided.clear()
        metrics_to_retrieve = []
        for i in range(self.cbMetricRet.count()):
            self.cbMetricRet.model().item(i).setEnabled(True)        
        self.setMode(0)
        

    def setMode( self, mode ):
        if mode == 0:
            self.gbRetrieveAvatar.setEnabled(False)
            self.gbRetrieveMetrics.setEnabled(False)
            self.butMetricsRet.setEnabled(False)
            self.butRetrieveAvatar.setEnabled(False)
            self.butCopyLink.hide()
            self.butCopyMetrics.hide()
            self.TellUser('Input a valid data code')
        if mode == 1:
            self.gbRetrieveAvatar.setEnabled(True)
            self.gbRetrieveMetrics.setEnabled(True)
            self.butCopyLink.hide()
            self.butCopyMetrics.hide()
            self.butMetricsRet.setEnabled(False)
            self.butRetrieveAvatar.setEnabled(True)            
        if mode == 10:
            self.gbRetrieveAvatar.setEnabled(True)
            self.gbRetrieveMetrics.setEnabled(True)            
            self.butCopyLink.show()
        if mode == 20:
            self.gbRetrieveAvatar.setEnabled(True)
            self.gbRetrieveMetrics.setEnabled(True)            
            self.butCopyMetrics.show()


        

    def BuildJSONtextQAM( self ):
        cadena = ""
        for i,M in enumerate(metrics_to_retrieve):
            cadena = cadena + M
            if i<len(metrics_to_retrieve)-1:
                cadena = cadena+","
        jsontext = ""
        if len(cadena)>0:
            jsontext = jsontext+"{\n"
            jsontext = jsontext+"\"$class\": \"org.bodypass.model.QueryDataTypeQA_M\",\n"
            jsontext = jsontext+"  \"queryParams\": [\n"
            jsontext = jsontext+"      {\n"
            jsontext = jsontext+"         \"attribute\": \"data_code\",\n"
            jsontext = jsontext+"         \"value\": \""+(self.leDataCode.text())+"\"\n"
            jsontext = jsontext+"      },\n"
            jsontext = jsontext+"      {\n"
            jsontext = jsontext+"         \"attribute\": \"metrics\",\n"       
            jsontext = jsontext+"         \"value\": \""+cadena+"\"\n"
            jsontext = jsontext+"      }\n"
            jsontext = jsontext+"    ]\n"
            jsontext = jsontext+"}\n"
        return jsontext        

    def buttonCopyLink(self):
        pyperclip.copy(self.lUrl.text())

    def buttonCopyMetrics(self):
        cadena = ""
        for i in range(self.lvMetricsRetrieved.count()):
            cadena = cadena+self.lvMetricsRetrieved.item(i).text()+"\n"
        pyperclip.copy(cadena)


    def buttonAddMetricRetPressed(self):
        if(not(self.cbMetricRet.currentText()=="")):
            metrics_to_retrieve.append(self.cbMetricRet.currentText())
            self.listWidget_2.clear()

            for M in metrics_to_retrieve:
                self.listWidget_2.addItem(M)
            
            self.cbMetricRet.model().item(self.cbMetricRet.currentIndex()).setEnabled(False)
            self.cbMetricRet.setCurrentIndex(0)
            self.butMetricsRet.setEnabled(True)
        
      

    def buttonRetrieveAvatar(self):
        identity = self.lToken.text()
        self.lUrl.setText("")
        if (identity.find('Current identity') == -1):
            QMessageBox.about(self, "Error", "No token loaded. Use the 'Load token' option in the menu to load a valid token.")
            return
        ses, token = BP.initSession( self.JWTToken.text() )
        code = self.leDataCode.text()
        self.TellUser("performing QA_3D for model "+code)
        TRID_3D = BP.QA_3D( token, code)
        self.TellUser("retrieving PATH to model")
        path=''
        path = BP.getModelPath( token, code )
        self.TellUser(path)
        if( path.find('error')> -1 ):
            self.lUrl.setText("An error ocurred. Check the code and try again.")
        else:
            self.lUrl.setText(path)
            self.setMode(10)
            self.TellUser("")
   
        
    def buttonRetrieveMetrics(self):
        ses, token = BP.initSession( self.JWTToken.text() )
        self.TellUser("Building and runing query")      

        inputjson = self.BuildJSONtextQAM( )
   
        TRID = BP.QA_metrics( token, inputjson )
        self.TellUser("Retrieving metrics from response")

        self.lvMetricsRetrieved.clear()

        if( TRID.find('error')== -1 ):
            resp=BP.getTransaction( token, TRID )
            datar= resp.json()
            self.lvMetricsRetrieved.clear()
            for K in (datar['eventsEmitted'][0])['measurements']:
                cadena = K['metricID'].split("#")[0]+" = "+K['value'][0]
                self.lvMetricsRetrieved.addItem(cadena)
            self.TellUser("")
            self.butCopyMetrics.show()

        else:
            self.lvMetricsRetrieved.clear()
            self.TellUser("An error ocurred. Try to launch it again.")

    def TellUser(self, cadena):
        if(len(cadena)==0):
            self.lStatus.setText(cadena)
            self.lStatus.hide()
        else:
            self.lStatus.show()
            self.lStatus.setText(cadena)
        QCoreApplication.processEvents()

    def loadData(self):
        
        self.cbMetricRet.addItems(metricsAll)
        self.JWTToken.setText("")
        self.JWTToken.hide()
        self.lStatus.hide()
        self.lModelID.setText("")
        self.lModelID.hide()
        self.lStatus.hide()
        self.lStatus.show()
        self.leDataCode.setInputMask("\B\O\D\Y\_NNNNNN")
                     
            

            
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = First()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


    
