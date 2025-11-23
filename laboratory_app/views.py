from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def lab_journal(request):
  return render(request, 'laboratory/lab_journal.html')

@login_required
def lab_norms(request):
  return render(request, 'laboratory/lab_norms.html')

@login_required
def add_result(request):
  return render(request, 'laboratory/add_result.html')