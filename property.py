import mysql.connector
import config

image_property = {
    1: "🔮",
    2: "💪",
    3: "💰⊰",
    4: "🪵⊰",
    5: "🧱⊰",
    6: "🔩⊰",
    7: "🐠⊰",
    8: "🥩⊰",
    9: "🍷⊰",
    23: "🍏⊰",

    10: " 🍏⊰",
    11: "『⚔️』",
    12: "『🏹』",
    13: "『🔱』",
    14: "『🏇』",
    15: "『⛵️』",
    16: "『🛳』",
    17: "『🪜』",
    18: "『🚄』",
    19: "『🎯』",
    20: "『☄️』",
    21: "『🗼』",
    22: "『🪓』",
    24: "『🛳』",
    25: "『🛳』",
    26: "『🛳』",

}
image_production = {1: "🏦⊰",
    2: "🌳⊰",
    3: "⛰⊰",
    4: "🌋⊰",
    5: "🛕⊰",
    6: "🧑‍🌾⊰",
    7: "🐄⊰",
    8: "🎣⊰",
    9: "『⚔️』",
    10: "『🏹』",
    11: "『🔱』",
    12: "『🏇』",
    13: " ⚓️",
    14: "[🏭]",
    15: "『🩸』"   }
def get_property(chat_id, name):
    try:
        with mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database) as mydb:
            cursor = mydb.cursor()

            # دریافت اطلاعات قلعه و خاندان
            cursor.execute('''
                SELECT c.Title, c.Family, c.Id,c.ParentId
                FROM citytribe c
                WHERE c.ChatId = %s
            ''', (chat_id,))
            city_info = cursor.fetchone()
            if not city_info:
                return "⚠️ قلعه‌ای برای این کاربر یافت نشد.", False

            city_name, city_family, city_id, city_parent = city_info

            # دریافت دارایی‌های شهر
            cursor.execute('''
                SELECT r.Id, r.Title, r.type, COALESCE(pc.Amount, 0) AS Amount
                FROM property r
                LEFT JOIN property_city pc ON pc.CityId = %s AND pc.PropertyId = r.Id
                WHERE r.IsBasice = 0 OR pc.PropertyId IS NOT NULL
                ORDER BY r.type, r.OrderItem
            ''', (city_id,))
            properties = cursor.fetchall()

            # دریافت اطلاعات ساختمان‌ها و بازدهی
            cursor.execute('''
                SELECT b.Id, b.Title, COALESCE(bc.Level, 0) AS Level, b.type,
                       COALESCE(pb.PrimaryProperty * bc.Level, 0) AS Profit
                FROM building b
                LEFT JOIN building_city bc ON bc.BuildingId = b.Id AND bc.CityId = %s
                LEFT JOIN profit_building pb ON pb.BuildingId = b.Id
                ORDER BY b.type, b.OrderItem
            ''', (city_id,))
            buildings = cursor.fetchall()

            # دریافت ساختمان‌هایی که بازدهی دوبرابر دارند
            cursor.execute('''
                SELECT BuildingId FROM double_property WHERE CityId = %s
            ''', (city_parent,))
            double_property_ids = {row[0] for row in cursor.fetchall()}

        # ساخت خروجی نهایی
        property_text = (
            f'🧬 خاندان: ⊰ {city_family}\n'
            f'🏰 قلعه : ⊰ {city_name}\n'
            f'👑 لرد : ⊰ {name}\n\n'
            '💎 **دارایی‌ها:**\n'
        )

        current_type = None
        for prop_id, title, prop_type, amount in properties:
            if current_type != prop_type:
                current_type = prop_type
                property_text += "\n"
            image = image_property.get(prop_id)
            property_text += f'{image} {title} ⊱ {amount}\n'

        property_text += "\n🏗 **ساختمان‌ها:**\n"
        current_building_type = None
        for b_id, b_title, level, b_type, profit in buildings:
            if current_building_type != b_type:
                current_building_type = b_type
                property_text += "\n"
            image = image_production.get(b_id)
            profit_display = f"[{int(profit * 1.5)}] ⭐" if b_id in double_property_ids else (f"[{profit}]" if profit else "")
            property_text += f'{image} {b_title} ⊱ {level} {profit_display}\n'

        return property_text, True

    except Exception as e:
        print(e)
        return f"⚠️ خطا: {e}", False


def get_product():
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
            resource_query = f'''
                             SELECT Title, Id
                             FROM property
                             WHERE type = 1
                             '''
            cursor.execute(resource_query)
            resource = cursor.fetchall()
        except mysql.connector.Error as err:
            return str(err), False
        cursor.close()
        mydb.close()
        return resource, True
    except mysql.connector.Error as err:
        return str(err), False

def get_product_detail(product_id):
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
            resource_query = f'''
                              SELECT Title, Id
                              FROM property
                              WHERE Id = %s
                              '''
            cursor.execute(resource_query, (product_id,))
            resource = cursor.fetchone()
            if resource is None:
                return 'محصول یافت نشد', False
        except mysql.connector.Error as err:
            return str(err), False
        cursor.close()
        mydb.close()
        return resource, True
    except mysql.connector.Error as err:
        return str(err), False

def get_trade(product_id,amount,city_id,chat_id):
    try:
        # اتصال به دیتابیس
        with mysql.connector.connect(
                host=config.host,
                user=config.user,
                password=config.password,
                database=config.database
        ) as mydb:
            cursor = mydb.cursor()
            # شروع ترنسکشن
            mydb.start_transaction()

            try:
                # بررسی موجودی در شهر مبدا
                property_query = '''
                       SELECT amount, Id
                       FROM property_city
                       WHERE CityId = (SELECT Id FROM citytribe WHERE ChatId = %s) AND PropertyId = %s
                   '''
                cursor.execute(property_query, (chat_id, product_id))
                property = cursor.fetchall()

                if not property:
                    return "دارایی مورد نیاز برای ارسال رو ندارید", True
                if len(property) > 1:  # به جای count() از len استفاده می‌کنیم
                    return "تجارت انجام نشد .دارایی شما دچار مشکل می باشد @mohammadtazar پیگیری کن ببین چه مشکلی دارد.", True
                property = property[0]

                if property[0] < amount:
                    return "تعداد دارایی شما کمتر از میزان ارسالی می باشد", True

                # کم کردن مقدار از شهر مبدا
                update_query_mabda = '''
                       UPDATE property_city 
                       SET Amount = Amount - %s 
                       WHERE Id = %s
                   '''
                cursor.execute(update_query_mabda, (amount, property[1]))

                # اضافه کردن مقدار به شهر مقصد
                property_destination_query = '''
                       SELECT amount
                       FROM property_city
                       WHERE PropertyId = %s AND CityId = %s
                   '''
                cursor.execute(property_destination_query, (product_id, city_id))
                property_destination = cursor.fetchall()

                if not property_destination:
                    # اگر کالا در شهر مقصد موجود نیست، اضافه شود
                    insert_query = '''
                           INSERT INTO property_city (CityId, PropertyId, Amount) 
                           VALUES (%s, %s, %s)
                       '''
                    cursor.execute(insert_query, (city_id, product_id, amount))

                else:
                    # اگر کالا در شهر مقصد موجود است، مقدار آن به‌روزرسانی شود
                    update_query_dest = '''
                           UPDATE property_city 
                           SET Amount = Amount + %s 
                           WHERE PropertyId = %s AND CityId = %s
                       '''
                    cursor.execute(update_query_dest, (amount, product_id, city_id))
                # تایید تغییرات در دیتابیس
                mydb.commit()
                return 'عملیات با موفقیت انجام شد', True

            except mysql.connector.Error as err:
                mydb.rollback()  # بازگشت به حالت قبل در صورت خطا
                return f"خطا: {str(err)}", False

    except mysql.connector.Error as err:
        mydb.rollback()
        return str(err), False

def get_all_resource():
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

def resource_add(chat_id, resource_id, counts):
    try:
        counts = int(counts)
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
            resource_id_query = '''
                        SELECT Title FROM property WHERE Id = %s
                        '''
            cursor.execute(resource_id_query, (resource_id,))
            resource = cursor.fetchone()
            city_id_query = '''
            SELECT Id FROM citytribe WHERE ChatId = %s
            '''
            cursor.execute(city_id_query, (chat_id,))
            result = cursor.fetchall()

            # بررسی اینکه آیا نتیجه‌ای برگشته یا خیر
            if not result:
                cursor.close()
                mydb.close()
                return "شهر مربوط به این کاربر یافت نشد", False

            city_id = result[0][0]

            property_city = '''
                SELECT pc.Id, pc.Amount
                FROM property_city pc
                WHERE pc.CityId = %s AND pc.PropertyId = %s
            '''
            cursor.execute(property_city, (city_id, resource_id))
            result = cursor.fetchall()

            if result:
                property = result[0]
                update_query = '''
                    UPDATE property_city
                    SET Amount = Amount + %s
                    WHERE Id = %s
                '''
                cursor.execute(update_query, (counts, property[0]))
            else:
                insert_query = '''
                    INSERT INTO property_city(CityId, PropertyId, Amount)
                    VALUES (%s, %s, %s)
                '''
                cursor.execute(insert_query, (city_id, resource_id, counts))

            mydb.commit()
            cursor.close()
            mydb.close()
            return f"مقدار {counts} {resource[0]} اضافه شد", True

        except mysql.connector.Error as err:
            return str(err), False

    except Exception as e:
        return str(e), False

def resource_costs(chat_id, resource_id, counts):
    try:
        counts = int(counts)
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        try:
            resource_id_query = '''
                                   SELECT Title FROM property WHERE Id = %s
                                   '''
            cursor.execute(resource_id_query, (resource_id,))
            resource = cursor.fetchone()
            # دریافت city_id
            city_id_query = '''
            SELECT Id FROM citytribe WHERE ChatId = %s
            '''
            cursor.execute(city_id_query, (chat_id,))
            result = cursor.fetchall()

            if not result:
                return "شهر مربوط به این کاربر یافت نشد", False

            city_id = result[0][0]

            # بررسی موجودی منبع
            property_city = '''
                SELECT Id, Amount
                FROM property_city
                WHERE CityId = %s AND PropertyId = %s
            '''
            cursor.execute(property_city, (city_id, resource_id))
            result = cursor.fetchall()

            if result:
                property_id, amount = result[0]
                if amount < counts:
                    return 'مقدار کافی از این منبع موجود نیست', False

                # به روزرسانی مقدار
                update_query = '''
                    UPDATE property_city
                    SET Amount = Amount - %s
                    WHERE Id = %s
                '''
                cursor.execute(update_query, (counts, property_id))
                mydb.commit()
                return f"مقدار {counts} از {resource[0]} کم شد", True
            else:
                return 'منبع مورد نظر در شهر موجود نیست', False

        except mysql.connector.Error as err:
            return f"خطای دیتابیس: {str(err)}", False

        finally:
            cursor.close()
            mydb.close()

    except Exception as e:
        return f"خطای سیستمی: {str(e)}", False

def promotion(chat_id, promotion_id):
    try:
        # اتصال به دیتابیس
        with mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        ) as mydb:
            with mydb.cursor() as cursor:

                # دریافت city_id برای کاربر
                city_id_query = '''
                    SELECT Id FROM citytribe WHERE ChatId = %s
                '''
                cursor.execute(city_id_query, (chat_id,))
                result = cursor.fetchall()

                # بررسی اینکه نتیجه‌ای برگشته یا نه
                if not result:
                    return "شهر مربوط به این کاربر یافت نشد", False

                city_id = result[0][0]

                # بررسی اینکه ساختمان برای این شهر وجود دارد یا نه
                property_resource  = '''
                    SELECT Id
                    FROM property_city
                    WHERE CityId = %s AND PropertyId = 1
                '''
                cursor.execute(property_resource, (city_id,))
                result = cursor.fetchall()

                if result:
                    return 'شهر دارای دارایی می‌باشد', False

                # کوئری‌های درج منابع و ساختمان‌ها
                insert_resource_query = '''
                    INSERT INTO property_city (CityId, PropertyId, Amount)
                    VALUES (%s, %s, %s)
                '''
                insert_building_query = '''
                    INSERT INTO building_city (CityId, BuildingId, Level)
                    VALUES (%s, %s, %s)
                '''

                # مقادیر منابع و ساختمان‌ها بر اساس promotion_id
                resources = []
                buildings = []

                if int(promotion_id) == 1:
                    resources = [
                        (city_id, 3, 14000), (city_id, 2, 60), (city_id, 1, 60),
                        (city_id, 4, 2500), (city_id, 5, 2500), (city_id, 6, 2500),
                        (city_id, 10, 250),(city_id, 7, 250),(city_id, 8, 250),(city_id, 9, 50),
                        (city_id, 11, 200), (city_id, 12, 200),
                        (city_id, 13, 200), (city_id, 14, 200), (city_id, 22, 200),
                        (city_id, 15, 10), (city_id, 16, 10),
                        (city_id, 17, 10),(city_id, 18, 5),(city_id, 19, 5),(city_id, 20, 5),
                        (city_id, 21, 1)
                    ]
                    buildings = [
                        (city_id, 1, 4), (city_id, 2, 4), (city_id, 3, 4),(city_id, 4, 4),
                        (city_id, 5, 3),(city_id, 6, 3),(city_id, 7, 3), (city_id, 8, 3),
                        (city_id, 9, 2), (city_id, 10, 2), (city_id, 11, 2), (city_id, 12, 2), (city_id, 15, 2)
                    ]
                elif int(promotion_id) == 3:
                    resources = [
                        (city_id, 1, 50), (city_id, 2, 50), (city_id, 3, 7000), (city_id, 4, 1000),
                        (city_id, 5, 1000), (city_id, 6, 1000), (city_id, 7, 150), (city_id, 8, 150), (city_id, 9, 50),
                        (city_id, 10, 150), (city_id, 11, 100), (city_id, 12, 100), (city_id, 13, 100),
                        (city_id, 14, 100), (city_id, 22, 100),
                        (city_id, 15, 4), (city_id, 16, 2), (city_id, 17, 4), (city_id, 18, 4),
                        (city_id, 20, 1)
                    ]
                    buildings = [
                        (city_id, 1, 2), (city_id, 2, 1), (city_id, 3, 1), (city_id, 4, 1), (city_id, 5, 1),
                        (city_id, 6, 1), (city_id, 7, 1), (city_id, 8, 1), (city_id, 9, 1), (city_id, 10, 1),
                        (city_id, 11, 1), (city_id, 12, 1), (city_id, 15, 1)
                    ]
                elif int(promotion_id) == 2:
                    resources = [
                        (city_id, 1, 60), (city_id, 2, 60), (city_id, 3, 14000), (city_id, 4, 2000),
                        (city_id, 5, 2000), (city_id, 6, 2000), (city_id, 7, 300), (city_id, 8, 300), (city_id, 9, 100),
                        (city_id, 10, 300), (city_id, 11, 200), (city_id, 12, 200), (city_id, 13, 200),
                        (city_id, 14, 150),(city_id, 22, 150),
                        (city_id, 15, 8), (city_id, 16, 8), (city_id, 17, 8), (city_id, 18, 6),
                        (city_id, 19, 1),
                        (city_id, 20, 3)
                    ]
                    buildings = [
                        (city_id, 1, 3), (city_id, 2, 2), (city_id, 3, 2), (city_id, 4, 2), (city_id, 5, 2),
                        (city_id, 6, 2), (city_id, 7, 2), (city_id, 8, 2), (city_id, 9, 2), (city_id, 10, 2),
                        (city_id, 11, 2), (city_id, 12, 1), (city_id, 15, 1)
                    ]
                elif int(promotion_id) == 4:
                    resources = [
                        (city_id, 3, 10000), (city_id, 2, 50),
                        (city_id, 4, 1000), (city_id, 5, 1000), (city_id, 6, 1000),(city_id, 7, 300),
                        (city_id, 11, 20), (city_id, 12, 20),
                        (city_id, 13, 20), (city_id, 14, 20), (city_id, 22, 20),
                        (city_id, 15, 5), (city_id, 16, 5), (city_id, 17, 2),
                        (city_id, 18, 2),
                        (city_id, 29, 20),(city_id, 30, 20),(city_id, 31, 20),(city_id, 32, 60),
                        (city_id, 33, 20),(city_id, 35, 200),
                    ]
                    buildings = [
                        (city_id, 1, 1), (city_id, 2, 1), (city_id, 3, 1), (city_id, 4, 1), (city_id, 7, 1),
                        (city_id, 8, 1), (city_id, 9, 1), (city_id, 10, 1), (city_id, 11, 1), (city_id, 12, 1),
                        (city_id, 13, 1), (city_id, 14, 1), (city_id, 15, 1), (city_id, 16, 1), (city_id, 17, 1)

                    ]

                # درج داده‌ها در دیتابیس
                if resources:
                    cursor.executemany(insert_resource_query, resources)
                if buildings:
                    cursor.executemany(insert_building_query, buildings)

                mydb.commit()
                return 'قلعه با موفقیت ارتقا یافت', True

    except mysql.connector.Error as err:
        return str(err), False

    except Exception as e:
        return str(e), False

def get_all_dragon():
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
                              FROM dragon
                              WHERE ChatId = 0
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

def get_add_dragon(dragon_id,chat_id):
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()
        print(1)
        try:
            tribe_query = f'''
                                SELECT ChatId
                                FROM dragon
                                WHERE Id = %s
                                '''
            cursor.execute(tribe_query,(dragon_id,))
            result = cursor.fetchone()
            if result[0] !=0:
                return 'اژدها قبلا به شهر تخصیص داده شده است'

            query = '''
            UPDATE dragon
            SET ChatId = %s
            WHERE Id = %s'''
            cursor.execute(query,(chat_id,dragon_id))
            mydb.commit()
            cursor.close()
            mydb.close()
            return 'با موفقیت اضافه شد'
        except mysql.connector.Error as err:
            return str(err)
    except Exception as e:
        return str(e)

def get_remove_property(chat_id):
    try:
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        try:
            city_query = '''
            SELECT Id FROM citytribe WHERE ChatId = %s'''
            cursor.execute(city_query, (chat_id,))
            city_id = cursor.fetchone()
            if city_id:
                city_id = city_id[0]
            else:
                return "شهر یافت نشد"

            remove_query = '''
            DELETE FROM property_city 
            WHERE CityId = %s'''
            cursor.execute(remove_query, (city_id,))
            remove_build_query = '''
            DELETE FROM building_city
            WHERE CityId = %s
            '''
            cursor.execute(remove_build_query, (city_id,))
            mydb.commit()
            return 'دارایی با موفقیت حذف شد'
        except mysql.connector.Error as err:
            return f"خطای دیتابیس: {str(err)}", False

        finally:
            cursor.close()
            mydb.close()

    except Exception as e:
        return f"خطای سیستمی: {str(e)}", False