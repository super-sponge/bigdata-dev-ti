#!/usr/bin/python
#coding:utf8



import os
import sys
import hashlib

reload(sys)
sys.setdefaultencoding('utf-8')

def dirlist(path, allfile):
    filelist =  os.listdir(path)

    for filename in filelist:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dirlist(filepath, allfile)
        else:
            print filepath
            allfile.append((filepath, CalcSha1(filepath)))
    return allfile


def CalcSha1(filepath):
    with open(filepath,'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
    return hash

def CalcMD5(filepath):
    with open(filepath,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()        
    return hash

def delFile(files):
    for file in files:
        os.remove(file)
if __name__=='__main__':    
    dirOut = u"G:\\picduplicate_delete.txt"
    dirOutMD5 = u"G:\\file_md5.txt"
    lstPic = dirlist(u"G:\\整理后视频", [])
    lstPic = dirlist(u"G:\\整理后照片", lstPic)
    lstPic = dirlist(u"G:\\私人相册", lstPic)    
	
    mapPic = {}
    with open(dirOutMD5,'w') as fmd5:
        for item in lstPic:	
            if mapPic.has_key(item[1]):
                mapPic[item[1]].append(item[0])
            else:
                mapPic[item[1]] = [item[0],]
            fmd5.write(item[0] + ";" + item[1] + "\n")	
    with open(dirOut,'w') as f:
        for key, value in mapPic.items():
            if len(value) > 1 :                
                f.write(key + ";" + ";".join(value) + "\n")
                delFile(value[1:])
                print key , value[1:]
