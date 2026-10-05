from sqlalchemy.orm import Session
from sqlalchemy import select

from aw_api.models.products import (
    Product,
    ProductCategory,
    ProductSubCategory
)

def get_all_products(
    db: Session,
    limit: int,
    offset: int
):
    # search = db.execute(
    #         text(
    #             """
    #             SELECT *
    #             FROM production.product
    #             ORDER BY productid
    #             LIMIT :limit
    #             OFFSET :offset
    #             """
    #         ),
    #         {"limit": limit, "offset": offset}
    #     )
    # return search.mappings().all()
    
    stmt = (
        select(Product)
        .order_by(Product.productid)
        .limit(limit)
        .offset(offset)            
    )
    result = db.execute(stmt)
    
    # NOTE: mapppings().all() doesnt apply here because this brings a python "Product" instance of the actual table.
    return result.scalars().all()


def get_specific_product_by_id(db:Session, id: int):
    # info = db.execute(
    #         text(
    #             """
    #             select * from production.product where productid = :productid
    #             """
    #         ),
    #         {"productid": id}
    # )
    # return info.mappings().first()
    
    stmt = select(Product).where(Product.productid == id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def get_all_categories(db: Session):
    # get_all = db.execute(
    #     text("SELECT * FROM production.productcategory"),
    #     {}
    # )    
    # return get_all.mappings().all()
    stmt = select(ProductCategory)
    result = db.execute(stmt)
    return result.scalars().all()


def get_specific_category(db: Session, id: int):
    # TODO: make a better category query with more info being called about the category
    # get_specific = db.execute(
    #     text("SELECT name FROM production.productcategory WHERE productcategoryid = :productcategoryid"),
    #     {"productcategoryid": id}
    # )
    # return get_specific.mappings().first()
    stmt = select(ProductCategory).where(ProductCategory.productcategoryid == id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def get_subcategories_by_id(db: Session, id: int):
    # NOTE: First, check whether the category exists
    # category = db.execute(
    #     text(
    #         """
    #         SELECT productcategoryid
    #         FROM production.productcategory
    #         WHERE productcategoryid = :productcategoryid
    #         """
    #     ),
    #     {"productcategoryid": id}
    # ).first()
    
    category = db.execute(
        select(ProductCategory).where(ProductCategory.productcategoryid == id)
    ).scalar_one_or_none()
    
    if category is None:
        return None

    # NOTE: Category exists, so get its subcategories
    # info = db.execute(
    #     text(
    #         """
    #         SELECT *
    #         FROM production.productsubcategory
    #         WHERE productcategoryid = :productcategoryid
    #         """
    #     ),
    #     {"productcategoryid": id}
    # )

    #return info.mappings().all()

    stmt = select(ProductSubCategory).where(ProductSubCategory.productcategoryid == id)
    result = db.execute(stmt)
    return result.scalars().all()
    

def get_subcategory_detailed_by_id(db: Session, id: int):
    # category = db.execute(
    #     text("""
    #         SELECT productcategoryid
    #         FROM production.productcategory
    #         WHERE productcategoryid = :productcategoryid
    #     """),
    #     {"productcategoryid": id}
    # ).first()
    
    category = db.execute(
        select(ProductCategory).where(ProductCategory.productcategoryid == id)
    ).scalar_one_or_none()

    if category is None:
        return None
        
    # result = db.execute(
        
    #     text("""
    #         SELECT psc.productsubcategoryid, pc.name AS category_name, psc.name AS subcategory_name
    #         FROM production.productsubcategory AS psc
    #         JOIN production.productcategory AS pc 
    #             USING(productcategoryid)
    #         WHERE pc.productcategoryid = :productcategoryid
    #         """
    #     ),
    #     {"productcategoryid":id}
    # )
    # return result.mappings().all()
    
    stmt = (
        select(
            ProductSubCategory.productsubcategoryid,
            ProductCategory.name.label("category_name"), 
            ProductSubCategory.name.label("subcategory_name")
        )
        .join(ProductCategory, ProductSubCategory.productcategoryid == ProductCategory.productcategoryid)
        .where(ProductCategory.productcategoryid == id)
    )
    result = db.execute(stmt)
    return result.mappings().all()