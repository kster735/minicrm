from django.db import connection
from .utilities import dictfetchall

def messages_select(user_id):
    sql = "SELECT * FROM crm_message WHERE contact_id in (SELECT id FROM crm_contact WHERE user_id=%s)"
    cursor = connection.cursor()
    cursor.execute(sql, [str(user_id)])
    messages_list = dictfetchall(cursor)
    cursor.close()
    return messages_list

def messages_count(user_id):
    sql = "SELECT count(id) as m_count FROM crm_message "
    sql+= "WHERE contact_id in (SELECT id FROM crm_contact WHERE user_id=%s)"
    cursor = connection.cursor()
    cursor.execute(sql, [user_id])
    count = dictfetchall(cursor)[0]['m_count']
    cursor.close()
    return count

def messages_select_recent(user_id):
    sql = "SELECT * FROM crm_message "
    sql+= "WHERE contact_id in (SELECT id FROM crm_contact WHERE user_id=%s) "
    sql+= "ORDER BY message_datetime DESC "
    # sql+= "LIMIT %s"
    cursor = connection.cursor()
    cursor.execute(sql, [str(user_id)])
    messages_recent_list = dictfetchall(cursor)
    cursor.close()
    return messages_recent_list


# def messages_overdue(user_id):
#     sql = "SELECT count(id) as m_count FROM crm_message "
#     sql+= "WHERE contact_id in (SELECT id FROM crm_contact WHERE user_id=%s)"
#     cursor = connection.cursor()
#     cursor.execute(sql, [user_id])
#     count = dictfetchall(cursor)[0]['m_count']
#     cursor.close()
#     return count
