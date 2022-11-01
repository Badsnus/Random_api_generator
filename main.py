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
async def show_list(fields='', limit: int = 300, offset: int = None):
    fields, data = await db.select_datas(fields, min(limit, 300), offset)
    result = dict(count=len(data), items=[])
    if fields:
        for item in data:
            now_item = {}
            for name, value in zip(fields, item['row']):
                now_item[name] = value
            result['items'].append(now_item)
    else:
        result['items'] = [dict(item) for item in data]
    return result


@app.post("/list/")
async def create_item():
    return {'status': 'ok', 'info': 'Fake post done'}


@app.get("/list/{id}/")
async def show_list_item(id: int, fields=''):
    return await db.select_data(id, fields=fields)


@app.put("/list/{id}/")
async def update_list_item(id: int):
    return {'status': 'ok', 'info': f'Fake post {id} update'}


@app.delete("/list/{id}/")
async def update_list_item(id: int):
    return {'status': 'ok', 'info': f'Fake post {id} delete'}
