from typing import Dict,Any,List
import Tools.calculator
import Tools.get_time
import Tools.save_note
import Tools.search

class toolExecutor:
    def __init__(self):
        #工具库,字典套字典
        self.tools:Dict[str,Dict[str,Any]] = {}

    #注册工具
    def tool_add(self,tool_dict:Dict[str,Any]):



        #1.验证传入的必须是字典
        if not isinstance(tool_dict,dict):
            raise ValueError(f"传入的工具说明必须是字典!当前类型为:{type(tool_dict).__name__}")


        #2.判断注册的工具是否符合要求(工具说明必须含有"tool_name","description","func","parameters"这四个字段)
        for key in ("tool_name","description","func","parameters"):
            if key not in tool_dict:
                raise ValueError(f"注册失败!注册的工具格式不符合要求")



        name = tool_dict["tool_name"]
        description = tool_dict["description"]
        func = tool_dict["func"]
        parameters = tool_dict["parameters"]


        #***判断类型和内容是否为空时***，要先判断类型，其次才是判断内容是否为空

        #3-1.工具名字要符合字符串要求
        if not isinstance(name,str):
            raise TypeError(f"注册失败!工具名字必须是字符串!收到的类型为:{type(name).__name__}")

        #3-2工具描述要符合字符串要求
        if not isinstance(description,str):
            raise TypeError(f"注册失败!工具描述必须是字符串,当前类型为:{type(description).__name__}")

        #3-3工具参数要符合字典要求
        if not isinstance(parameters,Dict):
            raise TypeError(f"注册失败!工具parameters必须是字典,当前类型为:{type(parameters).__name__}")



        #4-1.工具名字不为空
        if not name.strip():
            raise ValueError(f"名字不能为空")

        #4-2.工具描述不能为空
        if not description.strip():
            raise ValueError(f"工具描述不能为空")


        #4-3.工具函数要可调用
        if not callable(func):
            raise TypeError(f"工具{name}的函数为不可调用对象,类型为:{type(func).__name__}")


        
        #5.注册的工具名和工具库已有工具的名字重合会触发注册失败
        if tool_dict["tool_name"] in self.tools:
            raise ValueError(f"添加失败!工具已存在")

        #5.以上校验通过，添加到工具库
        self.tools[tool_dict["tool_name"]] = dict(tool_dict)

        return None



    #查询工具库里的工具-单个工具信息
    def tool_inquire(self,name:str):


        if not isinstance(name,str):
            raise TypeError(f"查询工具必须输入字符串!当前类型为:{type(name).__name__}")

        if name not in self.tools:
            raise KeyError(f"工具不存在!") 

        #返回字典
        return dict(self.tools[name])


    #获取工具的执行函数
    def get_tool_func(self,name:str):
        #1.先确认要获取的工具名的类型是字符串
        if not isinstance(name,str):
            raise TypeError(f"错误!获取工具函数的工具名不是字符串,当前类型为:{type(name).__name__}")
        
        #2.然后确认工具名不为空
        if not name.strip():
            raise ValueError("错误!获取工具函数的工具名不能为空!")

        tool_func = self.tools.get(name,{}).get("func")
        return tool_func #这里返回的是一个函数


    #获取所有工具信息
    def get_tool_schemas(self):

        #给LLM看的所有工具信息列表
        tools:List[Dict[str,Any]] = []

        #先将工具库里的每个工具信息提取并填入到固定字典模板中
        for key,value in self.tools.items():
            
            tool_schemas = {
                "type":"function",
                "function":{
                    "name":key,
                    "description":value.get("description"),
                    "parameters":value.get("parameters")
                }
            }

            #将填写好的字典再添加到列表中
            tools.append(tool_schemas)

        return tools



tool_dict ={"calculator":Tools.calculator,"get_time":Tools.get_time,"save_note":Tools.save_note,"search":Tools.search}











if __name__=='__main__':
    a = toolExecutor()
    b = a.tool_add(Tools.calculator.tool_detail) #添加工具


    c = "calculator"
    d = a.tool_inquire(c) #查询工具

    e = a.get_tool_func(c) #获取工具执行函数
    f = "你好"  #参数1
    g = "(1+9*6)/(3+5)" #参数2
    h = e(expression = g)


    print(h)


