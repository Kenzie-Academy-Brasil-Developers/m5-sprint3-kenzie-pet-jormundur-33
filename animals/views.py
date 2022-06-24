from functools import partial
from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView, Response, status
from .serializers import AnimalSerializer
from .models import Animal


class AnimalView(APIView):

    def delete(self, request, animal_id):
        try:
            animal = Animal.objects.get(id=animal_id)
        except:
            return Response({"message": "Animal not found"},
                            status.HTTP_404_NOT_FOUND)
        animal.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, animal_id):
        try:
            animal = Animal.objects.get(id=animal_id)
        except Animal.DoesNotExist:
            return Response({"message": "Animal not found"},
                            status.HTTP_404_NOT_FOUND)

        serializer = AnimalSerializer(animal)
        return Response(serializer.data)

    def patch(self, request, animal_id):
        try:
            animal = Animal.objects.get(id=animal_id)
        except:
            return Response({"message":"Animal not found"},
                            status.HTTP_404_NOT_FOUND)
        serializer = AnimalSerializer(animal, request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            serializer.save()
        except KeyError:
            print(KeyError.__dict__)
            if 'sex' in request.data:
                return Response({"message":"You not update sex property"},
                                status.HTTP_422_UNPROCESSABLE_ENTITY)
            if 'group' in request.data:
                return Response({"message":"You not update group property"},
                                status.HTTP_422_UNPROCESSABLE_ENTITY)
        return Response(serializer.data)


class AnimalsView(APIView):

    def post(self, request):
        serializer = AnimalSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request):

        animals = Animal.objects.all()

        serializer = AnimalSerializer(animals, many=True)

        return Response(serializer.data)