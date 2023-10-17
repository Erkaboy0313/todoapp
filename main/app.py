from fastapi import FastAPI
from api.routes.routes import router
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()
app.include_router(router)
register_tortoise(
    app=app,
    db_url="sqlite://todo.db",
    add_exception_handlers=True,
    generate_schemas=True,
    modules={"models":['api.models.todo']}
)

@app.get('/')
async def home():
    return {'info':"to do app is running"}