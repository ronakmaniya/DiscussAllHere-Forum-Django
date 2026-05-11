from django.contrib.auth.models import User
from django.test import TestCase

from .models import Category, Discussion


class SlugGenerationTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username="tester", password="Pass1234!")

	def test_category_slug_uniqueness(self):
		first = Category.objects.create(name="General Discussion")
		second = Category.objects.create(name="General Discussion")

		self.assertEqual(first.slug, "general-discussion")
		self.assertEqual(second.slug, "general-discussion-1")

	def test_discussion_slug_uniqueness(self):
		category = Category.objects.create(name="Tech News")

		first = Discussion.objects.create(
			category=category,
			title="Same Title",
			content="First content",
			author=self.user,
		)
		second = Discussion.objects.create(
			category=category,
			title="Same Title",
			content="Second content",
			author=self.user,
		)

		self.assertEqual(first.slug, "same-title")
		self.assertEqual(second.slug, "same-title-1")
