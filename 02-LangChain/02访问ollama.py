from langchain_community.llms.tongyi import Tongyi
#from langchain_ollama import OllamaEmbeddings
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os

# 配置全局环境变量
load_dotenv()

api_key = os.getenv("DASHSCOPE_API_KEY")
model  = Tongyi(model = "qwen-max",dashscope_api_key=api_key)


#NOTE - 文本嵌入模型from langchain_community.embeddings import DashScopeEmbeddings
# 不传model默认使用 text-embedding-v1
# model = OllamaEmbeddings()

# print(model.embed_query("you are a spotted pigeon"))
# print(model.embed_documents(["you are a spotted pigeon","你是一只斑鸠"]))

model = ChatOllama(model="qwen2.5:7b")
res = model.invoke("你好呀")
print(res.content)