from rest_framework import serializers
from .models import Director, Movie, Review, User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserConfirmationSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(max_length=6)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars']

    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Stars must be between 1 and 5.")
        return value

class MovieSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, required=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'duration', 'reviews', 'rating']

    def get_rating(self, obj):
        average_rating = obj.reviews.aggregate(Avg('stars'))['stars__avg']
        return average_rating if average_rating is not None else 0

    def validate_duration(self, value):
        if value.total_seconds() <= 0:
            raise serializers.ValidationError("Duration must be a positive duration.")
        return value

    def create(self, validated_data):
        reviews_data = validated_data.pop('reviews', [])
        movie = Movie.objects.create(**validated_data)
        for review_data in reviews_data:
            Review.objects.create(movie=movie, **review_data)
        return movie

    def update(self, instance, validated_data):
        reviews_data = validated_data.pop('reviews', [])
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.save()

        for review_data in reviews_data:
            review_id = review_data.get('id', None)
            if review_id:
                review = Review.objects.get(id=review_id, movie=instance)
                review.text = review_data.get('text', review.text)
                review.stars = review_data.get('stars', review.stars)
                review.save()
            else:
                Review.objects.create(movie=instance, **review_data)

        return instance

class DirectorSerializer(serializers.ModelSerializer):
    movies_count = serializers.SerializerMethodField()

    class Meta:
        model = Director
        fields = ['id', 'name', 'movies_count']

    def get_movies_count(self, obj):
        return obj.movies.count()

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty.")
        return value
