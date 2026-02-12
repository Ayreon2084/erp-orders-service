"""Category repository."""
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.category import Category
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)

    async def get_by_id_with_children(self, id: int) -> Category | None:
        result = await self.session.execute(
            select(Category)
            .options(selectinload(Category.children))
            .where(Category.id == id, Category.is_deleted.is_(False))
        )
        return result.scalar_one_or_none()

    async def get_all_with_children(self, offset: int = 0, limit: int = 100) -> list[Category]:
        result = await self.session.execute(
            select(Category)
            .options(selectinload(Category.children))
            .where(Category.is_deleted.is_(False))
            .order_by(Category.parent_id.nulls_first(), Category.name)
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_all_flat(self) -> list[Category]:
        """Load all non-deleted categories (no relationships). For building tree in service."""
        result = await self.session.execute(
            select(Category)
            .where(Category.is_deleted.is_(False))
            .order_by(Category.parent_id.nulls_first(), Category.name)
        )
        return list(result.scalars().all())

    async def get_root_categories(self) -> list[Category]:
        result = await self.session.execute(
            select(Category)
            .options(selectinload(Category.children))
            .where(Category.parent_id.is_(None), Category.is_deleted.is_(False))
            .order_by(Category.name)
        )
        return list(result.scalars().all())

    async def get_children(self, parent_id: int) -> list[Category]:
        result = await self.session.execute(
            select(Category)
            .options(selectinload(Category.children))
            .where(Category.parent_id == parent_id, Category.is_deleted.is_(False))
            .order_by(Category.name)
        )
        return list(result.scalars().all())

    async def check_cycle(
        self, category_id: int | None, potential_parent_id: int
    ) -> bool:
        if category_id is not None and category_id == potential_parent_id:
            return True

        current_id: int | None = potential_parent_id
        visited = set()

        while current_id is not None:
            if category_id is not None and current_id == category_id:
                return True
            if current_id in visited:
                break
            visited.add(current_id)

            result = await self.session.execute(
                select(Category.parent_id).where(
                    Category.id == current_id, Category.is_deleted.is_(False)
                )
            )
            current_id = result.scalar_one_or_none()

        return False

    async def get_by_id(self, id: int) -> Category | None:
        result = await self.session.execute(
            select(Category).where(Category.id == id, Category.is_deleted.is_(False))
        )
        return result.scalar_one_or_none()

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[Category]:
        result = await self.session.execute(
            select(Category)
            .where(Category.is_deleted.is_(False))
            .order_by(Category.parent_id.nulls_first(), Category.name)
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update_root_category_id_for_subtree(
        self, category_id: int, new_root_id: int
    ) -> None:
        """Set root_category_id for this category and all descendants (e.g. when parent_id changes)."""
        await self.session.execute(
            text("""
                WITH RECURSIVE descendants AS (
                    SELECT id FROM categories WHERE id = :category_id
                    UNION ALL
                    SELECT c.id FROM categories c
                    JOIN descendants d ON c.parent_id = d.id
                )
                UPDATE categories SET root_category_id = :new_root_id
                WHERE id IN (SELECT id FROM descendants)
            """),
            {"category_id": category_id, "new_root_id": new_root_id},
        )
