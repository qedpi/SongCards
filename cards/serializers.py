#from rest_framework import serializers
from .models import Card


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        # fields = __all__ #dunder for all

        fields = ('topic', 'front', 'back', 'card_audio', 'card_score', 'card_pic')
