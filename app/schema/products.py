from pydantic import BaseModel, Field , field_validator , model_validator , computed_field
from typing import Annotated, List
from datetime import datetime

class Product(BaseModel):

    id: int

    sku: Annotated[
        str,
        Field(min_length=6, max_length=30, title="Stock Keeping Unit")
    ]

    name: str

    price: Annotated[
        float,
        Field(gt=0, description="Price must be greater than 0")
    ]

    brand: str

    category: str

    inStock: bool

    rating: Annotated[
        float,
        Field(ge=0, le=5)
    ]

    tags: List[str]


    @field_validator("sku",mode="after")
    @classmethod
    def validate_sku_format(cls,value:str):
        if "-" not in value:
            raise ValueError("SKU must have '-'")
        
        last=value.split("-")[-1]
        if not (len(last)==3 and last.isdigit()):
            raise ValueError("SKU must end with 3 _ digit sequence '-'")
        
        return value

    @model_validator(mode="after")
    @classmethod
    def validate_business_rules(cls,model:"Product"):
        if model.stock==0 and model.is_active is True:
            raise ValueError("if stock is 0,is_active must be false")
        
        return model
    
    
