from django.db import connection
from .utilities import dictfetchall

def users_select(order='', limit1=0, limit2=25):
    sql = "SELECT * FROM crm_user "
    sql+= "ORDER BY %s"
    sql+= "LIMIT %s, %s"
    cursor = connection.cursor()
    cursor.execute(sql, [order, limit1, limit2])
    contacts_list = dictfetchall(cursor)
    cursor.close()
    return contacts_list

def users_count():
    sql = "SELECT count(id) as u_count from crm_user "
    cursor = connection.cursor()
    cursor.execute(sql)
    count = dictfetchall(cursor)[0]['u_count']
    cursor.close()
    return count

def users_active():
    sql = "SELECT count(id) as u_count from crm_user "
    sql+= "WHERE user_is_active=True"
    cursor = connection.cursor()
    cursor.execute(sql)
    active = dictfetchall(cursor)[0]['u_count']
    cursor.close()
    return active

def user_is_active(username):
    sql = "SELECT user_is_active FROM crm_user "
    sql+= "WHERE  user_username=%s "
    sql+= "LIMIT 1"
    cursor = connection.cursor()
    cursor.execute(sql, [username])
    result = dictfetchall(cursor)[0]['user_is_active']
    cursor.close()
    return result
    
def users_percentage():
    return round(100 * users_active() / users_count()) 
