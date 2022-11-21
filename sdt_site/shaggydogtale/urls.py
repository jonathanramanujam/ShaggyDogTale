from . import views
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'shaggydogtale'
urlpatterns = [
    path('browse', views.Browse, name="browse"),
    path('create', views.Create, name="create"),
    path('contributed', views.Contributed, name="contributed"),
    path('contributed/<user_id>', views.Contributed, name="contributed"),
    path('view/<story_id>', views.View, name="view")
]

urlpatterns += staticfiles_urlpatterns()
