from __future__ import absolute_import, unicode_literals
from celery import Celery, shared_task

import os
import pefile
from pefile import ordlookup
import peutils
# import wmi
import subprocess
import platform
import time
# import win32api
# import string
# import math
# import hashlib
import io
import re
# from winmagic import magic

from hashlib import sha1 as hashlib_sha1
from string import printable as string_printable
from math import log as math_log

import numpy as np
import pandas as pd
import Orange
import pickle
import csv
from io import StringIO
from collections import OrderedDict
from Orange.data import Table, Domain, ContinuousVariable, DiscreteVariable

from django.conf import settings
from uploadFile.models import FileInfo, File

resourceDir = os.path.join(settings.MEDIA_ROOT,'exefiles')

# orange
def pandas_to_orange(df):
    domain, attributes, metas = construct_domain(df)
    orange_table = Orange.data.Table.from_numpy(domain = domain, X = df[attributes].values, Y = None, metas = df[metas].values, W = None)
    return orange_table

def construct_domain(df):
    columns = OrderedDict(df.dtypes)
    attributes = OrderedDict()
    metas = OrderedDict()
    for name, dtype in columns.items():

        if issubclass(dtype.type, np.number):
            if len(df[name].unique()) >= 13 or issubclass(dtype.type, np.inexact) or (df[name].max() > len(df[name].unique())):
                attributes[name] = Orange.data.ContinuousVariable(name)
            else:
                df[name] = df[name].astype(str)
                attributes[name] = Orange.data.DiscreteVariable(name, values = sorted(df[name].unique().tolist()))
        else:
            metas[name] = Orange.data.StringVariable(name)

    domain = Orange.data.Domain(attributes = attributes.values(), metas = metas.values())

    return domain, list(attributes.keys()), list(metas.keys())

# ---------------------------------------------------
@shared_task
def file_info(filepath, upload_id):
    created = time.ctime(os.path.getctime(filepath))   # create time
    last_modified = time.ctime(os.path.getmtime(filepath))   # modified time
    last_accessed = time.ctime(os.path.getatime(filepath))   # access time
    file_size = os.stat(filepath).st_size
   # file_attribute = win32api.GetFileAttributes(filepath)
    file_info_dict = {
        'file_name':filepath.split('/')[-1],
        'file_size':file_size,
       # 'file_attribute':file_attribute,
        'created':created,
        'last_modified':last_modified,
        'last_accessed':last_accessed

    }

    #sigcheck.exe output to dict
    sigcheck_dict = sigcheck(filepath.split('/')[-1])
    file_info_dict.update(sigcheck_dict)
    # BYTEWISE ANALYSIS
    byte_analysis_dict = byte_analysis(filepath)
    file_info_dict.update(byte_analysis_dict)

    file = FileInfo()
    # PE_FILE ANALYSIS
    try:
        pe_file = pefile.PE(filepath, fast_load=True)
        check_pack_dict = check_pack(pe_file)
        dll_import_analysis_dict = dll_import_analysis(pe_file)
        pefile_infos_dict = pefile_infos(pe_file)
        
        file_info_dict.update(check_pack_dict)
        file_info_dict.update(dll_import_analysis_dict)
        file_info_dict.update(pefile_infos_dict)
        file.peutils_packed = str(file_info_dict['pack'])
        file.entropy = file_info_dict['entropy']
        file.pe_machine = file_info_dict['Machine']
        file.pe_sectionNum = file_info_dict['NumberOfSections']
        file.pe_timeDateStamp = file_info_dict['TimeDateStamp']
        file.pe_characteristics = file_info_dict['Characteristics']
        file.pe_entryPoint = file_info_dict['AddressOfEntryPoint']
        file.pe_sections = str(file_info_dict['Section_info'])
        file.pe_imports = str(file_info_dict['Import_directories'])
        file.pe_exports = str(file_info_dict['Export_directories'])
    except:
        pass    

  
    file.upload_id = File.objects.get(id=upload_id)
    file.file_name = filepath.split('/')[-1]
    file.file_hash_sha1 = file_info_dict['file_sha1']
    file.file_size = os.stat(filepath).st_size
    #file.file_magic = str(magic.from_file(filepath)) 
    #file.file_state = win32api.GetFileAttributes(filepath)

    file.create_time = str(time.ctime(os.path.getctime(filepath)))
    file.modified_time = str(time.ctime(os.path.getmtime(filepath)))
    file.accessed_time = str(time.ctime(os.path.getatime(filepath)))
    try:
        file.signature_verification = str(file_info_dict['sigcheck_Verified'])
        file.company = str(file_info_dict['sigcheck_Company'])
        file.description = str(file_info_dict['sigcheck_Description'])
        file.product = str(file_info_dict['sigcheck_Product'])
        file.prod_version = str(file_info_dict['sigcheck_Prod version'])
        file.file_version = str(file_info_dict['sigcheck_File version'])
        file.machine_type = file_info_dict['sigcheck_MachineType'].split("\\")[0]
        file.link_date = str(file_info_dict['sigcheck_Link date'])
        file.signing_date = str(file_info_dict['sigcheck_Signing date'])
        file.signer = str(file_info_dict['Signers'])
        file.counter_signer = str(file_info_dict['Counter Signers'])
    except:
        pass

    # #file.printablestr_txt =
    # #file.byte_distribution =
    
    # 算分數
    data_dict = {}
    try:
        data_dict['AddressOfEntryPoint']=file_info_dict['AddressOfEntryPoint']
        data_dict['Characteristics']=file_info_dict['Characteristics']
        data_dict['Machine']=file_info_dict['Machine']
        data_dict['NumberOfSections']=file_info_dict['NumberOfSections']
        data_dict['TimeDateStamp']=file_info_dict['TimeDateStamp']
        data_dict['entropy']=file_info_dict['entropy']
        
        data_dict['file_size']=file_info_dict['file_size']
        data_dict['exec_ability']=file_info_dict['exec_ability']
        data_dict['network_ability']=file_info_dict['network_ability']
        data_dict['rw_ability']=file_info_dict['rw_ability']
        for i in range(len(file_info_dict['byte_summary'])):
            data_dict[i]=file_info_dict['byte_summary'][i]
    except:
        pass
    data_df = pd.DataFrame(data_dict,index=[0])
    orange_dt = pandas_to_orange(data_df)

    with open(os.path.join(settings.MEDIA_ROOT,'model',"tree.pkcls"), "rb") as f:   # tree.pkcls
        model = pickle.load(f)

    data = Orange.data.Table(orange_dt)  # 'test_data_bad.xlsx'
    pred_ind = model(data)  # array of predicted target values (indices)
    li = [model.domain.class_var.str_val(i) for i in pred_ind]  # convert to value names (strings)
    prob = model(data, model.Probs)  # array of predicted probabilities

    file.score = round(prob[0][1]*100)/10

    file.save()
    
    os.remove(filepath)
    #return "signer index: {} ,counter signer index: {}".format(file_info_dict['s_start'],file_info_dict['cs_start'])
    return "analysis {} task finished，score={}".format(filepath.split('/')[-1],str(prob[0][1]))
    # return FileInfo.objects.get(upload_id=upload_id)


# @shared_task
# def byte_analysis(filepath):
#     chunk_size = 8192
#     #printable_chars = set(bytes(string.printable,'ascii'))
#     printable_str_list = []
#     byte_list = [0] * 256
#     sha1 = hashlib.sha1()
#     byte_dic = {}

#     with open(filepath,'rb') as f:
#         while True:
#             chunk = f.read(chunk_size)
#             if not chunk:
#                 break
            
#             for byte in chunk:
#                 byte_list[byte] +=1
#             #__one_gram_byte_summary(chunk, byte_list)
#             #__byte_printable(chunk, printable_chars, printable_str_list)
#             sha1.update(chunk)
    
#     entropy = __entropy(byte_list)
    
#     for i in range(len(byte_list)):
#         byte_dic[i] = byte_list[i]

#     byte_analysis_dict = {
#         #'printable_strs' : printable_str_list,
#         'byte_summary' : byte_list,
#         'entropy' : entropy,
#         'file_sha1': sha1.hexdigest()
#     }
#     byte_analysis_dict.update(byte_dic)

#     return byte_analysis_dict

@shared_task
def file_hash(filepath):
    chunk_size = 8192
    sha1 = hashlib.sha1()
    with open(filepath,'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break        
            sha1.update(chunk)
    return sha1.hexdigest()

# @shared_task
# def __one_gram_byte_summary(chunk,byteList):
#     for byte in chunk:
#         byteList[byte] +=1
#     return byteList

# @shared_task       
# def __entropy(byteList):
#     entropy = 0
#     total = sum(byteList)
#     for item in byteList:
#         if item != 0 :
#             freq = item / total
#             entropy = entropy + freq * math.log(freq, 2)
#     entropy *= -1
#     return entropy

@shared_task
def byte_analysis(filepath):
    with open(filepath,'rb') as f:
        filebuffer = f.read()
        one_gram_dict = one_gram_byte_analysis(filebuffer)
        printable_strs = byte_printable(filebuffer)
    sha1 = hashlib_sha1()
    sha1.update(filebuffer)
    entropy = calc_entropy(one_gram_dict)
    
    byte_analysis_dict = {
        'printable_strs' : printable_strs,
        'entropy' : entropy,
        'file_sha1': sha1.hexdigest()
    }
    byte_analysis_dict.update(one_gram_dict)

    return byte_analysis_dict

@shared_task
def one_gram_byte_analysis(filebuffer):
    one_gram_byte_dict = {}
    for i in range(256):
        one_gram_byte_dict[hex(i)] = 0
    for byte in filebuffer:
        one_gram_byte_dict[hex(byte)] += 1
    
    return one_gram_byte_dict

@shared_task
def byte_printable(filebuffer):
    char_len_threshhold = 3
    printable_str_list = []
    printable_chars = set(bytes(string_printable,'ascii'))
    temp_bytes = b""
    for byte in filebuffer:
        if byte in printable_chars:
            temp_bytes += bytes([byte])
        
        elif not temp_bytes == b"\x00" and len(temp_bytes) > char_len_threshhold:
            printable_str_list.append(temp_bytes.decode("ascii"))
            temp_bytes = b""
        else:
            temp_bytes = b""
    return printable_str_list

@shared_task
def calc_entropy(byte_dict):
    entropy = 0
    total = sum(byte_dict.values())
    for key in byte_dict:
        if byte_dict[key] != 0 :
            freq = byte_dict[key] / total
            entropy = entropy + freq * math_log(freq, 2)
    entropy *= -1
    return entropy
    
@shared_task
def sigcheck(filepath):
    
    sigcheck_path = os.path.join(resourceDir,'sigcheck.exe')
    filepath = filepath.replace("\\", "//")
    sigcheck_dict={}
    args = ["wine", "\mnt\server\security_rabbit_linux\security_rabbit\media\exefiles\sigcheck64.exe", '-i', '-l', '-nobanner', "\mnt\server\security_rabbit_linux\security_rabbit\media//file_upload//"+filepath]
    pipe = subprocess.Popen(args, stdout=subprocess.PIPE)
    
    sigcheck_output = pipe.communicate()[0]
    sigcheck_str = ""

    sigcheck_str = sigcheck_output.decode('utf-8',"replace")
    #sigcheck_dict['process']=sigcheck_str
    #sigcheck_dict['args']=args
    #print(sigcheck_str)
    sigcheck_str = sigcheck_str.replace('\r\n\t'+'  ', '\n<Certificate>')
    sigcheck_str = sigcheck_str.replace('\r\n\t\t', '\n<Certi Info>')
    sigcheck_str = sigcheck_str.replace('\r\n\t', '\n<attribute>')
    sigcheck_str = sigcheck_str.replace('\t','')
    sigcheck_str += '<end>'
    #print(sigcheck_str)

    
    #sigcheck_dict['process']=sigcheck_str 
    for attr in re.findall('<attribute>.*',sigcheck_str):
        attr = attr.replace('<attribute>','')
        attribute_name, attribute_val = attr.split(":",1)
        sigcheck_dict["sigcheck_"+attribute_name] = attribute_val
    
    sigcheck_str_list = [line.replace('\n','').replace('\r','') for line in io.StringIO(sigcheck_str).readlines()]
    #sigcheck_dict['sig_li']=sigcheck_str_list
    signers_dict = __signers(sigcheck_str_list)

    sigcheck_dict.update(signers_dict)
    return sigcheck_dict
    
    # print(signers_dict)
    # print(sigcheck_dict)
   
@shared_task
def __signers(sigcheck_str_list):
    signer_list = []
    counter_signer_list = []
    signers_dict = {}
    try:
        signer_start_index = 0
        counter_signer_start_index = 0
        counter_signer = False
        tmp = []
        for index, sigcheck_str in enumerate(sigcheck_str_list):
            if '<attribute>Signers:' in sigcheck_str:
                signer_start_index = index
            elif '<attribute>Counter Signers' in sigcheck_str:
                counter_signer_start_index = index
                counter_signer = True
            elif '<Certificate>' in sigcheck_str:
                if tmp != [] and counter_signer == False:
                    signer_list.append(tmp)
                    tmp = []
                elif tmp != [] and counter_signer == True:
                    counter_signer_list.append(tmp)
                    tmp = []
                tmp.append(sigcheck_str_list[index].split('<Certificate> ')[-1])
            elif '<Certi Info>' in sigcheck_str:
                tmp.append(sigcheck_str_list[index].split('<Certi Info>')[-1])
                if index == len(sigcheck_str_list):
                    counter_signer_list.append(tmp)

        #signers_dict = {}
        #signers_dict['s_start']=signer_start_index
        #signers_dict['cs_start']=counter_signer_start_index
        
    except ValueError:
        #print(ValueError)
        pass
    except IndexError:
        pass
        #print(IndexError)

    signers_dict['Signers'] = signer_list
    signers_dict['Counter Signers'] = counter_signer_list

    #print(signers_dict)
    return signers_dict



#加殼
@shared_task
def check_pack(pe_file):
    signature_file = os.path.join(resourceDir,'userdb_filter.txt')
    signatures = None
    with open(signature_file,'r',encoding='utf-8') as f:
        sig_data = f.read()
        signatures = peutils.SignatureDatabase(data = sig_data)

    #matches = signatures.match(pe_file, ep_only = True)
    matchall = []
    matchall = signatures.match_all(pe_file, ep_only = True)
    if not matchall:
        matchall = []
    return { 'pack' : matchall }

@shared_task
def dll_import_analysis(pe_file):
    NETWORKING_AND_INTERNET_DLLS = ['dnsapi.dll', 'dhcpcsvc.dll', 'dhcpcsvc6.dll', 'dhcpsapi.dll', 'connect.dll', 
                           'httpapi.dll', 'netshell.dll', 'iphlpapi.dll', 'netfwv6.dll', 'dhcpcsvc.dll',
                           'hnetcfg.dll', 'netapi32.dll', 'qosname.dll', 'rpcrt4.dll', 'mgmtapi.dll', 'snmpapi.dll',
                           'smbwmiv2.dll', 'tapi32.dll', 'netapi32.dll', 'davclnt.dll', 'websocket.dll',
                           'bthprops.dll', 'wifidisplay.dll', 'wlanapi.dll', 'wcmapi.dll', 'fwpuclnt.dll',
                           'firewallapi.dll', 'winhttp.dll', 'wininet.dll', 'wnvapi.dll', 'ws2_32.dll',
                           'webservices.dll']
    FILE_MANAGEMENT_DLLS = ['advapi32.dll', 'kernel32.dll', 'wofutil.dll', 'lz32.dll']
    EXECUTION_FUNCTIONS = ['winexec']
    
    network_ability = []
    rw_ability = []
    exec_ability = []
    dll_analysis_dict = {}
    n_bool = False
    rw_bool = False
    exec_bool = False

    pe_file.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT']])
    if hasattr(pe_file, 'DIRECTORY_ENTRY_IMPORT'): 
        for entry in pe_file.DIRECTORY_ENTRY_IMPORT:
            dll = entry.dll.decode('utf-8').lower()
            # check if there is a matching dll import
            if dll in NETWORKING_AND_INTERNET_DLLS:
                network_ability.append(dll)
            if dll in FILE_MANAGEMENT_DLLS:
                rw_ability.append(dll)
            
            for imp in entry.imports:
                # check if there is a matching function import
                if imp in EXECUTION_FUNCTIONS:
                    exec_ability.append((hex(imp.address),imp.name.decode('utf-8')))
            
            if (network_ability != []): 
                n_bool=True 
            if (rw_ability != []): 
                rw_bool=True 
            if (exec_ability != []): 
                exec_bool=True 
                
            dll_analysis_dict = {
                'network_ability' : n_bool,
                'network_ability_dic' : network_ability,
                'rw_ability' : rw_bool,
                'rw_ability_dic' : rw_ability,
                'exec_ability' : exec_bool,
                'exec_ability_dic' : exec_ability,

            }
    return dll_analysis_dict

@shared_task
def pefile_infos(pe_file):

    # basic info
    basic_dic = {}
    basic_dic['Machine'] = pe_file.FILE_HEADER.Machine
    basic_dic['NumberOfSections'] = pe_file.FILE_HEADER.NumberOfSections
    basic_dic['TimeDateStamp'] = pe_file.FILE_HEADER.TimeDateStamp
    basic_dic['Characteristics'] = pe_file.FILE_HEADER.Characteristics
    
    basic_dic['AddressOfEntryPoint'] = pe_file.OPTIONAL_HEADER.AddressOfEntryPoint
    basic_dic['ImageBase'] = pe_file.OPTIONAL_HEADER.ImageBase
    
    # section_info [(Name, Virtual Address, Virtual Size, Raw Size, Entropy, SHA256, MD5), ...]
    section_li = []
    for section in pe_file.sections:
        section_li.append([section.Name.decode('ascii').rstrip('\x00'), section.VirtualAddress, section.Misc_VirtualSize, section.SizeOfRawData, section.get_entropy(), section.get_hash_sha256(), section.get_hash_md5()])
    basic_dic['Section_info'] = section_li
    
    # import_info { dll : [API, API,....], dll : [API, API,....], ...}
    # pe_file.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT']])   
    import_dic = {}
    pe_file.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT']])
    if hasattr(pe_file, 'DIRECTORY_ENTRY_IMPORT'):
        for entry in pe_file.DIRECTORY_ENTRY_IMPORT:
            import_dic[entry.dll.decode('ascii')] = []

            for imp in entry.imports:
                funcname = None
                if not imp.name:  #可能會發生沒有imp.name的情形，為了避免跑錯所以我自己參考pefile套件自己加的
                    funcname = ordlookup.ordLookup(entry.dll.lower(), imp.ordinal, make_name=True)
                    if not funcname:
                        raise Exception("Unable to look up ordinal %s:%04x" % (entry.dll, imp.ordinal))
                else:
                    funcname = imp.name
                    import_dic[entry.dll.decode('ascii')].append(imp.name.decode('ascii'))

                if not funcname:
                    continue

            # print(import_dic[entry.dll.decode('ascii')])
    # print(import_dic)
    basic_dic['Import_directories'] = import_dic
    
    # export_info   不是每個檔案都有，如果有問題的話可以只保留 exp.name.decode('ascii')即可
    # pe_file.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT']])
    export_li = []
    pe_file.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT']])
    if hasattr(pe_file, 'DIRECTORY_ENTRY_EXPORT'):
        for exp in pe_file.DIRECTORY_ENTRY_EXPORT.symbols:
            export_li.append(exp.name.decode('ascii'))    # export_li.append([hex(pe_file.OPTIONAL_HEADER.ImageBase + exp.address), exp.name.decode('ascii'), exp.ordinal])
    basic_dic['Export_directories'] = export_li
    
    # dump_info
    # pe.dump_info() 這個可以先照原本存在txt裡面~ 我有空再來想想看怎麼處理其他雜七雜八的資訊比較好~
            
    return basic_dic
