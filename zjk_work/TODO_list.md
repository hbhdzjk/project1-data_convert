# TODO List

## 目前已知的bug
- [x] **grid 读进去x,y是反着的**
    改这个地方：
    ```py
    # reshape
    scandata_shaped = scandata.reshape(nchanns, ndir, ny, nx)

    # resize from 1d to 3d
    #TODO:不知道这样ny，nx反过来会不会有影响 linecut？？
    griddata.resize(( nx, ny,exp_size_per_pix))
    ```
    目前来看读的时候必须要ny,nx这样resize，后边header也是nx,ny,看起来没有反
    ```py
    # 这样改了一下，横纵坐标维度反过来了，不知道后续会不会有影响
    griddata=griddata.transpose(1,0,2)
    ```
    看起来后续的写入3ds格式有问题
    ```py
    #could not broadcast input array from shape (120,160) into shape (160,120)
    # 解决方法如下：
    np.meshgrid(y,x)
    point_Spec_all=point_Spec_all.transpose(1,0,2)
    ```
- [x] **grid 读linecut 保存的时候 选择->didv 只存下来了 第二个频道**
    tmd干脆加一个选项完事了
    ```py
    # 20230225 p事些多
    # 直接加了一个选项
    elif command=='3ds转换为mat->linecut':
    raw_header['savemode']='linecut'
    ```
- [ ] **grid 读进去x,y是反着的，生成的Xr,Yr矩阵跟着不对**
    改这个地方：
    ```py
    # 这个问题只存在于主程序之中需要生成Xr,Yr 但是我们好像可以通过直接读para(:,:,3)这样来避免这个问题
    Xr_tmp,Yr_tmp=np.meshgrid(y,x)
    ```
- [x] **grid写的时候不能写纯二维数据**
    ```py
    # resize from 1d to 3d
    #TODO:不知道这样ny，nx反过来会不会有影响 linecut？？
    griddata.resize(( nx, ny,exp_size_per_pix))
    ```
    改了一下write的，写的时候不会报错，但是情况比较诡异：
    1. binary 无法识别topo，didv，current，但是能看到我写进去的第六个频道
    2. wsxm 可以看我写进去的didv，current，但是看不到topo，第六个频道
    ```py
    index_n=int(raw_mat.size/size_data[0]/size_data[1])
    # 如果是二维的就补成三维的
    if index_n==1:
        raw_mat=raw_mat[:,:,np.newaxis]
    ```
    
    理论上来说应该是可以的，但是不知道是不是本身的问题
    测试了一下，sxm一个频道的就可以转成3ds(转完是两个)
    ```py
    # 如果是二维的就补成三维的
    if index_n0==1:
        raw_mat=raw_mat[:,:,np.newaxis]
        raw_mat=np.concatenate([raw_mat,raw_mat],2) 
        index_n=2
    else:
        index_n=index_n0
    ```
    
- [x] **grid读的时候不能读没有写全的数据**
    ```py
    # resize from 1d to 3d
    #TODO:不知道这样ny，nx反过来会不会有影响 linecut？？
    griddata.resize(( nx, ny,exp_size_per_pix))

    # 解决办法：
    tmp_data=np.full((nx*ny*exp_size_per_pix,),np.nan)
    tmp_data[:griddata.size]=griddata.copy()
    tmp_data.resize((  ny,nx,exp_size_per_pix))
    griddata=tmp_data.copy()
    ```

- [ ] **grid读写的时候默认读了后边带【】的，这是多个sweep的格式，[-5:]取的太多了**
    ```py
    elif self.raw_header['savemode']=='all':
        data_3ds=self.data
        tmp_data={}
        tmp_data.update({'header':data_3ds.header})
        tmp_data.update({'params':data_3ds.signals['params']})
        for key in data_3ds.signals.keys():
            if '(' in key:
                tmp_key=key[:-5]
                tmp_key=tmp_key.replace(' ','_')
                tmp_key=tmp_key.replace('[','')
                tmp_key=tmp_key.replace(']','')
                tmp_data.update({tmp_key:data_3ds.signals[key]})
        scio.savemat(fname,tmp_data)
    ```

- [x] **Scan 读不了没写完的**
    好吧其实是可以的，scan文件里自己置了nan

- [x] **Scan 读nx,ny**
    坐标旋转不对
    解决办法：
    输出的时候再旋转
    ```py
    # tmp_data2 是要准备往文件里写的
    tmp_data2=tmp_data2.transpose(1,0)
    ```
    ```matlab
    % 单个使用， 还可以标定x,y
    mesh(Z_for','EdgeColor',"none",'FaceColor',"flat"); view(2)
    % 多个使用，标定实际坐标
    mesh(Xr,Yr,Z_back,'EdgeColor',"none",'FaceColor',"flat"); view(2)
    ```
- [x] **Scan 读取之后保存mat的时候由于scan——dir和forward & backward引起的数组翻转**
    ```py
    # 涉及数组翻转的问题
    if data_sxm.header['scan_dir']=='down':
        tmp_data2=np.flip(data_sxm.signals[channel][sweep],0)
        if sweep=='forward':
            pass
        elif sweep=='backward':
            tmp_data2=np.flip(tmp_data2,1)
    elif data_sxm.header['scan_dir']=='up':
        tmp_data2=data_sxm.signals[channel][sweep]
        if sweep=='forward':
            pass
        elif sweep=='backward':
            tmp_data2=np.flip(tmp_data2,1)
    tmp_data2=tmp_data2.transpose(1,0)
    ```
- [x] **Scan 由3ds保存来的时候没有考虑最后一行（倒数第二行的换行）**
    ```py
   # 会产生list ou of range 的报错
   可能是因为没有最后一行头文件写的不对
   fn2.write(':Data Convert:\n\t ver 0.0\r\n\r\n'.encode('utf-8')) # 人为的写一项带'\n\n'进去防止读的时候[:-3],之前 ':DATA_INFO:' 是最后一项看不出来
   # 又改了一下放到前边去了，以防万一还是data info 放到最后把，加入了以下：
   elif value==':COMMENT:':
        header_sxm[i]=header_sxm[i]+'\n'+'\t\t'+''
    elif value==':Data Convert:':
        header_sxm[i]=header_sxm[i]+'\n'+'\t\t'+'Ver 0.0'
                            
    ```


## 目前还没有实现的功能
- [x] **file 选择升级成为model 并添加搜索功能**
    2023.2.26 开始升级，记录一下其中的问题：
    ```py
    # 1.filesystem model 用在tree的时候只setrootpath不行
    QString dir = QDir::currentPath();
    fmodel.setRootPath(dir); //只有这个在树形列表中不起作用。
    treeView.setRootIndex(fmodel.index(dir));  //加上这个设置才会在显示中起作用。
    # 过滤功能
    self.ui.lineEdit_file_filter.textChanged.connect(self.refresh_file_filter)
    ```
- [ ] **高级header maker**
    目前的想法是
    通过拖动data_dict 的`treewidgetitem`来将数据先保存到~~剪切板~~上再drop到控件里，


    目前实现了：
    1. 右键保存为mat
    2. 拖动可以将data-tree 中的数据通过本地缓存为mat文件，再将mat文件倒入 2023.3.15
    3.


## 目前实现的功能
### 1.sxm 读取binary保存的切片（没有backward）
### 2.sxm 直转mat

    验证了矩阵的正确性

### 3.sxm 直转3ds
    所有的频道以及 forward+backward
### 4.

## nanonis 自己的问题
1. Scan无法读带中文的文件名
2. 3ds的slice只有forward
