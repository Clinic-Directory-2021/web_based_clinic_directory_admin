from django.shortcuts import render, redirect

from django.http import HttpResponse


from firebase_admin import credentials
from firebase_admin import firestore
import pyrebase
import firebase_admin

import datetime

from django.core.mail import send_mail

config={
    "apiKey": "AIzaSyDwWsW--ZHaZIOE4OXu5VhMIclZad8zDYw",
    "authDomain": "animal-clinic-directory-2021.firebaseapp.com",
    "databaseURL": "https://animal-clinic-directory-2021-default-rtdb.firebaseio.com/",
    "projectId": "animal-clinic-directory-2021",
    "storageBucket": "animal-clinic-directory-2021.appspot.com",
    "messagingSenderId": "165228810397",
    "appId": "1:165228810397:web:8378bcc8cb06dd52520474",
    "measurementId": "G-D4BEP96KMK"
}

firebase = pyrebase.initialize_app(config)
cred = credentials.Certificate("main_app\serviceAccountKey.json")
firebase_admin.initialize_app(cred)

auth = firebase.auth()
db = firebase.database()
firestoreDB = firestore.client()

storage = firebase.storage()



# Create your views here.
def login(request):
    if 'clinic_id' not in request.session:
        return render(request,'login.html')
    else:
        return redirect('/homepage')

def homepage(request):
    if 'clinic_id' in request.session:
        all_news = firestoreDB.collection('news').get()

        news = []

        for news_report in all_news:
            value = news_report.to_dict()
            news.append(value)

        data ={
            'news': news,
        }
        return render(request,'homepage.html', data)
    else:
        return redirect('login')
    #return render(request,'homepage.html')

def request(request):
    if 'clinic_id' in request.session:
        clinic_requests = firestoreDB.collection('queue').get()

        queue = []

        for clinic_request in clinic_requests:
            value = clinic_request.to_dict()
            queue.append(value)

        data ={
            'request_queue': queue,
        }
    
        return render(request,'request.html', data)
    else:
        return redirect('login')

def clinic(request):
    if 'clinic_id' in request.session:
        users = firestoreDB.collection('users').get()

        user_data = []

        for user in users:
            value = user.to_dict()
            user_data.append(value)


        if request.method == 'POST':
            userId = request.POST.get('user_id_post')
            items = firestoreDB.collection('items').document(userId).get()
            data = {
                'user_data': user_data,
                'item_data': items.to_dict(),
            }
            return render(request, 'item_data.html', {'item_data':items.to_dict()})
        else:
            data = {
                'user_data': user_data,
            }

        return render(request,'clinic.html', data)  

    else:
        return redirect('login')

def settings(request):
    return render(request,'settings.html')

def login_validation(request):
    if request.method == 'POST':
        email = request.POST.get('login_email')
        password = request.POST.get('login_password')
    
    try:
        user_signin = auth.sign_in_with_email_and_password(email,password)
        

        if user_signin['localId'] == 'DhLUuRJ7BOOkx9jF78JzvVSxTLb2':
            request.session['clinic_id'] = user_signin['localId']
            return HttpResponse('Success!')
        else:
            return HttpResponse('Invalid Email or Password!')

    except:
        return HttpResponse('Invalid Email or Password!')

def logout(request):
    try:
        del request.session['clinic_id']
    except:
        return redirect('/')
    return redirect('/')


def acceptClinic(request):
    if request.method == 'POST':
        clinicAddress = request.POST.get('clinicAddress')
        clinicContactNumber = request.POST.get('clinicContactNumber')
        clinicDescription = request.POST.get('clinicDescription')
        clinicImgDirectory = request.POST.get('clinicImgDirectory')
        clinicImgUrl = request.POST.get('clinicImgUrl')
        clinicName = request.POST.get('clinicName')
        openingTime = request.POST.get('openingTime')
        closingTime = request.POST.get('closingTime')
        clinicEmail = request.POST.get('clinicEmail')
        clinicLatitude = request.POST.get('clinicLatitude')
        clinicLongitude = request.POST.get('clinicLongitude')
        totalItems = request.POST.get('totalItems')
        userId = request.POST.get('userId')

        doc_ref = firestoreDB.collection('users').document(userId)
        doc_ref.set({
            'user_id': userId,
            'clinic_img_url' : clinicImgUrl,
            'clinic_img_directory' : clinicImgDirectory,
            'clinic_name': clinicName,
            'clinic_address': clinicAddress,
            'clinic_contact_number': clinicContactNumber,
            'latitude': clinicLatitude,
            'longitude': clinicLongitude,
            'email': clinicEmail,
            'opening_time': openingTime,
            'closing_time': closingTime,
            'clinic_description': clinicDescription,
            'total_items': totalItems,
        })

        firestoreDB.collection('queue').document(userId).delete()

        now = datetime.datetime.now()

        doc_ref2 = firestoreDB.collection('news').document(userId)

        doc_ref2.set({
            'date_accepted': now,
            'clinic_name': clinicName,
        })

        email_message = 'Congratulations Your Request for your Clinic to be Added in Animal Clinic Directory has now been approved, You can now Sign In with Your Email and Password Provided on the Registration Page that You have Already Filled Up Before'

        send_mail(
            'Animal Clinic Directory',
            email_message,
            'clinic.directory.2021@gmail.com',
            [clinicEmail],
            fail_silently=False,
        )

        return HttpResponse('Accepted')

def declineClinic(request):
    if request.method == 'POST':
        userId = request.POST.get('userId')
        clinicImgDirectory = request.POST.get('clinicImgDirectory')
        clinicEmail = request.POST.get('clinicEmail')
        clinicName = request.POST.get('clinicName')
        clinicPassword = request.POST.get('clinicPassword')

        deleteUser = auth.sign_in_with_email_and_password(clinicEmail, clinicPassword)
        auth.delete_user_account(deleteUser['idToken'])

        firestoreDB.collection('queue').document(userId).delete()

        storage.delete(clinicImgDirectory, userId)
        
        email_message = 'We Appreciate Your Effort But Your Request to add Your Clinic in Animal Clinic Directory Have Been Declined.'

        send_mail(
            'Animal Clinic Directory',
            email_message,
            'clinic.directory.2021@gmail.com',
            [clinicEmail],
            fail_silently=False,
        )


        now = datetime.datetime.now()

        doc_ref2 = firestoreDB.collection('news').document(userId)

        doc_ref2.set({
            'date_rejected': now,
            'clinic_name': clinicName,
        })

        return HttpResponse('Declined')

