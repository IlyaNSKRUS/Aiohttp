from aiohttp import web
from models import User, Advertisement, Session, Token, MODEL, MODEL_TYPE
from errors import get_http_error
from sqlalchemy.exc import IntegrityError


async def get_item_by_id(model: MODEL_TYPE, item_id: int, session: Session) -> MODEL:
    item = await session.get(model, item_id)
    # user = await session.get(User, user_id)
    if item is None:
        raise get_http_error(web.HTTPNotFound, f"{model.__name__} not found")
    return item


async def add_item(item: MODEL, session: Session) -> MODEL:
    session.add(item)
    try:
        await session.commit()
    except IntegrityError as err:
        raise get_http_error(web.HTTPNotFound, f"{item.__class__.__name__} already exists")
    return item


async def create_item(model: MODEL_TYPE, json_data: dict, session: Session) -> MODEL:
    item = model(**json_data)
    item = await add_item(item, session)
    return item


async def delete_item(item: MODEL, session: Session):
    await session.delete(item)
    await session.commit()


async def update_item(item: MODEL, json_data: dict, session: Session) -> MODEL:
    for field, value in json_data.items():
        setattr(item, field, value)
    await add_item(item, session)
    return item


async def update_item_by_id(model: MODEL_TYPE, item_id: int, json_data: dict, session: Session) -> MODEL:
    item = await get_item_by_id(model, item_id, session)
    await update_item(item, json_data, session)
    return item


async def val_creator_adv(json_data, adv):
    if int(json_data['creator']) != adv.creator:
        raise get_http_error(web.HTTPConflict, 'you are not the creator of the adv')
    return adv

#
#
#
#
#
#
#
# async def get_user_by_id(user_id: int, session: Session) -> User:
#     user = await session.get(User, user_id)
#     if user is None:
#         raise get_http_error(web.HTTPNotFound, 'user not found')
#     return user
#
# async def add_user(user: User, session: Session):
#     session.add(user)
#     try:
#         await session.commit()
#     except IntegrityError as err:
#         raise get_http_error(web.HTTPConflict, 'user already exist')
#
# async def delete_user(user: User, session: Session):
#     await session.delete(user)
#     await session.commit()
#
# async def add_adv(adv: Advertisement, session: Session):
#     session.add(adv)
#     try:
#         await session.commit()
#     except IntegrityError as er:
#         raise get_http_error(web.HTTPConflict, 'the creator is not registered')
#
# async def delete_adv(adv: Advertisement, session: Session):
#     await session.delete(adv)
#     await session.commit()
#
# async def get_adv_by_id(adv_id: int, session: Session) -> Advertisement:
#     adv = await session.get(Advertisement, adv_id)
#     if adv is None:
#         raise get_http_error(web.HTTPNotFound, 'advertisement not found')
#     return adv
#
# async def val_creator_adv(json_data, adv):
#     if int(json_data['creator']) != adv.creator:
#         raise get_http_error(web.HTTPConflict, 'you are not the creator of the adv')
#     return adv
#
# async def create_token(json_data: dict, session: Session) -> Token:
#     token = model(**json_data)
#     token = add_item(token, session)
#     return token