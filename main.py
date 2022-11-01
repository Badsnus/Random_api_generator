import asyncio

from fastapi import FastAPI

from loader import db


async def create_db():
    await db.create_data()


async def stop_db():
    await db.create_data()


def on_startup():
    asyncio.create_task(create_db())


def on_shutdown():
    asyncio.create_task(stop_db())


app = FastAPI(on_startup=on_startup(), on_shutdown=())


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/list/")
async def show_list(fields=None, limit: int = None, offset: int = None):
    fields, data = await db.select_datas(fields, limit, offset)
    result = dict(count=len(data), items=[])
    for item in data:
        now_item = {}
        for name, value in zip(fields, item['row']):
            now_item[name] = value
        result['items'].append(now_item)
    return result


@app.get("/list/{id}/")
async def show_list(fields=None):
    return await db.select_data(fields=fields)
