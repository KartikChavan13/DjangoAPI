from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Student
from .serializers import StudentSerializer
from django.shortcuts import render

from django.core.mail import send_mail
from django.http import HttpResponse

def home(request):
    return render(request, 'index.html')

@api_view(['GET', 'POST'])
def students(request):
    if request.method == 'GET':
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def student_detail(request, id):

    try:
        student = Student.objects.get(id=id)
    except Student.DoesNotExist:
        return Response(
            {"error": "Student not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(
            {"message": "Student deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )

@api_view(["POST"])
def send_email(request):

    email = request.data.get("email")

    if not email:
        return Response(
            {"success": False, "message": "Email is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    send_mail(
        subject="Welcome",
        message="Hello! Welcome to Django.",
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )

    return Response(
        {
            "success": True,
            "message": "Email sent successfully"
        },
        status=status.HTTP_200_OK
    )