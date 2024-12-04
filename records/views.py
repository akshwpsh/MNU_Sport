from django.views import View
from records.models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect,  get_object_or_404, render
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q

class CompetitionListView(View):
    def get(self, request):
        query = request.GET.get('q')
        if query:
            competitions = Competition.objects.filter(name__icontains=query)
        else:
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

class CompetitionDeleteView(View):
    def post(self, request, competition_id):
        competition = get_object_or_404(Competition, pk=competition_id)
        competition.delete()
        return redirect('competition_list')

class MatchListView(View):
    def get(self, request, competition_id):
        queue = request.GET.get('q')
        competition = get_object_or_404(Competition, pk=competition_id)
        if queue:
            matches = Match.objects.filter(
                Q(match_name__icontains=queue) | Q(sport__name__icontains=queue),
                competition=competition_id
            )
        else:
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

class MatchDeleteView(View):
    def post(self, request, competition_id, match_id):
        match = get_object_or_404(Match, pk=match_id)
        match.delete()
        return redirect('match_list', competition_id=competition_id)

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

class SportDeleteView(View):
    def post(self, request, sport_id):
        sport = get_object_or_404(Sport, pk=sport_id)
        sport.delete()
        return redirect('sport_list')

class GameResultView(View):
    def get(self, request, competition_id, match_id):
        competition = get_object_or_404(Competition, pk=competition_id)
        match = get_object_or_404(Match, pk=match_id)
        gameResults = GameResult.objects.filter(match=match)

        # Fetch team and player information along with their scores
        for gameResult in gameResults:
            team_game_result_mapping = TeamGameResultMapping.objects.filter(gameResult=gameResult)
            teams = []
            for result_mapping in team_game_result_mapping:
                team = result_mapping.team
                students = []
                team_student_mappings = TeamStudentMapping.objects.filter(team=team)
                for mapping in team_student_mappings:
                    student = mapping.student
                    # Fetch the player's score for this game result
                    player_score = PlayerScore.objects.filter(student=student, gameResult=gameResult).first()
                    students.append({
                        'name': student.name,
                        'student_id': student.student_id,
                        'score': player_score.score if player_score else 0
                    })
                teams.append({
                    'team_id': team.team_id,
                    'team_name': team.team_name,
                    'students': students
                })
            gameResult.teams = teams

        return render(request, 'records/game_result.html', {'gameResults': gameResults, 'match': match, 'competition': competition})

class GameResultDeleteView(View):
    def post(self, request, competition_id, match_id, game_result_id):
        gameResult = get_object_or_404(GameResult, pk=game_result_id)
        gameResult.delete()
        return redirect('game_result', competition_id=competition_id, match_id=match_id)

class GameResultCreateView(View):
    def get(self, request, competition_id, match_id):
        GameResult_form = GameResultForm()
        Team_form = TeamForm()
        match = get_object_or_404(Match, pk=match_id)
        competition = get_object_or_404(Competition, pk=competition_id)
        return render(request, 'records/game_result_form.html', {'gameResult_form': GameResult_form, 'team_form': Team_form, 'match': match, 'competition': competition})

    def post(self, request, competition_id, match_id):
        print("match_id: ", match_id)
        match = get_object_or_404(Match, pk=match_id)
        form = GameResultForm(request.POST)
        if form.is_valid():
            gameResult = form.save(commit=False)
            gameResult.match = match
            gameResult.save()
            TeamGameResultMapping.objects.create(team=Team.objects.get(team_id=form.cleaned_data['team_id'].team_id), gameResult=gameResult)

            player_scores = request.POST.dict()
            for key, score in player_scores.items():
                if key.startswith('player_scores[') and key.endswith(']'):
                    student_id = key[len('player_scores['):-1]
                    student = Student.objects.get(student_id=student_id)
                    PlayerScore.objects.create(student=student, gameResult=gameResult, score=score)
            return redirect('game_result', competition_id=competition_id, match_id=match_id)

        return render(request, 'records/game_result_form.html', {'form': form, 'match': match})

class StudentListView(View):
    def get(self, request):
        query = request.GET.get('q')
        if query:
            students = Student.objects.filter(
                Q(name__icontains=query) | Q(student_num__icontains=query)
            )
        else :
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

class StudentDeleteView(View):
    def post(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        student.delete()
        return redirect('student_list')

class StudentDetailView(View):
    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        games = PlayerScore.objects.filter(student=student)

        return render(request, 'records/student_detail.html', {'student': student, 'games': games, })

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
        if form.is_valid():
            team = form.save()
            for student in form.cleaned_data['students']:
                TeamStudentMapping.objects.create(team=team, student=student)
            return JsonResponse({'success': True, 'team_id': team.team_id, 'team_name': team.team_name})
        return JsonResponse({'success': False})

class AdminPageView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'records/admin_page.html')


class TeamsPlayersView(View):
    def get(self, request, team_id):
        team = get_object_or_404(Team, pk=team_id)
        team_student_mapping = TeamStudentMapping.objects.filter(team=team).values('student__student_id', 'student__name')
        return JsonResponse({'team_student_mapping': list(team_student_mapping)})
