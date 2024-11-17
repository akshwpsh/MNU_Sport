from django import forms
from .models import *

class CompetitionForm(forms.ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'}),
        }

class MatchForm(forms.ModelForm):
    sport = forms.ModelChoiceField(
        queryset=Sport.objects.all(),
        label="Sport",
        to_field_name="name",
        empty_label="Select a sport",
        widget=forms.Select(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'})
    )

    class Meta:
        model = Match
        fields = ['match_name', 'match_date', 'location', 'sport']
        widgets = {
            'match_name': forms.TextInput(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'}),
            'match_date': forms.DateInput(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'}),
            'location': forms.TextInput(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['sport'].label_from_instance = lambda obj: obj.name

class SportForm(forms.ModelForm):
    class Meta:
        model = Sport
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'}),
        }

class GameResultForm(forms.ModelForm):
    team_id = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        label="Team",
        to_field_name="team_id",
        empty_label="Select a team",
        widget=forms.Select(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'})
    )

    class Meta:
        model = GameResult
        fields = ['score', 'rank', 'result']
        widgets = {
            'score': forms.NumberInput(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'}),
            'rank': forms.NumberInput(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'}),
            'result': forms.TextInput(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super(GameResultForm, self).__init__(*args, **kwargs)
        self.fields['team_id'].label_from_instance = lambda obj: obj.team_name

    def save(self, commit=True):
        game_result = super(GameResultForm, self).save(commit=False)
        team = self.cleaned_data.get('team_id')
        if commit:
            game_result.save()
            TeamGameResultMapping.objects.create(team=team, gameResult=game_result)
        return game_result

class StudentForm(forms.ModelForm):
    major = forms.ModelChoiceField(
        queryset=Major.objects.all(),
        label="Major",
        to_field_name="name",
        empty_label="Select a major",
        widget=forms.Select(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'})
    )

    class Meta:
        model = Student
        fields = ['name', 'student_num', 'major']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'}),
            'student_num': forms.TextInput(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['major'].label_from_instance = lambda obj: obj.name

class MajorForm(forms.ModelForm):
    class Meta:
        model = Major
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'}),
        }

class TeamForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        label="Students",
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'})
    )

    class Meta:
        model = Team
        fields = ['team_name', 'students']
        widgets = {
            'team_name': forms.TextInput(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'}),
        }

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields['students'].label_from_instance = lambda obj: obj.name

class TeamStudentMappingForm(forms.ModelForm):
    class Meta:
        model = TeamStudentMapping
        fields = ['team', 'student']
        widgets = {
            'team': forms.Select(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'}),
            'student': forms.Select(attrs={'class': 'form-control p-2 border border-gray-300 rounded mb-4 w-full'}),
        }