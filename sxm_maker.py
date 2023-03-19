#-*- coding: utf-8 -*
import os,sys
sys.path.append("./UI_window/")
import scipy.io as scio
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QSettings,QMimeData,QVariant,Qt)
from PyQt5.QtGui import (QDragEnterEvent,QDropEvent,QDrag)
from PyQt5.QtWidgets import *
from UI_window.Ui_Child_Tab_sxmmaker import *

class Tab_Sxmmaker(QWidget):
    Signal_btn=QtCore.pyqtSignal(str)
    Signal_move_header_item=QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.ui=Ui_Tab_sxm()
        self.ui.setupUi(self)
        self.init_UI()
    
    def init_UI(self):
        # 处理header中的额外词条框架
        self.header_tree=Sxm_header_tree()                                                              # 创建header中的额外词条框架
        self.ui.verticalLayout_headerchannel.addWidget(self.header_tree)                                # 添加自定义框架
        self.ui.btn_header_delete.clicked.connect(self.deleteItem)                                      # signal 链接删除item
        self.ui.btn_header_new.clicked.connect(self.on_Newheader_item)                                  # signal 链接新建item
        self.Signal_move_header_item.connect(self.header_tree.move_item)                                # 设置上下键的信号直接发到控件的累里去处理
        self.ui.btn_header_up.clicked.connect(lambda: self.Signal_move_header_item.emit('up'))          # 设置上下键的信号直接发到控件的累里去处理
        self.ui.btn_header_down.clicked.connect(lambda: self.Signal_move_header_item.emit('down'))      # 设置下键的信号直接发到控件的累里去处理
        # 处理Data
        self.data_tree=Sxm_data_tree()                                                                  # 创建header中的额外词条框架
        self.ui.verticalLayout_datachannel.addWidget(self.data_tree)                                    # 添加自定义框架
        self.ui.btn_data_delete.clicked.connect(self.deleteItem)                                        # signal 链接删除item
        self.ui.btn_data_new.clicked.connect(self.on_Newheader_item)                                    # signal 链接新建item
        self.Signal_move_header_item.connect(self.data_tree.move_item)                                  # 设置上下键的信号直接发到控件的累里去处理
        self.ui.btn_data_up.clicked.connect(lambda: self.Signal_move_header_item.emit('up'))            # 设置上下键的信号直接发到控件的累里去处理
        self.ui.btn_data_down.clicked.connect(lambda: self.Signal_move_header_item.emit('down'))        # 设置下键的信号直接发到控件的累里去处理
        self.data_tree.Signal_data_change.connect(self.Slot_change_currentdata)
    # 删除控件树子节点/根节点
    def deleteItem(self):
        try:
            # 尝试删除子节点（通过其父节点，调用removeChild函数进行删除）
            if self.sender().objectName()=='btn_header_delete':
                currNode = self.header_tree.currentItem()
            elif self.sender().objectName()=='btn_data_delete':
                currNode = self.data_tree.currentItem()
            parent1 = currNode.parent()
            parent1.removeChild(currNode)
        except Exception:
            # 遇到异常时删除根节点
            try:
                if self.sender().objectName()=='btn_header_delete':
                    rootIndex = self.header_tree.indexOfTopLevelItem(currNode)
                    self.header_tree.takeTopLevelItem(rootIndex)
                elif self.sender().objectName()=='btn_data_delete':
                    rootIndex = self.data_tree.indexOfTopLevelItem(currNode)
                    self.data_tree.takeTopLevelItem(rootIndex)
                
                
            except Exception:
                print(Exception)
                
    def on_Newheader_item(self):
        if self.sender().objectName()=='btn_header_new':
            item=QTreeWidgetItem(self.header_tree)
            item.setText(0,'New item')
            item.setText(1,'New Value')
            self.header_tree.setCurrentItem(item)
            self.header_tree.onDoubleClick()
        elif self.sender().objectName()=='btn_data_new':
            print('TODO')
 
    def Slot_change_currentdata(self,temp_dict):
        self.current_data:np.ndarray=temp_dict['current_data']
        self.current_data_text=temp_dict['current_data']
        self.ui.pyqtgraph_datatree.setData(temp_dict)
        try:
            temp_data=self.current_data
            if temp_data.size/temp_data.shape[0]/temp_data.shape[1]==1:
                pass
            elif temp_data.size/temp_data.shape[0]/temp_data.shape[1]>1:
                temp_data=temp_data.transpose(2,0,1)
            self.ui.data_view.clear()
            self.ui.data_view.setImage(img=temp_data)
        except Exception as e:
            print(e)
 
class Sxm_data_tree(QTreeWidget):
    Signal_data_change=QtCore.pyqtSignal(dict)
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
        self.setHeaderLabels(["Channel", "Size"])
        # 拖拽设置
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QTreeWidget.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setSelectionMode(QTreeWidget.SingleSelection)
        self.doubleClicked.connect(self.onDoubleClick)
        
        self.item1=QTreeWidgetItem(self)
        self.item1.setText(0,'1')
        # self.item1.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable| QtCore.Qt.ItemIsDragEnabled| QtCore.Qt.ItemIsDropEnabled )  # 设为可编辑

        self.item2=QTreeWidgetItem(self)
        self.item2.setText(0,'2')
        # self.item2.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled| QtCore.Qt.ItemIsDropEnabled)  # 设为可编辑
        
    def onDoubleClick(self):
        item=self.currentItem()
        name=item.text(0)
        value=item.text(1)
        temp_data=item.data(0,QtCore.Qt.UserRole)
        self.Signal_data_change.emit({'current_data':temp_data,'current_item':item,'current_item_name':name})
        
        # dialog=MultiInputDialog(name,value)
        # if dialog.exec():
        #     tmp_name,tmp_value=dialog.get_data()
        #     if tmp_name:
        #         name=tmp_name
        #     if tmp_value:
        #         value=tmp_value
        # item.setText(0,name)
        # item.setText(1,value)
        
        
    def move_item(self,switch):
        try:
            # 获取一个列表关于treewidget的根节点，作为缓存，然后删除treewidget重新添加
            tree_list_name=[]
            tree_list_value=[]
            index=self.currentIndex()
            index_row=self.currentIndex().row()
            root=self.invisibleRootItem()
            root_child_count=root.childCount()
            for i in range(root_child_count):
                tree_list_name.append(root.child(i).text(0))
                tree_list_value.append(root.child(i).text(1))    
            temp_name=root.child(index_row).text(0)
            temp_value=root.child(index_row).text(1)
            tree_list_name.pop(index_row)
            tree_list_value.pop(index_row)
            if switch=='up':
                tree_list_name.insert(index_row-1,temp_name)
                tree_list_value.insert(index_row-1,temp_value)
            elif switch=='down':    
                tree_list_name.insert(index_row+1,temp_name)
                tree_list_value.insert(index_row+1,temp_value)
            # 重新添加item
            self.clear()
            for i in range(root_child_count):
                item=QTreeWidgetItem(self)
                item.setText(0,tree_list_name[i])
                item.setText(1,tree_list_value[i])
            model=self.model()
            # 把current选中放到这里
            if switch=='up':
                this_index=model.index(index_row-1,0,self.rootIndex())
                self.setCurrentIndex(this_index)
            elif switch=='down':    
                this_index=model.index(index_row+1,0,self.rootIndex())
                self.setCurrentIndex(this_index)
        except Exception as e:
            # 没有选择item即没有currentIndex()的时候不会触发
            print(e)    
            
            
    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Up and event.modifiers() == QtCore.Qt.ControlModifier:
            self.move_item('up')
        if event.key() == QtCore.Qt.Key_Down and event.modifiers() == QtCore.Qt.ControlModifier:
            self.move_item('down')
        if event.key() == QtCore.Qt.Key_Delete:
            try:
                # 尝试删除子节点（通过其父节点，调用removeChild函数进行删除）
                currNode = self.currentItem()
                parent1 = currNode.parent()
                parent1.removeChild(currNode)
            except Exception:
                # 遇到异常时删除根节点
                try:
                    rootIndex = self.indexOfTopLevelItem(currNode)
                    self.takeTopLevelItem(rootIndex)
                except Exception:
                    print(Exception)
            return super().keyPressEvent(event)    
    def dragEnterEvent(self, event):
        '''
        1.可以接受.mat 文件: 拥有 event.mimeData().urls()[0] & event.mimeData().text()
            两种来源:  1) 本地文件
                      2) data tree 
        '''
        self.urls = event.mimeData().urls()[0] if event.mimeData().hasUrls() else ""
        self.mimedata_text=event.mimeData().text() if event.mimeData().hasText() else ""
        try:
            # 1. 拥有urls并且文件格式为'.mat' 取第一个
            if event.mimeData().hasUrls() and self.urls.toLocalFile()[-4:]=='.mat':
                self.file_path=self.urls.toLocalFile()
                mat = scio.loadmat(self.file_path)
                for key in mat.keys():
                    if key[0]!='_':
                        break
                self.drop_temp_value=mat[key]
                # 1) 本地文件
                if self.mimedata_text.startswith('file:///'):
                    # self.drop_temp_name=os.path.basename(self.file_path)
                    self.drop_temp_name=key
                # 2) data tree view 文件
                else: 
                    self.drop_temp_name=self.mimedata_text
            elif (not event.mimeData().hasUrls()) and event.mimeData().hasText():
                event.ignore()
            else:
                event.ignore()
            event.acceptProposedAction()
            
        except Exception as e:
            print(e)
            event.ignore()
    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        if event.mimeData().hasText():
            event.accept()
    def dropEvent(self, event: QtGui.QDragMoveEvent):
        try:
            if self.drop_temp_name!=None and self.drop_temp_value.all()!=None:
                if isinstance(self.drop_temp_value, type(np.array([]))):
                    item=QTreeWidgetItem(self)
                    item.setData(0, QtCore.Qt.UserRole, QVariant(self.drop_temp_value))
                    item.setData(1, QtCore.Qt.UserRole+1, QVariant('numpy'))
                    item.setText(0,self.drop_temp_name)
                    item.setText(1, str(self.drop_temp_value.shape))
                    item.setToolTip(1, str(self.drop_temp_value))
                    event.acceptProposedAction()
                    self.drop_temp_name,self.drop_temp_value=None,None
        except Exception as e:
            print(e)
            event.ignore()

 
    
class Sxm_header_tree(QTreeWidget):

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
        # 拖拽设置
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QTreeWidget.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.setSelectionMode(QTreeWidget.SingleSelection)
        self.doubleClicked.connect(self.onDoubleClick)
        
        self.item1=QTreeWidgetItem(self)
        self.item1.setText(0,'1')
        # self.item1.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable| QtCore.Qt.ItemIsDragEnabled| QtCore.Qt.ItemIsDropEnabled )  # 设为可编辑

        self.item2=QTreeWidgetItem(self)
        self.item2.setText(0,'2')
        # self.item2.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsDragEnabled| QtCore.Qt.ItemIsDropEnabled)  # 设为可编辑
        
    def onDoubleClick(self):
        item=self.currentItem()
        # self.get_current_index()
        name=item.text(0)
        value=item.text(1)
        dialog=MultiInputDialog(name,value)
        if dialog.exec():
            tmp_name,tmp_value=dialog.get_data()
            if tmp_name:
                name=tmp_name
            if tmp_value:
                value=tmp_value
        item.setText(0,name)
        item.setText(1,value)
        
        
            
    # def get_current_index(self):
    #     index=self.currentIndex()
    #     # item=self.curr
    #     print(index.row())
        
    def move_item(self,switch):
        try:
            # 获取一个列表关于treewidget的根节点，作为缓存，然后删除treewidget重新添加
            tree_list_name=[]
            tree_list_value=[]
            index=self.currentIndex()
            index_row=self.currentIndex().row()
            root=self.invisibleRootItem()
            root_child_count=root.childCount()
            for i in range(root_child_count):
                tree_list_name.append(root.child(i).text(0))
                tree_list_value.append(root.child(i).text(1))    
            temp_name=root.child(index_row).text(0)
            temp_value=root.child(index_row).text(1)
            tree_list_name.pop(index_row)
            tree_list_value.pop(index_row)
            if switch=='up':
                tree_list_name.insert(index_row-1,temp_name)
                tree_list_value.insert(index_row-1,temp_value)
            elif switch=='down':    
                tree_list_name.insert(index_row+1,temp_name)
                tree_list_value.insert(index_row+1,temp_value)
            # 重新添加item
            self.clear()
            for i in range(root_child_count):
                item=QTreeWidgetItem(self)
                item.setText(0,tree_list_name[i])
                item.setText(1,tree_list_value[i])
            model=self.model()
            # 把current选中放到这里
            if switch=='up':
                this_index=model.index(index_row-1,0,self.rootIndex())
                self.setCurrentIndex(this_index)
            elif switch=='down':    
                this_index=model.index(index_row+1,0,self.rootIndex())
                self.setCurrentIndex(this_index)
        except Exception as e:
            # 没有选择item即没有currentIndex()的时候不会触发
            print(e)    
            
            
    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key_Up and event.modifiers() == QtCore.Qt.ControlModifier:
            self.move_item('up')
        if event.key() == QtCore.Qt.Key_Down and event.modifiers() == QtCore.Qt.ControlModifier:
            self.move_item('down')
        if event.key() == QtCore.Qt.Key_Delete:
            try:
                # 尝试删除子节点（通过其父节点，调用removeChild函数进行删除）
                currNode = self.currentItem()
                parent1 = currNode.parent()
                parent1.removeChild(currNode)
            except Exception:
                # 遇到异常时删除根节点
                try:
                    rootIndex = self.indexOfTopLevelItem(currNode)
                    self.takeTopLevelItem(rootIndex)
                except Exception:
                    print(Exception)
        return super().keyPressEvent(event)    
    def dragEnterEvent(self, event):
        '''
        1.可以接受.mat 文件: 拥有 event.mimeData().urls()[0] & event.mimeData().text()
            两种来源:  1) 本地文件
                      2) data tree 
        2.可以接受纯文本信息: 只有 event.mimeData().text()
        '''
        self.urls = event.mimeData().urls()[0] if event.mimeData().hasUrls() else ""
        self.mimedata_text=event.mimeData().text() if event.mimeData().hasText() else ""
        try:
            # 1. 拥有urls并且文件格式为'.mat' 取第一个
            if event.mimeData().hasUrls() and self.urls.toLocalFile()[-4:]=='.mat':
                self.file_path=self.urls.toLocalFile()
                mat = scio.loadmat(self.file_path)
                for key in mat.keys():
                    if key[0]!='_':
                        break
                self.drop_temp_value=str(mat[key])
                # 1) 本地文件
                if self.mimedata_text.startswith('file:///'):
                    self.drop_temp_name=os.path.basename(self.file_path)
                # 2) data tree view 文件
                else: 
                    self.drop_temp_name=self.mimedata_text
            elif (not event.mimeData().hasUrls()) and event.mimeData().hasText():
                self.drop_temp_name=self.mimedata_text
                self.drop_temp_value=self.mimedata_text
            else:
                event.ignore()
            event.acceptProposedAction()
            
        except Exception as e:
            print(e)
            event.ignore()
    def dragMoveEvent(self, event: QtGui.QDragMoveEvent) -> None:
        if event.mimeData().hasText():
            event.accept()
    def dropEvent(self, event: QtGui.QDragMoveEvent):
        try:
            if self.drop_temp_name and self.drop_temp_value:
                item=QTreeWidgetItem(self)
                item.setText(0,self.drop_temp_name)
                item.setText(1,self.drop_temp_value)
                self.drop_temp_name,self.drop_temp_value=None,None
                event.acceptProposedAction()
            # event.mimeData.clear()
        except Exception as e:
            print(e)
            event.ignore()
    
    
class MultiInputDialog(QDialog):
    '''
    继承自QDialog的自定义多输入dialog
        开始的时候初始化两个值分别为原始的name和value
        然后需要在唤起的时候 1.赋值 2.设置如下格式接受返回数据
        if dialog.exec():
            tmp_name,tmp_value=dialog.get_data()
    '''
    def __init__(self,lineedit_value1,lineedit_value2) -> None:
        super().__init__()
        self.form1=QFormLayout(self)
        self.label_top=QLabel('User Input')
        self.form1.addRow(self.label_top)
        # 添加主体
        self.label_1=QLabel('Name: ')
        self.label_2=QLabel('Value: ')
        self.lineedit_1=QLineEdit(lineedit_value1)
        self.lineedit_2=QTextEdit(lineedit_value2)
        self.form1.addRow('Name',self.lineedit_1)
        self.form1.addRow(self.label_2,self.lineedit_2)
        # 添加button
        self.button=QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel )
        self.button.accepted.connect(self.accept)
        self.button.rejected.connect(self.reject)
        self.form1.addRow(self.button)
        self.show()
        
    def get_data(self):
        return self.lineedit_1.text() , self.lineedit_2.toPlainText()
           
    
if __name__=='__main__':
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)                #4K屏1K屏保持一致
    app = QApplication(sys.argv)
    window = Tab_Sxmmaker()
    window.show()
    sys.exit(app.exec_())
