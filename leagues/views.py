from django.shortcuts import render, redirect
from django.db.models import Q					# Q allows creation of complex queries with OR, AND statements; see lines 27-29
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
	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")