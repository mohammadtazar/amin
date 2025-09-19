import mysql.connector
import config

def get_military():
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        # اجرای کوئری
        try:
            build_all_city = f'''
                               SELECT Id, Title
                               FROM building
                               WHERE type = 2 or type = 3 or type = 4
                               '''
            cursor.execute(build_all_city)
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            return str(err), False
        cursor.close()
        mydb.close()
        return result, True
    except Exception as e:
        return str(e), False

def get_economic():
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        # اجرای کوئری
        try:
            build_all_city = f'''
                               SELECT Id, Title
                               FROM building
                               WHERE type = 1
                               '''
            cursor.execute(build_all_city)
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            return str(err), False
        cursor.close()
        mydb.close()
        return result, True
    except Exception as e:
        return str(e), False

def get_cost(build_id,chat_id):
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
            build_level_query = f'''
                               SELECT bc.id, bc.Level
                               FROM building_city bc
                               join citytribe c
                               on c.id = bc.CityId
                               WHERE c.ChatId = %s And bc.BuildingId = %s
                               '''
            cursor.execute(build_level_query, (chat_id, build_id))
            build_level = cursor.fetchall()
            if not build_level:
                level = 1
            else:
                if int(build_id) == 13:
                    if build_level[0][1] >= 3:
                        return 1, True
                if int(build_id) == 14:
                    if build_level[0][1] >= 5:
                        return 1, True
                level = build_level[0][1] + 1
        except mysql.connector.Error as err:
            return str(err), False

        try:
            cost_build_query = f'''
                                 SELECT bc.InitialValue, bc.SecondValue ,r.Title
                                 FROM building_cost bc
                                 join property r
                                 on r.Id = bc.PropertyId
                                 WHERE bc.BuildingId = %s
                                 '''
            cursor.execute(cost_build_query, (build_id,))
            cost_build = cursor.fetchall()

        except mysql.connector.Error as err:
            return str(err), False
        cursor.close()
        mydb.close()
        property_text = '\nهزینه ارتقا'

        for item in cost_build:
            property_text += f'\n {item[2]} : {item[0] + (item[1] * level)}'
        property_text += ('\n'
                          '\n'
                          'آیا از ارتقای خود اطمینان دارید?')
        return property_text, True
    except Exception as e:
        return str(e), False

def get_confirm_cost(build_id,chat_id):
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()
        mydb.start_transaction()

        try:
            build_title_query = '''
                               SELECT Title
                               FROM building 
                               WHERE Id = %s
                               '''
            cursor.execute(build_title_query, (build_id,))
            build_title = cursor.fetchone()

        except mysql.connector.Error as err:
            return str(err), False
        # دریافت سطح ساختمان

        try:
            build_level_query = '''
                                    SELECT bc.id, bc.Level
                                    FROM building_city bc
                                    JOIN citytribe c ON c.id = bc.CityId
                                    WHERE c.ChatId = %s AND bc.BuildingId = %s
                                    '''
            cursor.execute(build_level_query, (chat_id, build_id))
            build_level = cursor.fetchall()
            if not build_level:  # اگر سطحی وجود نداشت
                first = True
                level = 1
            else:
                first = False
                level = build_level[0][1] + 1
                if build_level[0][1] >= 50:
                    return 'شما حداکثر سطح موجود را بدست آوردید', True
        except mysql.connector.Error as err:
            return str(err), False

        # دریافت هزینه‌های ساختمان
        try:
            cost_build_query = '''
                                      SELECT bc.InitialValue, bc.SecondValue, r.Title, r.Id
                                      FROM building_cost bc
                                      JOIN property r ON r.Id = bc.PropertyId
                                      WHERE bc.BuildingId = %s
                                      '''
            cursor.execute(cost_build_query, (build_id,))
            cost_build = cursor.fetchall()
        except mysql.connector.Error as err:
            return str(err), False

        # دریافت دارایی‌های شهر
        try:
            property_query = '''
                                  SELECT pc.PropertyId, pc.Amount
                                  FROM property_city pc
                                  JOIN citytribe c ON c.id = pc.CityId
                                  WHERE c.ChatId = %s
                                  '''
            cursor.execute(property_query, (chat_id,))
            property = cursor.fetchall()
        except mysql.connector.Error as err:
            return str(err), False

        property_dict = {item[0]: item[1] for item in property}

        # بررسی دارایی‌ها
        updates = []
        for item in cost_build:
            initial_value, second_value, resource_title, resource_id = item

            # بررسی موجودی منبع
            available_amount = property_dict.get(resource_id, 0)
            required_amount = initial_value + level * second_value
            # اگر منابع کافی نبود
            if available_amount < required_amount:
                return (
                    f' {resource_title} به اندازه کافی موجود نیست. هزینه ارتقا {required_amount}موجودی : {available_amount}.\n'), True
            # آماده‌سازی برای به‌روزرسانی
            updates.append((required_amount, chat_id, resource_id))

        # به‌روزرسانی منابع در یک بار
        update_query = '''
                          UPDATE property_city 
                          SET Amount = Amount - %s
                          WHERE CityId = (SELECT Id FROM citytribe WHERE ChatId = %s)
                          AND PropertyId = %s
                        '''
        for required_amount, chat_id, resource_id in updates:
            cursor.execute(update_query, (required_amount, chat_id, resource_id))
        if first:
            city_id_query = '''
                              SELECT Id
                              FROM citytribe
                              WHERE ChatId = %s
                              '''
            cursor.execute(city_id_query, (chat_id,))
            city_id = cursor.fetchall()[0][0]

            insert_data_query = '''
              INSERT INTO building_city (BuildingId, CityId, Level)
              VALUES (%s, %s, 1)
              '''
            cursor.execute(insert_data_query, (build_id, city_id))

        else:
            update_build_query = '''
                                  UPDATE building_city
                                  SET Level = Level +1
                                  WHERE BuildingId = %s AND CityId = (SELECT Id FROM citytribe WHERE ChatId = %s)
                                  '''
            cursor.execute(update_build_query, (build_id, chat_id))
            # اعمال تغییرات
        mydb.commit()

        return f'ساختمان {build_title[0]} با موفقیت ارتقا یافت', True
    except Exception as e:
        mydb.rollback()  # در صورت بروز خطا، تغییرات برگشت داده می‌شوند
        return str(e), False
    finally:
        cursor.close()
        mydb.close()
def get_all_building_costs_and_profits():
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        # کوئری برای دریافت هزینه‌ها و بازدهی‌های همه ساختمان‌ها
        query = '''
            SELECT b.Title AS BuildingTitle,
                   COALESCE(r_cost.Title, 'نامشخص') AS CostResourceTitle,
                   COALESCE(bc.InitialValue, 0) AS InitialCost,
                   COALESCE(bc.SecondValue, 0) AS SecondCost,
                   COALESCE(r_profit.Title, 'نامشخص') AS ProfitResourceTitle,
                   COALESCE(pb.PrimaryProperty, 0) AS Profit
            FROM building b
            LEFT JOIN building_cost bc ON b.Id = bc.BuildingId
            LEFT JOIN property r_cost ON bc.propertyId = r_cost.Id
            LEFT JOIN profit_building pb ON b.Id = pb.BuildingId
            LEFT JOIN property r_profit ON pb.propertyId = r_profit.Id
            ORDER BY b.OrderItem, b.Title
        '''
        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        mydb.close()

        # بررسی داده‌های دریافت‌شده
        if not results:
            return "❌ هیچ هزینه یا بازدهی‌ای برای ساختمان‌ها یافت نشد."

        response_text = "📜 **هزینه‌ها و بازدهی‌های ساختمان‌ها:**\n"
        building_data = {}

        # دسته‌بندی اطلاعات هر ساختمان
        for building, cost_resource, initial_cost, second_cost, profit_resource, profit in results:
            if building not in building_data:
                building_data[building] = {
                    "costs": [],
                    "profits": []
                }
            if cost_resource and (initial_cost or second_cost):
                cost_text = f"{cost_resource}: اولیه {initial_cost}"
                if second_cost:
                    cost_text += f" | افزایش {second_cost}"
                building_data[building]["costs"].append(cost_text)
            if profit_resource and profit:
                building_data[building]["profits"].append(f"{profit_resource}: {profit}")

        # ساختن متن نهایی گزارش
        for building, data in building_data.items():
            response_text += f"\n🏛 **{building}**\n"
            if data["costs"]:
                response_text += "   💰 **هزینه‌ها:**\n"
                for cost in set(data["costs"]):
                    response_text += f"      - {cost}\n"
            if data["profits"]:
                response_text += "   ⚙ **بازدهی‌ها:**\n"
                for profit in set(data["profits"]):
                    response_text += f"      - {profit}\n"

        return response_text
    except Exception as e:
        return f"⚠️ خطا: {e}"

def get_all_building():
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        # اجرای کوئری
        try:
            build_all_city = f'''
                               SELECT Id, Title
                               FROM building
                               '''
            cursor.execute(build_all_city)
            result = cursor.fetchall()
        except mysql.connector.Error as err:
            return str(err), False
        cursor.close()
        mydb.close()
        return result, True
    except Exception as e:
        return str(e), False
def get_up_level(chat_id,building_id):
    try:
        building_id = int(building_id)
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()
        building_title_query = '''
        SELECT Title FROM building WHERE Id = %s'''

        cursor.execute(building_title_query, (building_id,))
        building_title = cursor.fetchone()[0]

        # اجرای کوئری
        try:
            city_query = '''
                    SELECT Id 
                    FROM citytribe
                    WHERE ChatId = %s'''
            cursor.execute(city_query, (chat_id,))
            city_id = cursor.fetchone()
            if city_id:
                city_id = city_id[0]
            else:
                return "شهر یافت نشد"
            building_id_query = '''
            SELECT Id
            FROM building_city
            WHERE CityId = %s AND BuildingId = %s'''
            cursor.execute(building_id_query, (city_id,building_id))
            building_city = cursor.fetchone()
            if building_city:
                update_query = '''
                UPDATE building_city
                SET Level = Level + 1
                WHERE Id = %s'''
                cursor.execute(update_query, (building_city[0],))
            else:
                insert_query = '''
                INSERT INTO building_city (CityId,BuildingId, Level)
                VALUES (%s, %s, 1)'''
                cursor.execute(insert_query, (city_id,building_id))
        except mysql.connector.Error as err:
            return str(err), False
        mydb.commit()
        cursor.close()
        mydb.close()
        return f'ساختمان {building_title} با موفیقت یک لول اضافه شد '
    except Exception as e:
        return str(e), False
def get_down_level(chat_id,building_id):
    try:
        building_id = int(building_id)
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()
        building_title_query = '''
        SELECT Title FROM building WHERE Id = %s'''
        cursor.execute(building_title_query, (building_id,))
        building_title = cursor.fetchone()[0]

        # اجرای کوئری
        try:
            city_query = '''
                    SELECT Id 
                    FROM citytribe
                    WHERE ChatId = %s'''
            cursor.execute(city_query, (chat_id,))
            city_id = cursor.fetchone()
            if city_id:
                city_id = city_id[0]
            else:
                return "شهر یافت نشد"
            update_query = '''
            UPDATE building_city
            SET Level = Level - 1
            WHERE BuildingId = %s AND CityId = %s'''
            cursor.execute(update_query, (building_id,city_id))

        except mysql.connector.Error as err:
            return str(err), False
        mydb.commit()
        cursor.close()
        mydb.close()
        return f'ساختمان {building_title} با موفیقت یک لول کم شد '
    except Exception as e:
        return str(e), False