from proto import Proto
import os
import json
def from_proto(path:str)->Proto:
    #get a proto from .wbt file
    if os.path.exists(path):
        with open(path,"r") as f:
            text:str=f.read()
        parse(text)
    else:
        raise(FileNotFoundError("file not found"))
def isValueLine(line:str)->bool:
    if len(line)<2:
        return False
    if '{' in line:
        return False
    if '[' in line:
        return False
    if ' ' not in line:
        return False
    return True
def contain_list(line:str)->int:# -1 means false, >0 index
    prev_space:bool=True
    count:int=0
    for index in range(len(line)):
        if line[index]in [' ','\t']:
            if not prev_space:
                count+=1
            prev_space=True
        else:
            prev_space=False
            if count>=1:
                return index
    return -1
    
def name_start(line:str):
    prev_space:bool=True
    count:int=0
    begin:int=0
    lock:bool=True
    first_char:bool=False
    for index in range(len(line)):
        if line[index] in [' ','\t']:
            if not prev_space:
                count+=1
            prev_space=True
        else:
            if prev_space:
                if not first_char:begin=index
            if not first_char:
                first_char=True
            lock=False
            if count>=1:
                if '{' not in line:
                    return begin,index
                if not lock:
                    if line[index] == '{':
                        return begin,index
            prev_space=False
    return -1
def contain_a_digt(line:str)->bool:
    if ':' not in line:
        raise(SyntaxError("missing : in line'{}'".format(line)))
    for i in line[line.index(':'):] :
        if i.isdigit():
          return True 
    return False
def only_package(line:str)->bool:
    if ':' not in line:
        raise(SyntaxError("missing : in line'{}'".format(line)))
    for i in line[line.index(':'):] :
        if i.isdigit():
          return False 
    return True
def parse(code:str)->None:#Proto:
    text:list[str]=code.split("\n")
    line_num:int=0
    names_def_levels:dict[str,int|tuple[int,int]]=[]
    first_ele:bool=False
    first_ele_index:int=0
    for line_num in range(len(text)):
        #print(i)
        if '{' in text[line_num]:
            first_ele = True
        if not first_ele :
            first_ele_index+=1
            continue
        else:
            if (']' in text[line_num]):
                text[line_num]=text[line_num].replace(']','}')

            place:int=contain_list(text[line_num])
            name_place:int|tuple[int,int]=name_start(text[line_num])
            names_def_levels.append({
              'index':line_num,

            })
            if place>0:
                if '{' not in text[line_num]:
                    if ('"' not in text[line_num]):
                        if ('[' in text[line_num]):
                            text[line_num]=text[line_num].replace('[','{')

                        elif ('[' not in text[line_num]):
                            text[line_num] =text[line_num][:place] + ": ["+text[line_num][place:].replace(' ',',') + ']'
                            if line_num!=len(text):
                                if contain_list(text[line_num+1])>-1:
                                    text[line_num]+=','
                    else:
                        text[line_num]=text[line_num][:place]+": "+text[line_num][place:]
                if type(name_place)==tuple:
                    text[line_num]=text[line_num][:name_place[0]]+'"'+text[line_num][name_place[0]:name_place[1]-1]+'"'+text[line_num][name_place[1]-1:]
                if '{' in text[line_num]:text[line_num]=text[line_num].replace('{',' : {')
        text= [i if i!='}' else '},' for i in text]
    new_code:str='{'+'\n'.join(text[first_ele_index:])+'}'
    with open('f.json','w',encoding='utf-8') as f:
      print(new_code,file=f)
    json.loads(new_code)
