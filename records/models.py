from django.db import models



class Major(models.Model):
    major_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'Major'

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    student_num = models.BigIntegerField(blank=True, null=True)
    major_id = models.ForeignKey(Major, on_delete=models.CASCADE)

    class Meta:
        db_table = 'student'

class Rally(models.Model):
    rally_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'Rally'


class Sport(models.Model):
    sport_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Sport'

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=50, blank=True, null=True)
    rally_id = models.ForeignKey(Rally, on_delete=models.CASCADE)
    sport_id = models.ForeignKey(Sport, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Team'

class TeamStudentMapping(models.Model):
    team_student_mapping_id = models.AutoField(primary_key=True)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Team-Student_Mapping'


class Match(models.Model):
    match_id = models.AutoField(primary_key=True)
    match_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    match_name = models.CharField(max_length=50, blank=True, null=True)
    rally_id = models.ForeignKey(Rally, on_delete=models.CASCADE)
    sport_id = models.ForeignKey(Sport, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Match'


class GameResult(models.Model):
    game_result_id = models.AutoField(primary_key=True)
    score = models.BigIntegerField(blank=True, null=True)
    rank = models.BigIntegerField(blank=True, null=True)
    result = models.CharField(max_length=50, blank=True, null=True)
    match_id = models.ForeignKey(Match, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = 'GameResult'

class PlayerScore(models.Model):
    player_score_id = models.AutoField(primary_key=True)
    score = models.BigIntegerField(blank=True, null=True)
    student_id = models.BigIntegerField()
    gameResult_id = models.ForeignKey(GameResult, on_delete=models.CASCADE)

    class Meta:
        db_table = 'PlayerScore'