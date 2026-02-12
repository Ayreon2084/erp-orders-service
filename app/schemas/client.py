from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ClientBase(BaseModel):
    full_name: str = Field(..., max_length=255, description="Full name or company name")
    address: str | None = Field(None, max_length=500, description="Physical delivery address")
    email: EmailStr = Field(..., description="Unique contact email")


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    full_name: str | None = Field(None, max_length=255)
    address: str | None = Field(None, max_length=500)
    email: EmailStr | None = None


class ClientResponse(ClientBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
