import mysql.connector
import config
import mysql.connector

import mysql.connector


def get_resource_efficiency():
    try:
        with mysql.connector.connect(
                host=config.host,
                user=config.user,
                password=config.password,
                database=config.database
        ) as mydb:
            with mydb.cursor() as cursor:
                # دریافت لیست شهرها
                cursor.execute("SELECT Id, ParentId FROM citytribe WHERE ParentId IS NOT NULL")
                cities = cursor.fetchall()

                # دریافت اطلاعات ساختمان‌های سودآور
                cursor.execute("SELECT BuildingId, PropertyId, PrimaryProperty FROM profit_building")
                profit_building = {row[0]: {'ResourceId': row[1], 'PrimaryProperty': row[2]} for row in
                                   cursor.fetchall()}
                insert_data = []
                update_data = []
                cursor.execute("SELECT CityId, PropertyId, Amount, Id FROM property_city")
                property_city_data = {(row[0], row[1]): {"Amount": row[2], "Id": row[3]} for row in cursor.fetchall()}
                for city in cities:
                    city_id = city[0]
                    city_parent = city[1]
                    cursor.execute('''
                                    SELECT BuildingId FROM double_property WHERE CityId = %s
                                ''', (city_parent,))
                    double_property_ids = {row[0] for row in cursor.fetchall()}
                    # دریافت ساختمان‌های شهر
                    cursor.execute("""
                        SELECT bc.BuildingId, bc.Level, b.type 
                        FROM building_city bc
                        LEFT JOIN building b ON bc.BuildingId = b.Id
                        WHERE bc.CityId = %s
                    """, (city_id,))
                    buildings = cursor.fetchall()
                    # دریافت محبوبیت شهر
                    cursor.execute("SELECT Amount FROM property_city WHERE CityId = %s AND PropertyId = 1", (city_id,))
                    popularity = cursor.fetchone()
                    popularity = (popularity[0] // 10) * 10 if popularity else 50  # گرد کردن به دهگان پایین‌تر

                    # ضریب تأثیر محبوبیت
                    popularity_multiplier = {
                        0: 0.75, 10: 0.80, 20: 0.85, 30: 0.90, 40: 0.95,
                        50: 1.00, 60: 1.05, 70: 1.10, 80: 1.15, 90: 1.20, 100: 1.25
                    }.get(popularity, 1.00)

                    for building in buildings:
                        building_id, level, type_build = building
                        data = profit_building.get(building_id)
                        if not data:
                            continue

                        resource_id = data['ResourceId']
                        if building_id in double_property_ids:
                            total_amount = data['PrimaryProperty'] * level * 1.5
                        else:
                            total_amount = data['PrimaryProperty'] * level
                        if type_build == 1:
                            total_amount = total_amount * popularity_multiplier
                        else:
                            total_amount = total_amount

                        # مقدار جدید درج شود
                        existing_data = property_city_data.get((city_id, resource_id))

                        if existing_data:
                            update_data.append((total_amount, existing_data["Id"]))
                        else:
                            insert_data.append((city_id, resource_id, total_amount))
                if update_data:
                    cursor.executemany("UPDATE property_city SET Amount = Amount + %s WHERE Id = %s", update_data)
                    # اعمال `INSERT` ها
                if insert_data:
                    cursor.executemany("INSERT INTO property_city (CityId, PropertyId, Amount) VALUES (%s, %s, %s)",
                                       insert_data)

                mydb.commit()
                return "محاسبات با موفقیت انجام شد 🎉", True

    except mysql.connector.Error as err:
        return str(err), False


def cost_food():
    try:
        # اتصال به دیتابیس
        with mysql.connector.connect(
                host=config.host,
                user=config.user,
                password=config.password,
                database=config.database
        ) as mydb:
            with mydb.cursor() as cursor:
                city_not_resource = []

                # گرفتن لیست شهرها
                city_query = '''
                    SELECT Id,Title
                    FROM citytribe
                    WHERE ParentId IS NOT NULL
                '''
                cursor.execute(city_query)
                cities = cursor.fetchall()

                # پردازش اطلاعات برای هر شهر
                for city in cities:
                    # دریافت اطلاعات پیاده‌نظام
                    infantry_query = '''
                        SELECT Amount 
                        FROM property_city
                        WHERE CityId = %s AND PropertyId IN (11, 12, 13)
                    '''
                    cursor.execute(infantry_query, (city[0],))
                    infantries = cursor.fetchall()
                    infantries_sum = sum([infantry[0] for infantry in infantries]) if infantries else 0

                    # دریافت اطلاعات ویژه
                    special_query = '''
                        SELECT Amount 
                        FROM property_city
                        WHERE CityId = %s AND PropertyId IN (14, 22)
                    '''
                    cursor.execute(special_query, (city[0],))
                    special = cursor.fetchall()
                    special_sum = sum([row[0] for row in special]) * 2 if special else 0

                    # مجموع هزینه‌ها
                    sum_cost = infantries_sum + special_sum

                    # دریافت اطلاعات ماهی
                    fish_query = '''
                        SELECT Amount, Id
                        FROM property_city
                        WHERE CityId = %s AND PropertyId = 7
                    '''
                    cursor.execute(fish_query, (city[0],))
                    fish = cursor.fetchone()

                    # بررسی وجود ماهی و اجرای کوئری‌های مرتبط
                    if fish:
                        fish_amount = fish[0] * 2
                        fish_id = fish[1]

                        # اگر ماهی کافی بود به شهر بعدی برو
                        if fish_amount >= sum_cost:
                            new_fish_amount = (fish_amount - sum_cost)
                            update_fish_query = '''
                                UPDATE property_city
                                SET Amount = %s
                                WHERE Id = %s
                            '''
                            cursor.execute(update_fish_query, (new_fish_amount, fish_id))
                            sum_cost = 0
                        else:
                            # اگر ماهی کافی نبود، ماهی صفر شود و کوئری جدید اجرا شود
                            update_fish_query = '''
                                UPDATE property_city
                                SET Amount = 0
                                WHERE Id = %s
                            '''
                            cursor.execute(update_fish_query, (fish_id,))
                            sum_cost = sum_cost - fish_amount

                    # استفاده از گوشت اگر ماهی کافی نبود
                    if sum_cost > 0:
                        beef_query = '''
                            SELECT Amount, Id
                            FROM property_city
                            WHERE CityId = %s AND PropertyId = 8
                        '''
                        cursor.execute(beef_query, (city[0],))
                        beef = cursor.fetchone()

                        if beef:
                            beef_amount = beef[0] * 3
                            beef_id = beef[1]
                            if beef_amount >= sum_cost:
                                new_beef_amount = (beef_amount - sum_cost)
                                update_beef_query = '''
                                    UPDATE property_city
                                    SET Amount = %s
                                    WHERE Id = %s
                                '''
                                cursor.execute(update_beef_query, (new_beef_amount, beef_id))
                                sum_cost = 0
                            else:
                                update_beef_query = '''
                                    UPDATE property_city
                                    SET Amount = 0
                                    WHERE Id = %s
                                '''
                                cursor.execute(update_beef_query, (beef_id,))
                                sum_cost = sum_cost - beef_amount

                    # استفاده از گندم اگر ماهی و گوشت کافی نبود
                    if sum_cost > 0:
                        wheat_query = '''
                            SELECT Amount, Id
                            FROM property_city
                            WHERE CityId = %s AND PropertyId = 10
                        '''
                        cursor.execute(wheat_query, (city[0],))
                        wheat = cursor.fetchone()

                        if wheat:
                            wheat_amount = wheat[0]
                            wheat_id = wheat[1]
                            if wheat_amount >= sum_cost:
                                new_wheat_amount = wheat_amount - sum_cost
                                update_wheat_query = '''
                                    UPDATE property_city
                                    SET Amount = %s
                                    WHERE Id = %s
                                '''
                                cursor.execute(update_wheat_query, (new_wheat_amount, wheat_id))
                                sum_cost = 0
                            else:
                                update_wheat_query = '''
                                    UPDATE property_city
                                    SET Amount = %s
                                    WHERE Id = %s
                                '''
                                new_wheat_amount = wheat_amount - sum_cost
                                cursor.execute(update_wheat_query, (new_wheat_amount, wheat_id,))
                                city_not_resource.append(city[1])  # ذخیره شهرهایی که منابع کافی ندارند

            mydb.commit()  # تایید تغییرات در دیتابیس

    except mysql.connector.Error as err:
        return str(err), False
    property_text = (f" \n"
            f"عملیات با موفقیت انجام شد.\n"
            f"\n"
            f"شهر هایی که غذای مورد نیاز نداشتند :")
    for city in city_not_resource :
        property_text += f"\n {city}"
    return property_text, True
def cost_casualties():
    try:
        # لیست منابع مختلف پیاده‌نظام بر اساس ResourceId
        resources = [(11, 'swordsman'), (12, 'archer'), (13, 'speared'),(14,'cavalry'),(22,'special')]

        # اتصال به دیتابیس
        with mysql.connector.connect(
                host=config.host,
                user=config.user,
                password=config.password,
                database=config.database
        ) as mydb:
            with mydb.cursor(buffered=True) as cursor:
                # گرفتن شهرهایی که گندم منفی دارند
                cereal_query = '''
                    SELECT pc.Id, pc.CityId, pc.Amount, c.Title
                    FROM property_city pc
                    JOIN citytribe c ON pc.CityId = c.Id
                    WHERE pc.Amount < 0 AND pc.PropertyId = 10
                '''
                cursor.execute(cereal_query)
                cereal = cursor.fetchall()

                # دیکشنری برای ذخیره اطلاعات کاهش سربازان
                casualties_report = {}

                # پردازش اطلاعات برای هر شهر
                for city in cereal:
                    city_id = city[1]
                    city_title = city[3]
                    cereal_residue = abs(city[2])

                    if city_id not in casualties_report:
                        casualties_report[city_id] = {
                            "swordsman": 0,
                            "archer": 0,
                            "speared": 0,
                            "cavalry" : 0,
                            "special" : 0,
                            "title": city_title,
                        }

                    for resource_id, resource_name in resources:
                        if cereal_residue == 0:
                            break
                        # دریافت اطلاعات پیاده‌نظام مورد نظر
                        query = '''
                            SELECT Amount, Id
                            FROM property_city
                            WHERE CityId = %s AND PropertyId = %s
                        '''
                        cursor.execute(query, (city_id, resource_id))
                        unit = cursor.fetchone()

                        if unit and unit[0] > 0:
                            unit_amount = unit[0] * 2 if resource_id == 14  else unit[0]
                            if unit_amount > cereal_residue:
                                cost = unit_amount - cereal_residue
                                cost = cost / 2 if resource_id == 14 else cost
                                update_query = '''
                                    UPDATE property_city
                                    SET Amount = %s 
                                    WHERE Id = %s
                                '''
                                cursor.execute(update_query, (cost, unit[1]))

                                casualties_report[city_id][resource_name] += cereal_residue
                                cereal_residue = 0
                            else:
                                update_query = '''
                                    UPDATE property_city
                                    SET Amount = 0 
                                    WHERE Id = %s
                                '''
                                cursor.execute(update_query, (unit[1],))

                                casualties_report[city_id][resource_name] += unit[0]
                                cereal_residue -= unit[0]

                    cereal_residue_query = '''
                        UPDATE property_city
                        SET Amount = %s 
                        WHERE Id = %s
                    '''
                    cursor.execute(cereal_residue_query, (-cereal_residue, city[0]))

            mydb.commit()

    except mysql.connector.Error as err:
        return f"خطای دیتابیس: {err}", False

    report_message = "گزارش کاهش سربازان:\n"
    for city_id, losses in casualties_report.items():
        report_message += '\n\n'
        report_message += f"شهر {losses['title']}\n"
        report_message += f" - شمشیرزن: {losses['swordsman']} نفر کاهش یافت.\n"
        report_message += f" - کماندار: {losses['archer']} نفر کاهش یافت.\n"
        report_message += f" - نیزه‌دار: {losses['speared']} نفر کاهش یافت.\n"
        report_message += f" - سواره نظام: {losses['cavalry']} نفر کاهش یافت.\n"
        report_message += f" - نیروی ویژه: {losses['special']} نفر کاهش یافت.\n"

    return report_message, True
def get_negative_supply():
    try:
        # اتصال به دیتابیس
        with mysql.connector.connect(
                host=config.host,
                user=config.user,
                password=config.password,
                database=config.database
        ) as mydb:
            with mydb.cursor(buffered=True) as cursor:
                # گرفتن شهرهایی که گندم منفی دارند
                cereal_query = '''
                       SELECT pc.Amount, c.Title
                       FROM property_city pc
                       join citytribe c
                       on pc.CityId = c.Id
                       WHERE pc.Amount < 0 AND pc.PropertyId = 10
                   '''
                cursor.execute(cereal_query)
                cereal = cursor.fetchall()
            property_text = 'قلعه ها دارای گندم منفی'
            for item in cereal:
                property_text += f'شهر : {item[1]} تعداد : {item[0]}'
        return property_text
    except mysql.connector.Error as err:
        return str(err)

def get_up_city(chat_id):
    try:
        with mysql.connector.connect(
                host=config.host,
                user=config.user,
                password=config.password,
                database=config.database
        ) as mydb:
            with mydb.cursor() as cursor:
                # دریافت لیست شهرها
                cursor.execute("SELECT Id, ParentId FROM citytribe WHERE ChatId = %s", (chat_id,))
                cities = cursor.fetchone()
                city_id = cities[0]
                city_parent = cities[1]
                # دریافت اطلاعات ساختمان‌های سودآور
                cursor.execute("SELECT BuildingId, PropertyId, PrimaryProperty FROM profit_building")
                profit_building = {row[0]: {'ResourceId': row[1], 'PrimaryProperty': row[2]} for row in
                                   cursor.fetchall()}
                insert_data = []
                update_data = []
                cursor.execute("SELECT CityId, PropertyId, Amount, Id FROM property_city where CityId = %s", (city_id,))

                property_city_data = {(row[0], row[1]): {"Amount": row[2], "Id": row[3]} for row in cursor.fetchall()}

                cursor.execute('''
                                SELECT BuildingId FROM double_property WHERE CityId = %s
                            ''', (city_parent,))
                double_property_ids = {row[0] for row in cursor.fetchall()}
                # دریافت ساختمان‌های شهر
                cursor.execute("""
                    SELECT bc.BuildingId, bc.Level, b.type 
                    FROM building_city bc
                    LEFT JOIN building b ON bc.BuildingId = b.Id
                    WHERE bc.CityId = %s
                """, (city_id,))
                buildings = cursor.fetchall()
                # دریافت محبوبیت شهر
                cursor.execute("SELECT Amount FROM property_city WHERE CityId = %s AND PropertyId = 1", (city_id,))
                popularity = cursor.fetchone()
                popularity = (popularity[0] // 10) * 10 if popularity else 50  # گرد کردن به دهگان پایین‌تر

                # ضریب تأثیر محبوبیت
                popularity_multiplier = {
                    0: 0.75, 10: 0.80, 20: 0.85, 30: 0.90, 40: 0.95,
                    50: 1.00, 60: 1.05, 70: 1.10, 80: 1.15, 90: 1.20, 100: 1.25
                }.get(popularity, 1.00)

                for building in buildings:
                    building_id, level, type_build = building
                    data = profit_building.get(building_id)
                    if not data:
                        continue

                    resource_id = data['ResourceId']
                    if building_id in double_property_ids:
                        total_amount = data['PrimaryProperty'] * level * 1.5
                    else:
                        total_amount = data['PrimaryProperty'] * level
                    if type_build == 1:
                        total_amount = total_amount * popularity_multiplier
                    else:
                        total_amount = total_amount

                    # مقدار جدید درج شود
                    existing_data = property_city_data.get((city_id, resource_id))

                    if existing_data:
                        update_data.append((total_amount, existing_data["Id"]))
                    else:
                        insert_data.append((city_id, resource_id, total_amount))
                if update_data:
                    cursor.executemany("UPDATE property_city SET Amount = Amount + %s WHERE Id = %s", update_data)
                    # اعمال `INSERT` ها
                if insert_data:
                    cursor.executemany("INSERT INTO property_city (CityId, PropertyId, Amount) VALUES (%s, %s, %s)",
                                       insert_data)

                mydb.commit()
                return "اپ با موفقیت خورده شد", True

    except mysql.connector.Error as err:
        return str(err), False