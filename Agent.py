from LLM_client import llm_client
from ToolExecutor import toolExecutor,tool_dict
from typing import Dict,List,Any
from Prompt import SYSTEM_PROMPT
import json


class Agent:
    def __init__(self,LLM_client:llm_client(),toolExecutor:toolExecutor(),tool_dict:Dict):
        self.llm_client = LLM_client  #获取大模型客户端实例对象

        self.tool_dict = tool_dict #获取工具字典(里面包含所有工具)

        self.toolexecutor = toolExecutor #获取工具执行实例对象 



        #依次导入工具文件,如果只是单纯的self.tool_dict,那么name只会得到键名,加上.values()才会获得对应的键值
        for name in self.tool_dict.values():

            #往将工具文件依次注册入工具库
            self.toolexecutor.tool_add(name.tool_detail) 
        

        
    #agent执行函数
    def run_agent(self,question,max_loop = 10):

        #1.获取所有工具信息
        tools_desc = self.toolexecutor.get_tool_schemas() #获取工具的所有工具信息



        #2.构建提示词和消息列表
        #2-1系统提示词
        sys_prompt = SYSTEM_PROMPT.format(
            tools = tools_desc
        )
        
        #2-3消息列表
        messages = [
            {"role":"system","content":sys_prompt},
            {"role":"user","content":question},
            ]


        try:

            #3.进入agent循环
            for i in range(max_loop):

                #3-1.调用LLM,并获取回答
                response = self.llm_client.think(messages=messages,tools=tools_desc)

                #3-2将LLM发过来的消息列表添加到消息列表里
                word = response.choices[0].message

                #3-3.如果LLM没有调用工具
                if not word.tool_calls:  #tool_calls为None
                    #仅添加LLM回复得内容到messages，添加完后跳出整个循环,并返回
                    messages.append({"role":"assistant","content":word.content})
                    return word.content
                
                
                #3-4模型调用了工具
                else:
                    
                    #LLM调用工具，就得把消息和工具信息一起添加到messages
                    messages.append({"role":"assistant","content":word.content,"tool_calls":word.tool_calls})

                    #3-5.逐次执行工具，获取工具执行结果，再将工具结果添加到messages中
                    for tool_call in response.choices[0].message.tool_calls:

                        #3-6获取要执行工具的名字和工具的入参参数
                        name = tool_call.function.name #获取LLM决定要调用的工具名字
                        arguments = json.loads(tool_call.function.arguments) #获取工具工具入参数据

                        #3-7.调用工具，获取工具的执行结果
                        tool_func = self.toolexecutor.get_tool_func(name=name) #获取工具的执行函数
                        result = tool_func(**arguments) #获取工具执行的结果

                        #3-8.将工具结果添加到messages中
                        messages.append({"role":"tool","tool_call_id":tool_call.id,"content":str(result)})
                        
        except Exception as e:
            return f"Agent运行错误:{e}"














if __name__=='__main__':
    #获取客户端
    agent = Agent(LLM_client =llm_client(),toolExecutor=toolExecutor(),tool_dict = tool_dict)
    prompt = ("1.DeepSeek_Harness和Coedx有什么区别?"
    "2.计算：((5+3)^2-8)/(6^2-4^2)，并返回当前时间"
    "3.告诉我上面你用了哪些工具")
    result = agent.run_agent(prompt)
    print(result)

