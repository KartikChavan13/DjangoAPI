from django.urls import path
from .views import students , student_detail , home
from .views import send_email
from . import views
urlpatterns = [
        path('', home, name='home'),
        path('students/', students),
        path('students/<int:id>/', student_detail),
          path("send-email/", views.send_email, name="send_email"),

]