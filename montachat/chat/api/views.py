import logging

from django.conf import settings
from openai import OpenAI
from rest_framework.exceptions import APIException
from rest_framework.mixins import CreateModelMixin
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import GenericViewSet

from montachat.chat.api.serializers import ConversationSerializer
from montachat.chat.api.serializers import MessageSerializer
from montachat.chat.models import Conversation
from montachat.chat.models import Message
from montachat.chat.models import Reply


class ConversationViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.all()
    lookup_field = "pk"

    def get_queryset(self):
        return self.queryset.filter(user__id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MessageViewSet(
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    lookup_field = "pk"

    def get_queryset(self):
        return self.queryset.filter(conversation__user__id=self.request.user.id)

    def perform_create(self, serializer):
        conversation = serializer.validated_data["conversation"]
        conversation_history = conversation.messages.all()
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        messages = []
        for msg in conversation_history:
            messages.append(
                {"role": "user", "content": msg.text, "name": conversation.user.name},
            )
            messages.extend(
                [
                    {"role": "assistant", "content": reply.text}
                    for reply in msg.replies.all()
                ],
            )
        messages.append(
            {
                "role": "user",
                "content": serializer.validated_data.get("text"),
                "name": conversation.user.name,
            },
        )
        try:
            response = client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                user=f"{conversation.user.id}",
                temperature=0,
            )
            reply_choice = response.choices[0]
            message = serializer.save()
            Reply.objects.create(message=message, text=reply_choice.message.content)
            message.refresh_from_db()
        except Exception as e:  # noqa: BLE001
            logging.info(e)
            error_message = "Something went wrong while contacting ChatGPT API"
            raise APIException(error_message) from e
        return message
