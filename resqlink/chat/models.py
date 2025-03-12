from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL  # e.g. "accounts.CustomUser"

class Conversation(models.Model):
    """
    A direct conversation between two users (sender, receiver).
    """
    # For a direct 1-to-1 chat, store exactly two participants:
    participant1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversation_initiated')
    participant2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversation_received')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation between {self.participant1.username} and {self.participant2.username}"

    def get_participants(self):
        return [self.participant1, self.participant2]

class Message(models.Model):
    """
    A message in a conversation.
    """
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"
