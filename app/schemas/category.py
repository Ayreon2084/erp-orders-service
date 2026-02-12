from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str = Field(..., max_length=255, description="Category name")
    parent_id: int | None = Field(None, description="ID of the parent category (null if root)")


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class CategoryTreeResponse(CategoryResponse):
    """Schema for returning category with its children (for tree view)"""
    children: list["CategoryTreeResponse"] = []


CategoryTreeResponse.model_rebuild()