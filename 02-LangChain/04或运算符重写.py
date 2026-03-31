#NOTE - chain的实现
class Test(object):
    def __init__(self,name):
        self.name = name                # 存放创建时的名字
    
    def __or__(self, other):
        return MySequence(self,other)   # 创建一个MySequence，把self和other打包在一起
    
    def __str__(self):
        return self.name                # print时直接输出变量而不是地址
    

class MySequence(object):
    def __init__(self,*args):           # 收纳传入的对象。*args：接收各种类型参数
        self.sequence = []
        for arg in args:
            self.sequence.append(arg)

    
    def __or__(self, other):
        self.sequence.append(other)     # 不会创建新对象，而是打包进来，避免嵌套
        return self
    
    def run(self):
        for i in self.sequence:         # 遍历并执行相同的操作（这里是打印，可以为invoke）
            print(i)


#ANCHOR - 使用
if __name__ == '__main__':
    a = Test('a')
    b = Test('b')
    c = Test('c')

    task = a|b|c
    task.run()