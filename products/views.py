from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Shoe
from .serializers import ShoeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# GET all shoes (public)
@api_view(["GET"])
def shoe_list(request):
    shoes = Shoe.objects.all()
    serializer = ShoeSerializer(shoes, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def shoe_create(request):
    serializer = ShoeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# GET single shoe, PUT update, PATCH partial update
@api_view(["GET", "PUT", "PATCH"])
def shoe_detail(request, pk):
    try:
        shoe = Shoe.objects.get(pk=pk)
    except Shoe.DoesNotExist:
        return Response({"error": "Shoe not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ShoeSerializer(shoe)
        return Response(serializer.data)

    elif request.method == "PUT":
        if not request.user.is_authenticated:  # manual check
            return Response({"error": "Login required"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ShoeSerializer(shoe, data=request.data)  # full update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PATCH":
        if not request.user.is_authenticated:  # manual check
            return Response({"error": "Login required"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ShoeSerializer(shoe, data=request.data, partial=True)  # partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
