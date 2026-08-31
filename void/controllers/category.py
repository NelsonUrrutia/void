from void.models.category import Category


class CategoryController:
    def get_categories_for_activities(self) -> list[tuple]:
        with Category() as ca:
            raw_categories = ca.get_active_categories_for_activities()
            categories = []
            for item in raw_categories:
                categories.append((item['category'], item['id']))
            return categories
