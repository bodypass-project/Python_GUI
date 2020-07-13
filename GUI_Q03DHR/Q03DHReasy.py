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
import csv
import json
import requests
from base64 import b64encode
import zipfile
import BodyPass as BP
import pyperclip
import os


metrics_provided = []
metrics_to_retrieve = []
metrics1D  = ["","BackNeckHeight", "InsideLegHeight", "NeckGirth", "BackShoulderWidth", "BustGirth", "UnderBustGirth", "WaistGirth", "OuterArmLength", "OuterArmLengthLeft", "OuterArmLengthRight", "LowerArmLengthLeft", "LowerArmlengthAvg", "LowerArmLengthRight", "UpperArmGirthLeft", "UpperArmGirthAvg", "UpperArmGirthRight", "WristGirthLeft", "WristGirthAvg", "WristGirthRight", "ThighGirthAvg", "KneeGirthLeft", "KneeGirthAvg", "KneeGirthRight"]
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
        self.butRunQ0.clicked.connect(self.buttonRunQ0Pressed)
        self.butCopyLink.clicked.connect(self.buttonCopyLink)
        self.butCopyMetrics.clicked.connect(self.buttonCopyMetrics)
        self.butAddMetricRet.clicked.connect(self.buttonAddMetricRetPressed)
        self.butMetricsRet.clicked.connect(self.buttonRetrieveMetrics)
        self.butLoadFile.clicked.connect(self.buttonLoadData)


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

        
    def buttonLoadData(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","ZIP Files (*.zip);;STL Files (*.stl);;PLY Files (*.ply);;OBJ Files (*.obj);;All Files (*)", options=options)
        if fileName:
            self.lFilename.setText(fileName)


    def setMode( self, mode ):
        if mode == 0:
            self.gbRetrieveAvatar.setEnabled(False)
            self.gbRetrieveMetrics.setEnabled(False)
            self.butMetricsRet.setEnabled(False)
            self.butCopyLink.hide()
            self.lstatusRetMet.hide()
        if mode == 1:
            self.gbRetrieveAvatar.setEnabled(True)
            self.gbRetrieveMetrics.setEnabled(True)
            self.butCopyLink.hide()
            self.butCopyMetrics.hide()
            self.butMetricsRet.setEnabled(False)
            self.lstatusRetMet.hide()
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
            jsontext = jsontext+"         \"value\": \""+(self.lModelID.text())+"\"\n"
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
        for i in range(self.listWidget_2.count()):
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
        

    def buttonRunQ0Pressed(self):
        identity = self.lToken.text()
        if (identity.find('Current identity') == -1):
            QMessageBox.about(self, "Error", "No token loaded. Use the 'Load token' option in the menu to load a valid token.")
            return
        
        if( self.sbWeight.value()<30 or self.sbWeight.value()>230 ):
            QMessageBox.about(self, "Error", "Value of parameter Weight is either too small or too large. It should be provided in Kg.")
            return
        if( self.sbHeight.value()<1000 or self.sbHeight.value()>2100 ):
            QMessageBox.about(self, "Error", "Value of parameter Height is either too small or too large. It should be provided in mm.")
            return
     
        if( self.sbAge.value()<10 or self.sbAge.value()>110 ):
            QMessageBox.about(self, "Error", "Value of parameter Age is either too small or too large. It should be provided in years.")
            return

        filename, file_extension = os.path.splitext(self.lFilename.text())
        file_extension = file_extension.replace('.','')

 
        if(file_extension == "zip" ):
            zipped = zipfile.ZipFile(self.lFilename.text())
            if(len(zipped.namelist()) != 1):
                QMessageBox.about(self, "Error", "Zip file must contain a single file")
                return
            aux,file_extension = os.path.splitext(zipped.namelist()[0])
            file_extension = file_extension.replace('.','')
        if( len(file_extension)<1):
            QMessageBox.about(self, "Error", "No file loaded")
            return
        if( file_extension.lower() not in ["obj","ply","stl","zip"] ):
            QMessageBox.about(self, "Error", "File extension not supported")
            return

        self.lStatusValue.setText("Building query")
        QCoreApplication.processEvents()
        self.lStatusValue.show()
        self.lStatus.show()
        QCoreApplication.processEvents()
 
        f = open(self.lFilename.text(),"rb")
        encoded = b64encode(f.read())
        cadena = encoded.decode('ASCII')

 
        json_str = "{"
        json_str = json_str+"\"$class\": \"org.bodypass.model.QueryDataTypeQ0_FB_3DHR\","
        json_str = json_str+"  \"queryParams\": ["
        json_str = json_str+"    {"
        json_str = json_str+"      \"attribute\": \"Height\","
        json_str = json_str+"      \"value\": \""+str(self.sbHeight.value())+"\""
        json_str = json_str+"    },"
        json_str = json_str+"    {"
        json_str = json_str+"      \"attribute\": \"Weight\","
        json_str = json_str+"      \"value\": \""+str(self.sbWeight.value())+"\""
        json_str = json_str+"    },"
        json_str = json_str+"    {"
        json_str = json_str+"      \"attribute\": \"Gender\","
        json_str = json_str+"      \"value\": \""+self.cbGender.currentText()+"\""
        json_str = json_str+"    },"
        json_str = json_str+"    {"
        json_str = json_str+"      \"attribute\": \"Age\","
        json_str = json_str+"      \"value\": \""+str(self.sbAge.value())+"\""
        json_str = json_str+"    },"
        json_str = json_str+"    {"
        json_str = json_str+"      \"attribute\": \"CountryCode\","
        json_str = json_str+"      \"value\": \""+self.cbCountryCode.currentText()+"\""
        json_str = json_str+"    },"
        json_str = json_str+"    {"
        json_str = json_str+"      \"attribute\": \"pose\","
        json_str = json_str+"      \"value\": \"aeroplane\""
        json_str = json_str+"    }"       
        json_str = json_str+"  ],"
        fln, real_extension = os.path.splitext(self.lFilename.text())        
        if(real_extension.lower() == ".zip" ):
            json_str = json_str+" \"content_file\": \""+cadena+"\","
            json_str = json_str+" \"extension\": \""+file_extension+"\","
            json_str = json_str+" \"zipped\": \"true\""
        else:
            json_str = json_str+" \"content_file\": \""+cadena+"\","
            json_str = json_str+" \"extension\": \""+file_extension+"\","
            json_str = json_str+" \"zipped\": \"false\""
        json_str = json_str+"}"


        if len(self.JWTToken.text())<20:
            QMessageBox.about(self, "Error", "No token loaded. Use the 'Load token' option in the menu to load a valid token.")
            return

        self.lStatusValue.setText("Executing query")
        QCoreApplication.processEvents()

        ses, SesToken = BP.initSession( self.JWTToken.text() )
        TRID = BP.Q0_FB_3DHR( SesToken, json_str )

        if( TRID.find('error')== -1 ):
            resp=BP.getDataCode( SesToken, TRID )
            datar= json.loads(resp)
            try:
                code = (datar['DataCode'])
                self.lModelID.setText(code)
                self.lStatusValue.setText("Query Executed ("+code+")")
                QMessageBox.about(self, "Message", "Model "+code+" was created and added to your collection.")
                self.setMode(1)
                QCoreApplication.processEvents()    
            except:
                print("Error on retrieval of data code")
                self.setMode( 0 )
        else:
            QMessageBox.about(self, "Error", "Error during query execution.")
            self.setMode( 0 )

        
        

    def buttonRetrieveAvatar(self):

        ses, token = BP.initSession( self.JWTToken.text() )
        code = self.lModelID.text()
        self.lUrl.setText("performing QA_3D for model "+code)
        QCoreApplication.processEvents()
        TRID_3D = BP.QA_3D( token, code)
        self.lUrl.setText("retrieving PATH to model")
        QCoreApplication.processEvents()
        path = BP.getModelPath( token, code )
        if( path.find('error')> -1 ):
            self.lUrl.setText("An error ocurred. Try to launch it again.")
        else:
            self.lUrl.setText(path)
            self.setMode(10)                      
            
        
        
    def buttonRetrieveMetrics(self):
        ses, token = BP.initSession( self.JWTToken.text() )
        self.lstatusRetMet.setEnabled(True)
        self.lstatusRetMet.show()
        self.lstatusRetMet.setText("Building and runing query")
        QCoreApplication.processEvents()

        inputjson = self.BuildJSONtextQAM( )
   
        TRID = BP.QA_metrics( token, inputjson )
        self.lstatusRetMet.setText("Retrieving metrics from response")

        self.lvMetricsRetrieved.clear()

        if( TRID.find('error')== -1 ):
            resp=BP.getTransaction( token, TRID )
            datar= resp.json()
            self.lvMetricsRetrieved.clear()
            for K in (datar['eventsEmitted'][0])['measurements']:
                cadena = K['metricID'].split("#")[0]+" = "+K['value'][0]
                self.lvMetricsRetrieved.addItem(cadena)
            self.lstatusRetMet.setText("")
            self.lstatusRetMet.hide()
            self.butCopyMetrics.show()
            self.listWidget_2.clear()
            for i in range(self.cbMetricRet.count()):
                self.cbMetricRet.model().item(i).setEnabled(True)            

        else:
            self.lvMetricsRetrieved.clear()
            self.lstatusRetMet.setText("An error ocurred. Try to launch it again.")
          

    def loadData(self):
        self.cbMetricRet.addItems(metricsAll)
        self.JWTToken.setText("")
        self.JWTToken.hide()
        self.lStatusValue.hide()
        self.lStatus.hide()
        self.lModelID.setText("")
        self.lModelID.hide()
                     
            

            
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = First()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


    
