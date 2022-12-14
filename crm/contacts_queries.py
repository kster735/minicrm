from django.db import connection
from .utilities import dictfetchall

def contacts_select(user_id, order='', limit1=0, limit2=25):
    sql = "SELECT * FROM crm_contact "
    sql+= "WHERE user_id= %s "
    sql+= "ORDER BY %s"
    sql+= "LIMIT %s, %s"
    cursor = connection.cursor()
    cursor.execute(sql, [user_id, order, limit1, limit2])
    contacts_list = dictfetchall(cursor)
    cursor.close()
    return contacts_list

def contacts_count_user(user_id):
    sql = "SELECT count(id) as c_count from crm_contact "
    sql+= "WHERE user_id= %s"
    cursor = connection.cursor()
    cursor.execute(sql, [user_id])
    count = dictfetchall(cursor)[0]['c_count']
    cursor.close()
    return count

def contacts_count():
    sql = "SELECT count(id) as c_count from crm_contact "
    cursor = connection.cursor()
    cursor.execute(sql)
    count = dictfetchall(cursor)[0]['c_count']
    cursor.close()
    return count

def contacts_active():
    sql = "SELECT count(id) as c_count from crm_contact "
    sql+= "WHERE contact_is_active=True"
    cursor = connection.cursor()
    cursor.execute(sql)
    active = dictfetchall(cursor)[0]['c_count']
    cursor.close()
    return active

def contacts_percentage():
    return round(100 * contacts_active() / contacts_count()) 