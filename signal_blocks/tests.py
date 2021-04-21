from django.test import TestCase, Client

# Create your tests here.

class EventBlock(TestCase):
    def test_intersect_event(self):
        request = {
            "input": {
                "event_type": "",
                "event_action": ""
            },
            "output": {
                "COMPUTATIONAL_BLOCK-1-1": {}
            }
        }

        assert False