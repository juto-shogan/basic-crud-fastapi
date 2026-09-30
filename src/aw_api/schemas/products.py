from datetime import date
from pydantic import BaseModel, Field


class Product(BaseModel):
    productid: int
    name: str
    color: str | None = None
    weight: float | None = None
    product_class: str | None = Field(alias='class')
    discontinueddate: date | None = None

class ProductCategory(BaseModel):
    name: str

class ProductSubcategory(BaseModel):
    productsubcategoryid: int
    productcategoryid: int
    name: str

class ProductSubcategoryDetailed(BaseModel):
    productsubcategoryid: int
    category_name: str
    subcategory_name: str