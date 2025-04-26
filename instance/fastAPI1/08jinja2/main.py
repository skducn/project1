from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.templating import Jinja2Templates

# app = FastAPI()
app = FastAPI(docs_url="/docs", redoc_url="/redoc")

template = Jinja2Templates(directory="templates")

@app.get("/index")
def index(request:Request):
    name = "root"
    book = ['金瓶梅','聊斋','剪灯新话','国色天香']
    info = {'name':"jinhao","age":"44","gender":"male"}
    return template.TemplateResponse("index.html", {"request": request, "user": name, "book": book, "info": info})


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)