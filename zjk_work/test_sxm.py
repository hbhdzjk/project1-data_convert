import scipy.io as scio
import numpy as np
import sys,os
import pytest
from nanonispy_zjk import read
'''
本模块测试 Sxm相关功能
'''
fn_sxm_normal=r"E:\OneDrive\python入坟\学习ing\qt-designer\data_test\NAS-066.sxm"
fn_sxm_rectangle=r"E:\OneDrive\python入坟\学习ing\qt-designer\data_test\不完整非对称\1999.sxm"
fn_sxm_incomplete=r"E:\OneDrive\python入坟\学习ing\qt-designer\data_test\不完整非对称\1001.sxm"


import pytest

class Test_only_read(object):

    def test_normal(self):
        fn_sxm_normal='..\\data_test\\NAS-066.sxm'
        fn=fn_sxm_normal
        data_sxm=read.Scan(fn)
        pass
        assert isinstance(data_sxm.signals['Z']['forward'],type(np.ndarray([])))
        assert data_sxm.signals['Z']['forward'].shape==(256,256)

    def test_imcomplete(self):
        fn_sxm_incomplete='..\\data_test\\不完整非对称\\1001.sxm'
        fn=fn_sxm_incomplete
        data_sxm=read.Scan(fn)
        pass
        assert isinstance(data_sxm.signals['Z']['forward'],type(np.ndarray([])))
        assert data_sxm.signals['Z']['forward'].shape==(256,256)

    def test_rectangle(self):
        '''
        原始矩阵大小1280*512
        '''
        fn_sxm_rectangle='..\\data_test\\不完整非对称\\1999.sxm'
        fn=fn_sxm_rectangle
        data_sxm=read.Scan(fn)
        pass
        assert isinstance(data_sxm.signals['Z']['forward'],type(np.ndarray([])))
        assert data_sxm.signals['Z']['forward'].shape==(512,1280)

class Test_read_and_write(object):
    '''
    sxm->mat
    '''
    def test_normal(self):
        fn_sxm_normal='..\\data_test\\NAS-066.sxm'
        fn=fn_sxm_normal
        data_sxm=read.Scan(fn)
        
        raw_header={}
        fname='temp.mat'
        raw_header['savepath']=fname
        read.Write(data_sxm,raw_header,'sxm','mat')
        
        mat=scio.loadmat(fname)
        
        pass
        assert isinstance(mat['Z_for'],type(np.ndarray([])))
        assert mat['Z_for'].shape==(256,256)
        
    def test_rectangle(self):
        fn_sxm_rectangle='..\\data_test\\不完整非对称\\1999.sxm'
        fn=fn_sxm_rectangle
        data_sxm=read.Scan(fn)
        
        raw_header={}
        fname='temp.mat'
        raw_header['savepath']=fname
        read.Write(data_sxm,raw_header,'sxm','mat')
        
        mat=scio.loadmat(fname)
        
        pass
        assert isinstance(mat['Z_for'],type(np.ndarray([])))
        assert mat['Z_for'].shape==(1280,512)
        
    def test_imcomplete(self):
        fn_sxm_incomplete='..\\data_test\\不完整非对称\\1001.sxm'
        fn=fn_sxm_incomplete
        data_sxm=read.Scan(fn)
        
        raw_header={}
        fname='temp.mat'
        raw_header['savepath']=fname
        read.Write(data_sxm,raw_header,'sxm','mat')
        
        mat=scio.loadmat(fname)
        
        pass
        assert isinstance(mat['Z_for'],type(np.ndarray([])))
        assert mat['Z_for'].shape==(256,256)
    '''
    sxm->3ds
    '''
    def test_imcomplete_3ds(self):
        fn_sxm_incomplete='..\\data_test\\不完整非对称\\1001.sxm'
        fn=fn_sxm_incomplete
        data_sxm=read.Scan(fn)
        
        raw_header={}
        fname='temp.3ds'
        raw_header['savepath']=fname
        raw_header['header']=data_sxm.header
        read.Write(data_sxm.signals,raw_header,'sxm','3ds')
        
        temp=read.Grid(fname)
        
        pass
        assert isinstance(temp.signals['LI Demod 1 X (A)'],type(np.ndarray([])))
        assert temp.signals['LI Demod 1 X (A)'].shape==(256,256,6)
    
    def test_rectangle_3ds(self):
        fn_sxm_rectangle='..\\data_test\\不完整非对称\\1999.sxm'
        fn=fn_sxm_rectangle
        data_sxm=read.Scan(fn)
        for key in data_sxm.signals.keys():
            assert isinstance(data_sxm.signals[key]['forward'],type(np.ndarray([])))
            assert isinstance(data_sxm.signals[key]['backward'],type(np.ndarray([])))
            assert data_sxm.signals[key]['forward'].shape==(512,1280)
            assert data_sxm.signals[key]['backward'].shape==(512,1280)
        
        raw_header={}
        fname='temp.3ds'
        raw_header['savepath']=fname
        raw_header['header']=data_sxm.header
        read.Write(data_sxm.signals,raw_header,'sxm','3ds')
        temp=read.Grid(fname)
        assert isinstance(temp.signals['LI Demod 1 X (A)'],type(np.ndarray([])))
        assert temp.signals['LI Demod 1 X (A)'].shape==(1280,512,6)
        
        data_3ds=temp
        raw_header={}
        raw_header['savepath']='temp.sxm'
        read.Write(data_3ds,raw_header,'3ds','sxm')
        data_sxm=read.Scan('temp.sxm')
        for key in data_sxm.signals.keys():
            assert isinstance(data_sxm.signals[key]['forward'],type(np.ndarray([])))
            assert isinstance(data_sxm.signals[key]['backward'],type(np.ndarray([])))
            assert data_sxm.signals[key]['forward'].shape==(512,1280)
            assert data_sxm.signals[key]['backward'].shape==(512,1280)
    
    # 二维数组成为3ds文件和sxm文件 
    def test_2D_mat(self):
        fn_mat='..\\data_test\\不完整非对称\\二维数组.mat'
        fn=fn_mat
        data_mat=scio.loadmat(fn)
        for key in data_mat.keys():
            if not key[0]=='_':
                raw_data=data_mat[key]
                break
        assert isinstance(raw_data,type(np.ndarray([])))
        assert raw_data.shape==(256,256)
        
        raw_header={}
        fname='temp.sxm'
        raw_header['savepath']=fname
        read.Write(data_mat,raw_header,'mat','sxm')
        data_sxm=read.Scan(fname)
        
        for key in data_sxm.signals.keys():
            assert isinstance(data_sxm.signals[key]['forward'],type(np.ndarray([])))
            assert isinstance(data_sxm.signals[key]['backward'],type(np.ndarray([])))
            assert data_sxm.signals[key]['forward'].shape==(256,256)
            assert data_sxm.signals[key]['backward'].shape==(256,256)
        
        raw_header={}
        fname='temp.3ds'
        raw_header['savepath']=fname
        tmp=read.Write(data_mat,raw_header,'mat','3ds')
        data_3ds=read.Grid(fname)
        assert data_3ds.signals['LI Demod 1 X (A)'].shape==(256, 256, 2)
        
      
    
if __name__ == '__main__':
    pytest.main(['-s'])