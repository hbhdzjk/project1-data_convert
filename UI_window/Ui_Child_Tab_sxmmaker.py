# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\OneDrive\python入坟\学习ing\qt-designer\project1-slide menu\UI_window\Child_Tab_sxmmaker.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Tab_sxm(object):
    def setupUi(self, Tab_sxm):
        Tab_sxm.setObjectName("Tab_sxm")
        Tab_sxm.resize(1131, 896)
        Tab_sxm.setStyleSheet("    background-color: rgb(45, 49, 59);\n"
"\n"
"/* LINE EDIT */\n"
"QLineEdit {\n"
"    background-color: rgb(27, 29, 35);\n"
"    border-radius: 5px;\n"
"    border: 2px solid rgb(27, 29, 35);\n"
"    padding-left: 10px;\n"
"}\n"
"QLineEdit:hover {\n"
"    border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(91, 101, 124);\n"
"}\n"
"\n"
"/* SCROLL BARS */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    height: 14px;\n"
"    margin: 0px 21px 0 21px;\n"
"    border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(85, 170, 255);\n"
"    min-width: 25px;\n"
"    border-radius: 7px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"    border-top-right-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"    width: 20px;\n"
"    border-top-left-radius: 7px;\n"
"    border-bottom-left-radius: 7px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"    border: none;\n"
"    background: rgb(52, 59, 72);\n"
"    width: 14px;\n"
"    margin: 21px 0 21px 0;\n"
"    border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {    \n"
"    background: rgb(85, 170, 255);\n"
"    min-height: 25px;\n"
"    border-radius: 7px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"    border-bottom-left-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"    border: none;\n"
"    background: rgb(55, 63, 77);\n"
"     height: 20px;\n"
"    border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* CHECKBOX */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid rgb(52, 59, 72);\n"
"    border: 3px solid rgb(52, 59, 72);    \n"
"    background-image: url(:/16x16/icons/16x16/cil-check-alt.png);\n"
"}\n"
"\n"
"/* RADIO BUTTON */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid rgb(52, 59, 72);\n"
"    width: 15px;\n"
"    height: 15px;\n"
"    border-radius: 10px;\n"
"    background: rgb(44, 49, 60);\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(58, 66, 81);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid rgb(94, 106, 130);\n"
"    border: 3px solid rgb(52, 59, 72);    \n"
"}\n"
"\n"
"/* COMBOBOX */\n"
"QComboBox{\n"
"    background-color: rgb(27, 29, 35);\n"
"    border-radius: 5px;\n"
"    border: 2px solid rgb(27, 29, 35);\n"
"    padding: 5px;\n"
"    padding-left: 10px;\n"
"}\n"
"QComboBox:hover{\n"
"    border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 25px; \n"
"    border-left-width: 3px;\n"
"    border-left-color: rgba(39, 44, 54, 150);\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;    \n"
"    background-image: url(:/16x16/icons/16x16/cil-arrow-bottom.png);\n"
"    background-position: center;\n"
"    background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"    color: rgb(85, 170, 255);    \n"
"    background-color: rgb(27, 29, 35);\n"
"    padding: 10px;\n"
"    selection-background-color: rgb(39, 44, 54);\n"
"}\n"
"\n"
"/* SLIDERS */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 9px;\n"
"    height: 18px;\n"
"    margin: 0px;\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:horizontal:hover {\n"
"    background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(85, 170, 255);\n"
"    border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"    border-radius: 9px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 9px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"    background-color: rgb(55, 62, 76);\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(85, 170, 255);\n"
"    border: none;\n"
"    height: 18px;\n"
"    width: 18px;\n"
"    margin: 0px;\n"
"    border-radius: 9px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(105, 180, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(65, 130, 195);\n"
"}\n"
"\n"
"")
        self.frame_common = QtWidgets.QFrame(Tab_sxm)
        self.frame_common.setGeometry(QtCore.QRect(9, 9, 260, 195))
        self.frame_common.setMaximumSize(QtCore.QSize(300, 16777215))
        self.frame_common.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_common.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_common.setObjectName("frame_common")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_common)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame_common)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(230,230,230)")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line = QtWidgets.QFrame(self.frame_common)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtWidgets.QLabel(self.frame_common)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(230,230,230)")
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.frame_common)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet("color: rgb(230,230,230)")
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 0, 4, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.frame_common)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(230,230,230)")
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.frame_common)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(230,230,230)")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame_common)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(230,230,230)")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.frame_common)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(230,230,230)")
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame_common)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(230,230,230)")
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 2, 1, 1)
        self.value_angle = QtWidgets.QDoubleSpinBox(self.frame_common)
        self.value_angle.setStyleSheet("QDoubleSpinBox{\n"
"    background-color: transparent;\n"
"    border-radius: 3px;\n"
"    border: 1px solid rgb(64, 71, 88);\n"
"    padding-left: 4px;\n"
"    color: rgb(200,200,200);\n"
"}\n"
"QDoubleSpinBox:hover {\n"
"    border: 1px solid rgb(64, 71, 88);\n"
"}\n"
"QDoubleSpinBox:focus {\n"
"    border: 1px solid rgb(85, 170, 255);\n"
"}\n"
"QDoubleSpinBox::up-button,QSpinBox::down-button\n"
"{\n"
"    width:0px;\n"
"}")
        self.value_angle.setReadOnly(False)
        self.value_angle.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.value_angle.setMinimum(-360.0)
        self.value_angle.setMaximum(360.0)
        self.value_angle.setStepType(QtWidgets.QAbstractSpinBox.AdaptiveDecimalStepType)
        self.value_angle.setObjectName("value_angle")
        self.gridLayout.addWidget(self.value_angle, 1, 4, 1, 1)
        self.value_size_x = QtWidgets.QDoubleSpinBox(self.frame_common)
        self.value_size_x.setStyleSheet("QDoubleSpinBox{\n"
"    background-color: transparent;\n"
"    border-radius: 3px;\n"
"    border: 1px solid rgb(64, 71, 88);\n"
"    padding-left: 4px;\n"
"    color: rgb(200,200,200);\n"
"}\n"
"QDoubleSpinBox:hover {\n"
"    border: 1px solid rgb(64, 71, 88);\n"
"}\n"
"QDoubleSpinBox:focus {\n"
"    border: 1px solid rgb(85, 170, 255);\n"
"}\n"
"QDoubleSpinBox::up-button,QSpinBox::down-button\n"
"{\n"
"    width:0px;\n"
"}")
        self.value_size_x.setReadOnly(False)
        self.value_size_x.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.value_size_x.setSuffix("")
        self.value_size_x.setMinimum(-360.0)
        self.value_size_x.setMaximum(360.0)
        self.value_size_x.setStepType(QtWidgets.QAbstractSpinBox.AdaptiveDecimalStepType)
        self.value_size_x.setObjectName("value_size_x")
        self.gridLayout.addWidget(self.value_size_x, 1, 3, 1, 1)
        self.value_value_y = QtWidgets.QDoubleSpinBox(self.frame_common)
        self.value_value_y.setStyleSheet("QDoubleSpinBox{\n"
"    background-color: transparent;\n"
"    border-radius: 3px;\n"
"    border: 1px solid rgb(64, 71, 88);\n"
"    padding-left: 4px;\n"
"    color: rgb(200,200,200);\n"
"}\n"
"QDoubleSpinBox:hover {\n"
"    border: 1px solid rgb(64, 71, 88);\n"
"}\n"
"QDoubleSpinBox:focus {\n"
"    border: 1px solid rgb(85, 170, 255);\n"
"}\n"
"QDoubleSpinBox::up-button,QSpinBox::down-button\n"
"{\n"
"    width:0px;\n"
"}")
        self.value_value_y.setReadOnly(False)
        self.value_value_y.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.value_value_y.setSuffix("")
        self.value_value_y.setMinimum(-360.0)
        self.value_value_y.setMaximum(360.0)
        self.value_value_y.setStepType(QtWidgets.QAbstractSpinBox.AdaptiveDecimalStepType)
        self.value_value_y.setObjectName("value_value_y")
        self.gridLayout.addWidget(self.value_value_y, 2, 3, 1, 1)
        self.value_center_x = QtWidgets.QDoubleSpinBox(self.frame_common)
        self.value_center_x.setStyleSheet("QDoubleSpinBox{\n"
"    background-color: transparent;\n"
"    border-radius: 3px;\n"
"    border: 1px solid rgb(64, 71, 88);\n"
"    padding-left: 4px;\n"
"    color: rgb(200,200,200);\n"
"}\n"
"QDoubleSpinBox:hover {\n"
"    border: 1px solid rgb(64, 71, 88);\n"
"}\n"
"QDoubleSpinBox:focus {\n"
"    border: 1px solid rgb(85, 170, 255);\n"
"}\n"
"QDoubleSpinBox::up-button,QSpinBox::down-button\n"
"{\n"
"    width:0px;\n"
"}")
        self.value_center_x.setReadOnly(False)
        self.value_center_x.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.value_center_x.setSuffix("")
        self.value_center_x.setMinimum(-360.0)
        self.value_center_x.setMaximum(360.0)
        self.value_center_x.setStepType(QtWidgets.QAbstractSpinBox.AdaptiveDecimalStepType)
        self.value_center_x.setObjectName("value_center_x")
        self.gridLayout.addWidget(self.value_center_x, 1, 1, 1, 1)
        self.value_center_y = QtWidgets.QDoubleSpinBox(self.frame_common)
        self.value_center_y.setStyleSheet("QDoubleSpinBox{\n"
"    background-color: transparent;\n"
"    border-radius: 3px;\n"
"    border: 1px solid rgb(64, 71, 88);\n"
"    padding-left: 4px;\n"
"    color: rgb(200,200,200);\n"
"}\n"
"QDoubleSpinBox:hover {\n"
"    border: 1px solid rgb(64, 71, 88);\n"
"}\n"
"QDoubleSpinBox:focus {\n"
"    border: 1px solid rgb(85, 170, 255);\n"
"}\n"
"QDoubleSpinBox::up-button,QSpinBox::down-button\n"
"{\n"
"    width:0px;\n"
"}")
        self.value_center_y.setReadOnly(False)
        self.value_center_y.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.value_center_y.setSuffix("")
        self.value_center_y.setMinimum(-360.0)
        self.value_center_y.setMaximum(360.0)
        self.value_center_y.setStepType(QtWidgets.QAbstractSpinBox.AdaptiveDecimalStepType)
        self.value_center_y.setObjectName("value_center_y")
        self.gridLayout.addWidget(self.value_center_y, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.label_2 = QtWidgets.QLabel(self.frame_common)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(230,230,230)")
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_9 = QtWidgets.QLabel(self.frame_common)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("color: rgb(230,230,230)")
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.label_10 = QtWidgets.QLabel(self.frame_common)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color: rgb(230,230,230)")
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.value_pix_x = QtWidgets.QSpinBox(self.frame_common)
        self.value_pix_x.setStyleSheet("QSpinBox{\n"
"    background-color: transparent;\n"
"    border-radius: 3px;\n"
"    border: 1px solid rgb(64, 71, 88);\n"
"    padding-left: 4px;\n"
"    color: rgb(200,200,200);\n"
"}\n"
"QSpinBox:hover {\n"
"    border: 1px solid rgb(64, 71, 88);\n"
"}\n"
"QSpinBox:focus {\n"
"    border: 1px solid rgb(85, 170, 255);\n"
"}\n"
"QSpinBox::up-button,QSpinBox::down-button\n"
"{\n"
"    width:0px;\n"
"}")
        self.value_pix_x.setMaximum(9999)
        self.value_pix_x.setStepType(QtWidgets.QAbstractSpinBox.AdaptiveDecimalStepType)
        self.value_pix_x.setObjectName("value_pix_x")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.value_pix_x)
        self.value_pix_x_2 = QtWidgets.QSpinBox(self.frame_common)
        self.value_pix_x_2.setStyleSheet("QSpinBox{\n"
"    background-color: transparent;\n"
"    border-radius: 3px;\n"
"    border: 1px solid rgb(64, 71, 88);\n"
"    padding-left: 4px;\n"
"    color: rgb(200,200,200);\n"
"}\n"
"QSpinBox:hover {\n"
"    border: 1px solid rgb(64, 71, 88);\n"
"}\n"
"QSpinBox:focus {\n"
"    border: 1px solid rgb(85, 170, 255);\n"
"}\n"
"QSpinBox::up-button,QSpinBox::down-button\n"
"{\n"
"    width:0px;\n"
"}")
        self.value_pix_x_2.setMaximum(9999)
        self.value_pix_x_2.setStepType(QtWidgets.QAbstractSpinBox.AdaptiveDecimalStepType)
        self.value_pix_x_2.setObjectName("value_pix_x_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.value_pix_x_2)
        self.verticalLayout.addLayout(self.formLayout)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.frame_2 = QtWidgets.QFrame(Tab_sxm)
        self.frame_2.setGeometry(QtCore.QRect(9, 217, 511, 331))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.splitter = QtWidgets.QSplitter(self.frame_2)
        self.splitter.setStyleSheet("QSplitter::handle{\n"
"    border: 1px solid rgb(52, 59, 72);\n"
"    background: transparent;\n"
"    width: 1px ;\n"
"    height: 0px;\n"
"}\n"
"QSplitter::handle:hover{/*splitter->handle(1)->setAttribute(Qt::WA_Hover, true);才生效*/\n"
"    border-color: rgb(85, 170, 255);\n"
"    background:  rgb(85, 170, 255);\n"
"    width:5px;\n"
"}\n"
"QSplitter::handle:pressed{\n"
"    border-color: rgb(85, 170, 255);\n"
"    background:  rgb(85, 170, 255);\n"
"    width:5px;\n"
"}")
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_13 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("color: rgb(230,230,230)")
        self.label_13.setObjectName("label_13")
        self.verticalLayout_2.addWidget(self.label_13)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_headerchannel = QtWidgets.QVBoxLayout()
        self.verticalLayout_headerchannel.setObjectName("verticalLayout_headerchannel")
        self.horizontalLayout.addLayout(self.verticalLayout_headerchannel)
        self.verticalLayout_fuction = QtWidgets.QVBoxLayout()
        self.verticalLayout_fuction.setObjectName("verticalLayout_fuction")
        self.btn_header_new = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_header_new.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_header_new.setStyleSheet("QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_header_new.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/find/icons/find/更多_more.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_header_new.setIcon(icon)
        self.btn_header_new.setObjectName("btn_header_new")
        self.verticalLayout_fuction.addWidget(self.btn_header_new)
        self.btn_header_up = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_header_up.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_header_up.setStyleSheet("QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_header_up.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/find/icons/find/内部扩大_internal-expansion.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_header_up.setIcon(icon1)
        self.btn_header_up.setObjectName("btn_header_up")
        self.verticalLayout_fuction.addWidget(self.btn_header_up)
        self.btn_header_down = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_header_down.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_header_down.setStyleSheet("QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_header_down.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/find/icons/find/内部缩小_internal-reduction.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_header_down.setIcon(icon2)
        self.btn_header_down.setObjectName("btn_header_down")
        self.verticalLayout_fuction.addWidget(self.btn_header_down)
        self.btn_header_delete = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_header_delete.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_header_delete.setStyleSheet("QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_header_delete.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/find/icons/find/关闭_close.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_header_delete.setIcon(icon3)
        self.btn_header_delete.setObjectName("btn_header_delete")
        self.verticalLayout_fuction.addWidget(self.btn_header_delete)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_fuction.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout_fuction)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_12 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("color: rgb(230,230,230)")
        self.label_12.setObjectName("label_12")
        self.verticalLayout_3.addWidget(self.label_12)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_datachannel = QtWidgets.QVBoxLayout()
        self.verticalLayout_datachannel.setObjectName("verticalLayout_datachannel")
        self.horizontalLayout_2.addLayout(self.verticalLayout_datachannel)
        self.verticalLayout_fuction_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_fuction_2.setObjectName("verticalLayout_fuction_2")
        self.btn_data_new = QtWidgets.QPushButton(self.layoutWidget1)
        self.btn_data_new.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_data_new.setStyleSheet("QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_data_new.setText("")
        self.btn_data_new.setIcon(icon)
        self.btn_data_new.setObjectName("btn_data_new")
        self.verticalLayout_fuction_2.addWidget(self.btn_data_new)
        self.btn_data_up = QtWidgets.QPushButton(self.layoutWidget1)
        self.btn_data_up.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_data_up.setStyleSheet("QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_data_up.setText("")
        self.btn_data_up.setIcon(icon1)
        self.btn_data_up.setObjectName("btn_data_up")
        self.verticalLayout_fuction_2.addWidget(self.btn_data_up)
        self.btn_data_down = QtWidgets.QPushButton(self.layoutWidget1)
        self.btn_data_down.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_data_down.setStyleSheet("QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_data_down.setText("")
        self.btn_data_down.setIcon(icon2)
        self.btn_data_down.setObjectName("btn_data_down")
        self.verticalLayout_fuction_2.addWidget(self.btn_data_down)
        self.btn_data_delete = QtWidgets.QPushButton(self.layoutWidget1)
        self.btn_data_delete.setMaximumSize(QtCore.QSize(20, 20))
        self.btn_data_delete.setStyleSheet("QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 59, 72);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_data_delete.setText("")
        self.btn_data_delete.setIcon(icon3)
        self.btn_data_delete.setObjectName("btn_data_delete")
        self.verticalLayout_fuction_2.addWidget(self.btn_data_delete)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_fuction_2.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.verticalLayout_fuction_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_5.addWidget(self.splitter)
        self.textEdit = QtWidgets.QTextEdit(Tab_sxm)
        self.textEdit.setGeometry(QtCore.QRect(300, 40, 211, 131))
        self.textEdit.setObjectName("textEdit")
        self.data_view = ImageView(Tab_sxm)
        self.data_view.setGeometry(QtCore.QRect(530, 20, 381, 521))
        self.data_view.setObjectName("data_view")
        self.pyqtgraph_datatree = DataTreeWidget(Tab_sxm)
        self.pyqtgraph_datatree.setGeometry(QtCore.QRect(20, 560, 881, 241))
        self.pyqtgraph_datatree.setObjectName("pyqtgraph_datatree")

        self.retranslateUi(Tab_sxm)
        QtCore.QMetaObject.connectSlotsByName(Tab_sxm)

    def retranslateUi(self, Tab_sxm):
        _translate = QtCore.QCoreApplication.translate
        Tab_sxm.setWindowTitle(_translate("Tab_sxm", "Form"))
        self.label.setText(_translate("Tab_sxm", "Frame"))
        self.label_6.setText(_translate("Tab_sxm", "Yc"))
        self.label_11.setText(_translate("Tab_sxm", "Angle (°)"))
        self.label_7.setText(_translate("Tab_sxm", "W"))
        self.label_3.setText(_translate("Tab_sxm", "Center (nm)"))
        self.label_4.setText(_translate("Tab_sxm", "Size (nm)"))
        self.label_5.setText(_translate("Tab_sxm", "Xc"))
        self.label_8.setText(_translate("Tab_sxm", "H"))
        self.value_angle.setSuffix(_translate("Tab_sxm", "°"))
        self.label_2.setText(_translate("Tab_sxm", "Data Acquisition"))
        self.label_9.setText(_translate("Tab_sxm", "Pixels"))
        self.label_10.setText(_translate("Tab_sxm", "Lines"))
        self.label_13.setText(_translate("Tab_sxm", "Header"))
        self.label_12.setText(_translate("Tab_sxm", "Data"))
from pyqtgraph import DataTreeWidget, ImageView
import icon_rc
