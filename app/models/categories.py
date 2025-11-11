from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))  # add if startup problem
from app.database import Base

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from app.models.products import Product


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)
    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")
    parent: Mapped["Category|None"] = relationship("Category", back_populates="children", remote_side="Category.id")
    children: Mapped[list["Category"]] = relationship("Category", back_populates="parent")


if __name__ == "__main__":
    from sqlalchemy.schema import CreateTable
    from app.models.products import Product

    print(CreateTable(Product.__table__))
    print(CreateTable(Category.__table__))
    '''
    CREATE TABLE categories (
        id INTEGER NOT NULL, 
        name VARCHAR(50) NOT NULL, 
        is_active BOOLEAN NOT NULL, 
        parent_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(parent_id) REFERENCES categories (id)
    )
    '''
