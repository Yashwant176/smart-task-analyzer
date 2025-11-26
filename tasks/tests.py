from django.test import TestCase, Client
from .scoring import analyze_tasks, CircularDependencyError
from datetime import date, timedelta
import json

class ScoringUnitTests(TestCase):
    def test_basic_sorting(self):
        today = date.today()
        tasks = [
            {"id":1, "title":"Quick urgent", "due_date": (today + timedelta(days=1)).isoformat(), "estimated_hours":0.5, "importance":5, "dependencies":[]},
            {"id":2, "title":"Big later", "due_date": (today + timedelta(days=10)).isoformat(), "estimated_hours":6, "importance":9, "dependencies":[]},
            {"id":3, "title":"Medium", "due_date": (today + timedelta(days=3)).isoformat(), "estimated_hours":2, "importance":6, "dependencies":[]},
        ]
        out = analyze_tasks(tasks, strategy='smart_balance')
        self.assertIsInstance(out, list)
        self.assertGreaterEqual(out[0]['score'], out[-1]['score'])

    def test_past_due_priority(self):
        today = date.today()
        tasks = [
            {"id":1,"title":"Past due","due_date":(today - timedelta(days=2)).isoformat(),"estimated_hours":4,"importance":5,"dependencies":[]},
            {"id":2,"title":"Far","due_date":(today + timedelta(days=30)).isoformat(),"estimated_hours":1,"importance":5,"dependencies":[]},
        ]
        out = analyze_tasks(tasks)
        self.assertGreater(out[0]['score'], out[1]['score'])

    def test_detect_cycle(self):
        tasks = [
            {"id":1,"title":"A","due_date":None,"estimated_hours":1,"importance":5,"dependencies":[2]},
            {"id":2,"title":"B","due_date":None,"estimated_hours":1,"importance":5,"dependencies":[1]},
        ]
        with self.assertRaises(CircularDependencyError):
            analyze_tasks(tasks)

class ApiIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_analyze_endpoint_and_suggest(self):
        sample = [
            {"id":1,"title":"T1","due_date":None,"estimated_hours":1,"importance":5,"dependencies":[]},
            {"id":2,"title":"T2","due_date":None,"estimated_hours":2,"importance":6,"dependencies":[1]},
        ]
        res = self.client.post('/api/tasks/analyze/', data=json.dumps(sample), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn('tasks', data)
        # now suggest
        res2 = self.client.get('/api/tasks/suggest/')
        self.assertEqual(res2.status_code, 200)
        sd = res2.json()
        self.assertIn('suggestions', sd)
        self.assertTrue(len(sd['suggestions']) <= 3)
