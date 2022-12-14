from django.shortcuts import render, redirect
from .models import User, Contact, Message
from django.db import connection
from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from .utilities import dictfetchall
from .contacts_queries import *
from .users_queries import *
from .messages_queries import *

def index(request):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        user_username = request.session['user_username']
        print(user_username)
        c_count = contacts_count()
        c_active = contacts_active()
        c_percentage = contacts_percentage()
        u_count = users_count()
        u_active = users_active()
        u_percentage = users_percentage()
        m_recent = messages_select_recent(user_id)
        context = {
                    'user_id': user_id, 
                    'user_username': user_username, 
                    'contacts_count': c_count,
                    'contacts_active': c_active,
                    'contacts_percentage': c_percentage,
                    'users_count': u_count,
                    'users_active': u_active,
                    'users_percentage': u_percentage,
                    'messages_recent': m_recent
                }
        template = 'crm/index.html'
        return render(request, template, context)
    else:
        return redirect('login')
        
def landing(request):
    if not 'user_id' in request.session:
        return render(request, 'crm/landing.html')
    else:
        return redirect('index')


def login(request):
    if request.method == 'POST':
        username = request.POST['userUserName']
        password = request.POST['userPassword']
        cursor = connection.cursor()
        sql  = "SELECT * "
        sql += "FROM crm_user WHERE "
        sql += "user_username=%s"
        cursor.execute(sql, [username])
        user = dictfetchall(cursor)
        if user and user_is_active(username):
            hashed_password = user[0]['user_password']
            if check_password(password, hashed_password):
                request.session['user_id'] = user[0]['id']
                request.session['user_username'] = user[0]['user_username']
                request.session.set_expiry(1200)
                return redirect('index')
        else:
            return render(request, 'crm/login.html', {'errormsg': 'Please enter valid Username or Password.', 'username': username})
    return render(request, 'crm/login.html')

def logout(request):
    try:
        del request.session['user_id']
    except:
        return redirect('login')
    return redirect('login')

def users(request, user_id):
    if not isloggedin(request):
        return redirect('login')
    user_list = users_select('id',0, 2)
    print(user_list)
    template ='crm/users.html'
    context = {
        'user_list': user_list,
        'user_id': user_id,
    }
    return render(request, template, context)

def users_insert_form(request, user_id):
    if not isloggedin(request):
        return redirect('login')

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM crm_user WHERE id=%s", str(user_id))
    user = dictfetchall(cursor)
    cursor.close()
    return render(request, 'crm/users_insert_form.html', {'user': user[0], 'user_id': user_id})

def user_store(request):
    pass


def contacts(request, user_id, viewuserid = None, error = None):
    if not isloggedin(request):
        return redirect('login')
    
    if viewuserid == None:
        contacts_list = contacts_select(user_id, ' contact_lastname ', 5, 25)
    else:
        contacts_list = contacts_select(viewuserid, ' contact_lastname ', 5, 25)
        contacts_count_u = contacts_count_user(user_id)
        user_id = viewuserid
    return render(request, 'crm/contacts.html', {'contacts_list': contacts_list, 'contacts_count_user': contacts_count_u, 'user_id': user_id, 'errormessage': error})

def contacts_insert_form(request, user_id, viewuserid, error=None):
    if not isloggedin(request):
        return redirect('login')
    
    if user_id == viewuserid:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM crm_user WHERE id=%s", str(user_id))
        user = dictfetchall(cursor)
        cursor.close()
        return render(request, 'crm/contacts_insert_form.html', {'user': user[0], 'user_id': user_id, 'errormessage': error})
    return redirect('index')

def contact_store(request, user_id, viewuserid):
    if not isloggedin(request):
        return redirect('login')
    cfname = request.POST['contactFirstName']
    clname = request.POST['contactLastName']
    cemail = request.POST['contactEmail']
    cphone =request.POST['contactPhone']
    cmobile =request.POST['contactMobile']
    caddress = request.POST['contactAddress']
    ccompany = request.POST['contactCompany']
    cvatno = request.POST['contactVatNo']
    sql = "INSERT INTO crm_contact (`user_id`,`contact_firstname`,`contact_lastname`,`contact_email`,`contact_phone`,`contact_mobile`,`contact_address`, `contact_company`,`contact_vat_no`)"
    sql += " VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor = connection.cursor()
        cursor.execute(sql, [str(user_id), cfname, clname, cemail, cphone, cmobile, caddress, ccompany, cvatno])
        cursor.close()
        sql = "SELECT * FROM crm_contact WHERE user_id=%s"
        cursor = connection.cursor()
        cursor.execute(sql, [str(user_id)])
        contacts_list = Contact.objects.filter(user = user_id)
        cursor.close()
        return render(request, 'crm/contacts.html', {'contacts_list': contacts_list, 'user_id': user_id})
    except Exception as ex:
        error = ex
        return redirect('contacts_insert_form', user_id = user_id, viewuserid = user_id, error=ex)


def messages(request, user_id):
    if not isloggedin(request):
        return redirect('login')
    messages_list = messages_select(user_id)
    return render(request, 'crm/messages.html', {'messages_list': messages_list,'user_id': user_id})

def messages_insert_form(request, user_id, error=None):
    if not isloggedin(request):
        return redirect('login')
    cursor = connection.cursor()
    cursor.execute("SELECT id, contact_firstname, contact_lastname FROM crm_contact WHERE user_id=%s ORDER BY contact_lastname, contact_firstname", str(user_id))
    contacts = dictfetchall(cursor)
    cursor.close()
    return render(request, 'crm/messages_insert_form.html', {'contacts': contacts, 'user_id': user_id, 'user_username': request.session['user_username'], 'errormessage': error})

def message_store(request, user_id):
    if not isloggedin(request):
        return redirect('login')
    contact_id = request.POST['messageContact']
    message_title =  request.POST['messageTitle']
    message_content = request.POST['messageContent']
    message_datetime = request.POST['messageDateTime']
    message_channel = request.POST['messageChannel']
    message_due_date = request.POST['messageDueDateTime']
    message_processed_str = request.POST.get('messageProcessed', 'False')
    message_processed = True if message_processed_str == 'True' else False
    sql = "INSERT INTO crm_message (`contact_id`,`message_title`,`message_content`,`message_datetime`,`message_channel`,`message_due_datetime`,`message_processed`)"
    sql += " VALUES ( %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor = connection.cursor()
        cursor.execute(sql, [str(contact_id), message_title, message_content, message_datetime, message_channel, message_due_date, message_processed])
        cursor.close()
        sql = "SELECT * FROM crm_message WHERE contact_id=%s"
        cursor = connection.cursor()
        cursor.execute(sql, [str(contact_id)])
        messages_list = dictfetchall(cursor)
        cursor.close()
        return render(request, 'crm/messages.html', {'messages_list': messages_list, 'user_id': user_id, 'contact_id': contact_id})
    except Exception as e:
        return redirect('messages_insert_form', user_id = user_id, error=e)



def test(request):
    sessionduration = request.session.get_expiry_age() 
    cookieage = request.session.get_session_cookie_age()
    # user_id = request.session['user_id']
    cookiecontext = {'cookieage': cookieage, 'sessionduration': sessionduration}
    message = {'message': 'ok'}
    context = message | cookiecontext | {'mybool': 'False'}

    myboolean = request.POST.get('myCheck', 'False')
    message = {'message': request.POST['message']}    
    context = message | cookiecontext | {'mybool': myboolean}
    return render(request, 'crm/test.html', context)

def isloggedin(req) -> bool:
    if 'user_id' in req.session:
        return True
    return False
