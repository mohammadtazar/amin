import mysql.connector
import config
import mysql.connector
from mysql.connector import Error

def get_all_ship():
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
                               FROM property
                               where type = 4
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

def get_cost_ship(chat_id, ship_id):
    try:
        ship_id = int(ship_id)
        # اتصال به دیتابیس
        with mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        ) as mydb:
            with mydb.cursor() as cursor:
                # دریافت شهر کاربر
                city_query = '''
                            SELECT Id, ParentId
                            FROM citytribe 
                            WHERE ChatId = %s
                            '''
                cursor.execute(city_query, (chat_id,))
                city = cursor.fetchone()

                if not city:
                    return 'شهر یافت نشد', 0, False

                # دریافت سطح ساختمان مربوط به کشتی
                build_level_query = '''
                                    SELECT Level
                                    FROM building_city
                                    WHERE CityId = %s AND BuildingId = 13
                                    '''
                cursor.execute(build_level_query, (city[0],))
                build_level = cursor.fetchone()

                if not build_level:
                    return 'قلعه شما ساختمان مورد نیاز را ندارد', 0, True

                level = build_level[0]

                if ship_id in [16, 26,45] and level < 2:
                    return 'شما سطح لازم برای ارتقا را ندارید', 0, True

                if ship_id in [26,45] and level < 3:
                    return 'شما سطح لازم برای ارتقا را ندارید', 0, True
                # تعیین ویژگی‌های کشتی‌ها
                ships_data = {
                    15: ('کشتی چوبی', 250, 500, 0),
                    16: ('کشتی جنگی', 1000, 500, 500),
                    26: ('کشتی خونی', 4000, 1500, 0),
                    45: ('کشتی سایلنت', 4000, 0, 1500),
                }

                if ship_id not in ships_data:
                    return 'شناسه کشتی نامعتبر است', 0, True

                ship_name, coins, wood, iron = ships_data[ship_id]

                # قالب‌بندی متن خروجی
                property_text = (f'{ship_name}\n'
                                 f'هزینه\n'
                                 f'{coins} سکه\n'
                                 f'{wood} چوب\n'
                                 f'{iron} آهن')

        return property_text, 1, True

    except Error as err:
        return f'خطای دیتابیس: {err}', 0, False
    except Exception as e:
        return f'خطای سیستم: {e}', 0, False

def get_config_ship(chat_id, ship_id):
    try:
        ship_id = int(ship_id)

        # اتصال به دیتابیس
        with mysql.connector.connect(
                host=config.host,
                user=config.user,
                password=config.password,
                database=config.database
        ) as mydb:
            with mydb.cursor() as cursor:
                # دریافت شهر کاربر
                city_query = '''
                            SELECT Id, ParentId
                            FROM citytribe 
                            WHERE ChatId = %s
                            '''
                cursor.execute(city_query, (chat_id,))
                city = cursor.fetchone()

                if not city:
                    return 'شهر یافت نشد', 0, True

                # دریافت سطح ساختمان مربوط به کشتی
                build_level_query = '''
                                    SELECT Level
                                    FROM building_city
                                    WHERE CityId = %s AND BuildingId = 13
                                    '''
                cursor.execute(build_level_query, (city[0],))
                build_level = cursor.fetchone()

                if not build_level:
                    return 'قلعه شما ساختمان مورد نیاز را ندارد', 0, True

                level = build_level[0]

                if ship_id in [16, 26,45] and level < 2:
                    return 'شما سطح لازم برای ارتقا را ندارید', 0, True

                if ship_id in [26,45] and level < 3:
                    return 'شما سطح لازم برای ارتقا را ندارید', 0, True

                # هزینه کشتی‌ها (شناسه منبع: 1 = سکه، 2 = چوب، 3 = آهن)
                ships_cost_data = {
                    15: {3: 250, 4: 500, 6: 0},
                    16: {3: 1000, 4: 500, 6: 500},
                    26: {3: 4000, 4: 1500, 6: 0},
                    45: {3: 4000, 4: 0, 6: 1500},
                }

                if ship_id not in ships_cost_data:
                    return 'شناسه کشتی نامعتبر است', 0, True

                ship_costs = ships_cost_data[ship_id]

                # دریافت منابع فعلی کاربر
                property_query = '''
                SELECT PropertyId, Amount
                FROM property_city
                WHERE CityId = %s
                '''
                cursor.execute(property_query, (city[0],))
                user_resources = cursor.fetchall()

                # تبدیل منابع کاربر به دیکشنری برای دسترسی راحت‌تر
                user_resource_dict = {res[0]: res[1] for res in user_resources}

                # بررسی اینکه کاربر آیا منابع کافی دارد یا نه
                for resource_id, required_amount in ship_costs.items():
                    if user_resource_dict.get(resource_id, 0) < required_amount:
                        return 'منابع کافی برای ساخت کشتی ندارید', 0, True

                # کسر منابع از موجودی کاربر
                for resource_id, required_amount in ship_costs.items():
                    updated_amount = user_resource_dict[resource_id] - required_amount
                    update_resource_query = '''
                    UPDATE property_city
                    SET Amount = %s
                    WHERE CityId = %s AND PropertyId = %s
                    '''
                    cursor.execute(update_resource_query, (updated_amount, city[0], resource_id))

                # بررسی موجودیت کشتی
                ship_query = '''
                SELECT Id
                FROM property_city
                WHERE CityId = %s AND PropertyId = %s
                '''
                cursor.execute(ship_query, (city[0], ship_id))
                ship = cursor.fetchone()

                if not ship:
                    # درج کشتی جدید
                    insert_ship = '''
                    INSERT INTO property_city (CityId, PropertyId, Amount)
                    VALUES (%s, %s, 1)
                    '''
                    cursor.execute(insert_ship, (city[0], ship_id))
                else:
                    # به‌روزرسانی تعداد کشتی
                    update_ship = '''
                    UPDATE property_city
                    SET Amount = Amount + 1
                    WHERE Id = %s
                    '''
                    cursor.execute(update_ship, (ship[0],))

                mydb.commit()  # اعمال تغییرات در دیتابیس

                return 'کشتی با موفقیت ساخته شد', 1, True

    except mysql.connector.Error as err:
        return f'خطای دیتابیس: {err}', 0, False
    except Exception as e:
        return f'خطای سیستم: {e}', 0, False

def get_all_tools():
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
                              FROM property
                              where type = 5
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

def get_cost_tools(chat_id,tools_id):
    try:
        tools_id = int(tools_id)
        # اتصال به دیتابیس
        with mysql.connector.connect(
                host=config.host,
                user=config.user,
                password=config.password,
                database=config.database
        ) as mydb:
            with mydb.cursor() as cursor:
                # دریافت شهر کاربر
                city_query = '''
                               SELECT Id, ParentId
                               FROM citytribe 
                               WHERE ChatId = %s
                               '''
                cursor.execute(city_query, (chat_id,))
                city = cursor.fetchone()

                if not city:
                    return 'شهر یافت نشد', 0, False

                build_level_query = '''
                                       SELECT Level
                                       FROM building_city
                                       WHERE CityId = %s AND BuildingId = 14
                                       '''
                cursor.execute(build_level_query, (city[0],))
                build_level = cursor.fetchone()

                if not build_level:
                    return 'قلعه شما ساختمان مورد نیاز را ندارد', 0, True

                level = build_level[0]
                if level < 2 :
                    if tools_id in [18, 19, 20, 21]:
                        return 'شما سطح لازم برای ارتقا را ندارید', 0, True
                if level < 3:
                    if tools_id in [19, 20, 21]:
                        return 'شما سطح لازم برای ارتقا را ندارید', 0, True
                if level < 4 :
                    if tools_id in [20, 21]:
                        return 'شما سطح لازم برای ارتقا را ندارید', 0, True
                if level < 5 :
                    if tools_id in [21]:
                        return 'شما سطح لازم برای ارتقا را ندارید', 0, True

                tools_data = {
                    17: ('نرده بان دار', 500, 200, 0, 0),
                    18: ('دژکوب', 1000, 200, 100, 0),
                    19: ('اسکورب', 3500, 500, 500, 0),
                    20: ('منجنیق', 3000, 500, 0, 500),
                    21: ('برج محاصره', 4000, 1000, 0, 0),
                }

                if tools_id not in tools_data:
                    return 'شناسه کشتی نامعتبر است', 0, True

                ship_name, coins, wood, iron, snow = tools_data[tools_id]

                # قالب‌بندی متن خروجی
                property_text = (f'{ship_name}\n'
                                 f'هزینه\n'
                                 f'{coins} سکه\n'
                                 f'{wood} چوب\n'
                                 f'{snow} سنگ\n'
                                 f'{iron} آهن')

        return property_text, 1, True

    except Error as err:
        return f'خطای دیتابیس: {err}', 0, False
    except Exception as e:
        return f'خطای سیستم: {e}', 0, False

def get_config_tools(chat_id, tools_id):
    try:
        tools_id = int(tools_id)

        # اتصال به دیتابیس
        with mysql.connector.connect(
                host=config.host,
                user=config.user,
                password=config.password,
                database=config.database
        ) as mydb:
            with mydb.cursor() as cursor:
                # دریافت شهر کاربر
                city_query = '''
                               SELECT Id, ParentId
                               FROM citytribe 
                               WHERE ChatId = %s
                               '''
                cursor.execute(city_query, (chat_id,))
                city = cursor.fetchone()

                if not city:
                    return 'شهر یافت نشد', 0, True

                # دریافت سطح ساختمان مربوط به ادوات
                build_level_query = '''
                                       SELECT Level
                                       FROM building_city
                                       WHERE CityId = %s AND BuildingId = 14
                                       '''
                cursor.execute(build_level_query, (city[0],))
                build_level = cursor.fetchone()

                if not build_level:
                    return 'قلعه شما ساختمان مورد نیاز را ندارد', 0, True

                level = build_level[0]
                if level < 2:
                    if tools_id in [18, 19, 20, 21]:
                        return 'شما سطح لازم برای ارتقا را ندارید', 0, True
                if level < 3:
                    if tools_id in [19, 20, 21]:
                        return 'شما سطح لازم برای ارتقا را ندارید', 0, True
                if level < 4:
                    if tools_id in [20, 21]:
                        return 'شما سطح لازم برای ارتقا را ندارید', 0, True
                if level < 5:
                    if tools_id in [21]:
                        return 'شما سطح لازم برای ارتقا را ندارید', 0, True
                tools_data = {
                    17: {3: 500, 4: 200, 5: 0, 6:0},
                    18: {3: 1000, 4: 200, 5: 0, 6:100},
                    19: {3: 3500, 4: 500, 5: 0, 6:500},
                    20: {3: 3000, 4: 500, 5: 500, 6:0},
                    21: {3: 4000, 4: 1000, 5: 0, 6:0},
                }

                if tools_id not in tools_data:
                    return 'شناسه ادوات نامعتبر است', 0, True
                tools_costs = tools_data[tools_id]

                property_query = '''
                   SELECT PropertyId, Amount
                   FROM property_city
                   WHERE CityId = %s
                   '''
                cursor.execute(property_query, (city[0],))
                user_resources = cursor.fetchall()

                # تبدیل منابع کاربر به دیکشنری برای دسترسی راحت‌تر
                user_resource_dict = {res[0]: res[1] for res in user_resources}

                # بررسی اینکه کاربر آیا منابع کافی دارد یا نه
                for resource_id, required_amount in tools_costs.items():
                    if user_resource_dict.get(resource_id, 0) < required_amount:
                        return 'منابع کافی برای ساخت ادوات ندارید', 0, True

                # کسر منابع از موجودی کاربر
                for resource_id, required_amount in tools_costs.items():
                    updated_amount = user_resource_dict[resource_id] - required_amount
                    update_resource_query = '''
                       UPDATE property_city
                       SET Amount = %s
                       WHERE CityId = %s AND PropertyId = %s
                       '''
                    cursor.execute(update_resource_query, (updated_amount, city[0], resource_id))

                tools_query = '''
                   SELECT Id
                   FROM property_city
                   WHERE CityId = %s AND PropertyId = %s
                   '''
                cursor.execute(tools_query, (city[0], tools_id))
                ship = cursor.fetchone()

                if not ship:
                    # درج ادوات جدید
                    insert_ship = '''
                       INSERT INTO property_city (CityId, PropertyId, Amount)
                       VALUES (%s, %s, 1)
                       '''
                    cursor.execute(insert_ship, (city[0], tools_id))
                else:
                    # به‌روزرسانی تعداد ادوات
                    update_ship = '''
                       UPDATE property_city
                       SET Amount = Amount + 1
                       WHERE Id = %s
                       '''
                    cursor.execute(update_ship, (ship[0],))

                mydb.commit()  # اعمال تغییرات در دیتابیس

                return 'ادوات با موفقیت ساخته شد', 1, True

    except mysql.connector.Error as err:
        mydb.rollback()
        return f'خطای دیتابیس: {err}', 0, False
    except Exception as e:
        mydb.rollback()
        return f'خطای سیستم: {e}', 0, False

def get_all_army():
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
                              FROM property
                              where type = 2
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

def get_cost_army(tools_id, count, parent_id):
    try:
        tools_id = int(tools_id)
        parent_id = int(parent_id)

        # نیروهای معمولی
        tools_data = {
            11: ('شمشیرزن', 10, 1, 1, 1, 0, 0, 0, 1),
            12: ('کماندار', 15, 1, 1, 0, 1, 0, 0, 0),
            13: ('نیزه دار', 10, 1, 1, 0, 0, 1, 0, 1),
            14: ('سواره', 20, 1, 1, 1, 0, 0, 1, 1),
        }

        # نیروهای ویژه — بر اساس parent_id
        special_units = {
            146: ('نیروی ویژه شمال', 25, 1, 1, 1, 0, 0, 0, 1),
            147: ('نیروی ویژه ویل', 25, 1, 1, 0, 0, 1, 1, 1),
            148: ('نیروی ویژه ریور', 25, 1, 1, 0, 1, 0, 0, 0),
            149: ('نیروی ویژه کرونز', 25, 1, 1, 1, 0, 0, 0, 1),
            150: ('نیروی ویژه جزایر', 25, 1, 1, 1, 0, 0, 0, 1),
            151: ('نیروی ویژه استورم', 25, 1, 1, 1, 0, 0, 0, 1),
            152: ('نیروی ویژه ریچ', 25, 1, 1, 1, 0, 0, 1, 1),
            153: ('نیروی ویژه وستر', 25, 1, 1, 1, 0, 0, 0, 1),
            154: ('نیروی ویژه دورن', 25, 1, 1, 0, 0, 1, 0, 1),
        }

        # بررسی اینکه نیرو ویژه است یا نه
        if tools_id == 22:
            if parent_id not in special_units:
                return f"⚠ نوع نیرو ویژه با ParentId={parent_id}ادمین بات رو خبر کن تعریف نشده.", 0, False
            army_data = special_units[parent_id]
        elif tools_id in tools_data:
            army_data = tools_data[tools_id]
        else:
            return "اگر رو سرباز کاستوم زدی که هیچی، اگر نزدی به بات زن اطلاع بده", 0, True

        # باز کردن داده‌ها
        army_name, coins, serf, armor, sword, arrow, spear, horse, separ = army_data

        # قالب خروجی
        property_text = (
            f"{count} {army_name}\n"
            f"💰 هزینه:\n"
            f"{coins * count} سکه\n"
            f"{serf * count} رعیت\n"
            f"{armor * count} زره\n"
            f"{sword * count} شمشیر\n"
            f"{arrow * count} کمان\n"
            f"{spear * count} نیزه\n"
            f"{horse * count} اسب\n"
            f"{separ * count} سپر"
        )

        return property_text, 1, True

    except Exception as e:
        return f"خطای سیستم: {e}", 0, False

def get_config_army(chat_id, tools_id, count):
    try:
        tools_id = int(tools_id)

        with mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        ) as mydb:
            with mydb.cursor() as cursor:
                # دریافت شهر کاربر و parent_id
                city_query = '''
                    SELECT Id, ParentId
                    FROM citytribe 
                    WHERE ChatId = %s
                '''
                cursor.execute(city_query, (chat_id,))
                city = cursor.fetchone()

                if not city:
                    return 'شهر یافت نشد', 0, True

                city_id = city[0]
                parent_id = city[1]

                # نیروهای معمولی
                tools_data = {
                    11: {3: 10, 35: 1, 32: 1, 29: 1, 30: 0, 31: 0, 33: 0, 44: 1},
                    12: {3: 15, 35: 1, 32: 1, 29: 0, 30: 1, 31: 0, 33: 0, 44: 0},
                    13: {3: 10, 35: 1, 32: 1, 29: 0, 30: 0, 31: 1, 33: 0, 44: 1},
                    14: {3: 20, 35: 1, 32: 1, 29: 1, 30: 0, 31: 0, 33: 1, 44: 1},
                }

                # نیروهای ویژه بر اساس ParentId
                special_units = {
                    146: {3: 25, 35: 1, 32: 1, 29: 1, 30: 0, 31: 0, 33: 0, 44: 1},  # شمال
                    147: {3: 25, 35: 1, 32: 1, 29: 0, 30: 0, 31: 1, 33: 1, 44: 1},  # ویل
                    148: {3: 25, 35: 1, 32: 1, 29: 0, 30: 1, 31: 0, 33: 0, 44: 0},  # ریور
                    149: {3: 25, 35: 1, 32: 1, 29: 1, 30: 0, 31: 0, 33: 0, 44: 1},  # کرونز
                    150: {3: 25, 35: 1, 32: 1, 29: 1, 30: 0, 31: 0, 33: 0, 44: 1},  # جزایر
                    151: {3: 25, 35: 1, 32: 1, 29: 1, 30: 0, 31: 0, 33: 0, 44: 1},  # استورم
                    152: {3: 25, 35: 1, 32: 1, 29: 1, 30: 0, 31: 0, 33: 0, 44: 1},  # ریچ
                    153: {3: 25, 35: 1, 32: 1, 29: 1, 30: 0, 31: 0, 33: 0, 44: 1},  # وستر
                    154: {3: 25, 35: 1, 32: 1, 29: 0, 30: 0, 31: 1, 33: 0, 44: 1},  # دورن
                }

                # انتخاب هزینه‌ی مناسب
                if tools_id == 22:
                    if parent_id not in special_units:
                        return f"⚠ نیروی ویژه برای ParentId={parent_id} تعریف نشده، به ادمین اطلاع بده.", 0, True
                    tools_costs = special_units[parent_id]
                elif tools_id in tools_data:
                    tools_costs = tools_data[tools_id]
                else:
                    return 'شناسه ادوات نامعتبر است', 0, True

                # دریافت منابع شهر
                property_query = '''
                    SELECT PropertyId, Amount
                    FROM property_city
                    WHERE CityId = %s
                '''
                cursor.execute(property_query, (city_id,))
                user_resources = cursor.fetchall()
                user_resource_dict = {res[0]: res[1] for res in user_resources}

                # بررسی منابع کافی
                for resource_id, required_amount in tools_costs.items():
                    if user_resource_dict.get(resource_id, 0) < required_amount * count:
                        return '⚠ منابع کافی برای ساخت نیرو ندارید', 0, True

                # کسر منابع
                for resource_id, required_amount in tools_costs.items():
                    updated_amount = user_resource_dict[resource_id] - required_amount * count
                    update_resource_query = '''
                        UPDATE property_city
                        SET Amount = %s
                        WHERE CityId = %s AND PropertyId = %s
                    '''
                    cursor.execute(update_resource_query, (updated_amount, city_id, resource_id))

                # بررسی اینکه این نیرو قبلاً وجود دارد یا نه
                tools_query = '''
                    SELECT Id
                    FROM property_city
                    WHERE CityId = %s AND PropertyId = %s
                '''
                cursor.execute(tools_query, (city_id, tools_id))
                existing_army = cursor.fetchone()

                if not existing_army:
                    insert_query = '''
                        INSERT INTO property_city (CityId, PropertyId, Amount)
                        VALUES (%s, %s, %s)
                    '''
                    cursor.execute(insert_query, (city_id, tools_id, count))
                else:
                    update_query = '''
                        UPDATE property_city
                        SET Amount = Amount + %s
                        WHERE Id = %s
                    '''
                    cursor.execute(update_query, (count, existing_army[0]))

                mydb.commit()
                return '✅ نیرو با موفقیت ساخته شد', 1, True

    except mysql.connector.Error as err:
        if mydb.in_transaction:
            mydb.rollback()
        return f'خطای دیتابیس: {err}', 0, False
    except Exception as e:
        if mydb.in_transaction:
            mydb.rollback()
        return f'خطای سیستم: {e}', 0, False
