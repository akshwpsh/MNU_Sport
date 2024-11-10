from django import forms
from .models import Rally , Match, Sport

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