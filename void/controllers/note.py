from void.controllers.activity import ActivityController
from void.controllers.category import CategoryController
from void.models.note import Note


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

    def get_activities(self):
        """Every active activity as (id, name, category)."""
        return self.activity_ctrl.get_activities()

    def get_activity_total(self):
        return len(self.get_activities())

    def save_note(self, date_str, activities):
        with Note() as note:
            note_id = note.save_note(date_str)
            for activity in activities:
                activity_info, activity_note = activity
                self.save_note_details(note_id, activity_info, activity_note)

    def save_note_details(self, note_id, activity_info, activity_note):
        with Note() as note:
            note.save_note_detail(note_id, activity_info, activity_note)

    def get_day_note(self, date_str):
        with Note() as note:
            return note.get_day_note(date_str)

    def get_notes(self):
        with Note() as note:
            return note.get_notes()
