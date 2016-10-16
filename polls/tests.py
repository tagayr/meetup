from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question, Choice

# Create your tests here.


class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently should return false for questions that are published in the future
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently should return false for questions that are older than 1 day
        """
        time = timezone.now() - datetime.timedelta(days=2)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_new_question(self):
        """
        was_published_recently should return true for questions that have been created less than a day ago.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        new_question = Question(pub_date=time)
        self.assertEqual(new_question.was_published_recently(), True)




