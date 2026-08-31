from void.models.activity import Activity


class ActivityController:

    def get_activities(self) -> list[tuple]:
        with Activity() as ac:
            raw_activities = ac.get_active_activities()
            activities = []
            for item in raw_activities:
                activities.append((item['activity'], item['category']))
            return activities

    def create_activity(self, activity, category_id):
        with Activity() as ac:
            ac.create_activity(activity, category_id)
