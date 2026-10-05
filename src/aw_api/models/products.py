from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from aw_api.models.base import Base


class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"schema": "production"}
    
    productid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    
class ProductCategory(Base):
    __tablename__ = "productcategory"
    __table_args__ = {"schema": "production"}
    
    productcategoryid: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    
class ProductSubCategory(Base):
    __tablename__ = "productsubcategory"
    __table_args__ = {"schema": "production"}

    productsubcategoryid: Mapped[int] = mapped_column(primary_key=True)
    productcategoryid: Mapped[int] = mapped_column(
        ForeignKey(
            "production.productcategory.productcategoryid"
        )
    )
    name: Mapped[str]