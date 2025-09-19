import mysql.connector
import config

def get_all_city():
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()
        try:
            tribe_query = f'''
                            SELECT Id,Title
                            FROM citytribe
                            WHERE ParentId IS NULL
                            '''
            cursor.execute(tribe_query)
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            return str(err), False
        cursor.close()
        mydb.close()
        return result, True
    except Exception as e:
        return str(e), False

def get_city_by_parent_id(parent_id):
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()
        try:
            build_all_city = f'''
                               SELECT Id, Title
                               FROM citytribe
                               WHERE ParentId = %s
                               '''
            cursor.execute(build_all_city, (parent_id,))
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            return str(err), False
        cursor.close()
        mydb.close()
        return result, True
    except Exception as e:
        return str(e), False

def get_campaign_confirm(origin,destination,chat_id,time,campaign_type):
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()
        try:
            city_query = f'''
                               SELECT Title, Id,Family,ParentId
                               FROM citytribe
                               WHERE ChatId = %s
                               '''
            cursor.execute(city_query,(chat_id,))
            city = cursor.fetchall()[0]
        except mysql.connector.Error as err:
            return str(err), False
        try:
            origin_query = f'''
                               SELECT Title, Id
                               FROM citytribe
                               WHERE Id = %s
                               '''
            cursor.execute(origin_query,(origin,))
            origin = cursor.fetchall()[0]
        except mysql.connector.Error as err:
            return str(err), False
        try:
            destination_query = f'''
                               SELECT Title, Id
                               FROM citytribe
                               WHERE Id = %s
                               '''
            cursor.execute(destination_query,(destination,))
            destination = cursor.fetchall()[0]
        except mysql.connector.Error as err:
            return str(err), False
        cursor.close()
        mydb.close()
        if campaign_type == "1":
            type_campain = "لشکریان"
        else:
            type_campain = "نیروی دریایی "
        property_text = (f'{type_campain} خاندان {city[2]} از {origin[0]}  به سمت قلعه {destination[0]} حرکت کردند '
                         f'\n'
                         f'زمان رسیدن : {time}')
        return property_text, True,city[3]
    except Exception as e:
        return str(e), False

def get_city_by_chat_id(chat_id):
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        try:
            build_all_city = f'''
                               SELECT Id,Title, ParentId, ChatId,Family,Trade
                               FROM citytribe
                               WHERE ChatId = %s
                               '''
            cursor.execute(build_all_city, (chat_id,))
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            return str(err), False
        cursor.close()
        mydb.close()
        return result, True
    except Exception as e:
        return str(e), False

def get_city_by_id(id):
    try:
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()
        try:
            build_all_city = f'''
                               SELECT Id,Title, ParentId, ChatId,Family,Trade
                               FROM citytribe
                               WHERE Id = %s
                               '''
            cursor.execute(build_all_city, (id,))
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            return str(err), False
        cursor.close()
        mydb.close()
        return result, True
    except Exception as e:
        return str(e), False

def get_my_dragon(chat_id):
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        try:
            dragon_query = '''
            SELECT Id, Title
            FROM dragon
            WHERE ChatId = %s'''
            cursor.execute(dragon_query, (chat_id,))
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            return str(err), False

        cursor.close()
        mydb.close()
        return result, True
    except Exception as e:
        return str(e), False

def get_dragon_by_id(dragon_id):
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        try:
            dragon_query = f'''
                                  SELECT Id,Title
                                  FROM dragon
                                  WHERE Id = %s
                                  '''
            cursor.execute(dragon_query, (dragon_id,))
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            return str(err), False
        cursor.close()
        mydb.close()
        return result, True
    except Exception as e:
        return str(e), False
