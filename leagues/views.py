from django.shortcuts import render, redirect
from django.db.models import Q, Count	# Q allows creation of complex queries with OR, AND statements; see lines 27-29
from .models import League, Team, Player

from . import team_maker

def index(request):
	context = {
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
		"baseball_leagues": League.objects.filter(sport__iexact='baseball'),
		"womens_leagues": League.objects.filter(name__contains='women'),
		"hockey_leagues": League.objects.filter(sport__contains='hockey'),
		"non_football_leagues": League.objects.exclude(sport='Football'),
		"conference_leagues": League.objects.filter(name__contains='conference'),
		"atlantic_leagues": League.objects.filter(name__contains='atlantic'),
		"dallas_teams": Team.objects.filter(location='Dallas'),
		"raptors_teams": Team.objects.filter(team_name='Raptors'),
		"city_teams": Team.objects.filter(location__contains='city'),
		"t_teams": Team.objects.filter(team_name__startswith='t'),
		"alpha_teams": Team.objects.all().order_by('location'),
		"rev_alpha_teams": Team.objects.all().order_by('team_name').reverse(),
		"cooper_players": Player.objects.filter(last_name='Cooper'),
		"josh_players": Player.objects.filter(first_name='Joshua'),
		"not_josh_cooper_players": Player.objects.filter(last_name='Cooper').exclude(first_name='Joshua'),
		"alex_players_or_wyatt": Player.objects.filter(
			Q(first_name='Joshua') | Q(first_name='Wyatt')
			).order_by('last_name'),
		"teams_atlantic": Team.objects.filter(league__name='Atlantic Soccer Conference'),	# When filtering on Foreign Key, need "__[field name]" from that object
		"boston_players": Player.objects.filter(
			Q(curr_team__team_name='Penguins') & Q(curr_team__location='Boston')
			),
		"ICBC_players": Player.objects.filter(curr_team__league__name='International Collegiate Baseball Conference'),
		"lopez_players": Player.objects.filter(
			Q(curr_team__league__name='American Conference of Amateur Football') & Q(last_name='Lopez')
			),
		"football_players": Player.objects.filter(curr_team__league__sport__contains='football'), # Double-hop Player >> Team >> League
		"teams_sophia": Team.objects.filter(curr_players__first_name='Sophia'),
		"all_teams": Team.objects.all,
		"leagues_sophia": League.objects.filter(teams__curr_players__first_name='Sophia'),
		"players_flores": Player.objects.filter(last_name="Flores").exclude(curr_team__team_name="Roughriders"), 
		"teams_samuel": Team.objects.filter(all_players__id=115),
		"manitoba_players": Player.objects.filter(all_teams__id=37), 
		"vikings_players": Player.objects.filter(all_teams__id=40).exclude(curr_team__id=40), 
		"teams_jacob": Team.objects.filter(all_players__id=151).exclude(curr_players__id=151),
		"players_joshua": Player.objects.filter(
			Q(first_name='Joshua') & Q(all_teams__league__name='Atlantic Federation of Amateur Baseball Players')
		),
		"teams_12": Team.objects.annotate(num_players=Count('all_players')),# Count was imported up-top! Annotate allows the definition of a temp attribute. 
																			# https://docs.djangoproject.com/en/2.2/ref/models/querysets/#annotate
		"players_count": Player.objects.annotate(num_teams=Count('all_teams')).order_by('num_teams').reverse(),
	}

	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")