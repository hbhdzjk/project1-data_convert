## ==> GUI FILE
from main import *
import sys,os
import ctypes
import scipy.io as scio
from ui_function import *
from PyQt5 import QtCore, QtGui, QtWidgets,Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from UI_window.Ui_Main_window import *
from UI_window.Ui_Child_Tabwindow import *
from zjk_work.nanonispy_zjk import read

## ==> GLOBALS
GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True
GLOBAL_MENU_BAR_LAST = 'a'
GLOBAL_MENUWIDTH_LAST ={'value': -1,'status':True}

## ==> COUT INITIAL MENU
count = 1

class UIFunctions(MainWindow):

    ## ==> GLOBALS
    GLOBAL_STATE = 0                    # 0=normal, 1=max
    GLOBAL_TITLE_BAR = True
    GLOBAL_MENU_BAR_LAST = 'b'
    GLOBAL_MENUWIDTH_LAST = {'value': -1,'status':True}

    def returnStatus():
        return GLOBAL_STATE
    def setStatus(status):
        global GLOBAL_STATE
        GLOBAL_STATE = status
    def setLastMenu(btn):
        global GLOBAL_MENU_BAR_LAST
        GLOBAL_MENU_BAR_LAST = btn
    def setLastWidth(self):
        global GLOBAL_MENUWIDTH_LAST
        if self.ui.frame_menulist.width()!=0:
            GLOBAL_MENUWIDTH_LAST['value'] = self.ui.frame_menulist.width()
        else:
            pass
            
    # 最大化或者normal
    def restore_or_maximize_window(self): 
        global GLOBAL_STATE
        status = GLOBAL_STATE
        # If window is normal
        if status == 0:
            GLOBAL_STATE = 1
            self.showMaximized()
            # Change Icon
            self.ui.restore_window_button.setIcon(QtGui.QIcon(u":/icon24/icons/24x24/cil-window-maximize.png"))
            self.ui.frame_size_grip.hide()
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            # Change Icon
            self.ui.restore_window_button.setIcon(QtGui.QIcon(u":/icon24/icons/24x24/cil-window-restore.png"))
            self.ui.frame_size_grip.show()
        
            
    def selectMenu(getStyle):
        select = getStyle + ("QPushButton { border-left: 3px solid rgb(144, 149, 160); }")
        return select

    ## ==> DESELECT
    def deselectMenu(getStyle):
        deselect = getStyle.replace("QPushButton { border-left: 3px solid rgb(144, 149, 160); }", "")
        return deselect    
    
    ## ==> START SELECTION
    def selectStandardMenu(self, widget):
        for w in self.ui.frame_menubar.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(UIFunctions.selectMenu(w.styleSheet()))

    ## ==> RESET SELECTION
    def resetStyle(self, widget):
        for w in self.ui.frame_menubar.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(w.styleSheet()))   
    
    # 点击frame_menubar上的按钮
    def toggleMenu(self, maxWidth, btn):
        global GLOBAL_MENUWIDTH_LAST, GLOBAL_MENU_BAR_LAST
        standard = 200
        # GET WIDTH
        width = self.ui.frame_menulist.width()
        # print('Width = ',width,' Last name = ',GLOBAL_MENU_BAR_LAST,'Last Width = ',GLOBAL_MENUWIDTH_LAST['status'])
        if GLOBAL_MENU_BAR_LAST==btn:
            # SET MAX WIDTH
            if GLOBAL_MENUWIDTH_LAST['status']:
                width_start = self.ui.frame_menulist.width()
                width_end = 0

                GLOBAL_MENUWIDTH_LAST['status']=False
                # # ANIMATION
                # self.animation = QtCore.QPropertyAnimation(self.ui.frame_menulist, b"size")
                # self.animation.setDuration(300)
                # self.animation.setStartValue(QtCore.QSize(width_start,self.ui.frame_menulist.height()))
                # self.animation.setEndValue(QtCore.QSize(width_end,self.ui.frame_menulist.height()))
                # self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
                # self.animation.start()
                self.ui.frame_menulist.hide()
            else:
                width_start = 0
                width_end = GLOBAL_MENUWIDTH_LAST['value']
                GLOBAL_MENUWIDTH_LAST['status']=True
                self.ui.frame_menulist.show()
                # # ANIMATION
                # self.animation = QtCore.QPropertyAnimation(self.ui.frame_menulist, b"size")
                # self.animation.setDuration(300)
                # self.animation.setStartValue(QtCore.QSize(width_start,self.ui.frame_menulist.height()))
                # self.animation.setEndValue(QtCore.QSize(width_end,self.ui.frame_menulist.height()))
                # self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
                # self.animation.start()
        else:
            width_start = self.ui.frame_menulist.width()
            width_end = GLOBAL_MENUWIDTH_LAST['value']
            self.ui.frame_menulist.show()
            # self.ui.frame_menulist.resize(width_end,self.ui.frame_menulist.height())
            
            # # ANIMATION
            # self.animation = QtCore.QPropertyAnimation(self.ui.frame_menulist, b"size")
            # self.animation.setDuration(300)
            # self.animation.setStartValue(QtCore.QSize(width_start,self.ui.frame_menulist.height()))
            # self.animation.setEndValue(QtCore.QSize(width_end,self.ui.frame_menulist.height()))
            # self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            # self.animation.start()

    def uiDefinitions(self):
        self.resize(1500,800)
        self.setMouseTracking(True)
        ## # Remove window tittle bar 
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint) 
        ## # Set main background to transparent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ## # 添加图标和任务栏图标，需 import ctypes
        self.setWindowIcon(QIcon(":/find/icons/find/五个椭圆_five-ellipses.svg"))
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        ## # 设置标题
        self.setWindowTitle('MyGui')
        ## # Shadow effect style
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.centralwidget.setGraphicsEffect(self.shadow)
        # Window Size grip to resize window
        QSizeGrip(self.ui.size_grip)
        #Minimize window
        self.ui.minimize_window_button.clicked.connect(lambda: self.showMinimized())
        #Close window
        self.ui.close_window_button.clicked.connect(lambda: self.close())
        #Restore/Maximize window
        self.ui.restore_window_button.clicked.connect(lambda: self._restore_or_maximize_window())
        #hide
        # self.ui.frame_tab.hide()
        self.ui.splitter.handle(1).setAttribute(QtCore.Qt.WA_Hover,True)
        self.ui.splitter.handle(0).setAttribute(QtCore.Qt.WA_Hover,True)