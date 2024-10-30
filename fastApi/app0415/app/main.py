#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Project  :app0415
# @File     :main.py
# @Time     :2024/4/15 19:46
# @Author   :wangting_666

from fastapi import FastAPI, HTTPException
from config.config import settings
from app.logger import logger
from app.todo import WowInfo, get_wowinfo_all, get_wowinfo, create_wowinfo, update_wowinfo, delete_wowinfo
from typing import List

app = FastAPI(title=settings.app_name)


@app.get("/get_wowinfo_all/", response_model=List[WowInfo])
async def read_wowinfos():
    logger.info("查询所有魔兽世界角色...")
    return get_wowinfo_all()


@app.get("/get_wowinfo/{role}", response_model=WowInfo)
async def read_wowinfo(role: str):
    logger.info(f"查询魔兽世界角色名称为: {role}...")
    info = get_wowinfo(role)
    if info is None:
        logger.error(f" 角色 {role} 不存在.")
        raise HTTPException(status_code=404, detail="查询失败")
    return info


@app.post("/create_wowinfo/", response_model=WowInfo)
async def create_new_wowinfo(info: WowInfo):
    logger.info("创建魔兽世界角色")
    return create_wowinfo(info)


@app.put("/update_wowinfo/{id}", response_model=WowInfo)
async def update_existing_wowinfo(id: int, wowinfo: WowInfo):
    logger.info(f"更新魔兽世界角色 id {id}...")
    existing_info = update_wowinfo(id, wowinfo)
    if existing_info is None:
        logger.error(f"职业信息ID:{id}不存在")
        raise HTTPException(status_code=404, detail="职业信息ID不存在")
    return existing_info


@app.delete("/delete_wowinfo/{id}")
async def delete_existing_wowinfo(id: int):
    logger.info(f"删除魔兽世界角色 id {id}...")
    success = delete_wowinfo(id)
    if not success:
        logger.error(f"兽世界角色 id {id} 不存在")
        raise HTTPException(status_code=404, detail="id 不存在")
    return {"status": "success", "message": "删除魔兽世界角色 id {id}成功"}
