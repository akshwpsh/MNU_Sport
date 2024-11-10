from django.urls import path
from .views import *

urlpatterns = [
    path('rally/', RallyListView.as_view(), name='rally_list'),
    path('rally/add/', RallyCreateView.as_view(), name='rally_add'),
    path('<int:rally_id>/matches/', MatchListView.as_view(), name='match_list'),
    path('<int:rally_id>/matches/add/', MatchCreateView.as_view(), name='match_add'),
    path('sport/', SportListView.as_view(), name='sport_list'),
    path('sport/add/', SportCreateView.as_view(), name='sport_add'),
    path('<int:rally_id>/<int:match_id>/result', GameResultView.as_view(), name='game_result'),
]