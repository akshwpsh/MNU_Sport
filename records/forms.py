from django import forms
from .models import *

class RallyForm(forms.ModelForm):
    class Meta:
        model = Rally
        fields = ['name', 'start_date', 'end_date']

class MatchForm(forms.ModelForm):
    sport_id = forms.ModelChoiceField(
        queryset=Sport.objects.all(),
        label="Sport",
        to_field_name="name",
        empty_label="Select a sport",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Match
        fields = ['match_name', 'match_date', 'location', 'sport_id']

    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['sport_id'].label_from_instance = lambda obj: obj.name

class SportForm(forms.ModelForm):
    class Meta:
        model = Sport
        fields = ['name']

class GameResultForm(forms.ModelForm):
    team_id = forms.ModelChoiceField(
        queryset=Team.objects.all(),
        label="Team",
        to_field_name="team_name",
        empty_label="Select a team",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = GameResult
        fields = ['score', 'rank', 'result', 'team_id']

    def __init__(self, *args, **kwargs):
        super(GameResultForm, self).__init__(*args, **kwargs)
        self.fields['team_id'].label_from_instance = lambda obj: obj.team_name

class StudentForm(forms.ModelForm):
    major_id = forms.ModelChoiceField(
        queryset=Major.objects.all(),
        label="Major",
        to_field_name="name",
        empty_label="Select a major",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Student
        fields = ['name', 'student_num', 'major_id']

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['major_id'].label_from_instance = lambda obj: obj.name

class MajorForm(forms.ModelForm):
    class Meta:
        model = Major
        fields = ['name']

class TeamForm(forms.ModelForm):
    rally_id = forms.ModelChoiceField(
        queryset=Rally.objects.all(),
        label="Rally",
        to_field_name="name",
        empty_label="Select a rally",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sport_id = forms.ModelChoiceField(
        queryset=Sport.objects.all(),
        label="Sport",
        to_field_name="name",
        empty_label="Select a sport",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        label="Students",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Team
        fields = ['team_name', 'rally_id', 'sport_id', 'students']

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields['rally_id'].label_from_instance = lambda obj: obj.name
        self.fields['sport_id'].label_from_instance = lambda obj: obj.name
        self.fields['students'].label_from_instance = lambda obj: obj.name

class TeamStudentMappingForm(forms.ModelForm):
    class Meta:
        model = TeamStudentMapping
        fields = ['team_id', 'student_id']

