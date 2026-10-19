from datetime import datetime

def get_time():
    now = datetime.now()

    week =["周一","周二","周三","周四","周五","周六","周日"]


    #将元组数据转为str字符串
    time = now.strftime("%Y-%m-%d %H:%M:%S"),week[now.weekday()]

    times = ",".join(map(str,time))

    return f"当前时间为:{times}"
    




tool_detail = {
    "tool_name":"get_time",
    "description":(
        "1.工具描述:该工具的能力是获取当前日期和时间;不需要入参,可以直接调用。"
        "2.触发这些条件时必须使用工具:a.用户声明需要获取当前时间,日期等;b.用户问题里有'昨天/今天/明天/后天/周几/一周后/未来几天'等等时间段,日期的词"
        "3.约束:禁止编造时间和日期"
        ),
    "func":get_time,
    "parameters":{
        "type":"object",#即使函数没有入参,也要用object,否则会报错
        "properties":{}
        }
    }








if __name__=='__main__':
    a =get_time()
    print(a)