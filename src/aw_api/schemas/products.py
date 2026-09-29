from datetime import date
from pydantic import BaseModel, Field


class ProductCategory(BaseModel):
    name: str

class ProductSubcategory(BaseModel):
    productsubcategoryid: int
    productcategoryid: int
    name: str

class Products(BaseModel):
    productid: int
    name: str
    color: str | None = None
    weight: int | None = None
    product_class: str | None = Field(alias='class')
    discontinueddate: date | None = None