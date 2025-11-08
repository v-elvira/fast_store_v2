from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))  # add if startup problem
from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


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
	    PRIMARY KEY (id)
    )
    '''
