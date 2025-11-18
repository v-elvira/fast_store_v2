from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, insert, update

from app.models.products import Product as ProductModel
from app.models.reviews import Review as ReviewModel
from app.models.users import User as UserModel
from app.schemas import Review as ReviewSchema, ReviewCreate
from app.db_depends import get_async_db
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_current_buyer, get_current_admin

router = APIRouter(
    prefix="",
    tags=["reviews"],
)


@router.get("/reviews", response_model=list[ReviewSchema])
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех активных отзывов.
    """
    result = await db.scalars(select(ReviewModel).where(ReviewModel.is_active==True))
    reviews = result.all()
    return reviews


@router.get("/products/{product_id}/reviews", response_model=list[ReviewSchema])
async def get_product_reviews(product_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список активных отзывов на товар по ID товара.
    """
    # Проверяем, существует ли активный товар
    result = await db.scalars(
        select(ProductModel).where(ProductModel.id == product_id, ProductModel.is_active == True)
    )
    product = result.first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")

    # Получаем активные отзывы по товару
    review_result = await db.scalars(
        select(ReviewModel).where(ReviewModel.product_id == product_id, ReviewModel.is_active == True)
    )
    return review_result.all()


async def update_product_rating(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active == True
        )
    )
    avg_rating = result.scalar() or 0.0
    product = await db.get(ProductModel, product_id)
    product.rating = avg_rating
    # await db.commit()


@router.post("/reviews", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def create_review(
        review: ReviewCreate,
        db: AsyncSession = Depends(get_async_db),
        current_user: UserModel = Depends(get_current_buyer),
):
    """
    Создаёт новый отзыв.
    """
    # Проверка существования товара по его ID
    result = await db.scalars(
        select(ProductModel).where(ProductModel.id == review.product_id, ProductModel.is_active == True)
    )
    product = result.first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")

    # Проверка отсутствия существующего отзыва покупателя на этот товар
    result = await db.scalars(
        select(ReviewModel).where(
            ReviewModel.product_id == review.product_id,
            ReviewModel.user_id == current_user.id,
            ProductModel.is_active == True
        )
    )
    existing_review = result.first()
    if existing_review:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This product review already exists")

    # Создание нового отзыва
    new_review = await db.scalar(insert(ReviewModel).values(
        **review.model_dump(),
        user_id = current_user.id,
    ).returning(ReviewModel))

    # Пересчет рейтинга товара
    await update_product_rating(db, review.product_id)

    await db.commit()
    return new_review


@router.delete("/reviews/{review_id}")
async def delete_review(
        review_id: int,
        db: AsyncSession = Depends(get_async_db),
        current_user: UserModel = Depends(get_current_admin),
):
    """
    Выполняет мягкое удаление отзыва по его ID, устанавливая is_active = False.
    """
    result = await db.scalars(
        select(ReviewModel).where(ReviewModel.id == review_id, ReviewModel.is_active == True)
    )
    review = result.first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    await db.execute(
        update(ReviewModel)
        .where(ReviewModel.id == review_id)
        .values(is_active=False)
    )

    # Пересчет рейтинга товара
    await update_product_rating(db, review.product_id)

    await db.commit()
    return {"message": "Review deleted"}
