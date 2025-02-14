from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import pandas as pd
import asyncio
import logging

# uvicorn main:app --log-level info

logging.basicConfig(level=logging.INFO, filename='myapp.log', encoding="utf-8")
logger = logging.getLogger(__name__)

app = FastAPI()

# 데이터 불러오기
file_path = "./data/edu_data_F.csv"
df = pd.read_csv(file_path)
df = df.iloc[:, :5]

# 스트리밍 종료 이벤트
stop_event = asyncio.Event()

async def stream_logs():
    for index, data in df.iterrows():
        if stop_event.is_set():  # 🔹 stop_event가 True이면 중단
            logger.info("-"*10,"Logging Stopped by User----","-"*10)
            break
        
        data_dict = data.to_dict()
        logger.info(data_dict)
        yield str(data_dict) + "\n"
        await asyncio.sleep(5)

@app.get("/getlog")
async def getlog():
    global stop_event
    stop_event.clear()  # 스트리밍 시작 시 이벤트 초기화
    return StreamingResponse(stream_logs())

@app.get("/stoplog/")
async def stoplog():
    global stop_event
    stop_event.set()  
    return {"message": "Logging Stopped"}
