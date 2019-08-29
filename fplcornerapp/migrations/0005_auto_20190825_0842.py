# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2019-08-25 08:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fplcornerapp', '0004_season_is_current'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('finished', models.BooleanField(default=False)),
                ('is_current', models.BooleanField(default=False)),
                ('event_id', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fixture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fixture_id', models.IntegerField(blank=True, null=True)),
                ('code', models.IntegerField(blank=True, null=True)),
                ('kickoff_time', models.DateTimeField()),
                ('started', models.BooleanField(default=False)),
                ('finished', models.BooleanField(default=False)),
                ('team_h_difficulty', models.IntegerField(blank=True, null=True)),
                ('team_a_difficulty', models.IntegerField(blank=True, null=True)),
                ('team_a_score', models.IntegerField(blank=True, null=True)),
                ('team_h_score', models.IntegerField(blank=True, null=True)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fplcornerapp.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Fixture_Stat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stat_name', models.CharField(max_length=100)),
                ('value', models.IntegerField(blank=True, null=True)),
                ('fixture', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fplcornerapp.Fixture')),
            ],
            options={
                'ordering': ['fixture'],
                'verbose_name': 'Fixture_Stat',
                'verbose_name_plural': 'Fixture_Stats',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.IntegerField(blank=True, null=True)),
                ('code', models.IntegerField(blank=True, null=True)),
                ('first_name', models.CharField(max_length=100)),
                ('second_name', models.CharField(max_length=100)),
                ('web_name', models.CharField(max_length=100)),
                ('news', models.TextField(blank=True, null=True)),
                ('chance_of_playing_this_round', models.FloatField(blank=True, null=True)),
                ('chance_of_playing_next_round', models.FloatField(blank=True, null=True)),
                ('now_cost', models.FloatField(blank=True, null=True)),
                ('total_points', models.IntegerField(blank=True, null=True)),
                ('points_per_game', models.FloatField(blank=True, null=True)),
                ('bonus', models.IntegerField(blank=True, null=True)),
                ('bps', models.FloatField(blank=True, null=True)),
                ('minutes', models.FloatField(blank=True, null=True)),
                ('dreamteam_count', models.IntegerField(blank=True, null=True)),
                ('goals_scored', models.IntegerField(blank=True, null=True)),
                ('assists', models.IntegerField(blank=True, null=True)),
                ('goals_conceded', models.IntegerField(blank=True, null=True)),
                ('clean_sheets', models.IntegerField(blank=True, null=True)),
                ('saves', models.IntegerField(blank=True, null=True)),
                ('penalties_saved', models.IntegerField(blank=True, null=True)),
                ('penalties_missed', models.IntegerField(blank=True, null=True)),
                ('yellow_cards', models.IntegerField(blank=True, null=True)),
                ('red_cards', models.IntegerField(blank=True, null=True)),
                ('own_goals', models.IntegerField(blank=True, null=True)),
                ('form', models.FloatField(blank=True, null=True)),
                ('value_form', models.FloatField(blank=True, null=True)),
                ('value_season', models.FloatField(blank=True, null=True)),
                ('ep_this', models.FloatField(blank=True, null=True)),
                ('ep_next', models.FloatField(blank=True, null=True)),
                ('influence', models.FloatField(blank=True, null=True)),
                ('creativity', models.FloatField(blank=True, null=True)),
                ('threat', models.FloatField(blank=True, null=True)),
                ('ict_index', models.FloatField(blank=True, null=True)),
                ('selected_by_percent', models.FloatField(blank=True, null=True)),
                ('transfers_in', models.IntegerField(blank=True, null=True)),
                ('transfers_out', models.IntegerField(blank=True, null=True)),
                ('transfers_in_event', models.IntegerField(blank=True, null=True)),
                ('transfers_out_event', models.IntegerField(blank=True, null=True)),
                ('cost_change_start', models.FloatField(blank=True, null=True)),
                ('cost_change_event_fall', models.FloatField(blank=True, null=True)),
                ('cost_change_start_fall', models.FloatField(blank=True, null=True)),
                ('cost_change_event', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_type_id', models.IntegerField(blank=True, null=True)),
                ('singular_name', models.CharField(max_length=30)),
                ('plural_name', models.CharField(max_length=30)),
                ('squad_min_play', models.IntegerField(blank=True, null=True)),
                ('squad_max_play', models.IntegerField(blank=True, null=True)),
                ('squad_select', models.IntegerField(blank=True, null=True)),
                ('plural_name_short', models.CharField(max_length=30)),
                ('singular_name_short', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('short_name', models.CharField(max_length=20)),
                ('code', models.IntegerField(blank=True, null=True)),
                ('played', models.IntegerField(blank=True, null=True)),
                ('win', models.IntegerField(blank=True, null=True)),
                ('loss', models.IntegerField(blank=True, null=True)),
                ('draw', models.IntegerField(blank=True, null=True)),
                ('points', models.IntegerField(blank=True, null=True)),
                ('position', models.IntegerField(blank=True, null=True)),
                ('form', models.FloatField(blank=True, null=True)),
                ('strength', models.IntegerField(blank=True, null=True)),
                ('strength_overall_home', models.FloatField(blank=True, null=True)),
                ('strength_overall_away', models.FloatField(blank=True, null=True)),
                ('strength_defence_home', models.FloatField(blank=True, null=True)),
                ('strength_defence_away', models.FloatField(blank=True, null=True)),
                ('strength_attack_home', models.FloatField(blank=True, null=True)),
                ('strength_attack_away', models.FloatField(blank=True, null=True)),
                ('unavailable', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='element_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fplcornerapp.Player_Type'),
        ),
        migrations.AddField(
            model_name='player',
            name='team_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fplcornerapp.Team'),
        ),
        migrations.AddField(
            model_name='fixture_stat',
            name='player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='fplcornerapp.Player'),
        ),
        migrations.AddField(
            model_name='fixture',
            name='team_a',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awayteam', to='fplcornerapp.Team'),
        ),
        migrations.AddField(
            model_name='fixture',
            name='team_h',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hometeam', to='fplcornerapp.Team'),
        ),
    ]
