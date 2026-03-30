from fastapi import HTTPException

from utils.exception import http_exception_handler,integrity_error_handler,sqlalchemy_error_handler,general_exception_handler

#ANCHOR - 注册所有异常处理函数
#NOTE - 子类前，父类后；具体前，抽象后
def register_exception_handlers(app):

    app.add_exception_handler(HTTPException, http_exception_handler) # 业务
    app.add_exception_handler(HTTPException, integrity_error_handler) # 数据完整性约束
    app.add_exception_handler(HTTPException, sqlalchemy_error_handler) # 数据库
    app.add_exception_handler(HTTPException, general_exception_handler) # 兜底

