from void.models.activity import Activity


class ActivityController:

    def get_activities(self) -> list[tuple]:
        with Activity() as ac:
            raw_activities = ac.get_active_activities()
            activities = []
            for item in raw_activities:
                activities.append((item['id'], item['activity'], item['category']))
            return activities

    def create_activity(self, activity, category_id):
        with Activity() as ac:
            ac.create_activity(activity, category_id)

    def update_activity(self, activity_id, activity, category_id):
        with Activity() as ac:
            ac.update_activity(activity_id, activity, category_id)

    def suspend_activity(self, activity_id):
        with Activity() as ac:
            ac.suspend_activity(activity_id)
