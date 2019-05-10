
import re
import json
import sys
import os

def searchTxtFile():
    fileList = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == '.txt']
    return fileList

def txt2json(filename):
    if os.path.splitext(filename)[1] != '.txt':
        return
    print('try transfer %s to json' % filename)
    list_sops = []
    dict_sop = {}
    dict_sub_sop = {}
    notes = ''
    list_sub_sop = []

    # 注意编码问题,txt unicode文本,需使用utf-16打开！！！
    with open(filename, "r", encoding="utf-16") as f:
    # with open(filename, "r") as f:
        lines = f.readlines()

        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
        
            # 3. xxx 一级目录，过滤，不处理
            if re.match(r'^\d{0,10}\. ', line):
                print('remove: ' + line)
                continue

            if re.match(r'^\d{0,10}\.\d{0,10}\. ', line):
                # 3.3. xxx 二级目录，含三级目录，处理三级目录
                if len(list_sub_sop) > 0:
                    dict_sub_sop['note'] = notes.strip()
                    notes = ''
                    list_sub_sop.append(dict_sub_sop.copy())                
                    dict_sub_sop.clear()
                    dict_sop['note'] = list_sub_sop.copy()
                    list_sub_sop.clear()
                    list_sops.append(dict_sop.copy())
                # notes非空,说明仅含二级目录
                if len(notes) > 0:
                    dict_sop['note'] = notes.strip()
                    notes = ''
                    list_sops.append(dict_sop.copy())

                dict_sop['title'] = line
                continue

            if re.match(r'^\d{0,10}\.\d{0,10}\.\d{0,10}\.', line) and (None == re.match(r'^\d{0,10}\.\d{0,10}\.\d{0,10}\.\d{0,10}\.', line)):
                # 三级目录处理
                if len(notes) > 0:
                    dict_sub_sop['note'] = notes.strip()
                    notes = ''
                    list_sub_sop.append(dict_sub_sop.copy())
                dict_sub_sop['title'] = line
                continue

            notes += line + '%0A'

        if len(list_sub_sop) > 0:
            dict_sub_sop['note'] = notes.strip()
            list_sub_sop.append(dict_sub_sop.copy())
            dict_sop['note'] = list_sub_sop.copy()
            list_sops.append(dict_sop.copy())                
            dict_sub_sop.clear()
            notes = ''
            list_sub_sop.clear()
                
        if len(notes) > 0:
            dict_sop['note'] = notes.strip()
            list_sops.append(dict_sop.copy())
            notes = ''

        dst = open(filename + '.json', "w", encoding="utf-8")
        json.dump(list_sops, dst, ensure_ascii=False)
        dst.close()
    

if __name__ == '__main__':
    flist = searchTxtFile()
    for x in flist:
        txt2json(x)
