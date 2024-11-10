from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from records.models import Rally, Match, Sport, GameResult
from .forms import RallyForm, MatchForm, SportForm

class RallyListView(View):
    def get(self, request):
        rallies = Rally.objects.all()
        return render(request, 'records/rally_list.html', {'rallies': rallies})


class RallyCreateView(View):
    def get(self, request):
        form = RallyForm()
        return render(request, 'records/rally_form.html', {'form': form})

    def post(self, request):
        form = RallyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rally_list')
        return render(request, 'records/rally_form.html', {'form': form})

class MatchListView(View):
    def get(self, request, rally_id):
        rally = get_object_or_404(Rally, pk=rally_id)
        matches = Match.objects.filter(rally_id=rally)
        return render(request, 'records/match_list.html', {'matches': matches, 'rally': rally})

# records/views.py
class MatchCreateView(View):
    def get(self, request, rally_id):
        form = MatchForm()
        rally = get_object_or_404(Rally, pk=rally_id)
        return render(request, 'records/match_form.html', {'form': form, 'rally': rally})

    def post(self, request, rally_id):
        rally = get_object_or_404(Rally, pk=rally_id)
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save(commit=False)
            match.rally_id = rally
            match.save()
            return redirect('match_list', rally_id=rally_id)
        return render(request, 'records/match_form.html', {'form': form, 'rally': rally})

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
    def get(self, request, rally_id, match_id):
        match = get_object_or_404(Match, pk=match_id)
        gameResults = GameResult.objects.filter(match_id=match)
        return render(request, 'records/game_result.html', {'gameResults': gameResults})