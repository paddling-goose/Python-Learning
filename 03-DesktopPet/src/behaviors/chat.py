import random, os
from dotenv import load_dotenv

load_dotenv()

GREETINGS = [
    "你好呀！🧡", "喝水了吗？💧", "休息一下吧！",
    "加油！我看好你", "今天写代码了吗", "有问题问我哦~",
    "摸摸我嘛！", "别忘了吃饭哦🍱",
]
IDLE_MSGS = ["喝水了吗？💧", "记得休息哦～", "加油！🧡", "摸摸我嘛~", "站起来动一动！"]


class Chat:
    def __init__(self):
        self._llm = None
        self._history = []
        self._init_llm()          # 启动时就尝试初始化

    def _init_llm(self):
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            return
        try:
            from langchain_community.chat_models import ChatTongyi
            self._llm = ChatTongyi(model="qwen-max", dashscope_api_key=api_key)
        except Exception as e:
            print(f"[Chat] LLM 初始化失败，降级为随机回复: {e}")

    def greet(self) -> str:
        return random.choice(GREETINGS)

    def idle_message(self) -> str:
        return random.choice(IDLE_MSGS)

    def reply(self, user_input: str) -> str:
        if self._llm is None:
            return random.choice(GREETINGS)
        try:
            from langchain_core.messages import HumanMessage
            self._history.append(HumanMessage(content=user_input))
            res = self._llm.invoke(self._history)
            self._history.append(res)
            return res.content
        except Exception as e:
            print(f"[Chat] LLM 调用失败: {e}")
            return random.choice(GREETINGS)