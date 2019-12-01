import sys
import requests
import os
import zipfile
import wmi
import subprocess
import platform
import json
import time

from PyQt5 import QtWidgets, QtCore, QtWidgets, QtGui
#from scanGUI import Ui_Form    #MyFirstUI 是你的.py檔案名字

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(495, 560)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 10, 455, 71))
        self.groupBox_2.setObjectName("groupBox_2")
        self.comboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox.setGeometry(QtCore.QRect(80, 30, 261, 24))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(20, 30, 70, 18))
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(20, 100, 455, 191))
        self.groupBox.setObjectName("groupBox")
        self.toolButton = QtWidgets.QToolButton(self.groupBox)
        self.toolButton.setGeometry(QtCore.QRect(320, 150, 29, 24))
        self.toolButton.setObjectName("toolButton")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setGeometry(QtCore.QRect(20, 30, 300, 22))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_2.setGeometry(QtCore.QRect(20, 60, 430, 22))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_3.setGeometry(QtCore.QRect(20, 90, 300, 22))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_4.setGeometry(QtCore.QRect(20, 120, 300, 22))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_5 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_5.setGeometry(QtCore.QRect(20, 150, 300, 22))
        self.checkBox_5.setObjectName("checkBox_5")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(90, 150, 221, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 310, 455, 171))
        self.groupBox_3.setObjectName("groupBox_3")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton.setGeometry(QtCore.QRect(20, 40, 141, 22))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_2.setGeometry(QtCore.QRect(20, 80, 161, 22))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.groupBox_3)
        self.radioButton_3.setGeometry(QtCore.QRect(20, 120, 161, 22))
        self.radioButton_3.setObjectName("radioButton_3")
        # self.plainTextEdit = QtWidgets.QPlainTextEdit(self.groupBox_3)
        # self.plainTextEdit.setGeometry(QtCore.QRect(190, 40, 151, 107))
        # self.plainTextEdit.setObjectName("plainTextEdit")
       
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 500, 115, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(360, 500, 115, 41))
        self.pushButton.setObjectName("pushButton")
        self.progressBar = QtWidgets.QProgressBar(Form)
        self.progressBar.setGeometry(QtCore.QRect(20, 505, 360, 30))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)
        self.retranslateUi(Form)


        # self.radioButton.clicked['bool'].connect(self.plainTextEdit.update)
        # self.radioButton_2.clicked['bool'].connect(self.plainTextEdit.update)
        # self.radioButton_3.clicked['bool'].connect(self.plainTextEdit.update)
        # self.pushButton.clicked.connect(self.progressBar.show)
        #self.checkBox_5.clicked.connect(self.chooseDir)
        self.toolButton.clicked.connect(self.Change_the_Checkbox_Function)
        self.toolButton.clicked.connect(self.chooseDir)
        
        QtCore.QMetaObject.connectSlotsByName(Form)

    def Change_the_Checkbox_Function(self):
        if self.checkBox_5.isChecked(): 
            pass
        else:
            self.checkBox_5.setChecked(True)

    def chooseDir(self):
        #startingDir = cmds.workspace(q=True, rootDirectory=True)
        destDir = QtWidgets.QFileDialog.getExistingDirectory(None, 
                                                         'Select Directory', 
                                                         os.path.join(os.environ['systemdrive'],""), 
                                                         QtWidgets.QFileDialog.ShowDirsOnly)
        self.lineEdit.setText(str(destDir))


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Security Rabbit"))
        Form.setWindowIcon(QtGui.QIcon('logo.png'))
        self.groupBox_2.setTitle(_translate("Form", "Basic Information"))
        self.comboBox.setItemText(0, _translate("Form", "SecurityRabbit Server1"))
        self.comboBox.setItemText(1, _translate("Form", "SecurityRabbit Server2"))
        self.label.setText(_translate("Form", "Server"))
        self.groupBox.setTitle(_translate("Form", "Directories"))
        self.toolButton.setText(_translate("Form", "..."))
        
        self.checkBox.setText(_translate("Form", 'homepath ('+os.environ['HOMEDRIVE']+os.environ['HOMEPATH']+')'))
        
        if(platform.architecture()[0] == "32bit"):
            self.checkBox_2.setText(_translate("Form", 'programfiles ('+os.environ["ProgramFiles"]+')'))
        elif(platform.architecture()[0] == "64bit"):
            self.checkBox_2.setText(_translate("Form", 'programfiles ('+os.environ["ProgramFiles"]+', '+os.environ["ProgramFiles(x86)"]+')'))

        self.checkBox_3.setText(_translate("Form", 'windir ('+os.environ['WINDIR']+')'))
        self.checkBox_4.setText(_translate("Form", 'systemdrive ('+os.environ['systemdrive']+')'))
        self.checkBox_5.setText(_translate("Form", "other"))
        
        self.groupBox_3.setTitle(_translate("Form", "Scanning Mode"))
        self.radioButton.setText(_translate("Form", "Normal Option"))
        self.radioButton.setChecked(True)
        self.radioButton_2.setText(_translate("Form", "Advanced Option"))
        self.radioButton_3.setText(_translate("Form", "Customize Option"))
        self.pushButton.setText(_translate("Form", "Scan"))
        self.pushButton_2.setText(_translate("Form", "Finished"))


class AppWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.show()

        # 之後要改成可辨認使用者的id
        self.userid = "1"
        p = subprocess.Popen('wmic csproduct get UUID',stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        scan_result = p.communicate()[0] 
        self.deviceuuid = str(scan_result).split('\\r\\r\\n')[1].strip()
        #self.deviceuuid = "38444335-3132-3344-4754-B4B686D36C7E"
        

        self.filename = "exeinfo_"+str(self.userid)+"_"+self.deviceuuid+".json"
        self.serverIps = ["140.119.19.21","127.0.0.1"]
        self.server = "140.119.19.21"

        self.client = None
        self.uploadURL = 'http://'+self.server+':8000/uploadjson/'+str(self.userid)+'/'+self.deviceuuid
        self.csrftoken = ""
                
        self.scanType = "0"
        self.args=[]

        self.ui.pushButton.clicked.connect(self.run)


    def run(self):
        self.ui.pushButton.setEnabled(False)
        
        self.server = self.serverIps[self.ui.comboBox.currentIndex()]
        self.uploadURL = 'http://'+self.server+':8000/uploadjson/'+str(self.userid)+'/'+self.deviceuuid
        self.startSession()
        self.downloadfile('srcore')
        self.progress()
        self.startScan()        
        

    def progress(self): # ,args
        try:
            self.ui.progressBar.show()
            self.ui.progressBar.setMinimum(0)
            self.ui.progressBar.setMaximum(0)
            # count_total = 0
            # for i in range(len(args)):
            #     if i != len(args):
            #         count_total += sum([len(files) for r, d, files in os.walk(args[i])])
            # print(count_total)
            self.timer = QtCore.QBasicTimer()
            self.timer.start(100, self)
            count = count + 1
            self.ui.progressBar.setValue(count)
            # count = 0
            # while count < 100:
            #     count += int(100/count_total/2)*0.00001
            #     #time.sleep(2)
                #self.ui.progressBar.setValue(count)
                #print(count)
        except:
            pass

    def finish(self):
        os.rename('data.json', self.filename)
        self.uploadfile(self.filename)
        self.closeSession()
        self.removeFiles()
        self.ui.pushButton.hide()
        self.ui.progressBar.hide()
        self.ui.pushButton_2.clicked.connect(QtWidgets.qApp.quit)

    def removeFiles(self):
        removeList = ["srcore.zip","__main__.exe","sigcheck.exe","userdb_filter.txt", self.filename, "error.json"] #,"error.json","exeInfo.xlsx"]
        for removefile in removeList:
            try:
                os.remove(removefile)
            except:
                print("{} already removed".format(removefile))

    def startScan(self):
        
        # self.process = QtCore.QProcess(self)
        zipfile_name = 'srcore.zip'
        z_file = zipfile.ZipFile(zipfile_name)
        zipfile.ZipFile.extract(z_file, '__main__.exe')
        zipfile.ZipFile.extract(z_file, 'sigcheck.exe')
        zipfile.ZipFile.extract(z_file, 'userdb_filter.txt')

        if(self.ui.checkBox.isChecked()):
            self.args.append(os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],""))
        if(self.ui.checkBox_2.isChecked()):
            if(platform.architecture()[0] == "32bit"):
                self.args.append(os.path.join(os.environ["ProgramFiles"],""))
            elif(platform.architecture()[0] == "64bit"):
                self.args.append(os.path.join(os.environ["ProgramFiles"],""))
                self.args.append(os.path.join(os.environ["ProgramFiles(x86)"],""))
        if(self.ui.checkBox_3.isChecked()):
            self.args.append(os.path.join(os.environ['WINDIR'],""))
        if(self.ui.checkBox_4.isChecked()):
            self.args.append(os.path.join(os.environ['systemdrive'],""))
        if(self.ui.checkBox_5.isChecked()):
            self.args.append(os.path.join(self.ui.lineEdit.text(),""))

        if(self.ui.radioButton.isChecked()):
            self.scanType="0"
        elif(self.ui.radioButton_2.isChecked()):
            self.scanType="1"
        elif(self.ui.radioButton_3.isChecked()):
            self.scanType="2" 

        self.args.append("--scan_type")
        self.args.append(self.scanType)

        self.process = QtCore.QProcess(self)

        self.process.start(u'__main__.exe', self.args)    

        self.process.finished.connect(self.finish)

        
    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            self.scanType = radioButton.scanType
    
    def startSession(self):
        self.client = requests.session()
        self.client.get(self.uploadURL)
        self.csrftoken=self.client.cookies['csrftoken']

    
    def uploadfile(self, to_upload):
        with open(to_upload,'rb') as xmlfile:
            self.client.post(
                self.uploadURL,
                files={'docfile':xmlfile},
                data={'csrfmiddlewaretoken':self.csrftoken}
                )

    def downloadfile(self, download_filename):
        r = self.client.get('http://'+self.server+':8000/downloadzip/'+ download_filename)
        pyfile = open(download_filename+".zip",'wb+')
        pyfile.write(r.content)
        pyfile.close()
    
    def closeSession(self):
        self.client.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    w = AppWindow()
    w.show()
    app.exec_()
