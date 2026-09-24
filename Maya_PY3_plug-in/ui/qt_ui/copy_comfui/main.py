# -*- coding: utf-8 -*-
import os
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, Response
from pydantic import BaseModel
import urllib.parse

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKFLOW_DIR = os.path.join(BASE_DIR, "workflows")

if not os.path.exists(WORKFLOW_DIR):
    os.makedirs(WORKFLOW_DIR)

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


# 工作流数据模型
class WorkflowData(BaseModel):
    last_node_id: int
    last_link_id: int
    nodes: list
    links: dict


@app.get("/")
async def read_index():
    return FileResponse(os.path.join(BASE_DIR, 'static/index.html'))


@app.get("/api/list")
async def list_workflows():
    files = [f for f in os.listdir(WORKFLOW_DIR) if f.endswith('.json')]
    # 确保返回UTF-8编码
    return JSONResponse(
        content=files,
        media_type="application/json; charset=utf-8"
    )


@app.get("/api/load/{filename}")
async def load_workflow(filename: str):
    # URL解码文件名
    filename = urllib.parse.unquote(filename)
    path = os.path.join(WORKFLOW_DIR, filename)

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="文件不存在")

    # 尝试多种编码读取
    encodings = ['utf-8', 'gbk', 'utf-16']
    content = None

    for enc in encodings:
        try:
            with open(path, 'r', encoding=enc) as f:
                content = json.load(f)
                break
        except (UnicodeDecodeError, json.JSONDecodeError):
            continue

    if content is None:
        raise HTTPException(status_code=500, detail="文件编码不支持或JSON格式损坏")

    # 确保返回UTF-8编码
    return JSONResponse(
        content=content,
        media_type="application/json; charset=utf-8"
    )


@app.post("/api/save/{filename}")
async def save_workflow(filename: str, workflow: WorkflowData, request: Request):
    try:
        # URL解码文件名
        filename = urllib.parse.unquote(filename)

        # 确保文件名以.json结尾
        if not filename.endswith('.json'):
            filename += '.json'

        # 安全文件名处理
        filename = "".join(c for c in filename if c.isalnum() or c in ('.', '-', '_'))

        path = os.path.join(WORKFLOW_DIR, filename)

        # 保存工作流数据，使用UTF-8编码
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(workflow.dict(), f, ensure_ascii=False, indent=2)

        # 确保返回UTF-8编码的响应
        response_data = {
            "status": "success",
            "message": "工作流保存成功",
            "filename": filename
        }

        return JSONResponse(
            content=response_data,
            media_type="application/json; charset=utf-8"
        )
    except Exception as e:
        # 错误响应也使用UTF-8编码
        error_detail = f"保存失败: {str(e)}"
        return JSONResponse(
            status_code=500,
            content={"error": error_detail},
            media_type="application/json; charset=utf-8"
        )