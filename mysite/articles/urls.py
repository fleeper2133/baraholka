from django.urls import path
from .views import *

urlpatterns = [
    path('', ArticlesMain.as_view(), name='home'),
    path('add_article/', AddArticle.as_view(), name='add_article'),
    path('<slug:cat_slug>', CategoryArticles.as_view(), name='categories'),
    path("work/", Work.as_view(), name="work"),
    path("work/update_acceptance", update_acceptance, name="update_acceptance"),
    path("work/update_article/<int:pk>/", UpdateArticle.as_view(), name="update_article"),
    path("about/", about, name="about")
]
