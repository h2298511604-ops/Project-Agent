from typing import Dict,List,Any
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()

class llm_client:
    def __init__(self,key=None,url=None,model=None):
        self.llm_key = key or os.getenv("DeepSeek_API_KEY")
        self.llm_url = url or os.getenv("DeepSeek_MODEL_URL")
        self.llm_model = model or os.getenv("DeepSeek_MODEL_1")


        #创建客户端
        self.client = OpenAI(
            api_key = self.llm_key,
            base_url = self.llm_url,
            timeout = 180
        )

    #开始调用LLM
    def think(self,messages:List[Dict[str,Any]],tools:Dict[str,Dict[str,Any]],stream=False):

        try:
            response = self.client.chat.completions.create(
                model = self.llm_model,
                messages = messages,
                temperature = 0.7,
                stream = stream,
                tools = tools
            )

            #选择输出的方式:流式输出/非流式输出,默认为非流式输出
            if stream:
                #获取LLM输出并在终端打印(流式输出)
                output = ""
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        output += chunk.choices[0].delta.content
                        print(chunk.choices[0].delta.content,end="")
                return output
            
            else:
                return response #非流式输出,返回整个LLM的json格式


        except Exception as e:
            print(f"调用模型{self.llm_model}出错：{e}")
            return None



if __name__== "__main__":
    prompt = "你好，请介绍一下你自己"
    messages = [{"role":"user","content":prompt}]
    action = llm_client()
    result = action.think(messages=messages)


