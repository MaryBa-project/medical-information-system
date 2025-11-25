from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from laboratory_app.models import MedReferral, ResultAnalysis, ResultParameter, TemplateParameter

@login_required
def lab_journal(request):
  return render(request, 'laboratory/lab_journal.html')

@login_required
def lab_norms(request):
  return render(request, 'laboratory/lab_norms.html')

@login_required
def add_result(request, referral_id):
    # Беремо направлення
    referral = get_object_or_404(MedReferral, id=referral_id)
    
    # Медкарта та тип аналізу
    card = referral.medcard
    ref_type = referral.type_analys

    # Параметри для цього типу аналізу
    parameters = TemplateParameter.objects.filter(type_analys=ref_type)

    if request.method == "POST":
        # Створюємо результат аналізу
        result_analysis = ResultAnalysis.objects.create(
            medcard=card,
            referral=referral,
            lab_assistent=request.user.laboratoryassistent,  # якщо користувач — лаборант
            report=request.POST.get("report", "")
        )

        # Створюємо результати параметрів
        for param in parameters:
            value = request.POST.get(f"value_{param.id}")
            unit = request.POST.get(f"unit_{param.id}") or param.unit_of_measurement
            comment = request.POST.get(f"comment_{param.id}", "")

            if value:  # перевіряємо, що щось введено
                ResultParameter.objects.create(
                    value=value,
                    unit_of_measurement=unit,
                    coment=comment,
                    template=param,
                    result_analys=result_analysis
                )
        referral.save()
        return redirect('card:journal_referral') 

    context = {
        'referral': referral,
        'card': card,
        'ref_type': ref_type,
        'parameters': parameters,
    }
    return render(request, 'laboratory/add_result.html', context)