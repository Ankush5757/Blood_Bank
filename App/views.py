from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from .models import Register, Profile_pictures, Request,Blood_Donor, Donate_Us
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        age = request.POST['age']
        blood_group = request.POST['blood_group']
        gender = request.POST['gender']
        city = request.POST['city']
        state = request.POST['state']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Age validation
        if not age.isdigit() or int(age) <= 18:
            messages.error(request, "You must be at least 18 years old to donate blood.")
            return redirect('/register/')

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email format. Please enter a valid email.")
            return redirect('/register/')

        # Password Validation
        if password == confirm_password:
            # Check if email already exists
            if Register.objects.filter(email=email).exists():
                messages.info(request, "Email Already Exists, Please try with new email")
                return redirect('/register/')
            # Check if mobile number already exists
            elif Register.objects.filter(mobile=mobile).exists():
                messages.info(request, "Mobile Number Already Exists, Please try with new number")
                return redirect('/register/')
            else:
                # Hash the password and create a new donor record
                password = make_password(password)
                new_donor = Register(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    mobile=mobile,
                    age=age,
                    blood_group=blood_group,
                    gender=gender,
                    city=city,
                    state=state,
                    password=password
                )
                new_donor.save()
                messages.info(request, 'Account created successfully.')
                return redirect('/login/')
        else:
            messages.info(request, "Passwords didn't match.")
            return redirect('/register/')
    return render(request, 'register.html')

def login(request):
    if request.method=="POST":
        mobile = request.POST['mobile']
        password = request.POST['password']
        
        try:
            user = Register.objects.get(mobile=mobile)
            if user.mobile == mobile and check_password(password,user.password):
                request.session['id'] = user.id
                return redirect('/dashboard/')
            else:
                messages.info(request,'Invalid Credentials')
                return redirect('/login')
            
        except Register.DoesNotExist:
            messages.info(request,'Mobile number does not exists')
            return redirect('/login/')
        
    return render(request, 'login.html', {'login':login})


def logout(request):
    request.session.flush()
    return redirect('/login/')

def profile_pic(request, id):
    if request.method == "POST":
        profile_picture = request.FILES.get('profile_pic')
        user_id = request.session.get('id')

        try:
            # Fetch the user instance
            user = Register.objects.get(id=user_id)
            
            # Create or update the profile picture
            profile_pic_obj, created = Profile_pictures.objects.update_or_create(
                user=user,
                defaults={'profile_pic': profile_picture}
            )
            profile_pic_obj.save()
            messages.success(request, "Profile picture updated successfully!")
        except Register.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect('/profile/')
        
    return redirect('/profile/')


def delete_profile_pic(request, id):
    try:
        profile_picture = Profile_pictures.objects.get(id=id)
        profile_picture.delete()
        messages.success(request, "Profile picture deleted successfully!")
    except Profile_pictures.DoesNotExist:
        messages.error(request, "Profile picture does not exist.")
    return redirect('/profile/')


def home(request):
    return render(request, 'home.html')

def profile(request) :
    user_id = request.session.get('id')
    profiles = Register.objects.get(id = user_id)

    try :
        profile_pic = Profile_pictures.objects.get(user = profiles)
        return render(request, 'profile.html', {'profiles' : profiles, 'profile_pic' : profile_pic})
    
    except Profile_pictures.DoesNotExist :
        return render(request, 'profile.html', {'profiles' : profiles})

def aboutus(request):
    return render(request, 'aboutus.html')
    

def dashboard(request):
    donors = Blood_Donor.objects.all()
    return render(request, 'dashboard.html', {'donors': donors})


def requests(request):
    if request.method == "POST":
        # Extract form data
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        city = request.POST.get('city')
        state = request.POST.get('state')
        blood_group = request.POST.get('blood_group')
        urgency = request.POST.get('urgency')
        donor_id = request.POST.get('donor_id')  # Donor ID passed via form

        # Validate required fields
        if not name or not mobile or not email or not city or not state or not blood_group or not urgency:
            messages.error(request, "All fields are required.")
            return redirect('/requests/')

        # Check if the mobile or email already exists
        if Request.objects.filter(mobile=mobile).exists():
            messages.error(request, "Mobile number already exists.")
            return redirect('/requests/')
        elif Request.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('/requests/')
        else:
            # Create a new Request object
            new_request = Request.objects.create(
                name=name,
                mobile=mobile,
                email=email,
                city=city,
                state=state,
                blood_group=blood_group,
                urgency=urgency
            )

            # Handle donor email notification if donor_id is provided
            if donor_id:
                donor = Register.objects.filter(id=donor_id).first()  # Get the donor details
                if donor:
                    subject = 'Blood Donation Request'
                    from_email = 'jadhavankush440@gmail.com'
                    message_user = f"You have requested blood from donor: {donor.first_name} {donor.last_name}. Blood Group: {donor.blood_group}. Please wait for their response."
                    message_donor = f"You have received a blood donation request from {name}. Blood Group: {new_request.blood_group}."

                    # Send email to the requesting user
                    to_email_user = email  # Use the email entered in the form
                    email_message_user = EmailMultiAlternatives(subject, message_user, from_email, [to_email_user])
                    email_message_user.content_subtype = 'html'
                    email_message_user.send()

                    # Send email to the donor
                    to_email_donor = donor.email  # Assuming donor email is directly in the Register model
                    email_message_donor = EmailMultiAlternatives(subject, message_donor, from_email, [to_email_donor])
                    email_message_donor.content_subtype = 'html'
                    email_message_donor.send()

                    messages.success(request, "Request sent successfully and emails are sent to the donor.")
                else:
                    messages.error(request, "Donor not found.")
            return redirect('/requests/')

    # If GET request, render the donor profiles and request form
    donor_profiles = Register.objects.all()  # Get all donors
    return render(request, 'requests.html', {'donor_profiles': donor_profiles})

def blood_request(request):
    user = Request.objects.all()
    return render(request, 'blood_request.html', {'user': user})

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.contrib import messages
from .models import Request  # Make sure this import is correct

def approve(request, id):
    try:
        # Retrieve the donor's request using the provided ID
        user_request = Request.objects.get(id=id)
    except Request.DoesNotExist:
        # If the request is not found, show an error message and redirect
        messages.error(request, 'The requested blood donation request does not exist or has already been processed.')
        return render(request, 'blood_request.html')  # Or redirect to a specific URL

    # Get all donor requests for display
    all_donors = Request.objects.all()

    # Email subject and sender details
    subject = 'Blood Donation Request Approved'
    from_email = 'jadhavankush440@gmail.com'  # Or use `settings.DEFAULT_FROM_EMAIL`

    # Construct the email message
    message = f"""
    <html>
        <body>
            <p>Dear {user_request.name},</p>  <!-- Accessing the requester's name -->
            <p>We are happy to inform you that your request for blood donation has been approved!</p>
            <p>You can now visit the hospital to complete the donation process.</p>
            <p>Please visit the hospital at your earliest convenience. Thank you for your patience, and we appreciate your cooperation!</p>
            <p>Kind regards,</p>
            <p>The Blood Bank Team</p>
        </body>
    </html>
    """
    
    # Email recipient (requester's email)
    to_email = user_request.email  # Accessing the requester's email address

    # Send the email
    email = EmailMultiAlternatives(subject, message, from_email, [to_email])
    email.content_subtype = 'html'  # Set email content type to HTML
    email.send()

    # Log the email send action (optional, for debugging)
    print("Email sent to:", to_email)

    # Delete the request after it has been approved
    user_request.delete()

    # Display the updated list of all donor requests
    return render(request, 'blood_request.html', {'user': all_donors})


def blood_donor(request):
    if request.method == "POST":
        donor_name = request.POST.get('donor_name')
        mobile = request.POST.get('mobile')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        blood_group = request.POST.get('blood_group')
        email = request.POST.get('email')
        city = request.POST.get('city')
        state = request.POST.get('state')
        image = request.FILES.get('image')

        if Blood_Donor.objects.filter(mobile=mobile).exists():
            messages.error(request, "Mobile number already exists.")
            return redirect('/blood_donor/')
        elif Blood_Donor.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('/blood_donor/')
        else:
            # Create a new Blood_Donor object
            Blood_Donor.objects.create(
                donor_name=donor_name,
                mobile=mobile,
                email=email,
                city=city,
                state=state,
                blood_group=blood_group,
                age=age, gender=gender, image=image
            )
            messages.success(request, "Blood donor added successfully!")
            return redirect('/dashboard/')

    return render(request, 'blood_donor.html')


def donate_us(request):
    return render(request, 'donate_us.html',)

def donation_success(request, payment_id,payment):
    user_id = request.session.get('id')
    if not user_id :
        redirect('/login/')

    try:
        user = Register.objects.get(id=user_id)

    except Register.DoesNotExist:
        redirect('/register/')

    if payment:
        final_donor =Donate_Us.objects.create(user = user, amount = payment, payment_id = payment_id)
        final_donor.save()
        
    return render(request, 'donation_success.html', {'payment_id': payment_id})

def filter_donors(request):
    blood_group = request.POST.get('blood_group')
    city = request.POST.get('city')
    state = request.POST.get('state')

    donors = Blood_Donor.objects.all()

    if state:
        donors = donors.filter(state__icontains=state)

    if blood_group:
        donors = donors.filter(blood_group=blood_group)

    if city:
        donors = donors.filter(city__icontains=city)

    return render(request, 'dashboard.html', {'donors': donors})


def update_profile(request, id):
    # Fetch the user profile by ID
    profile = Register.objects.get(id=id)

    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        city = request.POST.get('city')
        state = request.POST.get('state')

        if not mobile or not email or not city or not state:
            messages.error(request, 'All fields are required!')
        else:
            profile.mobile = mobile
            profile.email = email
            profile.city = city
            profile.state = state
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    return render(request, 'profile_update.html', {'profile': profile})
