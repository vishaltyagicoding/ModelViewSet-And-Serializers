# 🔥 When to Override What (IMPORTANT TABLE)
# Situation	Method to override
# Add logic during object creation	create()
# Customize update behavior	update()
# Validate multiple fields	validate()
# Validate single field	validate_<field>()
# Change response format	to_representation()
# Modify incoming data	to_internal_value()
# Dynamic fields	get_fields()

from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author', 'status']

    # ✅ Field-level validation
    # when post api call
    def validate_title(self, value):
        if "bad" in value.lower():
            raise serializers.ValidationError("Title contains inappropriate word")
        return value

    # ✅ Object-level validation
    # when post api call

    def validate(self, data):
        if len(data['content']) < 10:
            raise serializers.ValidationError("Content too short")
        return data

    # ✅ Modify incoming data
    # when post api call

    def to_internal_value(self, data):
        data['title'] = data.get('title', '').strip()
        return super().to_internal_value(data)

    # ✅ Custom create
    # when post api call

    def create(self, validated_data):
        validated_data['status'] = 'published'
        return super().create(validated_data)

    # ✅ Custom update
    # when put/patch api call
    def update(self, instance, validated_data):
        if instance.status == 'published':
            raise serializers.ValidationError("Cannot edit published post")
        return super().update(instance, validated_data)

    # ✅ Customize response
    # when get api call it come to use
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['summary'] = instance.content[:20]  # add extra field
        return data