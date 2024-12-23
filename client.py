import asyncio
import aiohttp



async def main():

    async with aiohttp.ClientSession() as session:
        # response = await session.post('http://127.0.0.1:8080/user',
        #                               json={
        #                                   'name': 'user_1',
        #                                   'password': 'qwerty1234',
        #                                   'email': 'user_1@gmail.ru'
        #                               }
        #                               )
        # response = await session.patch('http://127.0.0.1:8080/user/1',
        #                               json={
        #                                   'name': 'new_user',
        #                               }
        #                               )

        # response = await session.get('http://127.0.0.1:8080/user/1',)
        # response = await session.get('http://127.0.0.1:8080/adv/1',)
        # response = await session.delete('http://127.0.0.1:8080/user/1', )
        # response = await session.post('http://127.0.0.1:8080/adv',
        #         json={
        #             'heading': 'Продам Мерседес',
        #             'description': 'Продам автомобиль Мерседес A600, черный',
        #             'creator': '2'}
        #
        #        )
        response = await session.patch('http://127.0.0.1:8080/adv/12',
                                      json={
                                          'description': 'Продам автомобиль Мерседес S600, белый',
                                          'creator': '2',
                                      }
                                      )
        # response = await session.delete('http://127.0.0.1:8080/adv/2', )

        # response = await session.post('http://127.0.0.1:8080/login',
        #                               json={
        #                                   'user': 'user_1',
        #                                   'password': 'qwerty1234'
        #                               }
        #                               )


        print(response.status)
        print(await response.json())

asyncio.run(main())

# 'email': 'user@gmail.ru'