from . import views
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'shaggydogtale'
urlpatterns = [
    path('browse', views.Browse, name="browse"),
    path('create', views.Create, name="create"),
    path('<story_id>', views.View, name="view"),
]

urlpatterns += staticfiles_urlpatterns()
