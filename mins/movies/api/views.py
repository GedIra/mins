from .serializers import (
  UserSerializer, UserRegistrationSerializer, ReviewSerializer,
  CommentSerializer, LikeSerializer, MovieSerializer, User
)
from movies.models import (
  Movie, Review, Comment, Like
)
from rest_framework import generics
from rest_framework.permissions import (
  IsAuthenticated, IsAdminUser, SAFE_METHODS, 
  DjangoModelPermissionsOrAnonReadOnly, AllowAny, IsAuthenticatedOrReadOnly,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import MovieFilter
from .permissions import IsAdminUserOrIsOwnerOrReadOnly, IsAdminUserOrIsUserOrReadOnly

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

class UserslistAPIView(generics.ListAPIView):
  serializer_class = UserSerializer
  lookup_field = 'username'
  queryset = User.objects.all()
  permission_classes = [AllowAny]
  
class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = UserSerializer
  lookup_field = 'username'
  permission_classes = [IsAdminUserOrIsUserOrReadOnly]
  queryset = User.objects.all()

class MovieListCreateAPIView(generics.ListCreateAPIView):
  serializer_class = MovieSerializer
  queryset = Movie.objects.all()
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
  filterset_class = MovieFilter
  search_fields = ['title', 'director', 'released_date']
  ordering = ['title']
  ordering_fields = '__all__'
  
  permission_classes = [IsAuthenticatedOrReadOnly]

  def get_permissions(self):
    if self.request.method == 'POST':
      # Only admin users can create movies
      self.permission_classes = [IsAdminUser]
    else:
      # All users can retrieve and list movies
      self.permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    return super().get_permissions()
  
class MovieRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = MovieSerializer
  queryset =Movie.objects.all()
  lookup_field = 'slug'
  permission_classes = []

  def get_permissions(self):
    if self.request.method in SAFE_METHODS:
      # All users can retrieve and list movies
      self.permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    else:
      # Only admin users can update or delete movies
      self.permission_classes = [IsAdminUser]
    return super().get_permissions()
   
class ReviewListCreateAPIView(generics.ListCreateAPIView):
  serializer_class = ReviewSerializer
  queryset = Review.objects.all()
  permission_classes = [IsAuthenticatedOrReadOnly]
    
  def perform_create(self, serializer):
    #sets Review auhtor to the currrent user
    serializer.save(author = self.request.user)
    return super().perform_create(serializer)

  
class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = ReviewSerializer
  lookup_field = 'slug'
  permission_classes = [IsAdminUserOrIsOwnerOrReadOnly]
  queryset = Review.objects.all()
  
  def perform_update(self, serializer):
    #sets Review auhtor to the currrent user
    serializer.save(author = self.request.author)
    return super().perform_update(serializer)

class CommentListCreateAPIView(generics.ListCreateAPIView):
  serializer_class = CommentSerializer
  queryset = Comment.objects.all()
  permission_classes = [IsAuthenticatedOrReadOnly]
  
  def perform_create(self, serializer):
    #sets Comment auhtor to the currrent user
    serializer.save(author = self.request.author)
    return super().perform_create(serializer)
  
class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = CommentSerializer
  lookup_field = 'slug'
  permission_classes = [IsAdminUserOrIsOwnerOrReadOnly]
  queryset = Comment.objects.all()

  def perform_update(self, serializer):
    #sets Comment auhtor to the currrent user
    serializer.save(author = self.request.author)
    return super().perform_update(serializer)
  
class LikeListCreateAPIView(generics.ListCreateAPIView):
  serializer_class = LikeSerializer
  queryset = Like.objects.all()
  permission_classes = [IsAuthenticatedOrReadOnly]
  
  def perform_create(self, serializer):
    serializer.save(author = self.request.user)
    return super().perform_create(serializer)
  
class LikeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
  serializer_class = LikeSerializer
  lookup_field = 'slug'
  permission_classes = [IsAdminUserOrIsOwnerOrReadOnly]
  queryset = Like.objects.all()
  
  def perform_update(self, serializer):
    serializer.save(author = self.request.user)
    return super().perform_update(serializer)


