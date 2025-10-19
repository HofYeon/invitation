from rest_framework import serializers
from .models import Guestbook

class GuestbookSerializer(serializers.ModelSerializer):
    raw_password = serializers.CharField(write_only=True)

    class Meta:
        model = Guestbook
        fields = ['id', 'invitation', 'author_name', 'content', 'created_at', 'raw_password']
        read_only_fields = ['id', 'invitation', 'created_at']

    def create(self, validated_data):
        raw_password = validated_data.pop('raw_password')
        entry = Guestbook(**validated_data)
        entry.set_password(raw_password)   # 해시 저장
        entry.save()
        return entry