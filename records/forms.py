from django import forms
from .models import *

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'start_date', 'end_date']

class MatchForm(forms.ModelForm):
    sport = forms.ModelChoiceField(
        queryset=Sport.objects.all(),
        label="Sport",
        to_field_name="name",
        empty_label="Select a sport",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Match
        fields = ['match_name', 'match_date', 'location', 'sport']

    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['sport'].label_from_instance = lambda obj: obj.name

class SportForm(forms.ModelForm):
    class Meta:
        model = Sport
        fields = ['name']


class GameResultForm(forms.ModelForm):
    team_id = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        label="Team",
        to_field_name="team_id",  # Use team_id as the value
        empty_label="Select a team",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = GameResult
        fields = ['score', 'rank', 'result']

    def __init__(self, *args, **kwargs):
        super(GameResultForm, self).__init__(*args, **kwargs)
        self.fields['team_id'].label_from_instance = lambda obj: obj.team_name  # Display team name

    def save(self, commit=True):
        game_result = super(GameResultForm, self).save(commit=False)
        team = self.cleaned_data.get('team_id')
        if commit:
            game_result.save()
            # Handle the team_id separately if needed
            TeamGameResultMapping.objects.create(team=team, gameResult=game_result)
        return game_result


class StudentForm(forms.ModelForm):
    major = forms.ModelChoiceField(
        queryset=Major.objects.all(),
        label="Major",
        to_field_name="name",
        empty_label="Select a major",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Student
        fields = ['name', 'student_num', 'major']

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['major'].label_from_instance = lambda obj: obj.name

class MajorForm(forms.ModelForm):
    class Meta:
        model = Major
        fields = ['name']

class TeamForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        label="Students",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Team
        fields = ['team_name','students']

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields['students'].label_from_instance = lambda obj: obj.name

class TeamStudentMappingForm(forms.ModelForm):
    class Meta:
        model = TeamStudentMapping
        fields = ['team', 'student']

