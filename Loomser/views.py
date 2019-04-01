import pyrebase
from django.shortcuts import render
from django.contrib import auth 
config = {
'apiKey': "AIzaSyCiMKloqNVevDZnv1nEuXqhsW8_2T2KEKw",
    'authDomain': "kuchbhi-a4f24.firebaseapp.com",
    'databaseURL': "https://kuchbhi-a4f24.firebaseio.com",
    'projectId': "kuchbhi-a4f24",
    'storageBucket': "kuchbhi-a4f24.appspot.com",
    'messagingSenderId': "247457250673"
}
firebase = pyrebase.initialize_app(config)

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database=firebase.database()
def signIn(request):

    return render(request, "signIn.html")

def postsign(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message="invalid credentials"
        return render(request,"signIn.html",{"messg":message})
    print(user['idToken'])
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request, "address.html",{"e":email})
def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')


def signUp(request):

    return render(request,"signup.html")
def postsignup(request):

    name=request.POST.get('name')
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
        user=authe.create_user_with_email_and_password(email,passw)
        uid = user['localId']
        data={"name":name,"status":"1","email":email,"password":passw}
        database.child("users").child(uid).child("details").set(data)
    except:
        message="Unable to create account try again"
        return render(request,"signup.html",{"messg":message})
        

    
    return render(request,"signIn.html")

def address(request):
    return render(request,'address.hmtl')

def postaddress(request):
    address=request.POST.get('address')
    Phone=request.POST.get('Phone')
    addType=request.POST.get('addType')
    preftime=request.POST.get('preftime')

    idtoken= request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    data = {
        "address":address,
        "Phone":Phone,
        "addType":addType,
        "preftime":preftime,
    }
    database.child('users').child(a).child('address').set(data)
    name = database.child('users').child(a).child('details').child('name').get().val()
    return render(request,'welcome.html', {'e':name})