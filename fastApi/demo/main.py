# https://blog.csdn.net/wt334502157/article/details/137835168
# pip install fastapi
# pip install uvicorn
#    async 关键字用于定义异步函数。异步函数可以在执行过程中暂停并允许其他代码执行，直到某些条件满足后再恢复执行。在 FastAPI 中，使用 async 可以使函数能够处理异步操作，例如异步的数据库查询、IO 操作等，以提高性能和并发能力。
# 在这个例子中，read_root 和 read_item 函数都是异步函数，它们使用了 async 关键字来定义。这样的函数可以通过 await 关键字调用其他异步函数，或者执行需要等待的异步操作，而不会阻塞整个应用程序的执行。

# uvicorn main:app --reload
#  命令含义如下:
# main：main.py 文件（一个 Python “模块”）。
# app：在 main.py 文件中通过 app = FastAPI() 创建的对象。
# --reload：让服务器在更新代码后重新启动。仅在开发时使用该选项。

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}

from typing import Union
from fastapi import FastAPI

from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}