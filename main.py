#-*- coding: utf-8 -*
'''
        ´´´´´´´´██´´´´´´´
        ´´´´´´´████´´´´´´
        ´´´´´████████´´´´
        ''`´███▒▒▒▒███´´´´´
        ´´´███▒●▒▒●▒██´´´
        ´´´███▒▒▒▒▒▒██´´´´´
        ´´´███▒▒▒▒██´                      项目:        dataform convert 
        ´´██████▒▒███´´´´´                 语言：       python+pyqt5+qt designer
        ´██████▒▒▒▒███´´                   框架： 
        ██████▒▒▒▒▒▒███´´´´                构建工具：    vscode
        ´´▓▓▓▓▓▓▓▓▓▓▓▓▓▒´´                 版本控制：    目前还没有。。
        ´´▒▒▒▒▓▓▓▓▓▓▓▓▓▒´´´´´              
        '.▒▒▒´´▓▓▓▓▓▓▓▓▒´´´´´              
        '.▒▒´´´´▓▓▓▓▓▓▓▒                   编辑器：  python 3.9.7 & 3.9.13 
        ..▒▒.´´´´▓▓▓▓▓▓▓▒                           Name: PyQt5     Version: 5.15.4
        ´▒▒▒▒▒▒▒▒▒▒▒▒                               Name: pyqtgraph Version: 0.13.2 
        ´´´´´´´´´███████´´´´´                       Name: nanonispy Version: 1.1.0
        ´´´´´´´´████████´´´´´´´            author: zjk
        ´´´´´´´█████████´´´´´´
        ´´´´´´██████████´´´´             大部分人都在关注你飞的高不高，却没人在乎你飞的累不累，这就是现实！
        ´´´´´´██████████´´´                     我从不相信梦想，我，只，相，信，自，己！
        ´´´´´´´█████████´´
        ´´´´´´´█████████´´´
        ´´´´´´´´████████´´´´´
        ________▒▒▒▒▒
        _________▒▒▒▒
        _________▒▒▒▒
        ________▒▒_▒▒
        _______▒▒__▒▒
————————————————
'''
import sys,os
os.chdir(sys.path[0])  # 把目录改到现在这里
sys.path.append("./UI_window/")
import ctypes
import time
import tempfile
import scipy.io as scio
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QSettings,QMimeData,QVariant,Qt,QFile,QIODevice)
from PyQt5.QtGui import (QDragEnterEvent,QDropEvent,QDrag)
from PyQt5.QtWidgets import *
# from PyQt5.QtWebEngineWidgets import QWebEngineView  #用来显示markdown的
from ui_function import *
# from sxm_maker import *
from UI_window.Ui_Main_window import *
from UI_window.Ui_Child_Tabwindow import *
from UI_window.Ui_Child_Tab_start import *

# from zjk_work.nanonispy_zjk import read

global temp_dir
temp_dir=[]

class MainWindow(QMainWindow):
    global temp_dir
    Signal_filepath=QtCore.pyqtSignal(str)
    Signal_datarefreash=QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_UI()
        self.init_settings()
        self.current_file={'folder':'','path':''}
        self.project={}                             # Tab 计数
        
        self.path_folder=''                         # filetree 的dirname
        # global temp_dir                             # 用全局变量存临时文件夹地址
        # temp_dir = tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None)
        # self.temp_dir=temp_dir

        self._isPressed = False                     # 鼠标是否按下
        self._press_button = None                   # 鼠标按下的按键
        self._last_geometry = self.geometry()       # 初始化一下，要不然在双击前没有这个变量会报错（在self._move中最大化时移动）
        self._area = None                           # 判定鼠标点击位置相对于MainWindow的位置
        self._move_count = 0                        # 窗口移动反应灵敏度，反比
        self.MOVE_SENSITIVITY = 3                   # 窗口移动反应灵敏度，反比
        self.MARGIN = 10                            # 边缘宽度(拖动改变窗口大小)
        self.datatree_projectList = {}              # datatree更新使用，存储所有数据
        self.rootList=[]                            # datatree更新使用，临时变量，使用完后置零

        self.statusbar_style='''                    
        background-color: rgb(0, 122, 204);
        '''

            
        
    def  init_UI(self):
        
        UIFunctions.uiDefinitions(self)
        # self.ui.centralwidget.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        self.ui.centralwidget.setMouseTracking(True)
        self.ui.main_body.setMouseTracking(True)
        self.ui.main_interface.setMouseTracking(True)
        # self.ui.frame_menubar.setMouseTracking(True)
        # self.ui.frame_menubar.setMouseTracking(True)
        # self.ui.frame_menubar.setMouseTracking(True)
        # self.ui.header_frame.setMouseTracking(True)
        # self.ui.foot_left.setMouseTracking(True)
        # self.ui.footer.setMouseTracking(True)
        # self.ui.foot_center.setMouseTracking(True)
        # self.ui.status_label.setMouseTracking(True)
        # self.ui.header1.setMouseTracking(True)
        # self.ui.footer.setMouseTracking(True)
        # self.ui.header_left.setMouseTracking(True)
        #######################################################################
        self.ui.splitter.setStretchFactor(0, 1)
        self.ui.splitter.setStretchFactor(1, 6)
        
        self._last_geometry = self.geometry()                                          # 初始化一下，要不然在双击前没有这个变量会报错（在self._move中最大化时移动） 

        self.ui.btn_file.clicked.connect(lambda: self.Menu_Button())
        self.ui.btn_datadict.clicked.connect(lambda: self.Menu_Button())
        self.ui.btn_file_view.clicked.connect(lambda: self.Menu_Button())
        self.ui.btn_datamaker.clicked.connect(lambda: self.Menu_Button())
        self.ui.btn_settings.clicked.connect(lambda: self.Menu_Button())
        self.ui.btn_fileopen.clicked.connect(lambda: self.Open_Folder())
        self.ui.btn_file_filter.clicked.connect(lambda: self.Open_Folder2())
        # self.ui.btn_sxm_maker.clicked.connect(lambda: self.SxmMaker())
        self.ui.tabWidget.tabCloseRequested.connect(self.closeTab)
        
        self.resize(800,1000)
        self.ui.page_datamaker.hide()
        self.ui.page_file.hide()
        self.ui.btn_file.hide()
        self.ui.btn_datamaker.hide()
        self.ui.btn_settings.hide()
        self.ui.frame_tab.hide()

        self.datadict_tree=MyDataDictTreeWidget()
        self.ui.verticalLayout_8.addWidget(self.datadict_tree)
        self.datadict_tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.datadict_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)                    # 右键菜单
        self.datadict_tree.customContextMenuRequested.connect(self.data_dict_fun)               # 绑定右键菜单事件   

        self.datatree=self.ui.treeWidget_dict
        # self.datatree=MyDataDictTreeWidget(self.ui.treeWidget_dict)
        self.datatree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  #自适应宽度
        self.datatree.hide()

        self.ui.label_file_dir.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.ui.label_file_dir.setWordWrap(True)

        self.file_model=QFileSystemModel()
        self.file_model.setNameFilterDisables(False)                                            #过滤掉的灰色文件不显示
        self.file_tree_view=self.ui.file_treeView
        self.file_tree_view.setModel(self.file_model)
        self.file_tree_view.sortByColumn(2,QtCore.Qt.AscendingOrder)                            #按照类型排序
        self.file_tree_view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)                   #右键菜单
        self.file_tree_view.setDragDropMode(QAbstractItemView.DragOnly)
        self.file_tree_view.customContextMenuRequested.connect(self.rightclicked_tree_view)  
        self.file_tree_view.setColumnHidden(1,True)
        self.file_tree_view.setColumnHidden(2,True)
        self.file_tree_view.setColumnHidden(3,True)
        self.file_tree_view.doubleClicked.connect(self.On_doubleClicked_file_tree_model)
        self.ui.lineEdit_file_filter.textChanged.connect(self.refresh_file_filter)

        # 本来是想写个markdown集成进去，但是现在卡爆了，算了算了
        # 想用的话 打开前边
        # from PyQt5.QtWebEngineWidgets import QWebEngineView  #用来显示markdown的
        # self.MarkDownViewer=MarkDownViewer()
        # self.ui.tabWidget.addTab(self.MarkDownViewer,'Markdown')
        
        
        #Tab 开始页
        self.start_tab=Tab_start()
        self.ui.tabWidget.addTab(self.start_tab,'Start')
        self.start_tab.Signal_btn.connect(self.Slot_Tab_start_filepath)
        # Function to Move window on mouse drag event on the tittle bar
        # def moveWindow(e):
        #     if self._isPressed:
        #         # Detect if the window is  normal size
        #         if self.isMaximized() == False: #Not maximized
        #             # Move window only when window is normal size  
        #             #if left mouse button is clicked (Only accept left mouse button clicks)
        #             if e.buttons() == QtCore.Qt.LeftButton:  
        #                 #Move window 
        #                 self.move(self.pos() + e.globalPos() - self.clickPosition)
        #                 self.clickPosition = e.globalPos()
        #                 e.accept()
        #         else:
        #             self.showNormal()
        # self.ui.header_frame.mouseMoveEvent = moveWindow

    def init_settings(self):
        self.settings = QSettings('.\\zjk_work\\Config\\config.ini', QSettings.IniFormat)
        self.settings.setIniCodec('UTF-8')                                                              # 设置ini文件编码为 UTF-8
        self.recentFiles=self.settings.value('FileList/recentFiles') or []                              # 读最近的文件列表，后边新开一个文件会更新此列表
        self.maxNumRecentFiles=5                                                                        # 最近的文件列表最大储存数目
        
        global temp_dir
        self.temp_dir=self.settings.value('Temp/temp_dir') or []                                        # 临时文件夹目录
        if (not self.temp_dir==[]) and os.path.isdir(self.temp_dir) and os.path.exists(self.temp_dir):  # 判断是否存在
            temp_dir=tempfile.TemporaryDirectory(dir=self.temp_dir)
        elif self.temp_dir==[]:
            self.temp_dir=tempfile.gettempdir()
            self.settings.setValue('Temp/temp_dir', self.temp_dir)
            temp_dir=tempfile.TemporaryDirectory(dir=self.temp_dir)

    def mousePressEvent(self, event):
        """重写继承的鼠标按住事件"""

        self._isPressed = True                              # 判断是否按下
        self._press_button = event.button()                 # 按下的鼠标按键
        self._area = self._compute_area(event.pos())        # 计算鼠标所在区域
        self._move_count = 0                                # 鼠标移动计数，用于降低灵敏度
        self._posLast = event.globalPos()                   # 当前坐标
        self.clickPosition=self._posLast
        return QMainWindow.mousePressEvent(self, event)     # 交由原事件函数处理
    def mouseReleaseEvent(self, event):
        """重写继承的鼠标释放事件"""

        self._isPressed = False                             # 重置按下状态
        self._press_button = None                           # 清空按下的鼠标按键
        self._area = None                                   # 清空鼠标区域
        self._move_count = 0                                # 清空移动计数
        self.setCursor(QtCore.Qt.ArrowCursor)               # 还原光标图标

        return QMainWindow.mouseReleaseEvent(self, event)
    def mouseMoveEvent(self, event):
        """重写继承的鼠标移动事件，实现窗口移动及拖动改变窗口大小"""

        area = self._compute_area(event.pos())              # 计算鼠标区域
        # 调整窗口大小及移动
        if self._isPressed and self._press_button == QtCore.Qt.LeftButton:
            if self._area == 22:
                self._move(event)                           # 调用移动窗口的函数
            elif not self.isMaximized():
                self._resize(event)                         # 调用调整窗口大小的函数

            # 更新鼠标全局坐标
            self._posLast = event.globalPos()
            return None
        if not self._isPressed and not self.isMaximized():
            # 调整鼠标图标，按下鼠标后锁定状态
            self._change_cursor_icon(area)

        return QMainWindow.mouseMoveEvent(self, event)
    def mouseDoubleClickEvent(self, event):
        """重写继承的鼠标双击事件"""

        self._last_geometry = self.geometry()
        self._restore_or_maximize_window()

        return QMainWindow.mouseDoubleClickEvent(self, event)
    def keyPressEvent(self, event):
        #这里event.key（）显示的是按键的编码
        # print("按下：" + str(event.key()))
        if (event.key() == QtCore.Qt.Key_O) and QApplication.keyboardModifiers() == QtCore.Qt.ControlModifier:
            self.Open_Folder2()
        return QMainWindow.keyPressEvent(self, event)     # 交由原事件函数处理
    def _compute_area(self, pos):
        """计算鼠标在窗口中的区域
        Args:
            pos: 鼠标相对于窗口的位置
            margin: 以此值为外边框宽度，划为九宫格区域
        """
        margin = self.MARGIN

        # 定位列坐标
        if pos.x() < margin:
            line = 1
        elif pos.x() > self.width() - margin:
            line = 3
        else:
            line = 2
        # 定位行坐标并结合列坐标
        if pos.y() < margin:
            return 10 + line
        elif pos.y() > self.height() - margin:
            return 30 + line
        else:
            return 20 + line
    def _pos_percent(self, pos):
        """返回鼠标相对窗口的纵横百分比"""

        if pos.x() <= 0:
            x = 0
        else:
            x = round(pos.x() / self.width(), 3)

        if pos.y() <= 0:
            y = 0
        else:
            y = round(pos.y() / self.height(), 3)

        return x, y
    def _move(self, event):
        """实现窗口移动"""

        self._move_count += 1

        # 判断移动次数，减少灵敏度
        if self._move_count < self.MOVE_SENSITIVITY:
            return None

        # 最大化时需恢复并移动到鼠标位置
        if self.isMaximized():
            relative = self._pos_percent(event.pos())
            self._restore_or_maximize_window()
            gpos = event.globalPos()
            width = self._last_geometry.width()
            height = self._last_geometry.height()
            x = gpos.x() - round(width * relative[0])
            y = gpos.y() - round(height * relative[1])

            self.setGeometry(x, y, width, height)
            pass
        else:
            # 鼠标移动偏移量
            offsetPos = event.globalPos() - self._posLast
            # ~ print(self.pos(), '->', self.pos() + offsetPos)
            self.move(self.pos() + offsetPos)
    def _change_cursor_icon(self, area):
        """改变鼠标在窗口边缘时的图片"""

        if self.maximumWidth() == self.minimumWidth() and (area == 21 or area == 23):
            return None
        if self.maximumHeight() == self.minimumHeight() and (area == 12 or area == 32):
            return None

        if area == 11 or area == 33:
            self.setCursor(QtCore.Qt.SizeFDiagCursor)
        elif area == 12 or area == 32:
            self.setCursor(QtCore.Qt.SizeVerCursor)
        elif area == 13 or area == 31:
            self.setCursor(QtCore.Qt.SizeBDiagCursor)
        elif area == 21 or area == 23:
            self.setCursor(QtCore.Qt.SizeHorCursor)
        else:
            self.setCursor(QtCore.Qt.ArrowCursor)
    def _resize(self, event):
        """实现拖动调整窗口大小的函数

        以新旧坐标差计算偏移量，使用 QRect 实例附带位置坐标；
        核心算法做了三重校验，以确保任意情况下窗口都能以正确的方式调整大小：
            一: 横纵坐标与最值校验，确保在最值范围内调整大小；
            二: 横纵坐标与左右区块校验，确保鼠标在窗口边缘时才调整大小；
            三: 横纵坐标与极值偏移量校验，确保在改变坐标的情况下，窗口不会发生漂移
        """
        # 鼠标在窗口中的区域
        area = self._area
        # 鼠标偏移量
        offsetPos = event.globalPos() - self._posLast
        # 鼠标在窗口中的坐标
        winPos = event.pos()

        # 矩形实例，被赋予窗口的几何属性（x, y, width, height）
        # 利用其改变左上角坐标，但右下角坐标不变的特性，实现窗口移动效果
        rect = QtCore.QRect(self.geometry())

        x = rect.x()
        y = rect.y()
        width = rect.width()
        height = rect.height()

        minWidth = self.minimumWidth()
        minHeight = self.minimumHeight()
        maxWidth = self.maximumWidth()
        maxHeight = self.maximumHeight()

        # 根据不同区域选择不同操作
        if area == 11:
            # 左上
            pos = rect.topLeft()

            if offsetPos.x() < 0 and width < maxWidth or offsetPos.x() > 0 and width > minWidth:
                if offsetPos.x() < 0 and winPos.x() <= 0 or offsetPos.x() > 0 and winPos.x() >= 0:
                    if (maxWidth - width) >= -offsetPos.x() and (width - minWidth) >= offsetPos.x():
                        pos.setX(pos.x() + offsetPos.x())

            if offsetPos.y() < 0 and height < maxHeight or offsetPos.y() > 0 and height > minHeight:
                if offsetPos.y() < 0 and winPos.y() <= 0 or offsetPos.y() > 0 and winPos.y() >= 0:
                    if (maxHeight - height) >= -offsetPos.y() and (height - minHeight) >= offsetPos.y():
                        pos.setY(pos.y() + offsetPos.y())

            rect.setTopLeft(pos)

        elif area == 13:
            # 右上
            pos = rect.topRight()

            if offsetPos.x() < 0 and width > minWidth or offsetPos.x() > 0 and width < maxWidth:
                if offsetPos.x() < 0 and winPos.x() <= width or offsetPos.x() > 0 and winPos.x() >= width:
                    pos.setX(pos.x() + offsetPos.x())

            if offsetPos.y() < 0 and height < maxHeight or offsetPos.y() > 0 and height > minHeight:
                if offsetPos.y() < 0 and winPos.y() <= 0 or offsetPos.y() > 0 and winPos.y() >= 0:
                    if (maxHeight - height) >= -offsetPos.y() and (height - minHeight) >= offsetPos.y():
                        pos.setY(pos.y() + offsetPos.y())

            rect.setTopRight(pos)

        elif area == 31:
            # 左下
            pos = rect.bottomLeft()

            if offsetPos.x() < 0 and width < maxWidth or offsetPos.x() > 0 and width > minWidth:
                if offsetPos.x() < 0 and winPos.x() <= 0 or offsetPos.x() > 0 and winPos.x() >= 0:
                    if (maxWidth - width) >= -offsetPos.x() and (width - minWidth) >= offsetPos.x():
                        pos.setX(pos.x() + offsetPos.x())

            if offsetPos.y() < 0 and height > minHeight or offsetPos.y() > 0 and height < maxHeight:
                if offsetPos.y() < 0 and winPos.y() <= height or offsetPos.y() > 0 and winPos.y() >= height:
                    pos.setY(pos.y() + offsetPos.y())

            rect.setBottomLeft(pos)

        elif area == 33:
            # 右下
            pos = rect.bottomRight()

            if offsetPos.x() < 0 and width > minWidth or offsetPos.x() > 0 and width < maxWidth:
                if offsetPos.x() < 0 and winPos.x() <= width or offsetPos.x() > 0 and winPos.x() >= width:
                    pos.setX(pos.x() + offsetPos.x())

            if offsetPos.y() < 0 and height > minHeight or offsetPos.y() > 0 and height < maxHeight:
                if offsetPos.y() < 0 and winPos.y() <= height or offsetPos.y() > 0 and winPos.y() >= height:
                    pos.setY(pos.y() + offsetPos.y())

            rect.setBottomRight(pos)

        elif area == 12:
            # 中上
            if offsetPos.y() < 0 and height < maxHeight or offsetPos.y() > 0 and height > minHeight:
                if offsetPos.y() < 0 and winPos.y() <= 0 or offsetPos.y() > 0 and winPos.y() >= 0:
                    if (maxHeight - height) >= -offsetPos.y() and (height - minHeight) >= offsetPos.y():
                        rect.setTop(rect.top() + offsetPos.y())

        elif area == 21:
            # 中左
            if offsetPos.x() < 0 and width < maxWidth or offsetPos.x() > 0 and width > minWidth:
                if offsetPos.x() < 0 and winPos.x() <= 0 or offsetPos.x() > 0 and winPos.x() >= 0:
                    if (maxWidth - width) >= -offsetPos.x() and (width - minWidth) >= offsetPos.x():
                        rect.setLeft(rect.left() + offsetPos.x())

        elif area == 23:
            # 中右
            if offsetPos.x() < 0 and width > minWidth or offsetPos.x() > 0 and width < maxWidth:
                if offsetPos.x() < 0 and winPos.x() <= width or offsetPos.x() > 0 and winPos.x() >= width:
                    rect.setRight(rect.right() + offsetPos.x())

        elif area == 32:
            # 中下
            if offsetPos.y() < 0 and height > minHeight or offsetPos.y() > 0 and height < maxHeight:
                if offsetPos.y() < 0 and winPos.y() <= height or offsetPos.y() > 0 and winPos.y() >= height:
                    rect.setBottom(rect.bottom() + offsetPos.y())

        # 设置窗口几何属性（坐标，宽高）
        self.setGeometry(rect)
    def _restore_or_maximize_window(self):
        # If window is maxmized
        if self.isMaximized():
            self.showNormal()
            # Change Icon
            self.ui.restore_window_button.setIcon(QtGui.QIcon(u":/find/icons/find/内部扩大_internal-expansion.svg"))
            self.ui.frame_size_grip.hide()
        else:
            self.showMaximized()
            # Change Icon
            self.ui.restore_window_button.setIcon(QtGui.QIcon(u":/find/icons/find/内部缩小_internal-reduction.svg"))
            self.ui.frame_size_grip.show()
    def closeEvent(self, event):
        # self.temp_dir.cleanup()
        # event.accept()		# 表示同意了，结束吧
        return super().closeEvent(event)

    def Menu_Button(self):
        # GET BT CLICKED
        btnWidget = self.sender()
        # PAGE file_view
        if btnWidget.objectName() == "btn_file_view":
            self.ui.label_menustatus.setText('  File tree')
            self.ui.stackedWidget_menu.setCurrentWidget(self.ui.page_file_model)
            UIFunctions.resetStyle(self, "btn_file_view")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))
            UIFunctions.toggleMenu(self, 0, btnWidget.objectName())
        # PAGE datadict
        if btnWidget.objectName() == "btn_datadict":
            self.ui.label_menustatus.setText('  Data Tree')
            self.ui.stackedWidget_menu.setCurrentWidget(self.ui.page_datadict)
            UIFunctions.resetStyle(self, "btn_datadict")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))
            UIFunctions.toggleMenu(self, 0, btnWidget.objectName())
        # PAGE old file
        if btnWidget.objectName() == "btn_file":
            self.ui.label_menustatus.setText('  File')
            self.ui.stackedWidget_menu.setCurrentWidget(self.ui.page_file)
            UIFunctions.resetStyle(self, "btn_file")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))
            UIFunctions.toggleMenu(self, 0, btnWidget.objectName())
        # PAGE old file
        if btnWidget.objectName() == "btn_datamaker":
            self.ui.label_menustatus.setText('  Data maker')
            self.ui.stackedWidget_menu.setCurrentWidget(self.ui.page_datamaker)
            UIFunctions.resetStyle(self, "btn_datamaker")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))
            UIFunctions.toggleMenu(self, 0, btnWidget.objectName())
        # PAGE old settings
        if btnWidget.objectName() == "btn_settings":
            self.ui.label_menustatus.setText('  Settings')
            self.ui.stackedWidget_menu.setCurrentWidget(self.ui.page_settings)
            UIFunctions.resetStyle(self, "btn_settings")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))
            UIFunctions.toggleMenu(self, 0, btnWidget.objectName())
        

        UIFunctions.setLastMenu(btnWidget.objectName())
        UIFunctions.setLastWidth(self)    
    
    # @QtCore.pyqtSlot()   
    def Slot_Tab_start_filepath(self,filepath):
        # 把从Tab_Start 传过来的文件地址作为参数传入
        self.Open_Folder2(*[filepath])

    def Open_Folder(self,*selected_path):
        # *selected_path为 可选参数,为其他按键触发文件或者文件夹时自己操作
        try:
            tmp=self.path_folder
            """
                首先判定是否传进来了文件路径:
                    如果是的话 判定是否为 文件夹/文件
                    如果不是的话 打开文件选择对话框
                    将dir返回 self.path_folder 中
            """
            if selected_path:
                if os.path.isfile(selected_path[0]):
                    self.path_folder=os.path.dirname(selected_path[0])
                elif os.path.isdir(selected_path[0]):
                    self.path_folder=selected_path[0]
                else:
                    self.path_folder=''
            else:       
                self.path_folder = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
                
            if tmp !='':
                # rootIndex = self.file_tree.indexOfTopLevelItem(self.file_tree.currentItem())
                # self.file_tree.takeTopLevelItem(rootIndex)                                #不知道为啥用不了
                if self.path_folder=='':
                    pass
                else:
                    self.file_tree.clear()
                    self.file_tree.doubleClicked.disconnect(self.Filetree_doubleclicked)
                    self.file_tree.customContextMenuRequested.disconnect(self.treeWidgetItem_fun)
            self.file_tree = self.ui.treeWidget
            self.file_tree.setColumnCount(3)                                                # 虽然设置的只有一列显示，但是还有附加值属性 第一列文件名，第二列绝对地址，第三列是否为文件夹
            self.file_tree.setColumnWidth(0, 0)                                             # 第一列设置为0就可以限制splitter的最小宽度           
            self.file_tree.setColumnHidden(2,True)                                          # 隐藏后边的属性
            self.file_tree.setColumnHidden(1,True)                                          # 隐藏后边的属性
            self.file_tree.setHeaderHidden(True)
            self.file_tree.setIconSize(Qt.QSize(25, 25))
            # self.file_tree.setSortingEnabled(True)
            self.file_tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
            self.file_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)                # 右键菜单
            self.file_tree.customContextMenuRequested.connect(self.treeWidgetItem_fun)      # 绑定右键菜单事件   
            self.file_tree.doubleClicked.connect(self.Filetree_doubleclicked)               # 双击事件
            self.file_tree.sortItems(2,QtCore.Qt.AscendingOrder)                            # QtCore.Qt.AscendingOrder QtCore.Qt.DescendingOrder
            dirs = os.listdir(self.path_folder)
            print(self.path_folder)
    
            fileInfo = QtCore.QFileInfo(self.path_folder)
            fileIcon = QtWidgets.QFileIconProvider()
            icon = QtGui.QIcon(fileIcon.icon(fileInfo))
            root = QTreeWidgetItem(self.file_tree)
            root.setText(0,self.path_folder.split('/')[-1])
            root.setIcon(0,QtGui.QIcon(icon))
            root.setForeground(0,QtCore.Qt.white)
            self.CreateFileTree(dirs, root, self.path_folder)
            root.setExpanded(True)
            # self.file_tree.expand(self.file_tree)

            self.ui.page1_layout.addWidget(self.file_tree)
            QApplication.processEvents()
        except Exception as e:
            print(e)

    def Open_Folder2(self,*selected_path):
        '''
        *selected_path为 可选参数,为其他按键触发文件或者文件夹时自己操作
        Open_Folder2 为使用file system model 的专用
        '''
        try:
            tmp=self.path_folder
            """
                首先判定是否传进来了文件路径:
                    如果是的话 判定是否为 文件夹/文件
                    如果不是的话 打开文件选择对话框
                    将dir返回 self.path_folder 中
            """
            if selected_path:
                if os.path.isfile(selected_path[0]):
                    self.path_folder=os.path.dirname(selected_path[0])
                elif os.path.isdir(selected_path[0]):
                    self.path_folder=selected_path[0]
                else:
                    self.path_folder=''
            else:       
                self.path_folder = QFileDialog.getExistingDirectory(self, "选取文件夹", "./")
                
            if tmp !='':
                if self.path_folder=='':
                    self.path_folder=tmp
                else:
                    pass
            
            self.file_model.setRootPath(self.path_folder)
            self.file_tree_view.setRootIndex(self.file_model.index(self.path_folder))    # 更新Qfilesystemmoddel的监视位置
            self.updateRecentFiles(self.path_folder)                                     # 更新config.ini中的recent file
            self.ui.label_file_dir.setText(self.path_folder)
            self.start_tab.refresh_filelabel()                                           # 在不关闭tab_srart的情况下更新recent file label

        except Exception as e:
            print(e)

    def On_doubleClicked_file_tree_model(self,Qmodelidx):
        # print(self.file_model.filePath(Qmodelidx))
        # print(self.file_model.fileName(Qmodelidx))
        # print(self.file_model.fileInfo(Qmodelidx))
        Tab_name=self.file_model.fileInfo(self.file_tree_view.currentIndex()).fileName()
        root    =self.file_model.filePath(self.file_tree_view.currentIndex())
        self.addTab(Tab_name,root)

    def refresh_file_filter(self):
        file_extention=['3ds','mat','sxm','dat','*']

        if self.ui.lineEdit_file_filter.text()!='':
            name_filter=['*'+self.ui.lineEdit_file_filter.text()+'*.{0}'.format(x) for x in file_extention]
        else:
            name_filter=['*'+'*.{0}'.format(x) for x in file_extention]
        self.file_model.setNameFilters(name_filter)

    def CreateFileTree(self, dirs, root, path):

        def convert_path(path: str) -> str:                                                  #巧妙地函数适用于任何系统的地址转换
            seps = r'\/'
            sep_other = seps.replace(os.sep, '')
            return path.replace(sep_other, os.sep) if sep_other in path else path
        # def convert_path(path: str) -> str:                                                #功能一摸一样的函数更为简洁
        #    return path.replace(r'\/'.replace(os.sep, ''), os.sep)
 

        for i in dirs:
            # path_new = path + '\\' + i
            path_new = os.path.join(path,i)
            if os.path.isdir(path_new):                                                 #如果这一个是文件夹则创建为节点
                fileInfo = QtCore.QFileInfo(path_new)
                fileIcon = QtWidgets.QFileIconProvider()
                icon = QtGui.QIcon(fileIcon.icon(fileInfo))
                child = QTreeWidgetItem(root)
                child.setText(0,i)                                                      #第一个属性：文件名
                child.setText(1,convert_path(path_new))                                 #第二个属性：文件绝对地址
                child.setText(2,'10')                                                   #第三个属性：按照这个排序
                child.setForeground(0,QtCore.Qt.white)
                child.setIcon(0,QtGui.QIcon(icon))
                dirs_new = os.listdir(path_new)
                self.CreateFileTree(dirs_new, child, path_new)
            else:
                fileInfo = QtCore.QFileInfo(path_new)
                fileIcon = QtWidgets.QFileIconProvider()
                icon = QtGui.QIcon(fileIcon.icon(fileInfo))
                child = QTreeWidgetItem(root)
                child.setText(0,i)
                child.setText(1,convert_path(path_new))                                 #第二个属性：文件绝对地址
                child.setText(2,fileInfo.suffix())                                       #第三个属性：按照这个排序
                child.setIcon(0,QtGui.QIcon(icon))
                child.setForeground(0,QtCore.Qt.white)

    def treeWidgetItem_fun(self,pos):
        item = self.file_tree.currentItem()
        print("key=%s " % (item.text(0)))
        try:
            self.filecontextMenu = QMenu()                                                #创建对象
            self.action1 = self.filecontextMenu.addAction(u'打开为项目')                   #添加动作
            self.action2 = self.filecontextMenu.addAction(u'删除item')
            if item.text(0)[-4:]=='.3ds':
                self.action3 = self.filecontextMenu.addAction(u'3ds转换为mat->didv')
                self.action4 = self.filecontextMenu.addAction(u'3ds转换为mat->all')
                self.action4 = self.filecontextMenu.addAction(u'3ds转换为mat->linecut')
                self.action5 = self.filecontextMenu.addAction(u'3ds转换为dat->all')
                self.action6 = self.filecontextMenu.addAction(u'3ds转换为sxm')
            if item.text(0)[-4:]=='.sxm':
                self.action3 = self.filecontextMenu.addAction(u'sxm转换为3ds')
                self.action4 = self.filecontextMenu.addAction(u'sxm转换为mat')
            if item.text(0)[-4:]=='.dat':
                self.action3 = self.filecontextMenu.addAction(u'dat转换为3ds')
                self.action4 = self.filecontextMenu.addAction(u'dat转换为mat')
            if item.text(0)[-4:]=='.mat':
                self.action3 = self.filecontextMenu.addAction(u'mat转换为3ds')
                self.action4 = self.filecontextMenu.addAction(u'mat转换为sxm')
            self.filecontextMenu.triggered[QAction].connect(self.Action_filetree_rightclicked)
            self.filecontextMenu.exec_(self.mapToGlobal(pos))                             #随指针的位置显示菜单
            self.filecontextMenu.show()                                                   #显示
        except Exception as e:
            print(e)


    def Action_filetree_rightclicked(self,q):
        command=q.text()
        print(command)
        list_selected=self.file_tree.selectedItems()
        for item in list_selected:
            if command=='打开为项目':
                Tab_name=item.text(0)
                root    =item.text(1)
                self.addTab(Tab_name,root)
            elif command=='删除item':
                self.Filetree_deleteItem(item)
            elif command=='sxm转换为3ds':
                try:
                    raw_header={}
                    data_sxm=read.Scan(item.text(1))
                    fname,ftype=QFileDialog.getSaveFileName(self, 'save file: '+item.text(0), os.path.dirname(item.text(1))+'\\'+'sxm_'+item.text(0)[:-4], "3ds文件 (*.3ds);;All Files (*)")
                    raw_header['savepath']=fname
                    if fname=='':
                        raise IOError('没有文件地址')
                    raw_header['header']=data_sxm.header
                    tmp=read.Write(data_sxm.signals,raw_header,'sxm','3ds')
                    # tmp.Grid_write()
                    del tmp,raw_header,data_sxm,ftype
                    # timer=QtCore.QTimer()
                    self.ui.status_label.setText(command+'成功')
                    QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
                except Exception as e:
                    print(e)
                    self.ui.status_label.setText(command+'失败: '+str(e))
                    QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
            elif command=='sxm转换为mat':
                try:
                    raw_header={}
                    data_sxm=read.Scan(item.text(1))
                    fname,ftype=QFileDialog.getSaveFileName(self, 'save file: '+item.text(0), os.path.dirname(item.text(1))+'\\'+'sxm_'+item.text(0)[:-4], "mat文件 (*.mat);;All Files (*)")
                    raw_header['savepath']=fname
                    if fname=='':
                        raise IOError('没有文件地址')
                    tmp=read.Write(data_sxm,raw_header,'sxm','mat')
                    del tmp,raw_header,data_sxm,fname,ftype
                    self.ui.status_label.setText(command+'成功')
                    QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
                except Exception as e:
                    print(e)
                    self.ui.status_label.setText(command+'失败: '+str(e))
                    QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
            elif command=='mat转换为3ds':
                try:
                    raw_header={}
                    data_mat=scio.loadmat(item.text(1))
                    fname,ftype=QFileDialog.getSaveFileName(self, 'save file: '+item.text(0), os.path.dirname(item.text(1))+'\\'+'mat_'+item.text(0)[:-4],  "3ds文件 (*.3ds);;All Files (*)")
                    raw_header['savepath']=fname
                    if fname=='':
                        raise IOError('没有文件地址')
                    tmp=read.Write(data_mat,raw_header,'mat','3ds')
                    del tmp,raw_header,data_mat,fname,ftype
                    self.ui.status_label.setText(command+'成功')
                    QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
                except Exception as e:
                    print(e)
                    self.ui.status_label.setText(command+'失败: '+str(e))
                    QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
            elif command=='mat转换为sxm':
                try:
                    raw_header={}
                    data_mat=scio.loadmat(item.text(1))
                    fname,ftype=QFileDialog.getSaveFileName(self, 'save file: '+item.text(0), os.path.dirname(item.text(1))+'\\'+'mat_'+item.text(0)[:-4],  "sxm文件 (*.sxm);;All Files (*)")
                    raw_header['savepath']=fname
                    if fname=='':
                        raise IOError('没有文件地址')
                    tmp=read.Write(data_mat,raw_header,'mat','sxm')
                    del tmp,raw_header,data_mat,fname,ftype
                    self.ui.status_label.setText(command+'成功')
                    QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
                except Exception as e:
                    print(e)
                    self.ui.status_label.setText(command+'失败: '+str(e))
                    QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
            elif command=='3ds转换为mat->didv' or command=='3ds转换为mat->all' or command=='3ds转换为mat->linecut':
                try:
                    raw_header={}
                    data_3ds=read.Grid(item.text(1))
                    fname,ftype=QFileDialog.getSaveFileName(self, 'save file: '+item.text(0), os.path.dirname(item.text(1))+'\\'+'3ds_'+item.text(0)[:-4],  "mat文件 (*.mat);;All Files (*)")
                    raw_header['savepath']=fname
                    if fname=='':
                        raise IOError('没有文件地址')
                    if command=='3ds转换为mat->didv':
                        raw_header['savemode']='didv'
                    elif command=='3ds转换为mat->all':
                        raw_header['savemode']='all'
                    elif command=='3ds转换为mat->linecut':
                        raw_header['savemode']='linecut'
                    tmp=read.Write(data_3ds,raw_header,'3ds','mat')
                    del tmp,raw_header,data_3ds,fname,ftype
                    self.ui.status_label.setText(command+'成功')
                    QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
                except Exception as e:
                    print(e)
                    self.ui.status_label.setText(command+'失败: '+str(e))
                    QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
            
            elif command=='3ds转换为sxm':
                try:
                    raw_header={}
                    data_3ds=read.Grid(item.text(1))
                    fname,ftype=QFileDialog.getSaveFileName(self, 'save file: '+item.text(0), os.path.dirname(item.text(1))+'\\'+'3ds_'+item.text(0)[:-4],  "sxm文件 (*.sxm);;All Files (*)")
                    raw_header['savepath']=fname
                    if fname=='':
                        raise IOError('没有文件地址')
                    tmp=read.Write(data_3ds,raw_header,'3ds','sxm')
                    del tmp,raw_header,data_3ds,fname,ftype
                    self.ui.status_label.setText(command+'成功')
                    QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
                except Exception as e:
                    print(e)
                    self.ui.status_label.setText(command+'失败: '+str(e))
                    QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
            elif command=='3ds转换为dat->all':
                try:
                    raw_header={}
                    data_3ds=read.Grid(item.text(1))
                    fname,ftype=QFileDialog.getSaveFileName(self, 'save file: '+item.text(0), os.path.dirname(item.text(1))+'\\'+'3ds_'+item.text(0)[:-4],  "dat文件 (*.dat);;All Files (*)")
                    raw_header['savepath']=fname
                    if fname=='':
                        raise IOError('没有文件地址')
                    tmp=read.Write(data_3ds,raw_header,'3ds','dat')
                    del tmp,raw_header,data_3ds,fname,ftype
                    self.ui.status_label.setText(command+'成功')
                    QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
                except Exception as e:
                    print(e)
                    self.ui.status_label.setText(command+'失败: '+str(e))
                    QtCore.QTimer.singleShot(10000,self._Reset_status_bar)


    def Filetree_doubleclicked(self):
        root=self.file_tree.currentItem().text(1)
        print("root=%s " % (root))
        print(self.file_tree.currentItem().text(0),'  is file ? :',os.path.isfile(root))
        if os.path.isfile(root):
            self.addTab(self.file_tree.currentItem().text(0),root)

    # 删除控件树子节点/根节点
    def Filetree_deleteItem(self,currNode):
        try:
            # 尝试删除子节点（通过其父节点，调用removeChild函数进行删除）
            # currNode = self.file_tree.currentItem()
            parent1 = currNode.parent()
            parent1.removeChild(currNode)
        except Exception:
            # 遇到异常时删除根节点
            try:
                rootIndex = self.file_tree.indexOfTopLevelItem(currNode)
                self.file_tree.takeTopLevelItem(rootIndex)
            except Exception:
                print(Exception)

    def data_dict_fun(self,pos):
        item = self.datadict_tree.currentItem()
        print("key=%s " % (item.text(0)))
        try:
            self.filecontextMenu = QMenu()                                                #创建对象
            self.action1 = self.filecontextMenu.addAction(u'保存为mat')                   #添加动作
            self.filecontextMenu.triggered[QAction].connect(self.Action_datadict_rightclicked)
            self.filecontextMenu.exec_(self.mapToGlobal(pos))                             #随指针的位置显示菜单
            self.filecontextMenu.show()                                                   #显示
        except Exception as e:
            print(e)

    def Action_datadict_rightclicked(self,q):
        command=q.text()
        tmp_data={}
        print(command)
        item = self.datadict_tree.currentItem()
        tmp_data.update({'result':item.data(0,QtCore.Qt.UserRole)})
        fname,ftype=QFileDialog.getSaveFileName(self, 'save file: ', self.path_folder+'\\'+'saved_data', "mat文件 (*.mat);;All Files (*)")
        scio.savemat(fname,tmp_data)
        

        
    def rightclicked_tree_view(self,pos):
        path=self.file_model.filePath(self.file_tree_view.currentIndex())
        print(path)
        try:
            self.filecontextMenu = QMenu()                                                #创建对象
            self.action1 = self.filecontextMenu.addAction(u'打开为项目')                   #添加动作
            # self.action2 = self.filecontextMenu.addAction(u'删除item')
            self.action2 = self.filecontextMenu.addAction(u'复制文件地址')
            self.action3 = self.filecontextMenu.addAction(u'复制文件名称')
            if path[-4:]=='.3ds':
                self.action5 = self.filecontextMenu.addAction(u'3ds转换为mat->didv')
                self.action6 = self.filecontextMenu.addAction(u'3ds转换为mat->all')
                self.action7 = self.filecontextMenu.addAction(u'3ds转换为mat->linecut')
                self.action8 = self.filecontextMenu.addAction(u'3ds转换为dat->all')
                self.action9 = self.filecontextMenu.addAction(u'3ds转换为sxm')
            if path[-4:]=='.sxm':
                self.action5 = self.filecontextMenu.addAction(u'sxm转换为3ds')
                self.action6 = self.filecontextMenu.addAction(u'sxm转换为mat')
            if path[-4:]=='.dat':
                self.action5 = self.filecontextMenu.addAction(u'dat转换为3ds')
                self.action6 = self.filecontextMenu.addAction(u'dat转换为mat')
            if path[-4:]=='.mat':
                self.action5 = self.filecontextMenu.addAction(u'mat转换为3ds')
                self.action6 = self.filecontextMenu.addAction(u'mat转换为sxm')
            self.filecontextMenu.triggered[QAction].connect(self.rightclicked_tree_view_action)
            self.filecontextMenu.exec_(self.mapToGlobal(pos))                             #随指针的位置显示菜单
            self.filecontextMenu.show()                                                   #显示
        except Exception as e:
            print(e)

    def rightclicked_tree_view_action(self,q):
        
        def convert_path(path: str) -> str:                                                  #巧妙地函数适用于任何系统的地址转换
            seps = r'\/'
            sep_other = seps.replace(os.sep, '')
            return path.replace(sep_other, os.sep) if sep_other in path else path
        
        command=q.text()
        full_path=self.file_model.filePath(self.file_tree_view.currentIndex())
        file_name=self.file_model.fileInfo(self.file_tree_view.currentIndex()).fileName()
        file_ext =self.file_model.fileInfo(self.file_tree_view.currentIndex()).suffix()
        
        self.ui.footer.setStyleSheet('''background-color: rgb(0, 122, 204);''')
        if command=='打开为项目':
            try:
                Tab_name=file_name
                root    =full_path
                self.addTab(Tab_name,root)
            except Exception as e:
                print(e)
                self.ui.status_label.setText(command+'失败: '+str(e))
                self.ui.footer.setStyleSheet('''background-color: rgb(204,102,51);''')
                QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
        elif command=='删除item':
            pass
        elif command=='复制文件地址':
            clipboard = QApplication.clipboard()
            clipboard.setText(convert_path(full_path))
            self.ui.status_label.setText(command+'成功')
            QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
        elif command=='复制文件名称':
            clipboard = QApplication.clipboard()
            clipboard.setText(file_name)
            self.ui.status_label.setText(command+'成功')
            QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
        elif command=='sxm转换为3ds':
            try:
                raw_header={}
                data_sxm=read.Scan(full_path)
                fname,ftype=QFileDialog.getSaveFileName(self, 'save file: '+file_name, os.path.dirname(full_path)+'\\'+'sxm_'+file_name[:-4], "3ds文件 (*.3ds);;All Files (*)")
                raw_header['savepath']=fname
                if fname=='':
                    raise IOError('没有文件地址')
                raw_header['header']=data_sxm.header
                tmp=read.Write(data_sxm.signals,raw_header,'sxm','3ds')
                # tmp.Grid_write()
                del tmp,raw_header,data_sxm,ftype
                # timer=QtCore.QTimer()
                self.ui.status_label.setText(command+'成功')
                QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
            except Exception as e:
                print(e)
                self.ui.status_label.setText(command+'失败: '+str(e))
                self.ui.footer.setStyleSheet('''background-color: rgb(204,102,51);''')
                QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
        elif command=='sxm转换为mat':
            try:
                raw_header={}
                data_sxm=read.Scan(full_path)
                fname,ftype=QFileDialog.getSaveFileName(self, 'save file: '+file_name, os.path.dirname(full_path)+'\\'+'sxm_'+file_name[:-4], "mat文件 (*.mat);;All Files (*)")
                raw_header['savepath']=fname
                if fname=='':
                    raise IOError('没有文件地址')
                tmp=read.Write(data_sxm,raw_header,'sxm','mat')
                del tmp,raw_header,data_sxm,fname,ftype
                self.ui.status_label.setText(command+'成功')
                QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
            except Exception as e:
                print(e)
                self.ui.status_label.setText(command+'失败: '+str(e))
                self.ui.footer.setStyleSheet('''background-color: rgb(204,102,51);''')
                QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
        elif command=='mat转换为3ds':
            try:
                raw_header={}
                data_mat=scio.loadmat(full_path)
                fname,ftype=QFileDialog.getSaveFileName(self, 'save file: '+file_name, os.path.dirname(full_path)+'\\'+'mat_'+file_name[:-4],  "3ds文件 (*.3ds);;All Files (*)")
                raw_header['savepath']=fname
                if fname=='':
                    raise IOError('没有文件地址')
                tmp=read.Write(data_mat,raw_header,'mat','3ds')
                del tmp,raw_header,data_mat,fname,ftype
                self.ui.status_label.setText(command+'成功')
                QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
            except Exception as e:
                print(e)
                self.ui.status_label.setText(command+'失败: '+str(e))
                self.ui.footer.setStyleSheet('''background-color: rgb(204,102,51);''')
                QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
        elif command=='mat转换为sxm':
            try:
                raw_header={}
                data_mat=scio.loadmat(full_path)
                fname,ftype=QFileDialog.getSaveFileName(self, 'save file: '+file_name, os.path.dirname(full_path)+'\\'+'mat_'+file_name[:-4],  "sxm文件 (*.sxm);;All Files (*)")
                raw_header['savepath']=fname
                if fname=='':
                    raise IOError('没有文件地址')
                tmp=read.Write(data_mat,raw_header,'mat','sxm')
                del tmp,raw_header,data_mat,fname,ftype
                self.ui.status_label.setText(command+'成功')
                QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
            except Exception as e:
                print(e)
                self.ui.status_label.setText(command+'失败: '+str(e))
                self.ui.footer.setStyleSheet('''background-color: rgb(204,102,51);''')
                QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
        elif command=='3ds转换为mat->didv' or command=='3ds转换为mat->all' or command=='3ds转换为mat->linecut':
            try:
                raw_header={}
                data_3ds=read.Grid(full_path)
                fname,ftype=QFileDialog.getSaveFileName(self, 'save file: '+file_name, os.path.dirname(full_path)+'\\'+'3ds_'+file_name[:-4],  "mat文件 (*.mat);;All Files (*)")
                raw_header['savepath']=fname
                if fname=='':
                    raise IOError('没有文件地址')
                if command=='3ds转换为mat->didv':
                    raw_header['savemode']='didv'
                elif command=='3ds转换为mat->all':
                    raw_header['savemode']='all'
                elif command=='3ds转换为mat->linecut':
                    raw_header['savemode']='linecut'
                tmp=read.Write(data_3ds,raw_header,'3ds','mat')
                del tmp,raw_header,data_3ds,fname,ftype
                self.ui.status_label.setText(command+'成功')
                QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
            except Exception as e:
                print(e)
                self.ui.status_label.setText(command+'失败: '+str(e))
                self.ui.footer.setStyleSheet('''background-color: rgb(204,102,51);''')
                QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
        
        elif command=='3ds转换为sxm':
            try:
                raw_header={}
                data_3ds=read.Grid(full_path)
                fname,ftype=QFileDialog.getSaveFileName(self, 'save file: '+file_name, os.path.dirname(full_path)+'\\'+'3ds_'+file_name[:-4],  "sxm文件 (*.sxm);;All Files (*)")
                raw_header['savepath']=fname
                if fname=='':
                    raise IOError('没有文件地址')
                tmp=read.Write(data_3ds,raw_header,'3ds','sxm')
                del tmp,raw_header,data_3ds,fname,ftype
                self.ui.status_label.setText(command+'成功')
                QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
            except Exception as e:
                print(e)
                self.ui.status_label.setText(command+'失败: '+str(e))
                self.ui.footer.setStyleSheet('''background-color: rgb(204,102,51);''')
                QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
        elif command=='3ds转换为dat->all':
            try:
                raw_header={}
                data_3ds=read.Grid(full_path)
                fname,ftype=QFileDialog.getSaveFileName(self, 'save file: '+file_name, os.path.dirname(full_path)+'\\'+'3ds_'+file_name[:-4],  "dat文件 (*.dat);;All Files (*)")
                raw_header['savepath']=fname
                if fname=='':
                    raise IOError('没有文件地址')
                tmp=read.Write(data_3ds,raw_header,'3ds','dat')
                del tmp,raw_header,data_3ds,fname,ftype
                self.ui.status_label.setText(command+'成功')
                QtCore.QTimer.singleShot(10000,self._Reset_status_bar)
            except Exception as e:
                print(e)
                self.ui.status_label.setText(command+'失败: '+str(e))
                self.ui.footer.setStyleSheet('''background-color: rgb(204,102,51);''')
                QtCore.QTimer.singleShot(10000,self._Reset_status_bar)



    #更新最近文件
    def updateRecentFiles(self, fname):
        if fname not in self.recentFiles:
            self.recentFiles.insert(0, fname)
            if len(self.recentFiles) > self.maxNumRecentFiles:
                self.recentFiles.pop()
        # print(self.recentFiles)
        #保存更新后最近菜单列表
        self.settings.setValue('FileList/recentFiles', self.recentFiles)


    # @QtCore.pyqtSlot()    
    def addTab(self,Tab_name,file_root):
        self.project[Tab_name]=TabWindow()
        print(self.project)
        self.project[Tab_name].Signal_refreshdata.connect(self.Signal_accept_refreshdata)
        self.Signal_filepath.connect(self.project[Tab_name].Signal_accept_filepath)
        self.Signal_filepath.emit(file_root)
        self.Signal_filepath.disconnect(self.project[Tab_name].Signal_accept_filepath)       #tnnd一定要写这一个要不然所有的tab一起更新，操了
        self.ui.tabWidget.addTab(self.project[Tab_name],Tab_name)
        self.updateRecentFiles(file_root)
    def SxmMaker(self):
        self.tab_SxmMaker=Tab_Sxmmaker()
        self.ui.tabWidget.addTab(self.tab_SxmMaker,'Sxm maker')
    def closeTab(self,index):
        print('closed Tab index: ',index)
        # print()
        self.ui.tabWidget.removeTab(index)
        
    def Signal_accept_refreshdata(self,data):
        print('已经接收到data更新信号')
        for key,value in data.items():
            print(key)
        self.datatree_projectList.update({data['-1'] : data} )
        self.datatree.clear()
        self.Create_datatree(self.datatree_projectList, self.datatree)
        self.datatree.insertTopLevelItems(0, self.rootList)
        for key in self.rootList:
            key.setExpanded(True)
        self.rootList=[]

        self.datadict_tree.clear()
        self.Create_datatree(self.datatree_projectList, self.datadict_tree)
        self.datadict_tree.insertTopLevelItems(0, self.rootList)
        for key in self.rootList:
            key.setExpanded(True)
        self.rootList=[]

    def Create_datatree(self, data, root):
        if isinstance(data, dict):
            for key in data.keys():
                if key=='-1':
                    pass
                else:
                    child = QTreeWidgetItem()
                    child.setText(0, key)
                    if isinstance(root, QTreeWidget) == False:  # 非根节点，添加子节点
                        root.addChild(child)
                    self.rootList.append(child)
                    value = data[key]
                    self.Create_datatree(value, child)
        else:
            if isinstance(data, type(np.array([]))):
                # root.setData(0, QtCore.Qt.UserRole, QVariant.fromValue(data))
                root.setData(0, QtCore.Qt.UserRole, QVariant(data))
                root.setData(1, QtCore.Qt.UserRole+1, QVariant('numpy'))
                if data.size>100:
                    root.setText(1, str(data.shape))
                    root.setToolTip(1, str(data.shape))
                else:
                    root.setText(1, str(data))
                    root.setToolTip(1, str(data))
            else:
                root.setData(0, QtCore.Qt.UserRole, QVariant(data))
                root.setData(1, QtCore.Qt.UserRole+1, QVariant('str'))
                root.setText(1, str(data))
                root.setToolTip(1, str(data))
    def _Reset_status_bar(self):
        self.ui.status_label.setText('ver 1.0.0')
        self.ui.footer.setStyleSheet('''background-color: rgb(33, 37, 43);''')

class TabWindow(QWidget):
    Signal_refreshdata=QtCore.pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.ui=Ui_TabWindow()
        self.ui.setupUi(self)
        self.init_UI()

        self.inner_Header_public={                          #程序内通用数据格式 header会随着数据有所填充
            'filetype'    :'',
            'parent_path' :'',
            'basename'    :'',
            'sweep_signal':'',
            'scan_center' :np.array([]),
            'scan_range'  :np.array([]),
            'scan_angle'  :np.array([]),
            'scan_px'     :np.array([]),
            'scan_sweeps' :np.array([]),
            'channel'     :[],
            'experiment_name':'',
            'time'        :'',
            'comment'     :'',
            'signal_sweep':np.array([])
        }
        self.pro_dict={}

    def init_UI(self):
        self.ui.btn_refresh.clicked.connect(self.Signal_fun_refreshdata)
        self.ui.textEdit=MyTextEdit()
        # self.ui.textEdit_mat=MyTextEdit_mat()
        self.mat_textedit=MyTextEdit_mat()
        self.ui.verticalLayout_2.addWidget(self.mat_textedit)
        
    def Signal_accept_filepath(self,filepath):             #初始化数据格式
        self.ui.label1.setText(filepath)
        _, fname_ext = os.path.splitext(filepath)
        project      = os.path.basename(filepath)
        self.pro_dict[project]={'Header':self.inner_Header_public.copy()}
        self.pro_dict[project]['Header']['filetype']    =fname_ext
        self.pro_dict[project]['Header']['parent_path'] =filepath
        self.pro_dict[project]['Header']['basename']    =project
        self.pro_dict[project]['Data']={}
        self.pro_dict['-1']=project
        if fname_ext=='.3ds':
            tmp_data=read.Grid(filepath)
            #公共头文件
            self.pro_dict[project]['Header']['sweep_signal']    =tmp_data.header['sweep_signal']            # 当横坐标用 'Bias (V)'
            self.pro_dict[project]['Header']['scan_center']     =tmp_data.header['pos_xy']
            self.pro_dict[project]['Header']['scan_range']      =tmp_data.header['size_xy']
            self.pro_dict[project]['Header']['scan_angle']      =tmp_data.header['angle']
            self.pro_dict[project]['Header']['scan_px']         =tmp_data.header['dim_px']
            self.pro_dict[project]['Header']['sweep_points']    =tmp_data.header['num_sweep_signal']        # 单个sweep的点数
            self.pro_dict[project]['Header']['channel']         =tmp_data.header['channels']
            self.pro_dict[project]['Header']['experiment_name'] =tmp_data.header['experiment_name']         # 'Grid Spectroscopy' 区分line grid
            self.pro_dict[project]['Header']['time_acquire']    =tmp_data.header['end_time']
            self.pro_dict[project]['Header']['time_modify']     =time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.pro_dict[project]['Header']['comment']         =tmp_data.header['comment']
            self.pro_dict[project]['Header']['signal_sweep']    =tmp_data.signals['_sweep_signal']

            # x=np.linspace(0,self.pro_dict[project]['Header']['scan_range'][0],self.pro_dict[project]['Header']['scan_px'][0])-self.pro_dict[project]['Header']['scan_range'][0]/2
            # y=np.linspace(0,self.pro_dict[project]['Header']['scan_range'][1],self.pro_dict[project]['Header']['scan_px'][1])-self.pro_dict[project]['Header']['scan_range'][1]/2
            # Xr_tmp,Yr_tmp=np.meshgrid(y,x)
            # Xr=Xr_tmp*np.cos(float(self.pro_dict[project]['Header']['scan_angle'])/180*np.pi)+Yr_tmp*np.sin(float(self.pro_dict[project]['Header']['scan_angle'])/180*np.pi)+self.pro_dict[project]['Header']['scan_center'][0]
            # Yr=-Xr_tmp*np.sin(float(self.pro_dict[project]['Header']['scan_angle'])/180*np.pi)+Yr_tmp*np.cos(float(self.pro_dict[project]['Header']['scan_angle'])/180*np.pi)+self.pro_dict[project]['Header']['scan_center'][1]

            self.pro_dict[project]['Header']['signal_x']        =tmp_data.signals['params'][:,:,3]
            self.pro_dict[project]['Header']['signal_y']        =tmp_data.signals['params'][:,:,4]
            self.pro_dict[project]['Header']['signal_z']        =tmp_data.signals['_topo']
            #数据，与保存格式有关，过滤掉不往里边存的
            for key in tmp_data.signals.keys():
                if key[0]=='_':
                    pass
                else:
                    self.pro_dict[project]['Data'].update({key: tmp_data.signals[key]}) 
            for key in self.pro_dict[project]['Header'].keys():
                print(key,'shape = ',self.pro_dict[project]['Header'][key])
            for key in self.pro_dict[project]['Data'].keys():
                print(key,'shape = ',self.pro_dict[project]['Data'][key].shape)

        elif fname_ext=='.sxm':
            tmp_data=read.Scan(filepath)
            #公用头函数
            self.pro_dict[project]['Header']['sweep_signal']    ='Bias (V)'
            self.pro_dict[project]['Header']['scan_center']     =tmp_data.header['scan_offset']
            self.pro_dict[project]['Header']['scan_range']      =tmp_data.header['scan_range']
            self.pro_dict[project]['Header']['scan_angle']      =tmp_data.header['scan_angle']
            self.pro_dict[project]['Header']['scan_px']         =tmp_data.header['scan_pixels']
            self.pro_dict[project]['Header']['sweep_points']    =1                                                   # 单个sweep的点数               
            self.pro_dict[project]['Header']['channel']         =tmp_data.header['data_info']['Name']                # 这个不带单位
            self.pro_dict[project]['Header']['experiment_name'] ='Scan'
            self.pro_dict[project]['Header']['time_acquire']    =tmp_data.header['rec_date']+' '+tmp_data.header['rec_time']
            self.pro_dict[project]['Header']['time_modify']     =time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.pro_dict[project]['Header']['comment']         =tmp_data.header['comment']
            self.pro_dict[project]['Header']['signal_sweep']    =float(tmp_data.header['bias'])             # 能量点

            x=np.linspace(0,self.pro_dict[project]['Header']['scan_range'][0],self.pro_dict[project]['Header']['scan_px'][0])-self.pro_dict[project]['Header']['scan_range'][0]/2
            y=np.linspace(0,self.pro_dict[project]['Header']['scan_range'][1],self.pro_dict[project]['Header']['scan_px'][1])-self.pro_dict[project]['Header']['scan_range'][1]/2
            Xr_tmp,Yr_tmp=np.meshgrid(x,y)
            Xr= Xr_tmp*np.cos(float(self.pro_dict[project]['Header']['scan_angle'])/180*np.pi)+Yr_tmp*np.sin(float(self.pro_dict[project]['Header']['scan_angle'])/180*np.pi)+self.pro_dict[project]['Header']['scan_center'][0]
            Yr=-Xr_tmp*np.sin(float(self.pro_dict[project]['Header']['scan_angle'])/180*np.pi)+Yr_tmp*np.cos(float(self.pro_dict[project]['Header']['scan_angle'])/180*np.pi)+self.pro_dict[project]['Header']['scan_center'][1]
            
            self.pro_dict[project]['Header']['signal_x']        =Xr.transpose(1,0)
            self.pro_dict[project]['Header']['signal_y']        =Yr.transpose(1,0)
            self.pro_dict[project]['Header']['signal_z']        =tmp_data.signals['Z']['forward']
            #sxm 独有的头函数
            self.pro_dict[project]['Header']['signal_I']        =float(tmp_data.header['z-controller>setpoint'])     #电流
            #数据，与保存格式有关，过滤掉不往里边存的
            for key in tmp_data.signals.keys():
                if key[0]=='_':
                    pass 
                else:
                    self.pro_dict[project]['Data'].update({key: tmp_data.signals[key]}) 
            
            # for key in self.pro_dict[project]['Header'].keys():
            #     print(key,'shape = ',self.pro_dict[project]['Header'][key])
            # for key in self.pro_dict[project]['Data'].keys():
            #     print(key,'shape = ',self.pro_dict[project]['Data'][key].shape)
        elif fname_ext=='.dat':
            tmp_data=read.Spec(filepath)
            #公共头文件
            for signal_sweep in tmp_data.signals.keys():
                break
            self.pro_dict[project]['Header']['sweep_signal']    =signal_sweep                                        # 当横坐标用 'Bias (V)'
            self.pro_dict[project]['Header']['scan_center']     =np.array([float(tmp_data.header['X (m)']),float(tmp_data.header['Y (m)'])])
            self.pro_dict[project]['Header']['scan_range']      =np.array([0,0])
            self.pro_dict[project]['Header']['scan_angle']      =0
            self.pro_dict[project]['Header']['scan_px']         =np.array([1,1])
            self.pro_dict[project]['Header']['sweep_points']    =len(tmp_data.signals)
            self.pro_dict[project]['Header']['channel']         ='Current (A);LI Demod 1 X (A)'
            self.pro_dict[project]['Header']['experiment_name'] =tmp_data.header['Experiment']                      # 'Grid Spectroscopy' 
            self.pro_dict[project]['Header']['time_acquire']    =tmp_data.header['Saved Date']
            self.pro_dict[project]['Header']['time_modify']     =time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.pro_dict[project]['Header']['comment']         =''
            self.pro_dict[project]['Header']['signal_sweep']    =tmp_data.signals[signal_sweep]

            self.pro_dict[project]['Header']['signal_x']        =float(tmp_data.header['X (m)'])
            self.pro_dict[project]['Header']['signal_y']        =float(tmp_data.header['Y (m)'])
            self.pro_dict[project]['Header']['signal_z']        =float(tmp_data.header['Z (m)'])
            #私有头文件
            self.pro_dict[project]['Header']['signal_sweeps']   =((len(tmp_data.signals)-1)/2-2)/2
            count=0; data_dat=np.array([])
            for key in tmp_data.signals.keys():
                if count==0:
                    data_dat=tmp_data.signals[key].copy()
                elif count==1:
                    data_dat=np.stack([data_dat,tmp_data.signals[key]],axis=1)
                else:
                    data_dat=np.concatenate([data_dat,tmp_data.signals[key][:,np.newaxis]],axis=1)
                count+=1
            if self.pro_dict[project]['Header']['signal_sweeps']==-0.5:
                self.pro_dict[project]['Header']['signal_sweeps']=1
                self.pro_dict[project]['Header']['signal_ave_I']            =data_dat[:,1]
                self.pro_dict[project]['Header']['signal_ave_Ldos']         =data_dat[:,2]
                self.pro_dict[project]['Header']['signal_I_forward']        =data_dat[:,1]
                self.pro_dict[project]['Header']['signal_I_backward']       =np.array([])
                self.pro_dict[project]['Header']['signal_Ldos_forward']     =data_dat[:,2]
                self.pro_dict[project]['Header']['signal_Ldos_backward']    =np.array([])
            elif self.pro_dict[project]['Header']['signal_sweeps']==0:
                self.pro_dict[project]['Header']['signal_sweeps']=1
                self.pro_dict[project]['Header']['signal_ave_I']            =(data_dat[:,1]+data_dat[:,3])/2
                self.pro_dict[project]['Header']['signal_ave_Ldos']         =(data_dat[:,2]+data_dat[:,4])/2
                self.pro_dict[project]['Header']['signal_I_forward']        =data_dat[:,1]
                self.pro_dict[project]['Header']['signal_I_backward']       =data_dat[:,3]
                self.pro_dict[project]['Header']['signal_Ldos_forward']     =data_dat[:,2]
                self.pro_dict[project]['Header']['signal_Ldos_backward']    =data_dat[:,4]
            else:
                num_sweep=int(self.pro_dict[project]['Header']['signal_sweeps'])
                self.pro_dict[project]['Header']['signal_ave_I']            =(data_dat[:,1]+data_dat[:,1+2*num_sweep])/2
                self.pro_dict[project]['Header']['signal_ave_Ldos']         =(data_dat[:,2]+data_dat[:,2+2*num_sweep])/2
                self.pro_dict[project]['Header']['signal_I_forward']        =data_dat[:,3:2+2*num_sweep:2]
                self.pro_dict[project]['Header']['signal_I_backward']       =data_dat[:,5+2*num_sweep:4+4*num_sweep:2]
                self.pro_dict[project]['Header']['signal_Ldos_forward']     =data_dat[:,4:3+2*num_sweep:2]
                self.pro_dict[project]['Header']['signal_Ldos_backward']    =data_dat[:,6+2*num_sweep:5+4*num_sweep:2]
            
            self.pro_dict[project]['Data']=tmp_data.signals.copy()

            for key in self.pro_dict[project]['Header'].keys():
                print(key,'shape = ',self.pro_dict[project]['Header'][key])
            for key in self.pro_dict[project]['Data'].keys():
                print(key,'shape = ',self.pro_dict[project]['Data'][key].shape)
        elif fname_ext=='.mat':
            tmp_data=scio.loadmat(filepath)
            #公共头文件
            str_channel=''
            for key in tmp_data.keys():
                if key[:2]=='__':
                    pass
                else:
                    self.pro_dict[project]['Data'].update({key:tmp_data[key].copy()})
                    if str_channel=='':
                        str_channel=key
                    else:
                        str_channel=str_channel+';'+key
            size_data=self.pro_dict[project]['Data'][key].shape
            self.pro_dict[project]['Header']['sweep_signal']    ='Bias (V)'                                        # 当横坐标用 'Bias (V)'
            self.pro_dict[project]['Header']['scan_center']     =(size_data[0]/2,size_data[1]/2)
            self.pro_dict[project]['Header']['scan_range']      =(size_data[0],size_data[1])
            self.pro_dict[project]['Header']['scan_angle']      =0
            self.pro_dict[project]['Header']['scan_px']         =(size_data[0],size_data[1])
            self.pro_dict[project]['Header']['sweep_points']    =self.pro_dict[project]['Data'][key].size/(size_data[0]*size_data[1])
            self.pro_dict[project]['Header']['channel']         =str_channel
            self.pro_dict[project]['Header']['experiment_name'] ='mat'                      # 'Grid Spectroscopy' 
            self.pro_dict[project]['Header']['time_acquire']    =time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.pro_dict[project]['Header']['time_modify']     =time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.pro_dict[project]['Header']['comment']         ='mat'
            self.pro_dict[project]['Header']['signal_sweep']    =np.linspace(1,self.pro_dict[project]['Header']['sweep_points'],int(self.pro_dict[project]['Header']['sweep_points']))
            x=np.linspace(1,self.pro_dict[project]['Header']['scan_range'][0],self.pro_dict[project]['Header']['scan_px'][0])
            y=np.linspace(1,self.pro_dict[project]['Header']['scan_range'][1],self.pro_dict[project]['Header']['scan_px'][1])
            Xr_tmp,Yr_tmp=np.meshgrid(x,y)
            self.pro_dict[project]['Header']['signal_x']        =Xr_tmp
            self.pro_dict[project]['Header']['signal_y']        =Yr_tmp
            self.pro_dict[project]['Header']['signal_z']        =np.zeros((size_data[0],size_data[1]))
            for key in self.pro_dict[project]['Header'].keys():
                print(key,'shape = ',self.pro_dict[project]['Header'][key])
            for key in self.pro_dict[project]['Data'].keys():
                print(key,'shape = ',self.pro_dict[project]['Data'][key].shape)
        else:
            pass
        print('TODO:读取完成')
        self.Signal_refreshdata.emit(self.pro_dict)

    def Signal_fun_refreshdata(self):
        self.Signal_refreshdata.emit(self.pro_dict)

class Tab_start(QWidget):
    Signal_btn=QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.ui=Ui_Tab_start()
        self.ui.setupUi(self)
        self.init_UI()
        self.settings = QSettings('.\\zjk_work\\Config\\config.ini', QSettings.IniFormat)
        self.settings.setIniCodec('UTF-8')  # 设置ini文件编码为 UTF-8
        self.init_recent()
    
    def init_UI(self):
        self.ui.btn_open_file.setCursor(QtCore.Qt.PointingHandCursor)
        self.ui.btn_open_folder.setCursor(QtCore.Qt.PointingHandCursor)
        self.ui.btn_open_file.clicked.connect(self.Slot_btn_file)
        self.ui.btn_open_folder.clicked.connect(self.Slot_btn_file)

    def init_recent(self):
        self.recentFiles=self.settings.value('FileList/recentFiles') or []
        btn_style='''
        QPushButton {	
            border: none;
            color: rgb(0,122,204);
            background-color: transparent;
            text-align : left;
        }
        QPushButton:hover {
            background-color: transparent;
        }
        QPushButton:pressed {	
            background-color: transparent;
        }
        '''
        for i,value in enumerate(self.recentFiles,start=1):
            tmp=None
            exec('self.strat_btn'+str(i)+"=QPushButton('')")
            tmp=eval('self.strat_btn'+str(i))
            tmp.setText(value)
            tmp.setStyleSheet(btn_style)
            tmp.setCursor(QtCore.Qt.PointingHandCursor)
            tmp.clicked.connect(self.Slot_btn_file)
            self.ui.verticalLayout_latest.addWidget(tmp)
        self.num_label=i                                              # 记录总共有多少个；label refresh的时候不会超

    def refresh_filelabel(self):
        self.recentFiles=self.settings.value('FileList/recentFiles') or []
        for i,value in enumerate(self.recentFiles,start=1):
            tmp=None
            if i<self.num_label:
                tmp=eval('self.strat_btn'+str(i))
                tmp.setText(value)


    def Slot_btn_file(self):
        signal_sender=self.sender()
        if signal_sender==self.ui.btn_open_file:
            self.Signal_btn.emit('open_file')
        elif signal_sender==self.ui.btn_open_folder:
            self.Signal_btn.emit('open_file')
        else:
            self.Signal_btn.emit(signal_sender.text())

class MyTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragEnterEvent):
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            for url in urls:
                self.append(url.toLocalFile())
            event.acceptProposedAction()

class MyTextEdit_mat(QTextEdit):
    '''
    只接受mat格式数据
    '''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        self.urls = event.mimeData().urls()[0] if event.mimeData().hasUrls() else ""
        try:
            self.file_path=self.urls.toLocalFile()
            event.acceptProposedAction()
        except Exception as e:
            print(e)
            event.ignore()

    def dropEvent(self, event):
        if self.file_path[-4:]=='.mat':
            mat = scio.loadmat(self.file_path)
            for key in mat.keys():
                if key[0]!='_':
                    break
            self.setText(key+' : '+str(mat[key]))
            event.acceptProposedAction()
        else:
            event.ignore()

class MyDataType():
        def __init__(self, data):
            self.data = data
            
# class MarkDownViewer(QWidget):
#     '''
#     用倒是能用,就是卡爆了,不知道为什么
#     '''
#     def __init__(self) -> None:
#         super().__init__()
#         self.initUI()
#         # 读取Markdown文件
#         with open('.\\zjk_work\\TODO_list.html', 'r', encoding='utf-8') as f:
#             html = f.read()
#         # 创建QTextEdit，并将HTML插入其中
#         self.browser.setHtml(html)

#     def initUI(self):
#         self.browser = QWebEngineView()
#         self.layout1=QVBoxLayout()
#         self.layout1.addWidget(self.browser)
#         self.setLayout(self.layout1)
        
class MyDataDictTreeWidget(QTreeWidget):
    global temp_dir
    def __init__(self):
        super().__init__()
        # self.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents) #自适应宽度
        self.setColumnCount(2)
        self.style='''
            QTreeWidget{
                background: transparent;
                border: none;
                color: white;
                font-family: "Segoe UI";
                font-size: 9pt;
            }

            QTreeView::item:selected:active{
                background: rgb(63, 147, 168);
            }
            
            QTreeView::item:selected:!active {
                background: rgb(63, 147, 168);
            }
            /*表头*/
            QHeaderView::section{
                text-align:left;
                background:transparent;
                padding:0px;
                margin:0px;
                color: rgb(170,170,170);
                padding-left: 5px;
                border-left :0.5px solid rgb(170,170,170);
                border-right:0.5px solid rgb(170,170,170);
                border-top:0px solid #000;
            }
        '''
        self.setStyleSheet(self.style)
        self.setHeaderLabels(["Name", "Value"])
        self.setDragEnabled(True)
        self.setDragDropMode(QTreeWidget.DragOnly)
        self.setSelectionMode(QTreeWidget.SingleSelection)
        
        

    def startDrag(self, supportedActions):
        # my_data_type_id = QMetaType.registerType(MyDataType)
        item = self.currentItem()
        if item is not None:
            data_type=item.data(1,QtCore.Qt.UserRole+1)
            data=item.data(0,QtCore.Qt.UserRole)
            
            print(type(data))
            # print(data)
            
            global temp_dir                             # 用全局变量存临时文件夹地址
            print(temp_dir)
            tmp_file_path=temp_dir.name+'\\s.mat'
            tmp_data={}
            tmp_data.update({'result':data})
            scio.savemat(tmp_file_path,tmp_data)
            file_url = QtCore.QUrl.fromLocalFile(tmp_file_path)
            
            mimeData = QMimeData()
            mimeData.setText(item.text(0))
            mimeData.setUrls([file_url])
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.exec_(QtCore.Qt.CopyAction)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event: QtGui.QDragLeaveEvent) -> None:  #现在不对
        print('现在离开了')
        return super().dragLeaveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasText():
            filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)")

            if filename:
                text = event.mimeData().text()
                with open(filename, "w") as f:
                    f.write(text)

                event.accept()
        else:
            event.ignore()


if __name__=='__main__':
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)                #4K屏1K屏保持一致
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())