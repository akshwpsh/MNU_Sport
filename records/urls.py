from django.urls import path
from .views import *

urlpatterns = [
    path('', CompetitionListView.as_view(), name='home'),
    path('competition/', CompetitionListView.as_view(), name='competition_list'),
    path('competition/add/', CompetitionCreateView.as_view(), name='competition_add'),
    path('<int:competition_id>/matches/', MatchListView.as_view(), name='match_list'),
    path('<int:competition_id>/matches/add/', MatchCreateView.as_view(), name='match_add'),
    path('<int:competition_id>/<int:match_id>/result', GameResultView.as_view(), name='game_result'),
    path('<int:competition_id>/<int:match_id>/result/add/', GameResultCreateView.as_view(), name='game_result_add'),

    path('admin/', AdminPageView.as_view(), name='admin_page'),
    path('sport/', SportListView.as_view(), name='sport_list'),
    path('sport/add/', SportCreateView.as_view(), name='sport_add'),
    path('sport/delete/<int:sport_id>/', SportDeleteView.as_view(), name='sport_delete'),
    path('student/', StudentListView.as_view(), name='student_list'),
    path('student/add/', StudentCreateView.as_view(), name='student_add'),
    path('students/delete/<int:student_id>/', StudentDeleteView.as_view(), name='student_delete'),
    path('student/detail/<int:student_id>/', StudentDetailView.as_view(), name='student_detail'),
    path('major/', MajorListView.as_view(), name='major_list'),
    path('major/add/', MajorCreateView.as_view(), name='major_add'),
    path('team/', TeamListView.as_view(), name='team_list'),
    path('team/add/', TeamCreateView.as_view(), name='team_add'),
    path('teams/<int:team_id>/students/', TeamsPlayersView.as_view(), name=' team_players'),
]