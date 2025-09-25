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
def get_production():
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor(dictionary=True)
        # اجرای کوئری
        try:
            build_all_city = f'''
                                  SELECT Id, Title
                                  FROM building
                                  WHERE type in(1,2)
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
            if build_id in (13,14,18):
                return get_specil_build_cost(build_id,level)
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
def get_specil_build_cost(build_id, level):
    # دیکشنری هزینه‌ها برای ساختمان‌های خاص
    special_build_costs = {
        13: {   # ساختمان id=13
            1: {"چوب": 100, "سکه": 1500, "آهن": 0},
            2: {"چوب": 100, "سکه": 2000, "آهن": 200},
            3: {"چوب": 300, "سکه": 3000, "آهن": 400},
        },
        14: {   # ساختمان id=14
            1: {"چوب": 100, "سکه": 500},
            2: {"چوب": 500, "سکه": 700},
            3: {"چوب": 700, "سکه": 1000},
            4: {"چوب": 1000, "سکه": 1500},
            5: {"چوب": 500, "سکه": 2000, "آهن": 500, "سنگ": 200},
        },
        18: {   # ساختمان id=23
            1: {"رایگان": 0},
            2: {"چوب": 2000, "سکه": 10000},
            3: {"چوب": 2500, "سنگ": 2500, "سکه": 20000},
            4: {"چوب": 3000, "سنگ": 2000, "آهن": 2000, "سکه": 28000},
            5: {"چوب": 5000, "سنگ": 5000, "آهن": 5000, "سکه": 38000,"کیر دراگون": 1000}
        }
    }

    # اگر لول مورد نظر در دیکشنری وجود نداشت
    if build_id not in special_build_costs or level not in special_build_costs[build_id]:
        return "برای این سطح هزینه تعریف نشده است.", False

    costs = special_build_costs[build_id][level]

    # متن خروجی برای نمایش به کاربر
    property_text = "\nهزینه ارتقا "
    for res, val in costs.items():
        property_text += f"\n {res} : {val}"

    property_text += ('\n\n'
                      'آیا از ارتقای خود اطمینان دارید؟')

    return property_text, True


def get_specil_build_cost_make(build_id, level):
    # دیکشنری هزینه‌ها برای ساختمان‌های خاص
    special_build_costs = {
        13: {   # ساختمان id=13
            1: {"4": 100, "3": 1500, "6": 0},
            2: {"4": 100, "3": 2000, "6": 200},
            3: {"4": 300, "3": 3000, "6": 400},
        },
        14: {   # ساختمان id=14
            1: {"4": 100, "3": 500},
            2: {"4": 500, "3": 700},
            3: {"4": 700, "3": 1000},
            4: {"4": 1000, "3": 1500},
            5: {"4": 500, "3": 2000, "6": 500, "5": 200},
        },
        18: {   # ساختمان id=23
            2: {"4": 2000, "3": 10000},
            3: {"4": 2500, "5": 2500, "3": 20000},
            4: {"4": 3000, "5": 2000, "6": 2000, "3": 28000},
            5: {"4": 5000, "5": 5000, "6": 5000, "3": 38000,"37": 1000}
        }
    }

    if build_id not in special_build_costs or level not in special_build_costs[build_id]:
        return None  # یعنی هزینه تعریف نشده

    return special_build_costs[build_id][level]


def get_confirm_cost(build_id, chat_id):
    try:
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()
        mydb.start_transaction()

        # دریافت عنوان ساختمان
        cursor.execute("SELECT Title FROM building WHERE Id = %s", (build_id,))
        build_title = cursor.fetchone()

        # دریافت سطح ساختمان
        cursor.execute('''
            SELECT bc.id, bc.Level
            FROM building_city bc
            JOIN citytribe c ON c.id = bc.CityId
            WHERE c.ChatId = %s AND bc.BuildingId = %s
        ''', (chat_id, build_id))
        build_level = cursor.fetchall()

        if not build_level:
            first = True
            level = 1
        else:
            first = False
            level = build_level[0][1] + 1
            if build_level[0][1] >= 50:
                return 'شما حداکثر سطح موجود را بدست آوردید', True

        # دریافت دارایی‌های شهر
        cursor.execute('''
            SELECT pc.PropertyId, pc.Amount
            FROM property_city pc
            JOIN citytribe c ON c.id = pc.CityId
            WHERE c.ChatId = %s
        ''', (chat_id,))
        property_rows = cursor.fetchall()
        property_dict = {item[0]: item[1] for item in property_rows}

        updates = []

        # اگر ساختمان خاص بود
        if build_id in (13, 14, 18):
            costs = get_specil_build_cost_make(build_id, level)
            if not costs:
                return "هزینه‌ای برای این سطح تعریف نشده است.", False

            for resource_id, required_amount in costs.items():
                available_amount = property_dict.get(int(resource_id), 0)
                if available_amount < required_amount:
                    return f' {resource_id} به اندازه کافی موجود نیست. نیاز: {required_amount} موجودی: {available_amount}', True
                updates.append((required_amount, chat_id, int(resource_id)))

        else:  # سایر ساختمان‌ها طبق دیتابیس
            cursor.execute('''
                SELECT bc.InitialValue, bc.SecondValue, r.Id
                FROM building_cost bc
                JOIN property r ON r.Id = bc.PropertyId
                WHERE bc.BuildingId = %s
            ''', (build_id,))
            cost_build = cursor.fetchall()

            for initial_value, second_value, resource_id in cost_build:
                available_amount = property_dict.get(resource_id, 0)
                required_amount = initial_value + level * second_value
                if available_amount < required_amount:
                    return f' منبع {resource_id} کافی نیست. نیاز: {required_amount} موجودی: {available_amount}', True
                updates.append((required_amount, chat_id, resource_id))

        # به‌روزرسانی منابع
        update_query = '''
            UPDATE property_city 
            SET Amount = Amount - %s
            WHERE CityId = (SELECT Id FROM citytribe WHERE ChatId = %s)
            AND PropertyId = %s
        '''
        for required_amount, chat_id, resource_id in updates:
            cursor.execute(update_query, (required_amount, chat_id, resource_id))

        # ثبت یا ارتقا ساختمان
        if first:
            cursor.execute("SELECT Id FROM citytribe WHERE ChatId = %s", (chat_id,))
            city_id = cursor.fetchall()[0][0]
            cursor.execute("INSERT INTO building_city (BuildingId, CityId, Level) VALUES (%s, %s, 1)", (build_id, city_id))
        else:
            cursor.execute('''
                UPDATE building_city
                SET Level = Level +1
                WHERE BuildingId = %s AND CityId = (SELECT Id FROM citytribe WHERE ChatId = %s)
            ''', (build_id, chat_id))

        mydb.commit()
        return f'ساختمان {build_title[0]} با موفقیت ارتقا یافت', True

    except Exception as e:
        mydb.rollback()
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

def get_multiple_cost(build_id, chat_id, level):
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        # دریافت لول فعلی ساختمان
        cursor.execute('''
            SELECT bc.Level
            FROM building_city bc
            JOIN citytribe c ON c.id = bc.CityId
            WHERE c.ChatId = %s AND bc.BuildingId = %s
        ''', (chat_id, build_id))
        build_level = cursor.fetchone()

        if not build_level:
            current_level = 0
        else:
            current_level = build_level[0]
        target_level = current_level + level

        # اگر ساختمان معمولی بود (طبق جدول building_cost)
        cursor.execute('''
            SELECT bc.InitialValue, bc.SecondValue, r.Title
            FROM building_cost bc
            JOIN property r ON r.Id = bc.PropertyId
            WHERE bc.BuildingId = %s
        ''', (build_id,))
        cost_build = cursor.fetchall()

        total_costs = {}
        for lvl in range(current_level + 1, target_level + 1):
            for initial_value, second_value, res_title in cost_build:
                required = initial_value + (second_value * lvl)
                total_costs[res_title] = total_costs.get(res_title, 0) + required

        property_text = f"\nهزینه ارتقا از لول {current_level} به {target_level}:"
        for res, val in total_costs.items():
            property_text += f"\n {res} : {val}"
        property_text += "\n\nآیا از ارتقای خود اطمینان دارید؟"

        cursor.close()
        mydb.close()

        return property_text, True

    except Exception as e:
        return str(e), False
def get_confirm_multiple_cost(build_id, chat_id, level):
    try:
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()
        mydb.start_transaction()

        # دریافت عنوان ساختمان
        cursor.execute("SELECT Title FROM building WHERE Id = %s", (build_id,))
        build_title = cursor.fetchone()

        # دریافت سطح ساختمان فعلی
        cursor.execute('''
            SELECT bc.Level
            FROM building_city bc
            JOIN citytribe c ON c.id = bc.CityId
            WHERE c.ChatId = %s AND bc.BuildingId = %s
        ''', (chat_id, build_id))
        build_level = cursor.fetchone()

        if not build_level:
            current_level = 0
            first = True
        else:
            current_level = build_level[0]
            first = False
        target_level = current_level + level
        if target_level > 50:
            return "بیشتر از لول 50 امکان‌پذیر نیست.", False

        # دریافت دارایی‌های شهر
        cursor.execute('''
            SELECT pc.PropertyId, pc.Amount
            FROM property_city pc
            JOIN citytribe c ON c.id = pc.CityId
            WHERE c.ChatId = %s
        ''', (chat_id,))
        property_rows = cursor.fetchall()
        property_dict = {item[0]: item[1] for item in property_rows}

        # محاسبه هزینه کل
        total_costs = {}

        if build_id in (13, 14, 18):  # ساختمان‌های خاص
            for lvl in range(current_level + 1, target_level + 1):
                costs = get_specil_build_cost_make(build_id, lvl)
                if not costs:
                    return f"برای سطح {lvl} هزینه تعریف نشده است.", False
                for res_id, amount in costs.items():
                    total_costs[res_id] = total_costs.get(res_id, 0) + amount
        else:  # ساختمان‌های معمولی
            cursor.execute('''
                SELECT bc.InitialValue, bc.SecondValue, r.Id
                FROM building_cost bc
                JOIN property r ON r.Id = bc.PropertyId
                WHERE bc.BuildingId = %s
            ''', (build_id,))
            cost_build = cursor.fetchall()

            for lvl in range(current_level + 1, target_level + 1):
                for initial_value, second_value, res_id in cost_build:
                    required_amount = initial_value + (second_value * lvl)
                    total_costs[res_id] = total_costs.get(res_id, 0) + required_amount

        # بررسی منابع
        for res_id, total_required in total_costs.items():
            available_amount = property_dict.get(res_id, 0)
            if available_amount < total_required:
                return f'منبع {res_id} کافی نیست. نیاز: {total_required} موجودی: {available_amount}', True

        # کم کردن منابع
        update_query = '''
            UPDATE property_city 
            SET Amount = Amount - %s
            WHERE CityId = (SELECT Id FROM citytribe WHERE ChatId = %s)
            AND PropertyId = %s
        '''
        for res_id, total_required in total_costs.items():
            cursor.execute(update_query, (total_required, chat_id, res_id))

        # ثبت یا ارتقا ساختمان
        if first:
            cursor.execute("SELECT Id FROM citytribe WHERE ChatId = %s", (chat_id,))
            city_id = cursor.fetchall()[0][0]
            cursor.execute(
                "INSERT INTO building_city (BuildingId, CityId, Level) VALUES (%s, %s, %s)",
                (build_id, city_id, target_level)
            )
        else:
            cursor.execute('''
                UPDATE building_city
                SET Level = %s
                WHERE BuildingId = %s AND CityId = (SELECT Id FROM citytribe WHERE ChatId = %s)
            ''', (target_level, build_id, chat_id))

        mydb.commit()
        return f'ساختمان {build_title[0]} با موفقیت از سطح {current_level} به سطح {target_level} ارتقا یافت', True

    except Exception as e:
        mydb.rollback()
        return str(e), False
    finally:
        cursor.close()
        mydb.close()


