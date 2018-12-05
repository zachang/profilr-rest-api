from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .serializers import HelloSerializer, UserProfileSerializer, ProfileFeedItemSerializer
from .models import UserProfile, ProfileFeedItem
from .permissions import UpdateOwnProfile, PostOwnStatus

# Create your views here.

class HelloApiView(APIView):
    """Test Api Views"""

    serializer_class = HelloSerializer

    def get(self, request, format=None):
        """Returns a list of APIView feature"""

        an_api = [
            'Is mapped manually to URLs',
            'Gives most control over your logic',
            'It is like traditional Django Views'
        ]

        return Response({'message': 'Hello', 'an_api': an_api})

    def post(self, request):
        """Create Hello message with name"""

        serializer = HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, pk=None):
        """Handles object update"""

        return Response({'method': 'put'})

    def patch(self, request, pk=None):
        """Handles object partial update"""

        return Response({'method': 'patch'})

    def delete(self, request, pk=None):
        """Handles object deletion"""

        return Response({'method': 'delete'})

class  HelloViewSet(viewsets.ViewSet):
    """Testing API Viewset"""

    serializer_class = HelloSerializer

    def list(self, request):
        """Return hello message"""

        a_viewset = [
            'Uses actions (list, create,retrieve, update, partial update, destroy)',
            'Automatically maps to url using Routers',
            'Provides more functionality with less code'
        ]

        return Response({'message': 'Hello', 'a_viewset': a_viewset})

    def create(self, request):
        """Create new hello message"""

        serializer = HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = f'Hello {name}'

            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handles getting a single object"""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        """Handles object update"""

        return Response({'http_method': 'PUT' })

    def partial_update(self, request, pk=None):
        """Handles object partial update"""

        return Response({'http_method': 'PATCH' })

    def destroy(self, request, pk=None):
        """Handles object deletion"""

        return Response({'http_method': 'DELETE' })

class UserProfileViewset(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile"""

    serializer_class = UserProfileSerializer

    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)

class LoginViewset(viewsets.ViewSet):
    """Checks email and password then returns authtoken"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        """Use ObtainAuthToken APIView to validate and create token"""

        serializer = AuthTokenSerializer(data=request.data)

        return ObtainAuthToken().post(request)

class UserProfileFeedViewset(viewsets.ModelViewSet):
    """Handles creating, reading and updating profile feed item"""

    serializer_class = ProfileFeedItemSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (PostOwnStatus, IsAuthenticated,)
    queryset = ProfileFeedItem.objects.all()

    def perform_create(self, serializer):
        """Sets user profile to logged in user"""

        serializer.save(user_profile=self.request.user)
