from aiohttp import web
from models import User, Advertisement, Session, Token
from crud import add_item, create_item, delete_item, get_item_by_id, update_item, val_creator_adv
from auth import hash_password, check_password, check_token
from shema import CreatAdv, UpdateAdv, CreatUser, UpdateUser, Login
from tools import validate
from errors import get_http_error
from sqlalchemy.future import select

class UserView(web.View):

    @property
    def user_id(self) -> int:
        return int(self.request.match_info['user_id'])

    @property
    def session(self) -> Session:
        return self.request.session

    @property
    def user(self) -> User:
        return self.request.token.user

    # @check_token
    async def get(self):
        print(self.user_id)
        user = await get_item_by_id(User, self.user_id, self.session)
        print(user)
        return web.json_response(user.dict)

    async def post(self):
        json_data = await self.request.json()
        json_data = validate(CreatUser,json_data)
        json_data['password'] = hash_password(json_data['password'])
        user = User(**json_data)
        await add_item(user, self.session)
        return web.json_response(user.dict_id)

    # @check_token
    async def patch(self):
        user = await get_item_by_id(User, self.user_id, self.session)
        json_data = await self.request.json()
        json_data = validate(UpdateUser, json_data)
        if 'password' in json_data:
            json_data['password'] = hash_password(json_data['password'])
        for field, value in json_data.items():
            setattr(user, field, value)
        await update_item(self.token.user, json_data, self.session)
        return web.json_response(user.dict_id)

    # @check_token
    async def delete(self):
        user = await get_item_by_id(User, self.user_id, self.session)
        print(user)
        await delete_item(user, self.session)
        return web.json_response({'status': 'success'})


class AdvView(web.View):

    @property
    def adv_id(self) -> int:
        return int(self.request.match_info['adv_id'])

    @property
    def session(self) -> Session:
        return self.request.session

    # @check_token
    async def get(self):
        adv = await get_item_by_id(Advertisement, self.adv_id, self.session)
        return web.json_response(adv.dict)

    # @check_token
    async def post(self):
        json_data = await self.request.json()
        json_data = validate(CreatAdv,json_data)
        json_data['creator'] = int(json_data['creator'])
        adv = Advertisement(**json_data)
        await add_item(adv, self.session)
        return web.json_response(adv.dict)

    # @check_token
    async def patch(self):
        adv = await get_item_by_id(Advertisement, self.adv_id, self.session)
        json_data = await self.request.json()
        json_data = validate(UpdateAdv, json_data)
        json_data['creator'] = int(json_data['creator'])
        await val_creator_adv(json_data, adv)
        for field, value in json_data.items():
            setattr(adv, field, value)
        await add_item(adv, self.session)
        return web.json_response(adv.dict)

    # @check_token
    async def delete(self):
        adv = await get_item_by_id(Advertisement, self.adv_id, self.session)
        await delete_item(adv, self.session)
        return web.json_response({'status': 'success'})


class LoginView(web.View):

    @property
    def session(self) -> Session:
        return self.request.session

    async def post(self):
        json_data = await self.request.json()
        query = select(User).filter_by(name=json_data['user'])
        result = await self.session.execute(query)
        user = result.scalars().all()
        # if user is None:
        if user == []:
            raise get_http_error(web.HTTPConflict, 'user not found')
        for i in user:
            if check_password(json_data['password'],i.password):
                token = await create_item(Token, {'user_id': i.id}, self.session)
                await add_item(token, self.session)
                return web.json_response({'token': str(token.token)})
