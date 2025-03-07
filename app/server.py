from fastapi import FastAPI
from datetime import datetime 
from schema import *
import crud
from lifespan import lifespan
from models import Session
from dependancy import SessionDependancy
import models
from sqlalchemy import select
from constant import *


app = FastAPI(
    title="BUY/SELL Advertisments API",
    description="API for BUY/SELL Advertisments",
    version="1.0.0",
    lifespan=lifespan
)   


@app.post(
    "/advertisments/",
    tags=["advertisments"],
    response_model=CreateAdvResponse
)
async def create_Advertisment(request:createAdvRequest, session: SessionDependancy):
    Adv_dict = request.model_dump(exclude_unset=True)
    Adv_orm_obj = models.Advertisment(**Adv_dict)
    await crud.add_item(session, Adv_orm_obj)
    return Adv_orm_obj.id_dict


@app.get(
    "/advertisments/{Adv_id}",
    tags=["get advertisments"],
    response_model=GetAdvResponse
)
async def get_Advertisment(Adv_id:int, session: SessionDependancy):
    Adv_orm_obj = await crud.get_item_by_id(session, models.Advertisment, Adv_id)
    return Adv_orm_obj.dict


@app.get(
    "/advertisments/",
    tags=["search advertisments"],
    response_model=SearchAdvResponse
)
async def search_Advertisment(session: SessionDependancy, Title: str):
    query = (select(models.Advertisment).where(models.Advertisment.Title == Title).limit(10000))
    Advs = await session.scalars(query)
    return {"results": [Adv.dict for Adv in Advs]}


@app.patch(
    "/advertisments/{response_model.id}",
    tags=["update advertisments"],
    response_model=UpdateAdvResponse
)
async def update_Advertisment(Adv_id:int, Adv_data: UpdateAdvRequest, session: SessionDependancy):
    Adv_dict = Adv_data.model_dump(exclude_unset=True)
    Adv_orm_obj = await crud.get_item_by_id(session, models.Advertisment, Adv_id)
    for field, value in Adv_dict.items():
        setattr(Adv_orm_obj, field, value)
    await crud.add_item(session, Adv_orm_obj)

    return SUCCCESS_RESPONSE    


@app.delete(
    "/advertisments/{Adv_id}",
    tags=["delete advertisments"],
    response_model=DeleteAdvResponse
)
async def delete_Advertisment(Adv_id:int, session: SessionDependancy):
    Adv_orm_obj = await crud.get_item_by_id(session, models.Advertisment, Adv_id)
    await crud.delete_item(session, Adv_orm_obj)
    return SUCCCESS_RESPONSE