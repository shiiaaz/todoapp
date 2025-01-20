from django.test import TestCase
from django.urls import reverse
from base.models import Task
from django.contrib.auth.models import User
from datetime import datetime

class EditTaskViewTests(TestCase):

    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # Create a sample task for the user
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            due_date=datetime(2025, 1, 15, 10, 30),
            completed=False,
            user=self.user
        )

    def test_edit_task_view_renders_correct_template(self):
        # Test if the edit task view renders the correct template
        response = self.client.get(reverse('edit_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_task.html')

    def test_edit_task_success(self):
        # Test if a task is successfully updated
        updated_data = {
            'title': 'Updated Task Title',
            'description': 'Updated Description',
            'due_date': '2025-01-20T14:00',
            'completed': True,
        }
        response = self.client.post(reverse('edit_task', args=[self.task.id]), updated_data)

        self.assertEqual(response.status_code, 302)  # Should redirect after success
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task Title')
        self.assertEqual(self.task.description, 'Updated Description')
        self.assertEqual(self.task.due_date, datetime(2025, 1, 20, 14, 0))
        self.assertTrue(self.task.completed)

    def test_edit_task_invalid_data(self):
        # Test with invalid data (e.g., missing title)
        invalid_data = {
            'title': '',  # Title is required
            'description': 'Updated Description',
            'due_date': '2025-01-20T14:00',
            'completed': True,
        }
        response = self.client.post(reverse('edit_task', args=[self.task.id]), invalid_data)

        self.assertEqual(response.status_code, 200)  # Form errors should keep user on the same page
        self.assertContains(response, 'This field is required.')  # Check for validation error message

    def test_edit_task_unauthorized_access(self):
        # Test that a user cannot edit another user's task
        other_user = User.objects.create_user(username='otheruser', password='password123')
        self.client.login(username='otheruser', password='password123')

        response = self.client.get(reverse('edit_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 404)  # Should return 404 for unauthorized access

    def test_due_date_field_format(self):
        # Test that the due_date field is displayed in the correct format in the form
        response = self.client.get(reverse('edit_task', args=[self.task.id]))
        self.assertContains(response, 'value="2025-01-15T10:30"')  # Check if due_date is correctly formatted


# Run these tests with `python manage.py test`
