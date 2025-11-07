from django.dispatch import receiver
from cards_app.models import MedCards
from users_app.models import FamilyDoctor, Patient
from django.db.models.signals import post_save

@receiver(post_save, sender=Patient)
def create_medcard_for_patient(sender, instance, created, **kwargs):
    """Створює медичну картку, як тільки створюється об'єкт пацієнта."""
    if created:
        MedCards.objects.create(patient=instance)


@receiver(post_save, sender=FamilyDoctor)
def sync_doctor_to_medcards(sender, instance, created, **kwargs):
    """Оновлює поле 'doctor' в MedCards при зміні FamilyDoctor."""
    
    patient = instance.patient
    new_doctor = instance.doctor
    
    # 1. Знаходимо картку (вона вже гарантовано існує завдяки першому сигналу)
    try:
        medcard = MedCards.objects.get(patient=patient)
        
        # 2. Оновлюємо поле 'doctor'
        if medcard.doctor != new_doctor:
            medcard.doctor = new_doctor
            # Використовуємо update_fields, щоб уникнути нескінченного циклу
            medcard.save(update_fields=['doctor'])
            
    except MedCards.DoesNotExist:
        # Це не повинно траплятися, якщо перший сигнал спрацював.
        pass