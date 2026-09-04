from void.controllers.activity import ActivityController
from void.controllers.category import CategoryController


class NoteController:

    def __init__(self):
        self.category_ctrl = CategoryController()
        self.activity_ctrl = ActivityController()


    def get_activities_by_category(self):
        active_categories = self.category_ctrl.get_categories_for_activities()
        categories_and_activities = []
        for cat in active_categories:
            category, id = cat
            activities = self.activity_ctrl.get_activities_by_category(category_id=id)
            data = (id, category, activities)
            categories_and_activities.append(data)
        return categories_and_activities
