from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>', views.topic, name='topic'),
    path('addEntry/', views.addEntry, name='addEntry'),
    path('wiki/editEntry/<str:title>', views.editEntry, name='editEntry'),
    path('wiki/submitEditedEntry/<str:title>', views.submitEditedEntry, name='submitEditEntry'),
    path('wiki/', views.randomEntry, name='randomEntry'),
]


