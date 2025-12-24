import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles

from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.routers import categories, products, users, reviews, cart, orders


# Создаём приложение FastAPI
app = FastAPI(
    title="FastAPI Интернет-магазин",
    version="0.1.0",
)

app.mount("/media", StaticFiles(directory="media"), name="media")

# # Handle general Pydantic validation errors that might slip through  # for .as_form uncaught
## moved to ProductCreate schema .as_form try/except
# @app.exception_handler(ValidationError)
# async def validation_exception_handler(request: Request, exc: ValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content={"message": "Validation error", "details": exc.errors()},
#     )

# Подключаем маршруты категорий и товаров
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(reviews.router)
app.include_router(users.router)
app.include_router(cart.router)
app.include_router(orders.router)


# Корневой эндпоинт для проверки
@app.get("/")
async def root():
    """
    Корневой маршрут, подтверждающий, что API работает.
    """
    return {"message": "Добро пожаловать в API интернет-магазина!"}


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', reload=True, port=8000)
