from proto import Proto
import os
import json
def first_char_index(line:str)->int:
    for index in range(len(line)):
        if line[index] not in [' ','\t']:
            return index
    return -1
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
    first_ele:bool=False
    first_ele_index:int=0
    for line_num in range(len(text)):
        ##print(i)
        if "IS" in text[line_num].split():
            text[line_num]=text[line_num].replace('IS','"IS')+'"'
        if "USE" in text[line_num].split():
            first_char=first_char_index(text[line_num])
            if text[line_num][first_char:first_char+3]=='USE':
                text[line_num]=text[line_num].replace('USE','USE "USE')+'"'
            else:
                text[line_num]=text[line_num].replace('USE','"USE')+'"'
        if '{' in text[line_num]:
            first_ele = True
        if not first_ele :
            first_ele_index+=1
            continue
        else:
            next_line:str=text[line_num+1] if line_num<len(text)-1 else ''
            text[line_num]=adapt_line(text[line_num],next_line,line_num!=len(text))
    text=list(map(handel_url,text))
    #print('p1:',text)
    text=write_commas(text)
    new_code:str='{'+'\n'.join(text[first_ele_index:])+'}'
    #new_code=new_code.replace('}','},')
    with open('f.json','w',encoding='utf-8') as f:
      print(new_code,file=f)
    obj=dict(json.loads(new_code))
    #print(obj)
    return obj

def handel_url(line:str):
    if ("http" in line)or ("webots" in line):
        first_char:int=first_char_index(line)
        line=line[:first_char]+'"url":'+line[first_char:]
    return line


def adapt_line(line:str,next_line:str,last:bool)->str:
    if (']' in line):
        line=line.replace(']','}')

    place:int=contain_list(line)
    name_place:int|tuple[int,int]=name_start(line)
    if place>0:
        if '{' not in line:
            if ('"' not in line):
                if ('[' in line):
                    line=line.replace('[','{')

                elif ('[' not in line):
                    line =line[:place] + ": ["+line[place:].replace(' ',',') + ']'
                    if last:
                        if contain_list(next_line)>-1:
                            line+=','

            else:
                line=line[:place]+": "+line[place:]
        if type(name_place)==tuple:
            line=line[:name_place[0]]+'"'+line[name_place[0]:name_place[1]-1]+'"'+line[name_place[1]-1:]
        if '{' in line:line=line.replace('{',' : {')
    return line

def write_commas(text:list[str])->list[str]:
    prev_def_levels:list[int]=[]
    line_index:int=0
    def_level:int=first_char_index(text[line_index])
    prev_def_levels.append(def_level)

    for line_index in range(1,len(text)-1):
        def_level=first_char_index(text[line_index])
        next_def_level:int=first_char_index(text[line_index+1])
        if len(text[line_index]) > 0:
            if def_level==next_def_level:
                if (def_level in prev_def_levels) and (def_level>0):
                    if text[line_index][-1]not in [',',' ']:
                        if text[line_index+1][-1] not in ['}']:
                            text[line_index]=text[line_index]+','

                elif text[line_index][-1]not in [',',' ']:
                    if text[line_index+1][next_def_level]=='"':
                        if text[line_index+1][-1] not in ['}']:
                            text[line_index]=text[line_index]+','
        prev_def_levels.append(def_level)        
    return text
