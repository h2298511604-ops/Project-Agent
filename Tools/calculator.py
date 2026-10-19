import ast
import operator
import math

#表达式的计算，最终得出值
class Calculator(ast.NodeVisitor):

    #二元运算符字典
    BINARY_OPS ={
        ast.Add:operator.add, #加
        ast.Sub:operator.sub, #减
        ast.Mult:operator.mul, #乘
        ast.Div:operator.truediv, #除
        ast.FloorDiv:operator.floordiv, #整除
        ast.Mod:operator.mod, #
        ast.Pow:operator.pow,
    }

    #一元运算符字典
    UNARY_OPS={
        ast.USub:operator.neg,
        ast.UAdd:operator.pos
    }

    #比较运算符字典
    COMPARE_OPS={
        ast.Eq:    operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt:    operator.lt,
        ast.LtE:   operator.le,
        ast.Gt:    operator.gt,
        ast.GtE:   operator.ge,
    }


    #函数调用运算符字典
    SAFE_FUNCTIONS={
        'abs': abs, 'round': round, 'min': min, 'max': max,
        'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos,
        'tan': math.tan, 'log': math.log, 'log10': math.log10,
        'exp': math.exp, 'pow': pow, 'ceil': math.ceil, 'floor': math.floor
    }


    #Name-标识符运算字典
    SAFE_NAMES = {
        'pi':  math.pi,       # 3.141592653589793
        'e':   math.e,        # 2.718281828459045
        'tau': math.tau,      # 6.283185307179586
        'inf': math.inf,      # inf
    } 





    #常量
    def visit_Constant(self,node):
        return node.value #返回常数值


    #二元运算
    def visit_BinOp(self,node):
        left = self.visit(node.left) #获取节点左边的值
        right = self.visit(node.right) #获取节点右边的值
        op_func = self.BINARY_OPS[type(node.op)] #获取运算符
        return op_func(left,right) #根据获取的运算进行计算


    #一元运算
    def visit_UnaryOp(self,node):
        operand = self.visit(node.operand) #递归操作数
        op_func = self.UNARY_OPS[type(node.op)]

        #如果找不到一元运算符字典
        if op_func is None:
            raise TypeError(f"不支持的一元运算符:{type(node.op).__name__}")
        
        return op_func(operand) 

    
    #比较运算
    def visit_Compare(self,node):
        left = self.visit(node.left)

        for op,comparator in zip(node.ops, node.comparators):
            right = self.visit(comparator)

            op_func = self.COMPARE_OPS.get(type(op))
            if op_func is None:
                raise TypeError(f"不支持的比较运算符: {type(op).__name__}")

            if not op_func(left, right):
                return False

            left = right   # 链式比较：1 < x <= 10


        return True


    #函数调用运算
    def visit_Call(self,node):
        # 安全检查：func 必须是 Name（不允许 obj.method() 形式）
        if not isinstance(node.func,ast.Name):
            raise TypeError("只支持函数调用")
        
        #白名单检查
        func_name = node.func.id
        if func_name not in self.SAFE_FUNCTIONS:
            raise NameError(f"不允许调用:{func_name}")

        #递归求值所有参数
        args = [self.visit(arg) for arg in node.args]

        return self.SAFE_FUNCTIONS[func_name](*args)


    #标识符运算
    def visit_Name(self,node):
        if node.id in  self.SAFE_NAMES:
            return self.SAFE_NAMES[node.id]

        #NameError:表示错误类型为"变量未自定义"
        raise NameError(f"未知名称: '{node.id}'")

    #白名单防线
    def generic_visit(self,node):

        #TypeError:表示错误类型为"类型错误"
        raise TypeError(f"禁用的语法:{type(node).__name__}")


    #这个函数是非必要，如果传入的是xxx.body,那么会直接跳到对应的body节点类型所对应的函数中，根本不会执行这个函数
    def visit_Expression(self,node):
        return self.visit(node.body) #获取body的节点类型


#工具的函数入口
def calculator(expression:str,max_len=200):

    #1.判断传入的参数是否为字符串
    if not isinstance(expression,str):
        #isintansce:用于判断一个对象是不是某个类型的实例，返回True/False.
        #isintansce语法:isintansce(对象,类型)
        return f"计算失败:输入参数必须是表达字符串,现传入的参数为:{type(expression).__name__}"

    #2.判断是否为空
    exp = expression.strip()
    if not exp:
        return f"计算失败:输入参数为空!请给出一个表达式"


    #3.限制传入参数的长度
    if len(exp) > max_len:
        return f"计算失败:输入参数的长度为:{len(exp)},大于限制长度:{max_len}"

    
    #4.判断传入的参数是否符合表达式
    try:
        #调节器,把字符串变为树结构
        node = ast.parse(exp,mode='eval')

    except SyntaxError as e:
        hint = "（请使用半角符号，如 + - * / ( )）" if "invalid character" in (e.msg or "") else ""
        #hint的语法格式为:
        #hint = A if 条件 else B;意思是:如果条件成立,则为A，否则为B
        #等价于:
        #if "invalid character" in (e.msg or ""):
        #    hint = "（请使用半角符号，如 + - * / ( )）"
        #else:
        #    hint = ""

        #SyntaxError:表示错误的类型为"语法错误"
        return f"表达式语法错误:{e.msg}{hint}"


    #5.求值+异常收口
    try:
        #求值
        return str(Calculator().visit(node))

    except (ZeroDivisionError,ValueError,TypeError,NameError,OverflowError) as e:
        return f"计算错误:{type(e).__name__}:{e}"

    #这一行的作用捕获上一个异常捕获所漏掉的错误
    except Exception as e:
        return f"计算错误:{e}"



#工具说明
tool_detail = {
    "tool_name":"calculator", #工具的名字
    "description":( #工具说明，这个管的是LLM要不要进行调用，在什么情况下调用
        "1.计算一个数学表达式的值，入参为单个表达式字符串，如 '(1+2)*3'。"
        "2.支持 + - * / // % **、比较、括号，以及 abs/sqrt/sin/cos/log 等函数和 pi/e/tau 常量。"
        "3.凡是要进行计算时,必须使用该工具,不能够跳过它凭记忆进行心算得出结果"
    ),
    "func":calculator, #工具真正的执行函数
    "parameters":{   #整个函数的入参描述
        "type":"object", #入参整体式一个object(对象),比如字典Dict,或者列表List
        "properties":{   #逐个字段的详细定义
            "expression":{   #参数名,也即函数的入参名
                "type":"string",  #这个入参的数据类型,这里类型为字符串
                "description":(  #自然语言说明，教LLM怎么输入参数,以达到符合工具的入参要求
                    "1.入参为数学表达式的纯字符串,只含数字,运算符,括号;如 '(1+2)*3','(1+2)*4+3'。"
                    "2.不要包含等号,单位,问号等不符合数学表达式的字符串。"
                    "3.必须使用半角符号,不要用 × ÷ 或中文标点。"
                    "4.不支持的运算符'^',乘方请写成'**';例如:a.错误写法:(2+3)^2;b.正确写法:(2+3)**2"
                    )  
            }
        },
        "required":["expression"]  #哪些参数是必须填的。required:必须的
    }
}


if __name__ == '__main__':
    a = "(1+2)*4+3"
    b = calculator(expression = a)
    print(b)


    
