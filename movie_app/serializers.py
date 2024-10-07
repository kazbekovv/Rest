from rest_framework import serializers
from .models import Director, Movie, Review
from django.db.models import Avg

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['text', 'stars']

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'duration', 'reviews', 'rating']

    def get_rating(self, obj):
        average_rating = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        return average_rating if average_rating is not None else 0

class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = ['id', 'name', 'movies_count']

    def get_movies_count(self, obj):
        return obj.movies.count()

