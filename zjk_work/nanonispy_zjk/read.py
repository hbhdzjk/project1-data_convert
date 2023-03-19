import os,sys
import socket
import re
import struct
import warnings
import time
import numpy as np
import scipy.io as scio
from .constants import nanonis_format_dict, nanonis_end_tags

class NanonisFile:

    """
    Base class for Nanonis data files (grid, scan, point spectroscopy).

    Handles methods and parsing tasks common to all Nanonis files.

    Parameters
    ----------
    fname : str
        Name of Nanonis file.

    Attributes
    ----------
    datadir : str
        Directory path for Nanonis file.
    basename : str
        Just the filename, no path.
    fname : str
        Full path of Nanonis file.
    filetype : str
        filetype corresponding to filename extension.
    byte_offset : int
        Size of header in bytes.
    header_raw : str
        Unproccessed header information.
    """

    def __init__(self, fname):
        _data_format = nanonis_format_dict
        self.datadir, self.basename = os.path.split(fname)    #分割成文件名和路径
        self.fname = fname
        self.filetype = self._determine_filetype()
        self.byte_offset = self.start_byte()
        self.header_raw = self.read_raw_header(self.byte_offset)
       

    def _determine_filetype(self):
        """
        Check last three characters for appropriate file extension,
        raise error if not.

        Returns
        -------
        str
            Filetype name associated with extension.

        Raises
        ------
        UnhandledFileError
            If last three characters of filename are not one of '3ds',
            'sxm', or 'dat'.
        """

        _, fname_ext = os.path.splitext(self.fname)
        if fname_ext == '.3ds':
            return 'grid'
        elif fname_ext == '.sxm':
            return 'scan'
        elif fname_ext == '.dat':
            return 'spec'
        else:
            raise UnhandledFileError('{} is not a supported filetype or does not exist'.format(self.basename))

    def read_raw_header(self, byte_offset):
        """
        Return header as a raw string.

        Everything before the end tag is considered to be part of the header.
        the parsing will be done later by subclass methods.

        Parameters
        ----------
        byte_offset : int
            Size of header in bytes. Read up to this point in file.

        Returns
        -------
        str
            Contents of filename up to byte_offset as a decoded binary
            string.
        """

        with open(self.fname, 'rb') as f:
            return f.read(byte_offset).decode('utf-8', errors='replace')

    def start_byte(self):
        """
        Find first byte after end tag signalling end of header info.

        Caveat, I believe this is the first byte after the end of the
        line that the end tag is found on, not strictly the first byte
        directly after the end tag is found. For example in Scan
        __init__, byte_offset is incremented by 4 to account for a
        'start' byte that is not actual data.

        Returns
        -------
        int
            Size of header in bytes.
        """

        with open(self.fname, 'rb') as f:
            tag = nanonis_end_tags[self.filetype]

            # Set to a default value to know if end_tag wasn't found
            byte_offset = -1

            for line in f:
                # Convert from bytes to str
                try:
                    entry = line.strip().decode()
                except UnicodeDecodeError:
                    warnings.warn('{} has non-uft-8 characters, replacing them.'.format(f.name))
                    entry = line.strip().decode('utf-8', errors='replace')
                if tag in entry:
                    byte_offset = f.tell()
                    break

            if byte_offset == -1:
                raise FileHeaderNotFoundError(
                        'Could not find the {} end tag in {}'.format(tag, self.basename)
                        )

        return byte_offset

    def set_data_format(self, data_format):
        # default value is '>f4' big endian float 32 bit
        if data_format is None:
            self.data_format = nanonis_format_dict['big endian float 32']
        else:
            try:
                self.data_format = nanonis_format_dict[data_format]
            except KeyError as exc:
                self.data_format = nanonis_format_dict['big endian float 32']
                warnings.warn('{} is not a valid data format'.format(data_format))

class Grid(NanonisFile):

    """
    Nanonis grid file class.

    Contains data loading method specific to Nanonis grid file. Nanonis
    3ds files contain a header terminated by '\r\n:HEADER_END:\r\n'
    line, after which big endian encoded binary data starts. A grid is
    always recorded in an 'up' direction, and data is recorded
    sequentially starting from the first pixel. The number of bytes
    corresponding to a single pixel will depend on the experiment
    parameters. In general the size of one pixel will be a sum of

        - # fixed parameters
        - # experimental parameters
        - # sweep signal points (typically bias).

    Hence if there are 2 fixed parameters, 8 experimental parameters,
    and a 512 point bias sweep, a pixel will account 4 x (522) = 2088
    bytes of data. The class intuits this from header info and extracts
    the data for you and cuts it up into each channel, though normally
    this should be just the current.

    Currently cannot accept grids that are incomplete._is_valid_file

    Parameters
    ----------
    fname : str
        Filename for grid file.
    header_override : dict, optional
        A dict of key:value to override any corresponding key:value should
        they be wrong or missing in your header. Keys in header_override must
        match keys in Grid.header_raw.

    Attributes
    ----------
    header : dict
        Parsed 3ds header. Relevant fields are converted to float,
        otherwise most are string values.
    signals : dict
        Dict keys correspond to channel name, with values being the
        corresponding data array.

    Raises
    ------
    UnhandledFileError
        If fname does not have a '.3ds' extension.
    """

    def __init__(self, fname, header_override=None, data_format=None):
        _is_valid_file(fname, ext='3ds')
        super().__init__(fname)
        self.set_data_format(data_format)
        self.header = _parse_3ds_header(self.header_raw, header_override=header_override)
        self.signals = self._load_data()
        self.signals['_sweep_signal'] = self._derive_sweep_signal()
        self.signals['_bias'] = self._derive_sweep_signal()
        #脑子多少有点问题 不知道注释掉会不会有影响
        self.signals['_topo'] = self._extract_topo()
        
        # #TODO:内置一个header
        # self.inner_header_linear=[\
        #     'Grid dim="200 x 200"',
        #     'Grid settings=-4.948263E-7;-9.410877E-8;8.000000E-8;8.000000E-8;0.000000E+0', 
        #     'Filetype=Linear', 
        #     'Sweep Signal="Bias (V)"',
        #     'Fixed parameters="Sweep Start;Sweep End"',
        #     'Experiment parameters="X (m);Y (m);Z (m);Z offset (m);Settling time (s);Integration time (s);Z-Ctrl hold;Final Z (m);Scan:Current (A);Scan:Z (m);Scan:OC D1 Amplitude (m);Scan:OC M1 Freq. Shift (Hz);Scan:OC M1 Excitation (V)"',
        #     '# Parameters (4 byte)=15',
        #     'Experiment size (bytes)=144',
        #     'Points=18',
        #     'Channels="Current (A);LI Demod 1 X (A)"',
        #     'Delay before measuring (s)=0.000000E+0', 
        #     'Experiment="Grid Spectroscopy"', 
        #     'Start time="24.10.2021 20:44:06"',
        #     'End time="25.10.2021 13:53:46"', 
        #     'User=', 
        #     'Comment="100p 20m 30 30"'\
        #         ]
        # self.inner_header_MLS=[\
        #     'Grid dim="250 x 250"', 
        #     'Grid settings=5.610386E-7;-5.252778E-7;1.000000E-7;1.000000E-7;0.000000E+0', 
        #     'Filetype=MLS', 'Sweep Signal="Bias (V)"', 
        #     'Fixed parameters="Sweep Start;Sweep End"', 
        #     'Experiment parameters="X (m);Y (m);Z (m);Z offset (m);Z-Ctrl hold;Final Z (m);Scan:Current (A);Scan:Z (m);Scan:OC D1 Amplitude (m);Scan:OC M1 Freq. Shift (Hz);Scan:OC M1 Excitation (V)"', 
        #     '# Parameters (4 byte)=13', 
        #     'Segment Start (V), Segment End (V), Settling (s), Integration (s), Steps (xn), Lockin, Init. Settling (s)=300E-3,0E+0,10E-3,100E-3,30,0E+0,0E+0;0E+0,-500E-3,10E-3,100E-3,10,0E+0,0E+0', 
        #     'Experiment size (bytes)=624', 
        #     'Points=39', 
        #     'Channels="Current [AVG] (A);LI Demod 1 X [AVG] (A);Current [00001] (A);LI Demod 1 X [00001] (A)"', 
        #     'Delay before measuring (s)=0.000000E+0', 
        #     'Experiment="Grid Spectroscopy"', 
        #     'Start time="28.08.2021 23:32:35"', 
        #     'End time="01.09.2021 23:32:03"', 
        #     'User=', 'Date="26.08.2021 10:17:20"', 
        #     'Comment="300m 100p10mv modu"'\
        #         ]
        #其实存的是header_entery
        
    def _load_data(self):
        """
        Read binary data for Nanonis 3ds file.

        Returns
        -------
        dict
            Channel name keyed dict of 3d array.
        """
        # load grid params
        nx, ny = self.header['dim_px']
        num_sweep = self.header['num_sweep_signal']
        num_param = self.header['num_parameters']
        num_chan = self.header['num_channels']
        data_dict = dict()

        # open and seek to start of data
        f = open(self.fname, 'rb')
        f.seek(self.byte_offset)
        data_format = self.data_format
        griddata = np.fromfile(f, dtype=data_format)
        f.close()

        # pixel size in bytes
        exp_size_per_pix = num_param + num_sweep*num_chan

        # resize from 1d to 3d
        #TODO:不知道这样ny，nx反过来会不会有影响 linecut？？
        
        # if griddata.size<nx*ny*exp_size_per_pix:
        tmp_data=np.full((nx*ny*exp_size_per_pix,),np.nan)
        tmp_data[:griddata.size]=griddata.copy()
        tmp_data.resize((  ny,nx,exp_size_per_pix))
        griddata=tmp_data.copy()
        # elif griddata.size<nx*ny*exp_size_per_pix:
        #     griddata.resize((  ny,nx,exp_size_per_pix))
        griddata=griddata.transpose(1,0,2)

        # experimental parameters are first num_param of every pixel
        params = griddata[:, :, :num_param]
        data_dict['params'] = params

        # extract data for each channel
        for i, chann in enumerate(self.header['channels']):
            start_ind = num_param + i * num_sweep
            stop_ind = num_param + (i+1) * num_sweep
            data_dict[chann] = griddata[:, :, start_ind:stop_ind]

        return data_dict 

    def _derive_sweep_signal(self):
        #这个可能需要大改
        """
        Computer sweep signal.

        Based on start and stop points of sweep signal in header, and
        number of sweep signal points.

        Returns
        -------
        numpy.ndarray
            1d sweep signal, should be sample bias in most cases.
            
        Rnm,tq zhixielexianxingqingkuang    
        
        """
        #Linear
        if self.header['filetype']=='Linear':
            sweep_start, sweep_end = self.signals['params'][0, 0, :2]
            num_sweep_signal = self.header['num_sweep_signal']
            bias=np.linspace(sweep_start, sweep_end, num_sweep_signal, dtype=np.float32)
        elif self.header['filetype']=='MLS':
            #TODO:有出bug的可能性，不过很小，假如你设的电压不连续应该就会出bug，但是我懒得写了
            bias=np.array([])
            for i in range(len(self.header['segment'])):
                linshi=np.linspace(float(self.header['segment'][i].split(',')[0]),float(self.header['segment'][i].split(',')[1]),int(self.header['segment'][i].split(',')[4]),dtype=np.float32)
                bias=np.append(bias,linshi[:-1])
            bias=np.append(bias,linshi[-1])

        return bias

    def _extract_topo(self):
        #sb??
        """
        Extract topographic map based on z-controller height at each
        pixel.

        The data is already extracted, though it lives in the signals
        dict under the key 'parameters'. Currently the 4th column is the
        Z (m) information at each pixel, should update this to be more
        general in case the fixed/experimental parameters are not the
        same for other Nanonis users.

        Returns
        -------
        numpy.ndarray
            Copy of already extracted data to be more easily accessible
            in signals dict.
        """
        return self.signals['params'][:, :, 4]


class Scan(NanonisFile):

    """
    Nanonis scan file class.

    Contains data loading methods specific to Nanonis sxm files. The
    header is determinated by a 'SCANIT_END' tag followed by the \1A\04 #这个还是有必要看一下的
    code. The NanonisFile header parse method doesn't account for thi s
    so the Scan __init__ method just adds 4 bytes to the byte_offset
    attribute so as to not include this as a datapoint.

    Data is structured a little differently from grid files, obviously.
    For each pixel in the scan, each channel is recorded forwards and
    backwards one after the other.

    Currently cannot take scans that do not have both directions
    recorded for each channel, nor incomplete scans.

    Parameters
    ----------
    fname : str
        Filename for scan file.

    Attributes
    ----------
    header : dict
        Parsed sxm header. Some fields are converted to float,
        otherwise most are string values.
    signals : dict
        Dict keys correspond to channel name, values correspond to
        another dict whose keys are simply forward and backward arrays
        for the scan image.

    Raises
    ------
    UnhandledFileError
        If fname does not have a '.sxm' extension.
    """

    def __init__(self, fname, data_format=None):
        _is_valid_file(fname, ext='sxm')
        super().__init__(fname)
        self.set_data_format(data_format)
        self.header = _parse_sxm_header(self.header_raw)

        # data begins with 4 byte code, add 4 bytes to offset instead
        self.byte_offset += 4

        # load data
        self.signals = self._load_data()


    def _load_data(self):
        """
        Read binary data for Nanonis sxm file.

        Returns
        -------
        dict
            Channel name keyed dict of each channel array.
        """
        channs = list(self.header['data_info']['Name'])
        nchanns = len(channs)
        nx, ny = self.header['scan_pixels']

        data_dict = dict()

        # open and seek to start of data
        f = open(self.fname, 'rb')
        f.seek(self.byte_offset)
        data_format = self.data_format
        scandata = np.fromfile(f, dtype=data_format)
        f.close()

        # assume both directions for now
        # TODO:这里有一个ndir需要区分一下1/2
        if scandata.size/nx/ny<2:
            ndir = 1
        else:
            ndir = 2

        # reshape
        scandata_shaped = scandata.reshape(nchanns, ndir, ny, nx)
        
        # extract data for each channel
        # TODO:这里有一个ndir需要区分一下1/2
        for i, chann in enumerate(channs):
            if ndir==1:
                chann_dict = dict(forward=scandata_shaped[i, 0, :, :])
                data_dict[chann] = chann_dict
            else:
                chann_dict = dict(forward=scandata_shaped[i, 0, :, :],
                                backward=scandata_shaped[i, 1, :, :])
                data_dict[chann] = chann_dict

        return data_dict


class Spec(NanonisFile):

    """
    Nanonis point spectroscopy file class.

    These files are a little easier to handle since they are stored in
    ascii format.

    Parameters
    ----------
    fname : str
        Filename for spec file.

    Attributes
    ----------
    header : dict
        Parsed dat header.

    Raises
    ------
    UnhandledFileError
        If fname does not have a '.dat' extension.
    """

    def __init__(self, fname):
        _is_valid_file(fname, ext='dat')
        super().__init__(fname)
        self.header = _parse_dat_header(self.header_raw)
        self.signals = self._load_data()

    def _load_data(self):
        """
        Loads ascii formatted .dat file.

        Header ended by '[DATA]' tag.

        Returns
        -------
        dict
            Keys correspond to each channel recorded, including
            saved/filtered versions of other channels.
        """

        # done differently since data is ascii, not binary
        f = open(self.fname, 'r')
        f.seek(self.byte_offset)
        data_dict = dict()

        column_names = f.readline().strip('\n').split('\t')
        f.close()
        num_lines = self._num_header_lines()
        specdata = np.genfromtxt(self.fname, delimiter='\t', skip_header=num_lines)

        for i, name in enumerate(column_names):
            data_dict[name] = specdata[:, i]

        return data_dict

    def _num_header_lines(self):
        """Number of lines the header is composed of"""
        with open(self.fname, 'r') as f:
            data = f.readlines()
            for i, line in enumerate(data):
                if nanonis_end_tags['spec'] in line:
                    return i + 2  # add 2 to skip the tag itself and column names
        return 0


class UnhandledFileError(Exception):

    """
    To be raised when unknown file extension is passed.
    """
    pass


class FileHeaderNotFoundError(Exception):

    """
    To be raised when no header information could be determined.
    """
    pass

class Write():
    def __init__(self,data,header,data_type,write_type):
        self.data:dict=data
        self.raw_data_type=data_type
        self.raw_header=header
        self.write_type=write_type
        self.header_inner={
            '3ds':[\
                'Grid dim=',
                'Grid settings=', 
                'Filetype=Linear', 
                'Sweep Signal="Bias (V)"',
                'Fixed parameters="Sweep Start;Sweep End"',
                'Experiment parameters="X (m);Y (m);Z (m)',
                '# Parameters (4 byte)=',
                'Experiment size (bytes)=',
                'Points=',
                'Channels="Current (A);LI Demod 1 X (A)"',
                'Delay before measuring (s)=0.000000E+0', 
                'Experiment="Grid Spectroscopy"', 
                'Start time=',
                'End time=', 
                'User="???"', 
                'Comment='\
                    ],
            'dat':[
                'Experiment',
                'Saved Date',
                'User',
                'Date',
                'X (m)',
                'Y (m)',
                'Z (m)',
                'Z offset (m)',
                'Settling time (s)',
                'Integration time (s)',
                'Z-Ctrl hold',
                'Final Z (m)',
                'Start time',
                'Filter type',
                'Order',
                'Cutoff frq',
            ],
            'sxm':[
                ':NANONIS_VERSION:',
                ':SCANIT_TYPE:',
                ':REC_DATE:',
                ':REC_TIME:',
                ':REC_TEMP:',
                ':ACQ_TIME:',
                ':SCAN_PIXELS:',
                ':SCAN_FILE:',
                ':SCAN_TIME:',
                ':SCAN_RANGE:',
                ':SCAN_OFFSET:',
                ':SCAN_ANGLE:',
                ':SCAN_DIR:',
                ':BIAS:',
                ':Data Convert:',
                ':COMMENT:',
                ':DATA_INFO:'
            ]
        }
        self._determine_filetype()

    def _determine_filetype(self):
        fname_ext = self.write_type
        if fname_ext == '3ds':
            self.Grid_write()
        elif fname_ext == 'sxm':
            self.Sxm_write()
        elif fname_ext == 'dat':
            self.Dat_write()
        elif fname_ext == 'mat':
            self.Mat_write()
        else:
            raise UnhandledFileError('{} is not a supported filetype or does not exist'.format(self.basename))
    
    def Grid_write(self):
        if self.raw_data_type=='sxm':
            '''
            sxm格式下 
                    这个函数是右键菜单专用，不适用于项目中的数据
                    需要把整个data.signals 当作data传过来
                    raw_header['header']=data.header raw_header 字典还可以存一些命令过来
            '''
            ################### 处理头文件 #################
            # 先拷贝一个列表
            header_sxm=self.header_inner['3ds'].copy()
            for i,value in enumerate(header_sxm):
                if value=='Grid dim=':
                    header_sxm[i]=header_sxm[i]+'"'+str(self.raw_header['header']['scan_pixels'][0])+' x '+str(self.raw_header['header']['scan_pixels'][1])+'"'
                elif value=='Grid settings=':
                    header_sxm[i]=header_sxm[i]+str(self.raw_header['header']['scan_offset'][0])+';'+str(self.raw_header['header']['scan_offset'][1])+';'+str(self.raw_header['header']['scan_range'][0])+';'+str(self.raw_header['header']['scan_range'][1])+';'+str(self.raw_header['header']['scan_angle'])
                elif value=='Experiment parameters="X (m);Y (m);Z (m)':
                    tmp_channels=''; 
                    data1=np.array([]); 
                    channel_count=0; 
                    for channel,tmp in self.data.items():
                        for sweep,data in tmp.items():
                            tmp_channels=tmp_channels+';'+channel+' ['+sweep+']'
                            if sweep=='backward':
                                self.data[channel][sweep]=np.flip(self.data[channel][sweep],1)
                            channel_count+=1
                            if channel_count==1:
                                data1=self.data[channel][sweep]
                            elif channel_count==2:
                                data1=np.stack([data1,self.data[channel][sweep]],2)
                            else:
                                data1=np.concatenate([data1,self.data[channel][sweep][:,:,np.newaxis]],2)
                    header_sxm[i]=header_sxm[i]+tmp_channels
                    header_sxm[i]=header_sxm[i]+'"'
                elif value=='# Parameters (4 byte)=':
                    header_sxm[i]=header_sxm[i]+str(5+channel_count)
                elif value=='Experiment size (bytes)=':
                    header_sxm[i]=header_sxm[i]+str(channel_count*8)
                elif value=='Points=':
                    header_sxm[i]=header_sxm[i]+str(channel_count)
                elif value=='Start time=':
                    header_sxm[i]=header_sxm[i]+self.raw_header['header']['rec_date']+" "+self.raw_header['header']['rec_time']
                elif value=='End time=':
                    header_sxm[i]=header_sxm[i]+time.strftime('%Y.%m.%d %H:%M:%S', time.localtime())
                elif value=='Comment=':
                    header_sxm[i]=header_sxm[i]+tmp_channels[1:-1]
                # print(header_sxm[i])
            ################## 处理数据 ####################
            para=np.zeros((self.raw_header['header']['scan_pixels'][0],self.raw_header['header']['scan_pixels'][1],5+channel_count))
            para[:,:,1-1]=np.ones(self.raw_header['header']['scan_pixels'])
            para[:,:,2-1]=np.ones(self.raw_header['header']['scan_pixels'])*channel_count

            x=np.linspace(0,self.raw_header['header']['scan_range'][0],self.raw_header['header']['scan_pixels'][0])-self.raw_header['header']['scan_range'][0]/2
            y=np.linspace(0,self.raw_header['header']['scan_range'][1],self.raw_header['header']['scan_pixels'][1])-self.raw_header['header']['scan_range'][1]/2
            Xr_tmp,Yr_tmp=np.meshgrid(x,y)
            Xr=Xr_tmp*np.cos(float(self.raw_header['header']['scan_angle'])/180*np.pi)+Yr_tmp*np.sin(float(self.raw_header['header']['scan_angle'])/180*np.pi)+self.raw_header['header']['scan_offset'][0]
            Yr=-Xr_tmp*np.sin(float(self.raw_header['header']['scan_angle'])/180*np.pi)+Yr_tmp*np.cos(float(self.raw_header['header']['scan_angle'])/180*np.pi)+self.raw_header['header']['scan_offset'][1]
            para[:,:,3-1]=Xr.transpose(1,0)
            para[:,:,4-1]=Yr.transpose(1,0)
            if self.raw_header['header']['scan_dir']=='down':
                try:
                    para[:,:,5-1]=np.flip(self.data['Z']['forward'],0).transpose(1,0)
                except:
                    for kkk in self.data.keys():
                        break
                    para[:,:,5-1]=np.flip(self.data[kkk]['forward'],0).transpose(1,0)
                para[:,:,6-1:6-1+channel_count]=np.flip(data1,0).transpose(1,0,2)
            elif self.raw_header['header']['scan_dir']=='up':
                try:
                    para[:,:,5-1]=self.data['Z']['forward'].transpose(1,0)
                except:
                    for kkk in self.data.keys():
                        break
                    para[:,:,5-1]=self.data[kkk]['forward'].transpose(1,0)
                para[:,:,6-1:6-1+channel_count]=data1.transpose(1,0,2)

            current=np.zeros((self.raw_header['header']['scan_pixels'][0],self.raw_header['header']['scan_pixels'][1],channel_count))
            if self.raw_header['header']['scan_dir']=='down':
                didv=np.flip(data1,0)
            elif self.raw_header['header']['scan_dir']=='up':
                didv=data1
            point_Spec_all=para.copy()
            point_Spec_all=np.concatenate([point_Spec_all,current],2) 
            point_Spec_all=np.concatenate([point_Spec_all,didv.transpose(1,0,2)],2) 
            point_Spec_all=point_Spec_all.transpose(1,0,2)
            # point_Spec_all.shape=-1
            point_Spec_all=point_Spec_all.reshape([-1,1],order='C')         #order='C'/'F' 按照啥最大的来
            
            # print('数据处理结束')
            ############# 写入 ##########
            path_write=self.raw_header['savepath']
            with open(path_write,'wb') as fn2:
                for s in header_sxm:
                    s=s+'\r\n'
                    fn2.write(s.encode('utf-8'))
                fn2.write(':HEADER_END:\r\n'.encode('utf-8'))
                for value in point_Spec_all:
                    data_write=struct.pack('>f', value)
                    fn2.write(data_write)


        elif self.raw_data_type=='mat':
            '''
            mat格式下 只传入纯纯的数据
                      raw_header 只存储一个save的路径
            '''
            ################### 数据预处理 #################
            raw_mat=np.array([])
            for key in self.data.keys():
                if key[:2]=='__':
                    pass
                else:
                    raw_mat=self.data[key]
                    break
            size_data=raw_mat.shape
            header_mat=self.header_inner['3ds'].copy()  
            
            index_n0=int(raw_mat.size/size_data[0]/size_data[1])
            # 如果是二维的就补成三维的
            if index_n0==1:
                raw_mat=raw_mat[:,:,np.newaxis]
                raw_mat=np.concatenate([raw_mat,raw_mat],2) 
                index_n=2
            else:
                index_n=index_n0
            ################### 处理头文件 #################
            for i,value in enumerate(header_mat):
                if value=='Grid dim=':
                    header_mat[i]=header_mat[i]+'"'+str(size_data[0])+' x '+str(size_data[1])+'"'
                elif value=='Grid settings=':
                    header_mat[i]=header_mat[i]+str(size_data[0])+';'+str(size_data[1])+';'+str(size_data[0])+';'+str(size_data[1])+';'+str(0)
                elif value=='Experiment parameters="X (m);Y (m);Z (m)':
                    for n in range(0,index_n):
                        header_mat[i]=header_mat[i]+';index'+str(n+1)
                    header_mat[i]=header_mat[i]+'"'
                elif value=='# Parameters (4 byte)=':
                    header_mat[i]=header_mat[i]+str(5+index_n)
                elif value=='Experiment size (bytes)=':
                    header_mat[i]=header_mat[i]+str(index_n*8)
                elif value=='Points=':
                    header_mat[i]=header_mat[i]+str(index_n)
                elif value=='Start time=':
                    header_mat[i]=header_mat[i]
                elif value=='End time=':
                    header_mat[i]=header_mat[i]+time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                elif value=='Comment=':
                    header_mat[i]=header_mat[i]
            ################## 处理数据 ####################
            para=np.zeros((size_data[0],size_data[1],5+index_n))
            para[:,:,1-1]=np.ones((size_data[0],size_data[1]))
            para[:,:,2-1]=np.ones((size_data[0],size_data[1]))*index_n
            x=np.linspace(1,size_data[0],size_data[0])
            y=np.linspace(1,size_data[1],size_data[1])
            Xr_tmp,Yr_tmp=np.meshgrid(y,x)
            para[:,:,3-1]=Xr_tmp
            para[:,:,4-1]=Yr_tmp
            if index_n0==1:
                para[:,:,5-1]=self.data[key]
            else:
                para[:,:,5-1]=raw_mat[:,:,1]
            # para[:,:,5-1]=np.ones((size_data[0],size_data[1]))
            para[:,:,6-1:6-1+index_n]=raw_mat

            current=np.zeros((size_data[0],size_data[1],index_n))
            didv=raw_mat
            point_Spec_all=para.copy()
            point_Spec_all=np.concatenate([point_Spec_all,current],2) 
            
            # # 有时候是二维数组，没有第三个维度
            # if index_n==1:
            #     point_Spec_all=np.concatenate([point_Spec_all,didv[:,:,np.newaxis]],2) 
            # else:
            #     point_Spec_all=np.concatenate([point_Spec_all,didv],2) 
            point_Spec_all=np.concatenate([point_Spec_all,didv],2) 
            print(point_Spec_all.shape)
            
            point_Spec_all=point_Spec_all.transpose(1,0,2)
            point_Spec_all=point_Spec_all.reshape([-1,1],order='C')         #order='C'/'F' 按照啥最大的来
            ############# 写入 ##########
            path_write=self.raw_header['savepath']
            with open(path_write,'wb') as fn2:
                for s in header_mat:
                    s=s+'\r\n'
                    fn2.write(s.encode('utf-8'))
                fn2.write(':HEADER_END:\r\n'.encode('utf-8'))
                for value in point_Spec_all:
                    data_write=struct.pack('>f', value)
                    fn2.write(data_write)
                    
    def Sxm_write(self):
        if self.raw_data_type=='mat':
            '''
            mat格式下 
                    这个函数是右键菜单专用，不适用于项目中的数据
                    保存一个mat里的第一个矩阵,但是要求nx=xy,第三个维度无所谓
                    数据传入格式:self.data=scipy.io.loadmat(fname) ,dict 格式
                    保存格式为极简形式,只有内置的几种header
                    保存的数据格式为 channel: Name+Index(n)
            '''
            ################### 数据预处理 #################
            raw_mat=np.array([])
            tmp_data=np.array([])
            for channel in self.data.keys():
                if channel[:2]=='__':
                    pass
                else:
                    raw_mat=self.data[channel]
                    break
            size_data=raw_mat.shape
            index_n=int(raw_mat.size/size_data[0]/size_data[1])
            # print(size_data)
            for i in range(0,index_n):
                if i==0:
                    if index_n==1:
                        tmp_for=raw_mat
                        tmp_back=np.flipud(raw_mat)
                        tmp_data=np.concatenate([tmp_for[:,:,np.newaxis],tmp_back[:,:,np.newaxis]],2)
                    else:
                        tmp_for=raw_mat[:,:,i]
                        tmp_back=np.flipud(raw_mat[:,:,i])
                        tmp_data=np.concatenate([tmp_for[:,:,np.newaxis],tmp_back[:,:,np.newaxis]],2)
                else:
                    tmp_for=raw_mat[:,:,i]
                    tmp_back=np.flipud(raw_mat[:,:,i])
                    tmp_data=np.concatenate([tmp_data,tmp_for[:,:,np.newaxis]],2)
                    tmp_data=np.concatenate([tmp_data,tmp_back[:,:,np.newaxis]],2)
            tmp_data=tmp_data.reshape([-1,1],order='F')         #order='C'/'F' 按照啥最大的来
            #################### header预处理 ###################
            header_sxm=self.header_inner['sxm'].copy()
            for i,value in enumerate(header_sxm):
                if value==':NANONIS_VERSION:':
                    header_sxm[i]=header_sxm[i]+'\n'+'2'
                elif value==':SCANIT_TYPE:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t\t FLOAT            MSBFIRST'
                elif value==':REC_DATE:':
                    header_sxm[i]=header_sxm[i]+'\n'+' '+time.strftime("%d.%m.%Y", time.localtime()) 
                elif value==':REC_TIME:':
                    header_sxm[i]=header_sxm[i]+'\n'+time.strftime("%H:%M:%S", time.localtime()) 
                elif value==':REC_TEMP:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t'+'1314'
                elif value==':ACQ_TIME:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t'+'1314'
                elif value==':SCAN_PIXELS:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t '+str(size_data[0])+'\t'+str(size_data[1])
                elif value==':SCAN_FILE:':
                    header_sxm[i]=header_sxm[i]+'\n'+self.raw_header['savepath']
                elif value==':SCAN_TIME:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t\t '+'1314'+'\t'+'1314'
                elif value==':SCAN_RANGE:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t\t'+str(size_data[0]*1E-9)+'\t'+str(size_data[1]*1E-9)
                elif value==':SCAN_OFFSET:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t\t'+str(0)+'\t'+str(0)
                elif value==':SCAN_ANGLE:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t\t'+str(0)
                elif value==':SCAN_DIR:':
                    header_sxm[i]=header_sxm[i]+'\n'+'up'
                elif value==':BIAS:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t\t'+'1314'
                elif value==':COMMENT:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t\t'+''
                elif value==':Data Convert:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t\t'+'Ver 0.0'
                elif value==':DATA_INFO:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t'+'Channel'+'\t'+'Name'+'\t'+'Unit'+'\t'+'Direction'+'\t'+'Calibration'+'\t'+'Offset'+'\n'
                    tmp_str=''
                    for n in range(1,index_n+1):
                        tmp_str=tmp_str+'\t'+str(n)+'\t'+channel+str(n)+'\t'+'kk'+'\t'+'both'+'\t'+'1.000E+0'+'\t'+'1.000E+0'+'\n'
                    header_sxm[i]=header_sxm[i]+tmp_str
            #################### 写入 ###################
            path_write=self.raw_header['savepath']
            with open(path_write,'wb') as fn2:
                for s in header_sxm:
                    s=s+'\r\n'
                    fn2.write(s.encode('utf-8'))
                # fn2.write(':Data Convert:\n\t ver 0.0\r\n\r\n'.encode('utf-8')) # 人为的写一项带'\n\n'进去防止读的时候[:-3],之前 ':DATA_INFO:' 是最后一项看不出来
                fn2.write(':SCANIT_END:\n\n\n'.encode('utf-8'))
                fn2.write(chr(26).encode('utf-8'))
                fn2.write(chr(4).encode('utf-8'))
                for value in tmp_data:
                    data_write=struct.pack('>f', value)
                    fn2.write(data_write)

        elif self.raw_data_type=='3ds':
            '''
            3ds格式下 
                    这个函数是右键菜单专用，不适用于项目中的数据
                    保存一个3ds的didv channel 即第二个channel(默认情况下)
                    数据传入格式:self.data=read.Grid(fname) ,class 格式
                    保存格式为极简形式,只有内置的几种header
                    保存的数据格式为 channel: Name+Index(n)
            '''
            ################### 数据预处理 #################
            raw_3ds=np.array([])
            tmp_data=np.array([])
            count=1
            for channel in self.data.signals.keys():
                if count==3:                              # 1: param 2: I 3: didv
                    raw_3ds=self.data.signals[channel]    
                    break
                count+=1
            size_data=raw_3ds.shape
            index_n=int(raw_3ds.size/size_data[0]/size_data[1])
            # print(size_data)
            for i in range(0,index_n):
                if i==0:
                    if index_n==1:
                        tmp_for=raw_3ds
                        tmp_back=np.flipud(raw_3ds)
                        tmp_data=np.concatenate([tmp_for[:,:,np.newaxis],tmp_back[:,:,np.newaxis]],2)
                    else:
                        tmp_for=raw_3ds[:,:,i]
                        tmp_back=np.flipud(raw_3ds[:,:,i])
                        tmp_data=np.concatenate([tmp_for[:,:,np.newaxis],tmp_back[:,:,np.newaxis]],2)
                else:
                    tmp_for=raw_3ds[:,:,i]
                    tmp_back=np.flipud(raw_3ds[:,:,i])
                    tmp_data=np.concatenate([tmp_data,tmp_for[:,:,np.newaxis]],2)
                    tmp_data=np.concatenate([tmp_data,tmp_back[:,:,np.newaxis]],2)
            tmp_data=tmp_data.reshape([-1,1],order='F')         #order='C'/'F' 按照啥最大的来
            #################### header预处理 ###################
            header_sxm=self.header_inner['sxm'].copy()
            for i,value in enumerate(header_sxm):
                if value==':NANONIS_VERSION:':
                    header_sxm[i]=header_sxm[i]+'\n'+'2'
                elif value==':SCANIT_TYPE:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t\t FLOAT            MSBFIRST'
                elif value==':REC_DATE:':
                    header_sxm[i]=header_sxm[i]+'\n'+' '+time.strftime("%d.%m.%Y", time.localtime()) 
                elif value==':REC_TIME:':
                    header_sxm[i]=header_sxm[i]+'\n'+time.strftime("%H:%M:%S", time.localtime()) 
                elif value==':REC_TEMP:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t'+'1314'
                elif value==':ACQ_TIME:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t'+'1314'
                elif value==':SCAN_PIXELS:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t '+str(size_data[0])+'\t'+str(size_data[1])
                elif value==':SCAN_FILE:':
                    header_sxm[i]=header_sxm[i]+'\n'+self.raw_header['savepath']
                elif value==':SCAN_TIME:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t\t '+'1314'+'\t'+'1314'
                elif value==':SCAN_RANGE:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t\t'+str(self.data.header['size_xy'][0])+'\t'+str(self.data.header['size_xy'][1])
                elif value==':SCAN_OFFSET:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t\t'+str(self.data.header['pos_xy'][0])+'\t'+str(self.data.header['pos_xy'][1])
                elif value==':SCAN_ANGLE:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t\t'+str(self.data.header['angle'])
                elif value==':SCAN_DIR:':
                    header_sxm[i]=header_sxm[i]+'\n'+'up'
                elif value==':BIAS:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t\t'+'1314'
                elif value==':COMMENT:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t\t'+'1314'
                elif value==':Data Convert:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t\t'+'Ver 0.0'
                elif value==':DATA_INFO:':
                    header_sxm[i]=header_sxm[i]+'\n'+'\t'+'Channel'+'\t'+'Name'+'\t'+'Unit'+'\t'+'Direction'+'\t'+'Calibration'+'\t'+'Offset'+'\n'
                    tmp_str=''
                    for n in range(1,index_n+1):
                        tmp_str=tmp_str+'\t'+str(n)+'\t'+channel[:-3]+'bias='+str(self.data.signals['_sweep_signal'][n-1])+'\t'+'V'+'\t'+'both'+'\t'+'1.000E+0'+'\t'+'1.000E+0'+'\n'
                    header_sxm[i]=header_sxm[i]+tmp_str
            #################### 写入 ###################
            path_write=self.raw_header['savepath']
            with open(path_write,'wb') as fn2:
                for s in header_sxm:
                    s=s+'\r\n'
                    fn2.write(s.encode('utf-8'))
                # fn2.write(':Data Convert:\n\t ver 0.0\r\n\r\n'.encode('utf-8')) # 人为的写一项带'\n\n'进去防止读的时候[:-3],之前 ':DATA_INFO:' 是最后一项看不出来
                fn2.write(':SCANIT_END:\n\n\n'.encode('utf-8'))
                fn2.write(chr(26).encode('utf-8'))
                fn2.write(chr(4).encode('utf-8'))
                for value in tmp_data:
                    data_write=struct.pack('>f', value)
                    fn2.write(data_write)

    def Mat_write(self):
        if self.raw_data_type=='sxm':
            '''
            sxm格式下 
                    这个函数是右键菜单专用，不适用于项目中的数据
                    只保存channel+X,Y的数据,可以直接在matlab里画图mesh(Xr,Yr,channel)
                    需要考虑
            '''
            ###################处理数据格式#################
            data_sxm=self.data
            tmp_data={}
            x=np.linspace(0,data_sxm.header['scan_range'][0],data_sxm.header['scan_pixels'][0])-data_sxm.header['scan_range'][0]/2
            y=np.linspace(0,data_sxm.header['scan_range'][1],data_sxm.header['scan_pixels'][1])-data_sxm.header['scan_range'][1]/2
            Xr_tmp,Yr_tmp=np.meshgrid(x,y)
            Xr= Xr_tmp*np.cos(float(data_sxm.header['scan_angle'])/180*np.pi)+Yr_tmp*np.sin(float(data_sxm.header['scan_angle'])/180*np.pi)+data_sxm.header['scan_offset'][0]
            Yr=-Xr_tmp*np.sin(float(data_sxm.header['scan_angle'])/180*np.pi)+Yr_tmp*np.cos(float(data_sxm.header['scan_angle'])/180*np.pi)+data_sxm.header['scan_offset'][1]

            Xr=Xr.transpose(1,0)
            Yr=Yr.transpose(1,0)
            tmp_data.update({'Xr':Xr})
            tmp_data.update({'Yr':Yr})
            for channel in data_sxm.signals.keys():
                for sweep in data_sxm.signals[channel].keys():
                    if channel[0:2]=='LI':
                        str1="didv"
                    elif channel[0:7]=='Current':
                        str1="I"
                    else:
                        str1=channel
                    if sweep=='forward':
                        str2='for'
                    elif sweep=='backward':
                        str2='back'
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
                    tmp_data.update({str1+'_'+str2:tmp_data2})

            fname=self.raw_header['savepath']
            scio.savemat(fname,tmp_data)
            del data_sxm,x,y,Xr,Yr,Xr_tmp,Yr_tmp,fname,tmp_data

        elif self.raw_data_type=='3ds':
            '''
            3ds格式下 
                    这个函数是右键菜单专用，不适用于项目中的数据
                    两种格式:    1.只存didv 名字为result
                                 2.全存下来
            '''
            
            fname=self.raw_header['savepath']
            if self.raw_header['savemode']=='didv':
                data_3ds=self.data
                count=1
                for key in data_3ds.signals.keys():
                    if count==3:
                        print('保存的频道为：',key)
                        scio.savemat(fname,{'result':data_3ds.signals[key]})
                        break
                    count+=1
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
            elif self.raw_header['savemode']=='linecut':
                data_3ds=self.data
                tmp_data={}
                tmp_spec   =np.array([])
                tmp_current=np.array([])
                tmp_didv   =np.array([])
                count=1
                for key in data_3ds.signals.keys():
                    if count==2:
                        tmp_spec = data_3ds.signals[key]
                        tmp_current = data_3ds.signals[key]
                    elif count==3:
                        tmp_spec = np.concatenate([tmp_spec,data_3ds.signals[key]],1)   
                        tmp_didv = data_3ds.signals[key]
                    elif count>=4:
                        if key[0]=='_':
                            pass
                        else:
                            tmp_spec = np.concatenate([tmp_spec,data_3ds.signals[key]],1)   
                            if count%2==0:
                                tmp_current = np.concatenate([tmp_current,data_3ds.signals[key]],1)   
                            elif count%2==1:
                                tmp_didv = np.concatenate([tmp_didv,data_3ds.signals[key]],1)   
                        
                    count+=1
                    
                tmp_spec=tmp_spec.transpose(2,1,0)
                tmp_current=tmp_current.transpose(2,1,0)
                tmp_didv=tmp_didv.transpose(2,1,0)
                tmp_para=data_3ds.signals['params'].copy()
                tmp_para=tmp_para.transpose(2,1,0)
                
                tmp_data.update({'header':data_3ds.header})
                tmp_data.update({'params':tmp_para})
                tmp_data.update({'raw_linedata':tmp_spec})
                tmp_data.update({'raw_I':tmp_current})
                tmp_data.update({'raw_didv':tmp_didv})
                tmp_data.update({'bias':data_3ds.signals['_sweep_signal']})
                scio.savemat(fname,tmp_data)
    
    def Dat_write(self):
        if self.raw_data_type=='3ds':
            '''
            3ds格式下 
                    这个函数是右键菜单专用，不适用于项目中的数据
                    从params读取 XZY
                    第一列 bias
                    第二列 Current  AVG Forward
                    第三列 didv     AVG Forward
                    4:4+sweeps*2 :
                    5+2*sweeps: Current  AVG Backward
                    6+2*sweeps: didv     AVG Backward

                    savepath 选为文件夹 后加入 fname_X001_Y001.dat
            '''
            ###################处理数据格式#################
            data_dat=self.data
            tmp_data={}
            bias=data_dat.signals['_sweep_signal']

            count=1
            channel_str='Bias calc (V)'
            for key in data_dat.signals.keys():
                if key[0]=='_' or key=='params':
                    pass
                else :
                    if count==1:
                        tmp_data=data_dat.signals[key]
                        tmp_data=tmp_data[:,:,:,np.newaxis]
                        channel_str=channel_str+'\t'+key
                    else: 
                        tmp_data=np.concatenate([tmp_data,data_dat.signals[key][:,:,:,np.newaxis]],3)
                        channel_str=channel_str+'\t'+key
                    count+=1
            # tmp_data=np.concatenate([tmp_data],3)
            ###################处理header#################
            count=0
            for m in range(0,tmp_data.shape[0]):
                for n in range(0,tmp_data.shape[1]):
                    header_dat=self.header_inner['dat'].copy()
                    count+=1
                    for i,value in enumerate(header_dat):
                        if value=='Experiment':
                            header_dat[i]=header_dat[i]+'\t'+'bias spectroscopy'+'\t'
                        elif value=='Saved Date':
                            # header_dat[i]=header_dat[i]+'\t'+time.strftime('%d.%m.%Y %H:%M:%S', time.localtime())+'\t'
                            header_dat[i]=header_dat[i]+'\t'+time.strftime('%Y.%m.%d %H:%M:%S', time.localtime())+'\t'
                        elif value=='User':
                            header_dat[i]=header_dat[i]+'\t'+socket.gethostname()+'\t'
                        elif value=='Date':
                            header_dat[i]=header_dat[i]+'\t'+'X='+"{0:04d}".format(m+1)+' Y='+"{0:04d}".format(n+1)+'\t'
                        elif value=='X (m)':
                            header_dat[i]=header_dat[i]+'\t'+"{0:4.4E}".format(data_dat.signals['params'][m,n,2])+'\t'
                        elif value=='Y (m)':
                            header_dat[i]=header_dat[i]+'\t'+"{0:4.4E}".format(data_dat.signals['params'][m,n,3])+'\t'
                        elif value=='Z (m)':
                            header_dat[i]=header_dat[i]+'\t'+"{0:4.4E}".format(data_dat.signals['params'][m,n,4])+'\t'
                        elif value=='Z offset (m)':
                            header_dat[i]=header_dat[i]+'\t'+'0E+0'+'\t'
                        elif value=='Settling time (s)':
                            header_dat[i]=header_dat[i]+'\t'+'0E+0'+'\t'
                        elif value=='Integration time (s)':
                            header_dat[i]=header_dat[i]+'\t'+'0E+0'+'\t'
                        elif value=='Z-Ctrl hold':
                            header_dat[i]=header_dat[i]+'\t'+'TRUE'+'\t'
                        elif value=='Final Z (m)':
                            header_dat[i]=header_dat[i]+'\t'+'N/A'+'\t'
                        elif value=='Start time':
                            header_dat[i]=header_dat[i]+'\t'+time.strftime('%Y.%m.%d %H:%M:%S', time.localtime())+'\t'
                        elif value=='Filter type':
                            header_dat[i]=header_dat[i]+'\t'+'None'+'\t'
                        elif value=='Order':
                            header_dat[i]=header_dat[i]+'\t'+'0'+'\t'
                        elif value=='Cutoff frq':
                            header_dat[i]=header_dat[i]+'\t'+'\t'
                    data_write=tmp_data[m,n,:,:].copy()
                    data_write=np.concatenate([bias[:,np.newaxis],data_write],1)
                    size_write=data_write.shape
                    # for p in range(0,size_write[0]):
                    #     for q in range(0,size_write[1]):

                    path_write=self.raw_header['savepath'][:-4]+'_'+"{0:04d}".format(count)+'.dat'
                    header_write=''
                    for s in header_dat:
                        header_write=header_write+s+'\n'
                    header_write=header_write+'\n'+'[DATA]'+'\n'+channel_str    
                    np.savetxt(path_write,data_write, fmt='%E', delimiter='\t', newline='\n', header=header_write, footer='', comments='', encoding='utf-8')   

            pass
                    

def _parse_3ds_header(header_raw, header_override):
    """
    Parse raw header string.

    Empirically done based on Nanonis header structure. See Grid
    docstring or Nanonis help documentation for more details.

    Parameters
    ----------
    header_raw : str
        Raw header string from read_raw_header() method.

    Returns
    -------
    dict
        Channel name keyed dict of 3d array.
    """
    # cleanup string and remove end tag as entry
    header_entries = header_raw.split('\r\n')
    header_entries = header_entries[:-2]   
    # '3ds' 最后两行是':HEADER_END:', ''

    # Convert the strings to a dictionary.
    raw_dict = dict()
    for entry in header_entries:
        key, val = _split_header_entry(entry)
        raw_dict[key] = val

    if header_override is not None:
        for key, val in header_override.items():
            raw_dict[key] = val  # creates new entry if key doesn't match key in raw_dict

    # Transfer parameters from raw_dict to header_dict
    # Get the expected parameters first
    header_dict = dict()

    try:
        # grid dimensions in pixels
        header_dict['dim_px'] = [int(val) for val in raw_dict['Grid dim'].split(' x ')]
        raw_dict.pop('Grid dim')

        # grid frame center position, size, angle. Assumes len(raw_dict['Grid settings']) = 4
        header_dict['pos_xy'] = [float(val) for val in raw_dict['Grid settings'][:2]]
        header_dict['size_xy'] = [float(val) for val in raw_dict['Grid settings'][2:4]]
        header_dict['angle'] = float(raw_dict['Grid settings'][4])
        raw_dict.pop('Grid settings')

        #sb不写filetype
        header_dict['filetype']=raw_dict['Filetype']
        raw_dict.pop('Filetype')
        
        # sweep signal
        header_dict['sweep_signal'] = raw_dict['Sweep Signal']
        raw_dict.pop('Sweep Signal')

        # fixed parameters
        header_dict['fixed_parameters'] = raw_dict['Fixed parameters']
        raw_dict.pop('Fixed parameters')

        # experimental parameters
        header_dict['experimental_parameters'] = raw_dict['Experiment parameters']
        raw_dict.pop('Experiment parameters')

        # number of parameters (each 4 bytes)
        header_dict['num_parameters'] = int(raw_dict['# Parameters (4 byte)'])
        raw_dict.pop('# Parameters (4 byte)')

        #TODO:rnm,tq 不写分段函数头套给你薅掉
        for key in raw_dict.keys():
            if 'Segment' in key:
                header_dict['segment']=raw_dict[key]
                # print('\n\n\nrnm,tq \n\n\n')
                raw_dict.pop(key)
                break

        # experiment size in bytes
        header_dict['experiment_size'] = int(raw_dict['Experiment size (bytes)'])
        raw_dict.pop('Experiment size (bytes)')

        # number of points of sweep signal
        header_dict['num_sweep_signal'] = int(raw_dict['Points'])
        raw_dict.pop('Points')

        # channel names
        header_dict['channels'] = raw_dict['Channels']
        if type(header_dict['channels']) == str:
            # will be str if only one channel, make list of str so number of channels can be counted properly
            l = []
            l.append(header_dict['channels'])
            header_dict['channels'] = l
        header_dict['num_channels'] = len(header_dict['channels'])
        raw_dict.pop('Channels')

        # measure delay
        header_dict['measure_delay'] = float(raw_dict['Delay before measuring (s)'])
        raw_dict.pop('Delay before measuring (s)')

        # metadata
        header_dict['experiment_name'] = raw_dict['Experiment']
        header_dict['start_time'] = raw_dict['Start time']
        header_dict['end_time'] = raw_dict['End time']
        header_dict['user'] = raw_dict['User']
        header_dict['comment'] = raw_dict['Comment']
        raw_dict.pop('Experiment')
        raw_dict.pop('Start time')
        raw_dict.pop('End time')
        raw_dict.pop('User')
        raw_dict.pop('Comment')

    except (KeyError, ValueError) as e:
        msg = ' You can edit your header file or provide an override value in header_override'

        # guide user to using override dict
        if isinstance(e, KeyError):
            raise KeyError('[{key}] is missing from header.'.format(key=e.args[0]) + msg)
        elif isinstance(e, ValueError):
            print(e.args)
            raise ValueError('Unexpected value found in header.' + msg)
        else:
            raise

    # fold remaining header entries into dict
    for key, val in raw_dict.items():
        header_dict[key] = val

    return header_dict


def _parse_sxm_header(header_raw):
    """
    Parse raw header string.

    Empirically done based on Nanonis header structure. See Scan
    docstring or Nanonis help documentation for more details.

    Parameters
    ----------
    header_raw : str
        Raw header string from read_raw_header() method.

    Returns
    -------
    dict
        Channel name keyed dict of each channel array.
    """
    header_entries = header_raw.split('\n')
    header_entries = header_entries[:-3]

    header_dict = dict()
    entries_to_be_split = ['scan_offset',
                           'scan_pixels',
                           'scan_range',
                           'scan_time']

    entries_to_be_floated = ['scan_offset',
                             'scan_range',
                             'scan_time',
                             'bias',
                             'acq_time']

    entries_to_be_inted = ['scan_pixels']

    entries_to_be_dict = [':DATA_INFO:',
                          ':Z-CONTROLLER:',
                          ':Multipass-Config:']

    #目前看起来这个玩意是选出entries_to_be_dict的多行选项，其他的都可以一行搞定
    for i, entry in enumerate(header_entries): 
        if entry in entries_to_be_dict:
            count = 1
            for j in range(i+1, len(header_entries)):
                if header_entries[j].startswith(':'): #如果字符串以指定的值开头，则 startswith() 方法返回 True，否则返回 False。
                    break
                if header_entries[j][0] == '\t':
                    count += 1
            header_dict[entry.strip(':').lower()] = _parse_scan_header_table(header_entries[i+1:i+count])
            continue
        if entry.startswith(':'):
            header_dict[entry.strip(':').lower()] = header_entries[i+1].strip()

    for key in entries_to_be_split:
        header_dict[key] = header_dict[key].split()

    for key in entries_to_be_floated:
        if isinstance(header_dict[key], list):
            header_dict[key] = np.asarray(header_dict[key], dtype=np.float64)
        else:
            if header_dict[key]=='N/A':    #from 3ds file slice only have one channel
                header_dict[key]= np.nan
            else:
                header_dict[key] = np.float64(header_dict[key])
    for key in entries_to_be_inted:
        header_dict[key] = np.asarray(header_dict[key], dtype=np.int64)
    ##做个测试把np.int和np.float改成int和float 好像没问题而且还不警告了。。
    return header_dict


def _parse_dat_header(header_raw):
    """
    Parse point spectroscopy header.

    Each key-value pair is separated by '\t' characters. Values may be
    further delimited by more '\t' characters.

    Returns
    -------
    dict
        Parsed point spectroscopy header.
    """
    header_entries = header_raw.split('\r\n')
    header_entries = header_entries[:-3]
    header_dict = dict()
    for entry in header_entries:
        # homogenize output of .dat files with \t delimit at end of every key
        if entry[-1] == '\t':
            entry = entry[:-1]
        if '\t' not in entry:
            entry += '\t'

        key, val = entry.split('\t')
        header_dict[key] = val

    return header_dict


def _clean_sxm_header(header_dict):
    """
    Cleanup header dicitonary key-value pairs.

    Parameters
    ----------
    header_dict : dict
        Should be dict returned from _parse_sxm_header method.

    Returns
    -------
    clean_header_dict : dict
        Cleaned header dictionary.
    """
    pass


def _split_header_entry(entry):
    """
    Split 3ds header entries by '=' character. If multiple values split
    those by ';' character.
    """

    key_str, val_str = entry.split("=", 1)

    if ';' in val_str:
        return key_str, (val_str.strip('"').split(';'))
    else:
        return key_str, val_str.strip('"')


def save_array(file, arr, allow_pickle=True):
    """
    Wrapper to numpy.save method for arrays.

    The idea would be to use this to save a processed array for later
    use in a matplotlib figure generation scripts. See numpy.save
    documentation for details.

    Parameters
    ----------
    file : file or str
        File or filename to which the data is saved.  If file is a file-
        object, then the filename is unchanged.  If file is a string, a
        ``.npy`` extension will be appended to the file name if it does
        not already have one.
    arr : array_like
        Array data to be saved.
    allow_pickle : bool, optional
        Allow saving object arrays using Python pickles. Reasons for
        disallowing pickles include security (loading pickled data can
        execute arbitrary code) and portability (pickled objects may not
        be loadable on different Python installations, for example if
        the stored objects require libraries that are not available, and
        not all pickled data is compatible between Python 2 and Python
        3). Default: True
    """
    np.save(file, arr, allow_pickle=allow_pickle)


def load_array(file, allow_pickle=True):
    """
    Wrapper to numpy.load method for binary files.

    See numpy.load documentation for more details.

    Parameters
    ----------
    file : file or str
        The file to read. File-like objects must support the
    ``seek()`` and ``read()`` methods. Pickled files require that the
    file-like object support the ``readline()`` method as well.
    allow_pickle : bool, optional
        Allow loading pickled object arrays stored in npy files. Reasons
        for disallowing pickles include security, as loading pickled
        data can execute arbitrary code. If pickles are disallowed,
        loading object arrays will fail. Default: True

    Returns
    -------
    result : array, tuple, dict, etc.
        Data stored in the file. For ``.npz`` files, the returned
        instance of NpzFile class must be closed to avoid leaking file
        descriptors.
    """
    return np.load(file)


def _parse_scan_header_table(table_list):
    """
    Parse scan file header entries whose values are tab-separated
    tables.
    """
    table_processed = []
    for row in table_list:
        # strip leading \t, split by \t
        table_processed.append(row.strip('\t').split('\t'))

    # column names are first row
    keys = table_processed[0]
    values = table_processed[1:]

    zip_vals = zip(*values)

    return dict(zip(keys, zip_vals))#一个转置的方法变成dict


def _is_valid_file(fname, ext):
    """
    Detect if invalid file is being initialized by class.
    """
    #TODO: 想写一个如果没有选择文件就不提示的
    _, fname_ext = os.path.splitext(fname)
    if fname_ext[1:] != ext:
        raise UnhandledFileError('{} is not a {} file'.format(fname, ext))
