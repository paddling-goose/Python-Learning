from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate
from langchain_community.llms.tongyi import Tongyi
from dotenv import load_dotenv
import os

# 配置全局环境变量
load_dotenv()

api_key = os.getenv("DASHSCOPE_API_KEY")
model  = Tongyi(model = "qwen-max",dashscope_api_key=api_key)

# prompt模板
prompt_template = PromptTemplate.from_template(
    "my neighbour's family name is {lastname}, she just delivered a {gender} baby, please help give the baby a name."
)

# fewshot类型
example_template = PromptTemplate.from_template("单词：{word}, 反义词：{antonym}")

example_data = [
    {"word":"大","antonym" :"小"},
    {"word":"多","antonym" :"少"},
]

few_shot_prompt = FewShotPromptTemplate(
    example_prompt = example_template,
    examples = example_data,
    prefix = "给出给定词的反义词，有如下示例：",
    suffix = "基于实例告诉我，{input_word}的反义词是？",
    input_variables =  ['input_word']

)

# # 生成链
# chain = prompt_template |model
# # 基于链，调用模型获取结果
# res = chain.invoke(input = {"lastname" : "Chen","gender":"female"})
# print(res)

# 看看提示词填得怎么样：
prompt_text = few_shot_prompt.invoke(input={"input_word":"左"}).to_string()
print(prompt_text)