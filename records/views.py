from django.views import View
from records.models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect,  get_object_or_404, render
from django.urls import reverse
from django.http import JsonResponse

class CompetitionListView(View):
    def get(self, request):
        competitions = Competition.objects.all()
        return render(request, 'records/competition_list.html', {'competitions': competitions})


class CompetitionCreateView(View):
    def get(self, request):
        form = CompetitionForm()
        return render(request, 'records/competition_form.html', {'form': form})

    def post(self, request):
        form = CompetitionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('competition_list')
        return render(request, 'records/competition_form.html', {'form': form})

class MatchListView(View):
    def get(self, request, competition_id):
        competition = get_object_or_404(Competition, pk=competition_id)
        matches = Match.objects.filter(competition=competition)
        return render(request, 'records/match_list.html', {'matches': matches, 'competition': competition})

# records/views.py
class MatchCreateView(View):
    def get(self, request, competition_id):
        form = MatchForm()
        competition = get_object_or_404(Competition, pk=competition_id)
        return render(request, 'records/match_form.html', {'form': form, 'competition': competition})

    def post(self, request, competition_id):
        competition = get_object_or_404(Competition, pk=competition_id)
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.competition = competition
            match.save()
            return redirect('match_list', competition_id=competition_id)
        return render(request, 'records/match_form.html', {'form': form, 'competition': competition})

class SportListView(View):
    def get(self, request):
        sport = Sport.objects.all()
        return render(request, 'records/sport_list.html', {'sports': sport})

class SportCreateView(View):
    def get(self, request):
        form = SportForm()
        return render(request, 'records/sport_form.html', {'form': form})

    def post(self, request):
        form = SportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sport_list')
        return render(request, 'records/sport_form.html', {'form': form})

class GameResultView(View):
    def get(self, request, competition_id, match_id):
        competition = get_object_or_404(Competition, pk=competition_id)
        match = get_object_or_404(Match, pk=match_id)
        gameResults = GameResult.objects.filter(match=match)
        #gameResults의 각 팀 선수들 정보를 가져오기 위해 team_id를 이용해 team_student_mapping을 가져온다.
        for gameResult in gameResults:
            team_student_mapping = TeamStudentMapping.objects.filter(team = gameResult.team)
            students = []
            for mapping in team_student_mapping:
                student = Student.objects.get(student =mapping.student)
                students.append(student)
            gameResult.students = students
        return render(request, 'records/game_result.html', {'gameResults': gameResults, 'match': match, 'competition': competition})

class GameResultCreateView(View):
    def get(self, request, competition_id, match_id):
        GameResult_form = GameResultForm()
        Team_form = TeamForm()
        match = get_object_or_404(Match, pk=match_id)
        competition = get_object_or_404(Competition, pk=competition_id)
        return render(request, 'records/game_result_form.html', {'gameResult_form': GameResult_form, 'team_form': Team_form, 'match': match, 'competition': competition})

    def post(self, request, competition_id, match_id):
        match = get_object_or_404(Match, pk=match_id)
        form = GameResultForm(request.POST)
        if form.is_valid():
            gameResult = form.save(commit=False)
            gameResult.match_id = match
            gameResult.save()
            return redirect('game_result', Competition_id=competition_id, match_id=match_id)
        return render(request, 'records/game_result_form.html', {'form': form, 'match': match})

class StudentListView(View):
    def get(self, request):
        students = Student.objects.all()
        return render(request, 'records/student_list.html', {'students': students})

class StudentCreateView(View):
    def get(self, request):
        form = StudentForm()
        return render(request, 'records/student_form.html', {'form': form})

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
        return render(request, 'records/student_form.html', {'form': form})


class MajorListView(View):
    def get(self, request):
        majors = Major.objects.all()
        return render(request, 'records/major_list.html', {'majors': majors})

class MajorCreateView(View):
    def get(self, request):
        form = MajorForm()
        return render(request, 'records/major_form.html', {'form': form})

    def post(self, request):
        form = MajorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('major_list')
        return render(request, 'records/major_form.html', {'form': form})

class TeamListView(View):
    def get(self, request):
        teams = Team.objects.all()
        return render(request, 'records/team_list.html', {'teams': teams})

class TeamCreateView(View):
    def get(self, request):
        form = TeamForm()
        return render(request, 'records/team_form.html', {'form': form})

    def post(self, request):
        form = TeamForm(request.POST)
        mapping_form = TeamStudentMappingForm()
        if form.is_valid():
            team = form.save()
            for student in form.cleaned_data['students']:
                mapping = TeamStudentMapping(team_id=team, student_id=student)
                mapping.save()
            return JsonResponse({'success': True, 'team_id': team.team_id, 'team_name': team.team_name})
        return JsonResponse({'success': False})

class AdminPageView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'records/admin_page.html')


class TeamsPlayersView(View):
    def get(self, request, team_id):
        team = get_object_or_404(Team, pk=team_id)
        team_student_mapping = TeamStudentMapping.objects.filter(team_id=team)
        students = []
        for mapping in team_student_mapping:
            student = Student.objects.get(student_id=mapping.student_id.student_id)
            students.append(student)
        return JsonResponse({'team_name': team.team_name, 'students': students})

