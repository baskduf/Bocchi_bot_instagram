from django.urls import include, path

urlpatterns = [
    path('', include('instagram_bot.urls')),
]
