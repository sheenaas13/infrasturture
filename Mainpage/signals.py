from django.db.models.signals import post_save
from django.dispatch import receiver
from Mainpage.models import AlertMade, AlertRegistration
from django.core.mail import send_mail

@receiver(post_save, sender=AlertMade)
def send_alert_to_users(sender, instance, created, **kwargs):
    print("💥 test_signal triggered on save")
    try:
        location = instance.location.lower()

        users = AlertRegistration.objects.filter(
            location__iexact=location
        )

        print("📌 Matched Users:", users.count())

        for user in users:
            subject = f"🚨 New Alert: {instance.alert_type}"
            message = f"""
Dear {user.name},

We hope you're safe and well.

🚨 A new alert has just been issued for your area: **{instance.location}**.

━━━━━━━━━━━━━━━━━━━━━━━  
🔔 **Alert Type:** {instance.alert_type}  
📝 **Details:**  
{instance.message}  
━━━━━━━━━━━━━━━━━━━━━━━  

We encourage you to take any necessary precautions and stay informed.

Warm regards,  
**The Infrabuild Team**  
Building a Safer Tomorrow 🏗️  
_Keep looking forward — we're always here for you._
"""
            send_mail(
                subject,
                message,
                'sheeintern@gmail.com',
                [user.email],
                fail_silently=False
            )

    except Exception as e:
        print("Mail sending Failed:", e)
