"""Category business logic: create, update, tree and root_category_id."""
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.category import Category
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryTreeResponse


def _build_tree(categories: list[Category], parent_id: int | None = None) -> list[CategoryTreeResponse]:
    """Build CategoryTreeResponse tree from flat list (avoids lazy load during serialization)."""
    nodes = [c for c in categories if c.parent_id == parent_id]
    return [
        CategoryTreeResponse(
            id=c.id,
            name=c.name,
            parent_id=c.parent_id,
            children=_build_tree(categories, c.id),
        )
        for c in sorted(nodes, key=lambda x: x.name)
    ]


class CategoryService:
    """Category CRUD and hierarchy; maintains root_category_id on create/update."""

    def __init__(self, session: AsyncSession):
        self.repository = CategoryRepository(session)
        self.session = session

    async def create_category(self, data: CategoryCreate) -> Category:
        parent = None
        if data.parent_id:
            parent = await self.repository.get_by_id(data.parent_id)
            if not parent:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Parent category not found"
                )
            if await self.repository.check_cycle(None, data.parent_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot create category: would create a cycle"
                )

        new_category = Category(**data.model_dump())
        await self.repository.create(new_category)
        new_category.root_category_id = (
            (parent.root_category_id or parent.id) if parent else new_category.id
        )
        await self.repository.update(new_category)
        await self.session.commit()
        return new_category

    async def get_category(self, category_id: int) -> CategoryTreeResponse:
        flat = await self.repository.get_all_flat()
        by_id = {c.id: c for c in flat}
        if category_id not in by_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        c = by_id[category_id]
        return CategoryTreeResponse(
            id=c.id,
            name=c.name,
            parent_id=c.parent_id,
            children=_build_tree(flat, c.id),
        )

    async def get_categories(self, offset: int = 0, limit: int = 100) -> list[Category]:
        return await self.repository.get_all_with_children(offset, limit)

    async def get_root_categories(self) -> list[CategoryTreeResponse]:
        """Return root categories as a full tree (no lazy load during serialization)."""
        flat = await self.repository.get_all_flat()
        return _build_tree(flat, parent_id=None)

    async def get_category_children(self, category_id: int) -> list[CategoryTreeResponse]:
        flat = await self.repository.get_all_flat()
        by_id = {c.id: c for c in flat}
        if category_id not in by_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        return _build_tree(flat, category_id)

    async def update_category(
        self, category_id: int, data: CategoryCreate
    ) -> Category:
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        if data.parent_id and data.parent_id != category.parent_id:
            if await self.repository.check_cycle(category_id, data.parent_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Cannot update category: would create a cycle"
                )

        category.name = data.name
        old_parent_id = category.parent_id
        category.parent_id = data.parent_id

        if data.parent_id != old_parent_id:
            if data.parent_id:
                parent = await self.repository.get_by_id(data.parent_id)
                new_root_id = parent.root_category_id or parent.id
            else:
                new_root_id = category_id
            category.root_category_id = new_root_id
            await self.repository.update_root_category_id_for_subtree(
                category_id, new_root_id
            )

        await self.repository.update(category)
        await self.session.commit()
        return category

    async def delete_category(self, category_id: int) -> None:
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )

        category.is_deleted = True
        category.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)
        await self.repository.update(category)
        await self.session.commit()
