from dotenv import load_dotenv
from typing import Dict,Any
import requests
import os

#加载环境变量
load_dotenv()

#获取搜索API密钥
search_api = os.getenv("BAIDU_API_KEY")

#设置调用搜索API的地址
url = os.getenv("BAIDU_URL") 



def search(details):

    #1.设置请求头,设置数据格式为json,并加上API密钥
    headers = {
        "Content-Type":"application/json",#设置数据的格式(json)
        "Authorization":f"Bearer {search_api}" #搜索API的密钥
    }

    #2.设置请求体
    data = {
        "messages":[
            {"role":"user","content":details}
        ], #搜索输入，输入要搜索的内容
        "search_source":"baidu_search_v2",#使用的搜索引擎版本(现为默认版本)
        "search_recency_filter":"semiyear" #搜索的时间范围(semiyear:最近180天)
    }



    try:
        #3.发送请求(选用POST请求)
        result = requests.request("POST",url,headers=headers,json=data)
    
        #3-1.将响应的json数据解析成字典(Dict)
        result_s = result.json()

    except requests.exceptions.RequestException as e:
        return f"搜索失败!错误信息为:{type(e).__name__}:{e}"

    except ValueError as e:
        return f"搜索失败!错误信息为:{type(e).__name__}:{e}"

    except Exception as e:
        return f"搜索失败!错误信息为:{type(e).__name__}:{e}"
    



    #4.解析响应体
    #4-1.判断状态码,状态码反应API的调用状态,是判断成功与错误原因的关键
    if result.status_code != 200:
        return f"搜索失败!当前状态码为:{result.status_code}"


    #4-2.判断本次请求的ID是否存在，也是判断是否返回内容的关键
    if not result_s.get("request_id") and result_s.get("references")==None:
        return f"搜索失败!本次请求ID为:空。\n业务错误码为:{result_s.get('code')}\n错误消息为:{result_s.get('message')}"

    #4-3.过滤信息,去除无用的杂音
    #创建空的列表，用来装过滤好的内容
    result_new:list[Dict[str,Any]] =[] 

    #指定要获取的内容，其他过滤掉
    keys_want = ["id","content","date","title","url"]






    #获取搜索返回的详细列表(列表套字典)
    result_sx = result_s.get("references")

    #计算列表长度
    result_len = len(result_sx)

    #如果result_sx的长度小于10
    if result_len <=6:
        #将result_sx中的每一个字典提取出来
        for chenk in result_sx:
            #再提取指定内容的键名集合
            keys = list(filter(lambda k: k in keys_want,chenk))
            chenks ={}

            #根据指定内容的键名集合,填入相应的值,组成新的字典.chenk类型是字典
            for i in range(0,len(keys)):
                #用来装已过滤好的内容,
                
                chenks[keys[i]] = chenk[keys[i]]

            #将提取好的新字典内容放入列表里
            result_new.append(chenks)

    #大于10的只取前10条内容
    else:
        #将result_sx中的每一个字典提取出来
        for chenk in result_sx[:6]:
            #再提取指定内容的键名集合
            keys = list(filter(lambda k: k in keys_want,chenk))
            chenks ={}

            #根据指定内容的键名集合,填入相应的值,组成新的字典.chenk类型是字典
            for i in range(0,len(keys)):
                #用来装已过滤好的内容,
                chenks[keys[i]] = chenk[keys[i]]

            #将提取好的新字典内容放入列表里
            result_new.append(chenks)


        




    
    return result_new



tool_detail = {
    "tool_name":"search",
    "description":(
        "1.工具描述:这是一个通过调用百度API的搜索工具,可通过输入想要搜索的字符串内容进行信息搜索。"
        "2.触发这些条件时必须使用工具:遇到任何不确定的问题，没有把握的问题，在记忆里没有的问题，比如最近发生的热点以及新闻，事件等；必须调用搜索工具进行查找，根据查找内容再给出答案。"
        "3.约束:禁止在未知和不确定的情况下,不调用此工具而凭空捏造答案"
    ),
    "func":search,
    "parameters":{
        "type":"object",
        "properties":{
            "details":{
                "type":"string",
                "description":"1.入参类型为非空字符串,2.入参内容为你想要搜索的内容。"
            }
        },
        "required":["details"]
    }
}






if __name__=='__main__':
    que = "DeepSeek_Harness和Coedx有什么区别"
    action = search(que)
    print(action)



