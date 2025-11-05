from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def all_cards(request):
  return render(request, 'cards/all_cards.html')

@login_required
def index(request):
  return render(request, 'cards/index_card.html')

@login_required
def vaccine(request):
  return render(request, 'cards/vaccine.html')

@login_required
def med_referral(request):
  return render(request, 'cards/med_referral.html')

@login_required
def result_analysis(request):
  return render(request, 'cards/result_analysis.html')

@login_required
def card_profile(request):
  return render(request, 'cards/card_profile.html')

@login_required
def referral_profile(request):
  return render(request, 'cards/referral_profile.html')

@login_required
def vaccine_profile(request):
  return render(request, 'cards/vaccine_profile.html')

@login_required
def result_analysis_profile(request):
  return render(request, 'cards/result_analysis_profile.html')