
from django.contrib import admin
from django.urls import path
from app.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/node/', CreateNode.as_view()),
    path('app/path/', FindPath.as_view()),
    path('app/path/slow', SlowFindPath.as_view()),
    path('app/path/slow-result', GetSlowPathResult.as_view())
]
