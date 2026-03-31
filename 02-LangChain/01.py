from langchain_community.llms.tongyi import Tongyi
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
# from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

# 配置全局环境变量
load_dotenv()

api_key = os.getenv("DASHSCOPE_API_KEY")
model  = Tongyi(model = "qwen-max",dashscope_api_key=api_key)

#NOTE - 调用invoke向模型提问：全生成完再输出
# res = model.invoke(input="你好呀")
# print(res)


#NOTE - 流式输出:一边生成一边输出
# res = model.stream(input="告诉我有哪些鸲的品种？")

# for chunk in res:
# 	print(chunk,end="",flush=True)


#NOTE - chat模型
# chat  = ChatTongyi(model = "qwen3-max")

# messages_0 = [
#     SystemMessage(content= "你是一只夜鹭"),
#     HumanMessage(content="请介绍一下夜鹭的特点")
# ]

# messages_1= [
#     ("system","你是一只夜鹭,你只会说呱！"),
#     ("human","你好呀小鸟"),
#     ("ai","呱！呱呱！呱呱——"),
#     ("human","你是说呱呱吗？"),
#     ("ai","呱呱！"),
#     ("human","可以介绍一下你自己吗？")
# ]

# for chunk in chat.stream(input = messages_1):
#     print (chunk.content,end="",flush=True)


#NOTE - 文本嵌入模型
# 不传model默认使用 text-embedding-v1
model = DashScopeEmbeddings()

print(model.embed_query("you are a spotted pigeon"))
print(model.embed_documents(["you are a spotted pigeon","你是一只斑鸠"]))