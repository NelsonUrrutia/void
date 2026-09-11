import sqlite3

from void.models.category import Category


class CategoryController:
    def get_categories_for_activities(self) -> list[tuple]:
        with Category() as ca:
            raw_categories = ca.get_active_categories_for_activities()
            categories = []
            for item in raw_categories:
                categories.append((item['category'], item['id']))
            return categories

    def get_categories(self) -> list[tuple]:
        with Category() as ca:
            raw_categories = ca.get_active_categories()
            categories = []
            for item in raw_categories:
                categories.append((item['category'],))
            return categories

    def create_category(self, category) -> bool:
        """Return False when a category with that name already exists."""
        with Category() as ca:
            try:
                ca.create_category(category)
            except sqlite3.IntegrityError:
                return False
        return True
