from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer
from .models import Dialog, Message
from rest_framework import serializers
from .request_to_agent import take_answer

User = get_user_model()


class DialogModelSerializer(ModelSerializer):
    """
    Serializer class for the Dialog model.

    This serializer is used to serialize and deserialize Dialog objects.

    Fields:
        latest_message (SerializerMethodField): The latest message associated with the dialog.
    """

    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = Dialog
        fields = '__all__'

    def get_latest_message(self, obj):
        """
        Get the latest message associated with the dialog.

        This method retrieves the latest message associated with the dialog
        by filtering the messages based on the dialog ID and ordering them
        by descending ID. It returns the answer text of the latest message
        or None if no messages are found.

        Args:
            obj (Dialog): The Dialog object.

        Returns:
            str or None: The answer text of the latest message or None.
        """

        try:
            customer_account_query = Message.objects.filter(
                dialog_id=obj.id
            ).latest('id')

            return customer_account_query.answer_text
        except Exception as e:
            return None


class MessageModelSerializer(ModelSerializer):
    """
    Serializer class for the Message model.

    This serializer is used to serialize and deserialize Message objects.

    Methods:
        create(self, validated_data): Creates a new message instance.
    """

    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        """
        Creates a new message instance.

        This method creates a new Message instance with the provided data.
        It generates an answer text using the `take_answer` utility function.

        Args:
            validated_data (dict): The validated data containing message_text and dialog_id.

        Returns:
            Message: The created message instance.
        """

        if 'answer_text' in validated_data:
            validated_data.pop('answer_text')
        answer_text = take_answer(validated_data['message_text'], validated_data['dialog_id'])
        message = Message.objects.create(answer_text=answer_text, **validated_data)
        return message
