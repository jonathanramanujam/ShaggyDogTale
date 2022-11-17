from . import views
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'shaggydogtale'
urlpatterns = [
    path('', views.Browse, name="browse"),
    path('<story_id>', views.View, name="view")
]

urlpatterns += staticfiles_urlpatterns()
