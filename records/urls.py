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

    path('student/', StudentListView.as_view(), name='student_list'),
    path('student/add/', StudentCreateView.as_view(), name='student_add'),
    path('major/', MajorListView.as_view(), name='major_list'),
    path('major/add/', MajorCreateView.as_view(), name='major_add'),
    path('admin/', AdminPageView.as_view(), name='admin_page'),
    path('team/', TeamListView.as_view(), name='team_list'),
    path('team/add/', TeamCreateView.as_view(), name='team_add'),
    path('<int:rally_id>/<int:match_id>/result/add/', GameResultCreateView.as_view(), name='game_result_add'),
]