from datetime import timedelta
from django.utils import timezone
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from marketmates.models import Forum, Tag, FavoriteForum


class BaseCase(TestCase):
    """
    Base test case for integration tests in the MarketMates app.

    Provides:
    - A test user (authenticated)
    - Three tags (tag-1, tag-2, tag-3)
    - Three forums (forum-1, forum-2, forum-3) with different created_at dates and tags
    - One favorite forum (forum-1)

    This base is designed for reusability in other views.
    """

    def setUp(self):
        """
        Create shared test data:
        - Logs in a test user
        - Creates 3 tags
        - Creates 3 forums with increasing created_at timestamps
        - Assigns tags to forums
        - Marks forum-1 as a favorite
        """
        self.client = Client()
        User = get_user_model()

        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            status='Active'
        )
        self.client.login(username='testuser', password='testpass123')

        # Tags
        self.tag1 = Tag.objects.create(tag_name="tag-1")
        self.tag2 = Tag.objects.create(tag_name="tag-2")
        self.tag3 = Tag.objects.create(tag_name="tag-3")

        # Forums
        now = timezone.now()
        self.forum1 = Forum.objects.create(
            title="forum-1",
            description="desc-1",
            created_by=self.user,
            created_at=now - timedelta(days=3)
        )
        self.forum1.tags.set([self.tag1])

        self.forum2 = Forum.objects.create(
            title="forum-2",
            description="desc-2",
            created_by=self.user,
            created_at=now - timedelta(days=2)
        )
        self.forum2.tags.set([self.tag1, self.tag2])

        self.forum3 = Forum.objects.create(
            title="forum-3",
            description="desc-3",
            created_by=self.user,
            created_at=now - timedelta(days=1)
        )
        self.forum3.tags.set([self.tag3])

        # Favorite forum-1
        self.favorite = FavoriteForum.objects.create(
            user=self.user,
            forum=self.forum1
        )
