from void.database.connection import Connection

class Activity:

    def get_active_activities(self):
        with Connection() as db:
            sql = "SELECT * FROM activities WHERE is_active == 1;"
            result = db.querying(sql)
            return result
