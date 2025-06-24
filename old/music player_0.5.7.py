from PyQt5 import QtCore, QtGui
import sys
from pykeyboard import PyKeyboard
import time as t
from pykeyboard import PyKeyboard

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(630, 250)
        self.setWindowIcon(QtGui.QIcon('main.png'))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(647, 0))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setDragEnabled(True) #设置能接受拖放
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton_4 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_4.setMinimumSize(QtCore.QSize(112, 34))
        self.pushButton_4.setMaximumSize(QtCore.QSize(112, 16777215))
        self.pushButton_4.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_4.setAutoFillBackground(False)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setDragEnabled(True) #设置能接受拖放
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.pushButton_5 = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setMinimumSize(QtCore.QSize(112, 34))
        self.pushButton_5.setMaximumSize(QtCore.QSize(112, 16777215))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.doubleSpinBox.setRange(0, 10); #范围
        self.doubleSpinBox.setSingleStep(0.1);# 步长
        #self.doubleSpinBox.setWrapping(true);# 开启循环
        self.horizontalLayout_3.addWidget(self.doubleSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_4.addWidget(self.label_4)
        self.lineEdit_3 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_3.setDragEnabled(True) #设置能接受拖放
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.horizontalLayout_4.addWidget(self.lineEdit_3)
        self.pushButton_6 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_6.setMinimumSize(QtCore.QSize(112, 34))
        self.pushButton_6.setMaximumSize(QtCore.QSize(112, 16777215))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.horizontalLayout_4.addWidget(self.pushButton_6)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.pushButton_3 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.horizontalLayout_5.addWidget(self.pushButton_3)
        self.pushButton_2 = QtGui.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.horizontalLayout_5.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButton_4, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.view)
        QtCore.QObject.connect(self.pushButton_5, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.view1)
        QtCore.QObject.connect(self.doubleSpinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), MainWindow.numberchange)
        QtCore.QObject.connect(self.pushButton_6, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.view2)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.mainplay)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.transfer)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL(_fromUtf8("editingFinished()")), MainWindow.pathconfer)
        QtCore.QObject.connect(self.lineEdit_2, QtCore.SIGNAL(_fromUtf8("editingFinished()")), MainWindow.pathconfer_2)
        QtCore.QObject.connect(self.lineEdit_3, QtCore.SIGNAL(_fromUtf8("editingFinished()")), MainWindow.pathconfer_3)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.lineEdit, self.pushButton_4)
        MainWindow.setTabOrder(self.pushButton_4, self.lineEdit_2)
        MainWindow.setTabOrder(self.lineEdit_2, self.pushButton_5)
        MainWindow.setTabOrder(self.pushButton_5, self.doubleSpinBox)
        MainWindow.setTabOrder(self.doubleSpinBox, self.lineEdit_3)
        MainWindow.setTabOrder(self.lineEdit_3, self.pushButton_6)
        MainWindow.setTabOrder(self.pushButton_6, self.pushButton_3)
        MainWindow.setTabOrder(self.pushButton_3, self.pushButton_2)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "音乐播放&转换器", None))
        self.label.setText(_translate("MainWindow", "音乐路径:", None))
        #self.lineEdit.setText(_translate("MainWindow", "C:\\music player\\m.txt", None))
        self.pushButton_4.setText(_translate("MainWindow", "浏览", None))
        self.label_2.setText(_translate("MainWindow", "规则路径", None))
        #self.lineEdit_2.setText(_translate("MainWindow", "C:\\music player\\r.txt", None))
        self.pushButton_5.setText(_translate("MainWindow", "浏览", None))
        self.label_3.setText(_translate("MainWindow", "比率 (基准时间) :", None))
        self.label_4.setText(_translate("MainWindow", "输出路径", None))
        #self.lineEdit_3.setText(_translate("MainWindow", "C:\\music player\\a.bat", None))
        self.pushButton_6.setText(_translate("MainWindow", "浏览", None))
        self.pushButton_3.setText(_translate("MainWindow", "播放+转换", None))
        self.pushButton_2.setText(_translate("MainWindow", "转换", None))



class TestWnd(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(TestWnd, self).__init__(parent)
        wnd = self.setupUi(self)

    def view (self):
        view = QtGui.QFileDialog.getOpenFileName(self,"getOpenFileName","./","Text Files (*.txt);;All Files (*)")
        self.lineEdit.setText(_translate("MainWindow", view, None))
        load_music(view)
        self.statusBar.showMessage('音乐加载成功',2000)
        #print (u'文本框此刻输入的内容是：%s'%view)

    def view1 (self):
        view = QtGui.QFileDialog.getOpenFileName(self,"getOpenFileName","./","Text Files (*.txt);;All Files (*)")
        self.lineEdit_2.setText(_translate("MainWindow", view, None))
        load_rule(view)
        self.statusBar.showMessage('规则加载成功',2000)
        #print (u'文本框此刻输入的内容是：%s'%view)

    def view2 (self):
        global view2
        view2 = QtGui.QFileDialog.getSaveFileName(self, "getSaveFileName","./","Text Files (*.dat);;All Files (*)")
        self.lineEdit_3.setText(_translate("MainWindow", view2, None))
        self.statusBar.showMessage('输出路径明确',2000)
        #print (u'文本框此刻输入的内容是：%s'%view)

    def pathconfer(self):
        b = self.lineEdit.text()
        load_music(b)
        self.statusBar.showMessage('音乐加载成功',2000)
        #print (u'文本框此刻输入的内容是：%s'%b)

    def pathconfer_2(self):
        b = self.lineEdit_2.text()
        load_rule(b)
        self.statusBar.showMessage('规则加载成功',2000)
        #print (u'文本框此刻输入的内容是：%s'%b)

    def pathconfer_3(self):
        global view2
        view2 = self.lineEdit_3.text()
        self.statusBar.showMessage('输出路径明确',2000)
        #print (u'文本框此刻输入的内容是：%s'%view2)

    def numberchange (self):
        global standardtime
        standardtime = self.doubleSpinBox.value()
        print(standardtime)

    def mainplay (self):
        self.statusBar.showMessage('开始',3000)
        converse(m,r)
        play2(m2,gap)
        self.statusBar.showMessage('结束',3000)

    def transfer (self):
        self.statusBar.showMessage('开始',3000)
        global m,r
        converse(m,r)
        self.statusBar.showMessage('结束',3000)



def fileswrite(asd):
    with open(view2,'a') as f2:    #设置文件对象
        f2.write(asd + '\r')                 #将字符串写入文件中

def converse(m,r):
    global m1, m2, gap
    m = m.split(",")
    print (m)
    print (r)
    for i2 in range (len(m)):
        m1 = m[i2]
        if "|" not in m1:
            for i in range (0 , len(r)-1):
                m1 = m1.replace(r[i][0],r[i][-1])
            m2.append(m1)
            gap.append(standardtime)
            fileswrite(str(m1)+ "|" + str(standardtime))
            print(str(m1)+ "|" + str(standardtime))
            
        else:
            position = m1.index("|")
            m15 = m1[0:position]
            for i in range (0 , len(r)-1):
                m15 = m15.replace(r[i][0],r[i][-1])
            m20 = standardtime * eval(m1[position+1:])
            m2.append(m15)
            gap.append(m20)
            fileswrite(m15 + "|" + str(m20))
            print (m15 + "|" + str(m20))
    return m2,gap

def play(m,gap):
    k=PyKeyboard()
    if len(m) == len(gap):
        pass
    else:
        print("music and stopping time length aren't equal")
    for i1 in range (0,len(m)-1):
        k.tap_key(m[i1]) #点击
        t.sleep(gap[i1]) #间隔

def play2(Key,gap):
    k=PyKeyboard()
    for i in range (len(Key)):
        k.press_key(Key[i]) #按key键
        t.sleep(gap[i])
        k.release_key(Key[i]) #松开key键

def load_rule(p1):
    global r
    f1 = open(p1,"r")
    r = eval(f1.read())
    print("rule load success")
    return r

def load_music(p):
    global m
    f = open(p,"r")
    m = f.read()
    print("music load success")
    return m



if __name__ == '__main__':
    view2 = ''
    m = ""
    m1 = []
    m2 = []
    gap = []
    p = ""
    r = []
    standardtime = 0.5
    app = QtGui.QApplication(sys.argv)
    mywindow = TestWnd()
    mywindow.show()
    sys.exit(app.exec_())