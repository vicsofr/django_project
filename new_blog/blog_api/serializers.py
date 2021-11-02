import sys
sys.path.append("..")

from rest_framework import serializers
from blog.models import Posts, Comment
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer
from django.contrib.auth.models import User
from taggit.models import Tag


class CommentsListingField(serializers.RelatedField):
    def to_representation(self, value):
        if value.parent:
            return "* child * comment_id: %d, " \
                   "text: '%s', " \
                   "author: '%s', " \
                   "date: '%s', " \
                   "parent_comment_id: '%s'" % (value.id,
                                                value.text,
                                                value.author_id,
                                                value.comment_date.strftime('%d-%m-%Y %H:%m'),
                                                value.parent)
        else:
            return "comment_id: %d, " \
                   "text: '%s', " \
                   "author: '%s', " \
                   "date: '%s'" % (value.id,
                                   value.text,
                                   value.author_id,
                                   value.comment_date.strftime('%d-%m-%Y %H:%m'))


class PostsSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    author = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())
    comments = CommentsListingField(many=True, read_only=True)

    class Meta:
        model = Posts
        fields = ("id", "title", "description", "content", "picture", "date_add", "date_upd", "author",
                  "tags", "views", "comments")
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("name",)
        lookup_field = 'name'
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class RegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password2",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("id", "object_id", "author_id", "text", "parent", "comment_date", "is_child")
        lookup_field = 'id'
        extra_kwargs = {
            'url': {'lookup_field': 'id'}
        }
