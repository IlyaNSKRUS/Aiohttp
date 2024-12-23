from app import get_app
from models import init_orm, close_orm, Session
from aiohttp import web
from views import UserView, AdvView, LoginView

app = get_app()

async def orm_context(app: web.Application):
    print('START')
    await init_orm()
    yield
    await close_orm()
    print('FINISH')

@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        result = await handler(request)
        return result

app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


app.add_routes([
    web.post('/user', UserView),
    web.get('/user/{user_id:\\d+}', UserView),
    web.patch('/user/{user_id:\\d+}', UserView),
    web.delete('/user/{user_id:\\d+}', UserView),
    web.post('/adv', AdvView),
    web.get('/adv/{adv_id:\\d+}', AdvView),
    web.patch('/adv/{adv_id:\\d+}', AdvView),
    web.delete('/adv/{adv_id:\\d+}', AdvView),
    web.post("/login", LoginView)
])

if __name__ == "__main__":
    web.run_app(app)