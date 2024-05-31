from fastapi import FastAPI
from manager import monitor
import asyncio

app = FastAPI()


# 定义一个后台任务函数，该函数包含一个无限循环
async def infinite_loop_task():
    while True:
        monitor()
        await asyncio.sleep(60)  # 假设每秒执行一次


@app.on_event("startup")
async def startup_event():
    # 在应用启动时，启动后台任务
    asyncio.create_task(infinite_loop_task())


@app.get("/")
async def query_cache():
    return {"message": "Manager Running!"}