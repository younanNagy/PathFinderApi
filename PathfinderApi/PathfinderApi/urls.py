
from django.contrib import admin
from django.urls import path
from app.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-node/', CreateNode.as_view()),
    # path('find-path/', FindPath.as_view()),
    # path('slow-find-path/', SlowFindPath.as_view()),
    # path('get-slow-path-result/', GetSlowPathResult.as_view())
]
