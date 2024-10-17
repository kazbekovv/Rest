from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from .models import Director, Movie, Review, User
from .serializers import DirectorSerializer, MovieSerializer, ReviewSerializer, UserRegistrationSerializer, UserConfirmationSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Здесь можно отправить email с confirmation_code
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserConfirmationView(generics.GenericAPIView):
    serializer_class = UserConfirmationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['confirmation_code']
        try:
            user = User.objects.get(confirmation_code=code)
            user.is_active = True
            user.confirmation_code = ''
            user.save()
            return Response({"message": "User confirmed successfully."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Invalid confirmation code."}, status=status.HTTP_400_BAD_REQUEST)

class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
