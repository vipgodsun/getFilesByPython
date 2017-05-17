#! /usr/bin/env python
# coding=utf-8
import time
import tqdm
import sys
import os
import shutil
import re
import datetime

totalDict = {}

def test(source_file_directory, timedate, force):
    pattern = re.compile('%s\d\d.\d\d\d'%(timedate))
    for entry in os.scandir(source_file_directory):
        if not entry.name.startswith('.') and entry.is_file() and pattern.match(entry.name):
            fullpathSource = entry.path
            print(fullpathSource)
            fullFileNameTarget = fullpathSource.replace(r"\\172.19.1.151", r"D:\MS")
            fullpathTarget = fullFileNameTarget.replace(entry.name,"")
            print(fullpathTarget)
            if not os.path.exists(fullpathTarget):
                os.makedirs(fullpathTarget)
            if (force == 0):
                if(os.path.exists(fullFileNameTarget)):
                    if(os.path.getsize(fullFileNameTarget) < os.path.getsize(fullpathSource)):
                        totalDict[fullpathSource] = fullpathTarget
                else:
                    totalDict[fullpathSource] = fullpathTarget
                    print("777777777777777")
            if(force == 1):
                totalDict[fullpathSource] = fullpathTarget
        if entry.is_dir():
            print(entry.path)
            test(entry.path, timedate, force)


def copyDictDir(micapsdict):
    counter = len(micapsdict)
    with tqdm.tqdm(total=counter, unit='B', unit_scale=True) as pbar:
        for k, v in micapsdict.items():
            shutil.copy(k, v)
            pbar.update(1)
        

def copySurfaceFile(fromdir, todir, timedate, force):
    sizecounter = 0
    print(timedate)
    pattern = re.compile('%s\d\d.\d\d\d'%(timedate))
    fileDict = {}
    for parent, dirnames, files in os.walk(fromdir, topdown=True):
        for filename in files:
            if pattern.match(filename):
                fullpathSource = os.path.join(parent, filename)
                print(fullpathSource)
                fullpathTarget = parent.replace(r"\\172.19.1.151", r"D:\MS")
                fullFileNameTarget = fullpathSource.replace(r"\\172.19.1.151", r"D:\MS")
                print(fullFileNameTarget)
                if not os.path.exists(fullpathTarget):
                    os.makedirs(fullpathTarget)
                if (force == 0):
                    if(os.path.exists(fullFileNameTarget)):
                        if(os.path.getsize(fullFileNameTarget) < os.path.getsize(fullpathSource)):
                            sizecounter = sizecounter + 1
                            fileDict[fullpathSource] = fullpathTarget
                            print(sizecounter)
                    else:
                        sizecounter = sizecounter + 1
                        fileDict[fullpathSource] = fullpathTarget
                        print(sizecounter)
                if(force == 1):
                    sizecounter = sizecounter + 1
                    fileDict[fullpathSource] = fullpathTarget
                    print(sizecounter)
    print("需要调取的文件总数为:")
    print(sizecounter)
    with tqdm.tqdm(total=sizecounter, unit='B', unit_scale=True) as pbar:
        for k, v in fileDict.items():
            shutil.copy(k, v)
            pbar.update(1)


def copyFaxFile(fromdir, todir,force):
    sizecounter = 0
    fileDict = {}
    for parent, dirnames, files in os.walk(fromdir):
        for filename in files:
            fullpathSource = os.path.join(parent, filename)
            print(fullpathSource)
            fullpathTarget = parent.replace(r"\\172.19.1.151", r"D:\MS")
            fullFileNameTarget = fullpathSource.replace(r"\\172.19.1.151", r"D:\MS")
            print(fullFileNameTarget)
            if not os.path.exists(fullpathTarget):
                os.makedirs(fullpathTarget)
            if (force == 0):
                if(os.path.exists(fullFileNameTarget)):
                    if(os.path.getsize(fullFileNameTarget) < os.path.getsize(fullpathSource)):
                        sizecounter = sizecounter + 1
                        fileDict[fullpathSource] = fullpathTarget
                        print(sizecounter)
                else:
                    sizecounter = sizecounter + 1
                    fileDict[fullpathSource] = fullpathTarget
                    print(sizecounter)
            if(force == 1):
                sizecounter = sizecounter + 1
                fileDict[fullpathSource] = fullpathTarget
                print(sizecounter)
    print("需要调取的文件总数为:")
    print(sizecounter)
    with tqdm.tqdm(total=sizecounter, unit='B', unit_scale=True) as pbar:
        for k, v in fileDict.items():
            shutil.copy(k, v)
            pbar.update(1)


def getTimeDateNow(timeType):
    if(timeType == 1 or timeType == 3):
        nowTime = datetime.datetime.now()
        nowTime = nowTime.strftime("%y%m%d")
        return(nowTime)
    if(timeType == 2 or timeType == 4):
        beforeTime = datetime.datetime.now() + datetime.timedelta(days=-1)
        beforeTime = beforeTime.strftime("%y%m%d")
        return(beforeTime)


def beginGet(userGetType):
    if(userGetType == "1"):
        fileDateTime = getTimeDateNow(1)
        test(source_file_directory, fileDateTime, 0)
        copyDictDir(totalDict)
        #copySurfaceFile(source_file_directory, target_file_directory,fileDateTime,0)
    if(userGetType == "2"):
        fileDateTime = getTimeDateNow(2)
        test(source_file_directory, fileDateTime, 0)
        copyDictDir(totalDict)
        #copySurfaceFile(source_file_directory, target_file_directory,fileDateTime,0)
    if(userGetType == "3"):
        fileDateTime = getTimeDateNow(3)
        test(source_file_directory, fileDateTime, 1)
        copyDictDir(totalDict)
        #copySurfaceFile(source_file_directory, target_file_directory,fileDateTime,1)
    if(userGetType == "4"):
        fileDateTime = getTimeDateNow(4)
        test(source_file_directory, fileDateTime, 1)
        copyDictDir(totalDict)
        #copySurfaceFile(source_file_directory, target_file_directory,fileDateTime,1)


print("请输入你需要调取资料的序号:")
print("1.地面资料 2.高空资料 3.日本传真")
fileType = input()
if (fileType == "1"):
    source_file_directory = "\\\\172.19.1.151\micaps\surface"
    target_file_directory = "D:\MS\micaps\surface"
    source_storage_available = os.path.isdir(source_file_directory)
    if source_storage_available:
        print("Backup storage already connected.")
        #print(os.listdir(source_file_directory))
        print("你所需要的资料是地面资料,请输入你需要调取的地面资料时次:")
        print("1.今天地面资料非强制覆盖 2.昨天地面资料非强制覆盖")
        print("3.今天地面资料强制覆盖 4.昨天地面资料强制覆盖")
        fileGetType = input()
        beginGet(fileGetType)
    else:
        print("Connecting to backup storage.")
        mount_command = 'net use \\\\172.19.1.151\micaps\surface "" /USER:yjs'
        print(mount_command)
        os.system(mount_command)
        target_storage_available = os.path.isdir(source_file_directory)
        if source_storage_available:
            print("Connection success.")
            print("你所需要的资料是地面资料,请输入你需要调取的地面资料时次:")
            print("1.今天地面资料非强制覆盖 2.昨天地面资料非强制覆盖")
            print("3.今天地面资料强制覆盖 4.昨天地面资料强制覆盖")
            fileGetType = input()
            beginGet(fileGetType)
        else:
            raise Exception("Failed to find storage directory.")
if (fileType == "2"):
    print("你所需要的资料是高空资料")
    source_file_directory = "\\\\172.19.1.151\micaps\high"
    target_file_directory = "D:\MS\micaps\high"
    source_storage_available = os.path.isdir(source_file_directory)
    if source_storage_available:
        print("Backup storage already connected.")
        print("你所需要的资料是高空资料,请输入你需要调取的高空资料时次:")
        print("1.今天高空资料非强制覆盖 2.昨天高空资料非强制覆盖")
        print("3.今天高空资料强制覆盖 4.昨天高空资料强制覆盖")
        fileGetType = input()
        beginGet(fileGetType)
    else:
        print("Connecting to backup storage.")
        mount_command = 'net use \\\\172.19.1.151\micaps\high "" /USER:yjs'
        print(mount_command)
        os.system(mount_command)
        target_storage_available = os.path.isdir(source_file_directory)
        if source_storage_available:
            print("Connection success.")
            print("你所需要的资料是高空资料,请输入你需要调取的高空资料时次:")
            print("1.今天高空资料非强制覆盖 2.昨天高空资料非强制覆盖")
            print("3.今天高空资料强制覆盖 4.昨天高空资料强制覆盖")
            fileGetType = input()
            beginGet(fileGetType)
        else:
            raise Exception("Failed to find storage directory.")
if (fileType == "3"):
    print("你所需要的资料是日本传真")
    source_file_directory = "\\\\172.19.1.151\micaps\\fax\japan"
    target_file_directory = "D:\MS\micaps\fax\japan"
    source_storage_available = os.path.isdir(source_file_directory)
    if source_storage_available:
        print("Backup storage already connected.")
        print("你所需要的资料是日本传真资料,请输入你需要调取的日本传真资料时次:")
        print("1.日本传真资料非强制覆盖 2.日本传真资料强制覆盖")
        fileGetType = input()
        if(fileGetType == "1"):
            fileDateTime = getTimeDateNow(1)
            copyFaxFile(source_file_directory, target_file_directory,0)
        if(fileGetType == "2"):
            fileDateTime = getTimeDateNow(2)
            copyFaxFile(source_file_directory, target_file_directory,1)
    else:
        print("Connecting to backup storage.")
        mount_command = 'net use \\\\172.19.1.151\micaps\\fax\japan "" /USER:yjs'
        print(mount_command)
        os.system(mount_command)
        target_storage_available = os.path.isdir(source_file_directory)
        if source_storage_available:
            print("Connection success.")
            print("你所需要的资料是日本传真资料,请输入你需要调取的日本传真资料时次:")
            print("1.今天日本传真资料非强制覆盖 2.昨天日本传真资料强制覆盖")
            fileGetType = input()
            if(fileGetType == "1"):
                fileDateTime = getTimeDateNow(1)
                copyFaxFile(source_file_directory, target_file_directory,0)
            if(fileGetType == "2"):
                fileDateTime = getTimeDateNow(2)
                copyFaxFile(source_file_directory, target_file_directory,1)
        else:
            raise Exception("Failed to find storage directory.")
# for i in tqdm.tqdm(range(100)):
#     time.sleep(0.05)...