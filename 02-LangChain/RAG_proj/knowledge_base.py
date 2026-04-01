"""
知识库
"""
import os
import config_data as config

def check_md5():
    if not os.path.exists(config.md5_path):
        return False


def save_md5():
    pass


def get_string_md5():
    """传入字符串转化为md5字符串"""


class KnowledgeBaseService(object):
    def __init__(self):
        self.chroma = None
        self.spliter = None

    def upload_by_str(self,data,filename):
        """将传入的字符串进行向量化"""