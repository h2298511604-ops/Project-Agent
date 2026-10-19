import os

#1.先找出现在这个文件(save_note.py)的位置
site = os.path.abspath(__file__)

#2.找出这个文件(save_note.py)的父级目录地址
BASE_DIR = os.path.dirname(site)

#3.将父级目录地址和要写入的文件名用"\"拼一起，就变成这个文件的地址
NOTES_FILE = os.path.join(BASE_DIR,"save_note.txt")




def save_note(note:str):

    #检验传入的参数是否为str字符串类型
    if not isinstance(note,str):
        return f"写入失败:输入参数必须是字符串,现传入的参数类型为:{type(note).__name__}"

    #传入的参数不能为空
    if not note.strip():
        return f"写入失败:输入参数为空!请写入字符串类型的内容"

    #在指定的文件里写入内容，如果文件不存在，就会以指定文件的名字创建一个，再写入
    with open(NOTES_FILE,"a",encoding="utf-8") as f:
        f.write(f"\n{note}\n")

    return note




tool_detail ={
    "tool_name":"save_note",
    "description":(
        "1.工具描述:工具的能力是能够写入或者保存一段字符串到指定的文件中"
        "2.触发这些条件时必须使用工具:a.用户明确要求将：某段文字/内容,某个结果,或者一段记录等，保存下来"
        "3.约束:a.不得在未经用户允许的情况下,擅自保存某些记录和内容"),
    "func":save_note,
    "parameters":{
        "type":"object",
        "properties":{
            "note":{
                "type":"string",
                "description":"入参必须是一段str字符串"
            }
        },
        "required":["note"]

    }
}


if __name__ =='__main__':
    prompt="今天给agent添加了三个工具!!"
    action = save_note(prompt)
    print(action)
    print(os.path.abspath(__file__))
    print(BASE_DIR)
    print(NOTES_FILE)