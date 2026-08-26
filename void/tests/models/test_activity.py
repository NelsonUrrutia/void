import unittest


from void.models.activity import Activity

class TestActivity(unittest.TestCase):
    def test_get_active_activities(self):
        activity = Activity()
        result = activity.get_active_activities()
        names = {row["name"] for row in result}
        breakpoint()
        self.assertIn("Coding", names)

