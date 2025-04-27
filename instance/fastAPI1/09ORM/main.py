import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from setting import TORTOISE_ORM
from api.student import student_api

app = FastAPI(docs_url="/docs", redoc_url="/redoc")
app.include_router(student_api, prefix="/student", tags=['选课学生接口'])


# 该方法会在 fastapi 启动时触发，内部通过传递进去的 app 对象，监听服务启动和终止事件
# 当检测到启动事件时，会初始化 Tortoise 对象，如果 generate_schemas 为 True 则还会进行数据库迁移
# 当检测到终止事件时，会关闭连接
# fastapiy一旦运行，register_tortoise已经执行，实现监控
register_tortoise(
    app = app,
    config = TORTOISE_ORM
    # generate_schemas=True, # 如果数据库为空，则自动生成对应表单，生产环境不要开
    # add_exception_handlers=True, # 生产环境不要开，会泄露调试信息
)

if __name__ == '__main__':

    uvicorn.run("main:app", host="127.0.0.1", port=8003, reload=True)