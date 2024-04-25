from rest_framework import serializers

from montachat.chat.models import Conversation
from montachat.chat.models import Message
from montachat.chat.models import Reply


class ReplySerializer(serializers.ModelSerializer[Reply]):
    class Meta:
        model = Reply
        fields = ("text", "id")
        read_only_fields = ("id",)


class MessageSerializer(serializers.ModelSerializer[Message]):
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Message
        fields = ("conversation", "text", "id", "replies")
        read_only_fields = ("id", "replies")

    def validate_conversation(self, conversation):
        if conversation.user != self.context["request"].user:
            raise serializers.ValidationError(
                [f'Invalid pk "{conversation}" - object does not exist.'],
            )

        return conversation


class ConversationSerializer(serializers.ModelSerializer[Conversation]):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ("title", "id", "messages")
        read_only_fields = ("id", "messages")
