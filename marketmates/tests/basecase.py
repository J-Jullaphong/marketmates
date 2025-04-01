from datetime import timedelta
from django.utils import timezone
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from notifications.models import Notification
from marketmates.models import Forum, Tag, FavoriteForum, Comment, Expert, ChatRoom


class BaseCase(TestCase):
    """
    Base test case for integration tests in the MarketMates app.

    Provides:
    - 2 regular users (user1, user2) with active status
    - 2 expert users (expert_user1, expert_user2), each linked to an approved Expert profile
    - 3 tags (tag-1, tag-2, tag-3) for categorizing forums
    - 4 regular forums (forum-1 to forum-4), created by user1, each tagged and created on different days
    - 4 expert forums (expert-forum-1 to expert-forum-4), created by expert users
    - 2 comments created by user1 on forum-1 and forum-2
    - 1 favorite forum (forum-1), favorited by user1
    - 3 chat rooms (chatroom-1 to chatroom-3), each with different member combinations
    - 2 notifications with level="info", targeted to user1

    This base case is designed for reuse across views.
    """

    def setUp(self):
        """Set up shared test data"""
        User = get_user_model()

        # Normal User
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='#password123',
            status='Active'
        )
        self.client1 = Client()
        self.client1.login(username='user1', password='#password123')

        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='#password123',
            status='Active'
        )
        self.client2 = Client()
        self.client2.login(username='user2', password='#password123')

        # Tags
        self.tag1 = Tag.objects.create(tag_name="tag-1")
        self.tag2 = Tag.objects.create(tag_name="tag-2")
        self.tag3 = Tag.objects.create(tag_name="tag-3")

        # Forums are created by normal user (based on user1)
        now = timezone.now()
        self.forum1 = Forum.objects.create(
            title="forum-1",
            description="desc-1",
            created_by=self.user1,
            created_at=now - timedelta(days=4)
        )
        self.forum1.tags.set([self.tag1])

        self.forum2 = Forum.objects.create(
            title="forum-2",
            description="desc-2",
            created_by=self.user1,
            created_at=now - timedelta(days=3)
        )
        self.forum2.tags.set([self.tag1, self.tag2])

        self.forum3 = Forum.objects.create(
            title="forum-3",
            description="desc-3",
            created_by=self.user1,
            created_at=now - timedelta(days=2)
        )
        self.forum3.tags.set([self.tag3])

        self.forum4 = Forum.objects.create(
            title="forum-4",
            description="desc-4",
            created_by=self.user1,
            created_at=now - timedelta(days=1)
        )

        # Favorite forum-1
        self.favorite = FavoriteForum.objects.create(
            user=self.user1,
            forum=self.forum1
        )

        # Comment on forum-1
        self.comment1 = Comment.objects.create(
            forum=self.forum1,
            user=self.user1,
            comment_content="This is a comment on forum-1"
        )

        # Comment on forum-2
        self.comment2 = Comment.objects.create(
            forum=self.forum2,
            user=self.user1,
            comment_content="This is a comment on forum-2"
        )

        # Experts
        self.expert_user1 = User.objects.create_user(
            username='expert_user1',
            email='expert-user1@example.com',
            password='#password123',
            status='Active'
        )

        self.expert1 = Expert.objects.create(
            designation="desi-1",
            rank=1,
            user=self.expert_user1,
            status="Approved",
        )

        self.client3 = Client()
        self.client3.login(username='expert_user1', password='#password123')

        self.expert_user2 = User.objects.create_user(
            username='expert_user2',
            email='expert-user2@example.com',
            password='#password123',
            status='Active'
        )

        self.expert2 = Expert.objects.create(
            designation="desi-2",
            rank=2,
            user=self.expert_user2,
            status="Approved",
        )

        self.client4 = Client()
        self.client4.login(username='expert_user2', password='#password123')

        # Expert Forums are created by expert user (based on expert_user1)
        self.expert_forum1 = Forum.objects.create(
            title="expert-forum-1",
            description="expert-desc-1",
            created_by=self.expert_user1,
            created_at=now - timedelta(days=4)
        )
        self.expert_forum1.tags.set([self.tag1])

        self.expert_forum2 = Forum.objects.create(
            title="expert-forum-2",
            description="expert-desc-2",
            created_by=self.expert_user1,
            created_at=now - timedelta(days=3)
        )
        self.expert_forum2.tags.set([self.tag1, self.tag2])

        self.expert_forum3 = Forum.objects.create(
            title="expert-forum-3",
            description="expert-desc-3",
            created_by=self.expert_user2,
            created_at=now - timedelta(days=2)
        )
        self.expert_forum2.tags.set([self.tag3])

        self.expert_forum4 = Forum.objects.create(
            title="expert-forum-4",
            description="expert-desc-4",
            created_by=self.expert_user2,
            created_at=now - timedelta(days=1)
        )

        # ChatRooms
        self.chatroom1 = ChatRoom.objects.create(
            name="chatroom-1",
            capacity=15
        )
        self.chatroom1.members.set([self.user1, self.user2])

        self.chatroom2 = ChatRoom.objects.create(
            name="chatroom-2",
            capacity=10
        )
        self.chatroom2.members.set([self.user1, self.expert_user1])

        self.chatroom3 = ChatRoom.objects.create(
            name="chatroom-3",
            capacity=5
        )
        self.chatroom3.members.set([self.user2, self.expert_user2])

        # Notifications
        self.notification1 = Notification.objects.create(
            recipient=self.user1,
            actor=self.user2,
            verb="replied to your forum",
            target=self.forum1,
            level="info"
        )

        self.notification2 = Notification.objects.create(
            recipient=self.user1,
            actor=self.expert_user1,
            verb="mentioned you in a comment",
            target=self.forum2,
            level="info"
        )
