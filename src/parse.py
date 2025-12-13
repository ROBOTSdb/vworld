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
    names_def_levels:dict[str,int|tuple[int,int]]=[]
    first_ele:bool=False
    first_ele_index:int=0
    for line_num in range(len(text)):
        ##print(i)
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
              'name_place':name_place
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
    #print('p1:',text)
    text=write_commas(text)
    new_code:str='{'+'\n'.join(text[first_ele_index:])+'}'
    #new_code=new_code.replace('}','},')
    with open('f.json','w',encoding='utf-8') as f:
      print(new_code,file=f)
    obj=dict(json.loads(new_code))
    #print(obj)
    return obj
def write_commas(text:list[str])->list[str]:
    prev_def_levels:list[int]=[]
    line_index:int=0
    while line_index<len(text)-1:
        firstCharIndex:int=first_char_index(text[line_index])
        next_line_firstCharIndex=first_char_index(text[line_index+1])
        if firstCharIndex>-1:
            if firstCharIndex>=next_line_firstCharIndex:
                print(line_index)
                text[line_index]=text[line_index][:firstCharIndex]+',_+_+_+_+'+text[line_index][firstCharIndex:]
            if text[line_index][firstCharIndex]=='[':
                prev_def_levels.append(firstCharIndex)
            if text[line_index][firstCharIndex]==']':
                prev_def_levels.pop()
            if text[line_index][firstCharIndex] in ['}' ,']']:
                if len(prev_def_levels)>0:
                    if firstCharIndex<prev_def_levels[-1]:
                        text[line_index]=text[line_index][:prev_def_levels[0]]+','+text[line_index][prev_def_levels[0]:]
        line_index+=1
        
    return text
"""        
    proto:Proto=Proto(**dict(json.loads(str(text))))
    return proto"""

(parse("""#VRML_SIM R2025a utf8

EXTERNPROTO "https://raw.githubusercontent.com/cyberbotics/webots/R2025a/projects/objects/backgrounds/protos/TexturedBackground.proto"
EXTERNPROTO "https://raw.githubusercontent.com/cyberbotics/webots/R2025a/projects/objects/backgrounds/protos/TexturedBackgroundLight.proto"
EXTERNPROTO "https://raw.githubusercontent.com/cyberbotics/webots/R2025a/projects/objects/floors/protos/RectangleArena.proto"

WorldInfo {
}
Viewpoint {
  orientation 0.27373459355434776 0.03984522123410845 -0.9609795682721047 2.8636329465408457
  position 0.7357993402763815 0.4268963339358584 0.4381254455861484
}
TexturedBackground {
}
TexturedBackgroundLight {
}
RectangleArena {
}
Robot {
  translation 0 0 0.1
  children [
    Solid {
      translation 0 0.075 0.05
      children [
        HingeJoint {
          jointParameters HingeJointParameters {
            position 67.58400000000005
            axis 0 1 0
          }
          device [
            RotationalMotor {
              name "motor"
            }
          ]
          endPoint Solid {
            rotation 0 1 0 4.752146928204181
            children [
              Solid {
                translation 0 0.025 0.075
                children [
                  Shape {
                    appearance PBRAppearance {
                      baseColor 1 0 0
                    }
                    geometry Box {
                      size 0.05 0.05 0.2
                    }
                  }
                ]
              }
              Shape {
                appearance PBRAppearance {
                  baseColor 1 0 0
                }
                geometry Box {
                  size 0.05 0.05 0.05
                }
              }
            ]
          }
        }
      ]
      name "solid(1)"
    }
    Solid {
      children [
        Transform {
          children [
            DEF shape Shape {
              appearance PBRAppearance {
              }
              geometry Box {
                size 0.1 0.1 0.2
              }
            }
          ]
        }
      ]
    }
  ]
  controller "arm_hand"
}
"""))