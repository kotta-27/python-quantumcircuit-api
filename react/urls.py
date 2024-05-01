from django.urls import path
from myapp.views import execute_python_code

urlpatterns = [
    path("execute_python_code/", execute_python_code, name="execute_python_code"),
]
