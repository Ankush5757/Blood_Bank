# signals.py
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Donate_Us  # Replace with the correct model name for donation
from django.contrib.auth.models import User  # Assuming the user model is being used for login

# Signal handler to send the email
@receiver(post_save, sender=Donate_Us)
def send_donation_email(sender, instance, created, **kwargs):
    # Check if this is a new donation
    if created:
        # Assuming you have a 'user' field that links to the user who made the donation

        # Send email to the donor (session user)
        subject = 'Donation Successful - Thank You for Your Contribution'
        message = f"""
        Dear {instance.user.first_name},

        Thank you for your generous donation to our blood bank! Your contribution helps save lives and makes a significant impact on those in need.

        Payment Details:
        - Payment ID: {instance.payment_id}
        - Donation Amount: {instance.amount} 

        We appreciate your support. Should you need any further assistance or have questions, please feel free to reach out to us.

        Additionally, if you wish to visit our hospital or donation center to meet with our staff or learn more about how your donation is helping others, feel free to visit the following location:
        Fc, Road Pune
        Thank you once again for being part of this vital cause. Your generosity is truly appreciated.

        Best regards,
        The Blood Bank Management Team
        """

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.user.email]  # Sending email to the donor's email

        send_mail(subject, message, from_email, recipient_list)

        # Optional: Send email to admin or another recipient (if needed)
        # admin_email = 'admin@example.com'  # Replace with actual admin email
        # send_mail(
        #     'New Donation Received',
        #     f"A new donation has been made. Payment ID: {instance.payment_id}",
        #     from_email,
        #     [admin_email]
        # )
