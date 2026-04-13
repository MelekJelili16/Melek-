from django.contrib import admin # <--- AJOUTE CETTE LIGNE
from django.urls import path
from macronote.views import index, delete_task, toggle_task, delete_all
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('delete/<int:pk>/', delete_task, name='delete_task'),
    path('toggle/<int:pk>/', toggle_task, name='toggle_task'),
    # Ajoute cette ligne dans ton tableau urlpatterns
    path('delete-all/', delete_all, name='delete_all'),
]