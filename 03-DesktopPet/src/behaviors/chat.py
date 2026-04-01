"""
chat.py
消息与对话管理
现在：固定回复 + 随机提示
未来：接入 Ollama / Claude 实现真正的 AI 对话
"""
import random

# ── 固定回复库 ────────────────────────────────────────
GREETINGS = [
    "你好呀！🧡",
    "在学RAG吗~",
    "喝水了吗？💧",
    "休息一下吧！",
    "加油！我看好你",
    "今天写代码了吗",
    "有问题问我哦~",
    "摸摸我嘛！",
    "别忘了吃饭哦🍱",
]

IDLE_MSGS = [
    "喝水了吗？💧",
    "记得休息哦～",
    "加油！🧡",
    "摸摸我嘛~",
    "站起来动一动！",
]


class Chat:
    """
    管理桌宠说的话
    未来在这里接入 Ollama，让桌宠真正能回答问题
    """

    def __init__(self):
        self._llm = None   # 未来：存放 Ollama/Claude 实例
        self._history = [] # 未来：对话历史

    def greet(self) -> str:
        """点击时随机说一句话"""
        # TODO: 未来可以调用 LLM 生成个性化回复
        return random.choice(GREETINGS)

    def idle_message(self) -> str:
        """空闲时随机提示"""
        return random.choice(IDLE_MSGS)

    def reply(self, user_input: str) -> str:
        """
        回复用户输入
        现在：返回固定回复
        未来：调用 Ollama
        """
        # ── 未来接入 Ollama 的位置 ────────────────────
        # from langchain_ollama import ChatOllama
        # from langchain_core.messages import HumanMessage, SystemMessage
        #
        # if self._llm is None:
        #     self._llm = ChatOllama(model="qwen2.5:7b")
        #
        # self._history.append(HumanMessage(content=user_input))
        # res = self._llm.invoke(self._history)
        # self._history.append(res)
        # return res.content
        # ─────────────────────────────────────────────

        return random.choice(GREETINGS)

    def enable_llm(self, model_name: str = "qwen2.5:7b"):
        """
        开启 AI 模式（未来调用这个方法激活 LLM）
        """
        # TODO: 初始化 Ollama
        pass