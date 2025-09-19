import mysql.connector
import config

#region دیتابیس ها
def creat_city():
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        CityTribe_query = '''
                    CREATE TABLE IF NOT EXISTS citytribe (
                        Id INT AUTO_INCREMENT PRIMARY KEY,
                        Title VARCHAR(100) NOT NULL,
                        Family VARCHAR(100) NULL,
                        ParentId INT NULL,
                        ChatId BIGINT NOT NULL,
                        Trade BOOLEAN NULL,
                        FOREIGN KEY (ParentId) REFERENCES citytribe(Id) ON DELETE SET NULL
                    )
                '''
        cursor.execute(CityTribe_query)

        mydb.commit()
        print("Table CityTribe created successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        mydb.close()
# creat_city()

def create_resource():
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
            resource_query = '''
                CREATE TABLE IF NOT EXISTS property (
                    Id INT AUTO_INCREMENT PRIMARY KEY,
                    Title VARCHAR(100) NOT NULL,
                    orderItem INT,
                    type TINYINT,
                    IsBasice TINYINT NULL
                )CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;
            '''
            cursor.execute(resource_query)

            mydb.commit()
            print("Table resource created successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

        try:
            building_query = '''
                CREATE TABLE IF NOT EXISTS building (
                    Id INT AUTO_INCREMENT PRIMARY KEY,
                    Title VARCHAR(100) NOT NULL,
                    MaxLevel INT,
                    OrderItem INT,
                    type TINYINT,
                    IsBasice TINYINT NULL
                )CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;
            '''
            cursor.execute(building_query)

            mydb.commit()
            print("Table building created successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        try:
            property_city_query = '''
                CREATE TABLE IF NOT EXISTS property_city (
                    Id INT AUTO_INCREMENT PRIMARY KEY,
                    CityId INT NOT NULL,
                    PropertyId INT NOT NULL,
                    Amount INT,
                    FOREIGN KEY (CityId) REFERENCES citytribe(Id),
                    FOREIGN KEY (PropertyId) REFERENCES property(Id),
                    UNIQUE (PropertyId, CityId)
                )
            '''
            cursor.execute(property_city_query)

            mydb.commit()
            print("Table property_city created successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        try:
            building_city_query = '''
                CREATE TABLE IF NOT EXISTS building_city (
                    Id INT AUTO_INCREMENT PRIMARY KEY,
                    CityId INT NOT NULL,
                    BuildingId INT NOT NULL,
                    Level INT,
                    FOREIGN KEY (CityId) REFERENCES citytribe(Id),
                    FOREIGN KEY (BuildingId) REFERENCES building(Id),
                    UNIQUE (CityId, BuildingId)
                )
            '''
            cursor.execute(building_city_query)

            mydb.commit()
            print("Table resource created successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

        try:
            CityTribe_query = '''
                        CREATE TABLE IF NOT EXISTS building_cost (
                            Id INT AUTO_INCREMENT PRIMARY KEY,
                            BuildingId INT NOT NULL,
                            PropertyId INT NOT NULL,
                            InitialValue SMALLINT,
                            SecondValue SMALLINT,
                            FOREIGN KEY (BuildingId) REFERENCES building(Id),
                            FOREIGN KEY (PropertyId) REFERENCES property(Id)
                        )
                    '''
            cursor.execute(CityTribe_query)

            mydb.commit()
            print("Table resource created successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

        try:
            profit_building_query = '''
                       CREATE TABLE IF NOT EXISTS profit_building (
                           Id INT AUTO_INCREMENT PRIMARY KEY,
                           BuildingId INT NOT NULL,
                           PrimaryProperty INT,
                           PropertyId INT,
                           FOREIGN KEY (PropertyId) REFERENCES property(Id),
                           FOREIGN KEY (BuildingId) REFERENCES building(Id)
                       )
                   '''
            cursor.execute(profit_building_query)

            mydb.commit()
            print("Table resource created successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    finally:
        cursor.close()
        mydb.close()

# create_resource()

def create_user():
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        CityTribe_query = '''
            CREATE TABLE IF NOT EXISTS userdata (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                ChatId INT NOT NULL
            )CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;
        '''

        cursor.execute(CityTribe_query)

        mydb.commit()
        print("Table CityTribe created successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        mydb.close()
# create_user()

def creat_dragon():
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        dragon_query = '''
                    CREATE TABLE IF NOT EXISTS dragon (
                        Id INT AUTO_INCREMENT PRIMARY KEY,
                        Title VARCHAR(100) NOT NULL,
                        Family VARCHAR(100) NULL,
                        ChatId BIGINT NOT NULL
                    )CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;
                '''
        cursor.execute(dragon_query)

        mydb.commit()
        print("Table CityTribe created successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        mydb.close()
# creat_dragon()
def create_user():
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        CityTribe_query = '''
            CREATE TABLE IF NOT EXISTS userdata (
                Id INT AUTO_INCREMENT PRIMARY KEY,
                ChatId INT NOT NULL
            )
        '''

        cursor.execute(CityTribe_query)

        mydb.commit()
        print("Table CityTribe created successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        mydb.close()
# create_user()
def creat_double_property():
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        CityTribe_query = '''
                    CREATE TABLE IF NOT EXISTS double_property (
                        Id INT AUTO_INCREMENT PRIMARY KEY,
                        CityId INT NULL,
                        BuildingId INT NULL,
                        FOREIGN KEY (CityId) REFERENCES citytribe(Id) ON DELETE SET NULL,
                        FOREIGN KEY (BuildingId) REFERENCES building(Id) ON DELETE SET NULL
                    )
                '''
        cursor.execute(CityTribe_query)

        mydb.commit()
        print("Table CityTribe created successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        mydb.close()
# creat_double_property()
#endregion

#region دیتا
data_city = [
    (1, "North", None, None),
    (2, "Vale", None, None),
    (3, "RiverLands", None, None),
    (4, "IronIslands", None, None),
    (5, "CrownLands", None, None),
    (6, "StormLands", None, None),
    (7, "Reach", None, None),
    (8, "WesterLands", None, None),
    (9, "Dorne", None, None),
    (10, "FreeCities", None, None),
    (11, "Winterfell", 1, "Stark"),
    (12, "The_Deardfort", 1, "Bolton"),
    (13, "Oldcastle", 1, "locke"),
    (14, "White_Harbor", 1, "Manderly"),
    (15, "Bear_island", 1, "Mormont"),
    (16, "The_Eyrie", 2, "Arryn"),
    (17, "Runestone", 2, "Royce"),
    (18, "Gulltown", 2, "Grafton"),
    (19, "Redfort", 2, "Redfort"),
    (20, "Strongsong", 2, "Belmore"),
    (21, "Riverrun", 3, "Tully"),
    (22, "Twins", 3, "Ferry"),
    (23, "Raventree_hall", 3, "Blackwood"),
    (24, "Harenhall", 3, "Strong"),
    (25, "Seagard", 3, "Mallister"),
    (26, "Pyke", 4, "Greyjoy"),
    (27, "Ten_Towers", 4, "Halaw"),
    (28, "Hammerhorn", 4, "Goodbrothers"),
    (29, "Great_Wyk", 4, "Sparr"),
    (30, "Blacktyde", 4, "Blacktyde"),
    (31, "Duskendale", 5, "Rykker"),
    (32, "Stonedance", 5, "Massey"),
    (33, "Sharp_point", 5, "BarEmmon"),
    (34, "Rooks_Rest", 5, "Staunton"),
    (35, "Antlers", 5, "Buckwell"),
    (36, "Storms_End", 6, "Baratheon"),
    (37, "Evenfall_Hall", 6, "Tarth"),
    (38, "Blackhaven", 6, "Dondarrion"),
    (39, "Grifinsroost", 6, "Connington"),
    (40, "Bronzegate", 6, "Buckler"),
    (41, "Highgarden", 7, "Tyrell"),
    (42, "Goldengrove", 7, "Rowan"),
    (43, "Oldtown", 7, "Hightower"),
    (44, "Old_Oak", 7, "Oakheart"),
    (45, "Redwyne", 7, "Arbor"),
    (46, "Casterly Rock", 8, "Lannister"),
    (47, "Ashemark", 8, "Marbrand"),
    (48, "Deep_Den", 8, "Lydedn"),
    (49, "Golden_Tooth", 8, "Lefford"),
    (50, "Silverhall", 8, "Serrett"),
    (51, "Sunspear", 9, "Martell"),
    (52, "Ghost_Hill", 9, "Toland"),
    (53, "Starfall", 9, "Dayne"),
    (54, "Kingsgrave", 9, "Manwood"),
    (55, "Blackmont", 9, "Blackmont"),
    (56, "Braavose", 10, "ESSOS"),
    (57, "Tyrosh", 10, "ESSOS"),
    (58, "Myr", 10, "ESSOS"),
    (59, "Lys", 10, "ESSOS"),
    (60, "Pentos", 10, "ESSOS"),
]
data_property = [
    (1, "محبوبیت", 1, 0),
    (2, "روحیه", 2, 0),
    (3, "سکه", 3, 1),
    (4, "چوب", 4, 1),
    (5, "سنگ", 5, 1),
    (6, "آهن", 6, 1),
    (7, "ماهی", 7, 1),
    (8, "گوشت", 8, 1),
    (9, "شراب", 9, 1),
    (10, "گندم", 10, 1),
    (11, "شمشیرزن", 11, 2),
    (12, "کماندار", 12, 2),
    (13, "نیزه دار", 13, 2),
    (14, "سواره", 14, 2),
    (15, "کشتی چوبی", 15, 3),
    (16, "کشتی جنگی", 16, 3),
    (17, "نرده بان", 17, 4),
    (18, "دژکوب", 18, 4),
    (19, "اسکورپ", 19, 4),
    (20, "منجنیق", 20, 4),
    (21, "برج محاصره", 21, 4),
    (22, "نیروی ویژه", 22, 2),
    (23, "میوه", 10, 1),

]
data_building = [
    (1, "خزانه", 1, 1),
    (2, "چوب بری", 2, 1),
    (3, "معدن سنگ", 3, 1),
    (4, "معدن آهن", 4, 1),
    (5, "تاکستان", 5, 1),
    (6, "میوه", 6, 1),
    (7, "دامداری", 7, 1),
    (8, "ماهیگیری", 8, 1),
    (9, "کمپ شمشیرزن", 9, 2),
    (10, "کمپ کماندار", 10, 2),
    (11, "کمپ نیزه دار", 11, 2),
    (12, "کمپ سواره", 12, 2),
    (13, "کشتی سازی", 14, 3),
    (14, "کاراگاه ادوات", 15, 4),
    (15, "کمپ نیروی ویژه", 13, 2),
]
data_cost_building = [
    (1, 3, 900, 100),
    (1, 4, 90, 10),
    (1, 5, 90, 10),
    (2, 3, 400, 100),
    (2, 5, 160, 40),
    (3, 3, 400, 100),
    (3, 4, 160, 40),
    (4, 3, 200, 50),
    (4, 4, 80, 20),
    (4, 5, 80, 20),
    (6, 3, 450, 50),
    (6, 4, 45, 5),
    (6, 5, 45, 5),
    (7, 3, 1350, 150),
    (7, 5, 135, 15),
    (8, 3, 900, 100),
    (8, 4, 90, 10),
    (9, 3, 500, 500),
    (9, 5, 125, 125),
    (9, 6, 125, 125),
    (10, 3, 500, 500),
    (10, 4, 125, 125),
    (10, 5, 125, 125),
    (11, 3, 500, 500),
    (11, 4, 125, 125),
    (11, 6, 125, 125),
    (12, 3, 750, 750),
    (12, 4, 75, 75),
    (12, 5, 75, 75),
    (12, 6, 75, 75),
    (15, 3, 1000, 1000),
    (15, 4, 100, 100),
    (15, 5, 100, 100),
    (15, 6, 100, 100),
    (13, 3, 600, 200),
    (13, 4, 150, 50),
    (13, 5, 150, 50),
    (13, 6, 150, 50),
    (14, 3, 0, 400),
    (14, 4, 0, 100),
    (14, 5, 0, 100),
    (14, 6, 0, 100),
]
data_profit_building = [
    (1, 3, 2000),
    (2, 4, 500),
    (3, 5, 500),
    (4, 6, 500),
    (5, 9, 50),
    (6, 10, 100),
    (7, 8, 100),
    (8, 7, 100),
    (9, 11, 50),
    (10, 12, 50),
    (11, 13, 50),
    (12, 14, 50),
    (15, 22, 50),
]
resources = [
    (None, 3, 4000), (None, 2, 50), (None, 1, 50),
    (None, 4, 500), (None, 5, 500), (None, 6, 500),
    (None, 10, 1000), (None, 11, 100), (None, 12, 100),
    (None, 13, 100), (None, 14, 100), (None, 22, 100),
    (None, 15, 5), (None, 16, 5), (None, 17, 4),
    (None, 18, 2), (None, 20, 1)
]
buildings = [1, 2, 3, 6, 9]
data_dragon = [
    (1, "شیپ استیلر"),
    (2, "سایرکس"),
    (3, "کراکسیس"),
    (4, "میلیس"),
    (5, "ورمیثور"),
    (6, "ورمکس"),
    (7, "سانفایر"),
    (8, "ویگار"),
    (9, "سیلوروینگ"),
    (10, "سی اسموک"),
    (11, "دریم فایر"),
    (12, "تساریون"),
    (13, "گری گوست"),
]
#endregion

#region insert_query

def insert_data_city(data_list):
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        # کوئری برای وارد کردن داده‌ها به جدول CityTribe
        insert_query = '''
            INSERT INTO citytribe (Id, Title, ParentId, ChatId, Family, Trade)
            VALUES (%s, %s, %s, 0, %s, 0)
        '''

        # اجرای کوئری برای داده‌های متعدد
        cursor.executemany(insert_query, data_list)

        # تأیید تغییرات در دیتابیس
        mydb.commit()
        print(f"{cursor.rowcount} record(s) inserted.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # بستن ارتباط با دیتابیس
        cursor.close()
        mydb.close()

def insert_data_property(data_list):
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        # کوئری برای وارد کردن داده‌ها به جدول resource
        insert_query = '''
            INSERT INTO property (Id, Title, OrderItem, type, IsBasice)
            VALUES (%s, %s, %s, %s, 0)
        '''

        # اجرای کوئری برای داده‌های متعدد
        cursor.executemany(insert_query, data_list)

        # تأیید تغییرات در دیتابیس
        mydb.commit()
        print(f"{cursor.rowcount} record(s) inserted.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # بستن ارتباط با دیتابیس
        cursor.close()
        mydb.close()

def insert_data_building(data_list):
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        # کوئری برای وارد کردن داده‌ها به جدول building
        insert_query = '''
            INSERT INTO building (Id, Title, MaxLevel, OrderItem, type)
            VALUES (%s, %s, 100, %s, %s)
        '''

        # اجرای کوئری برای داده‌های متعدد
        cursor.executemany(insert_query, data_list)

        # تأیید تغییرات در دیتابیس
        mydb.commit()
        print(f"{cursor.rowcount} record(s) inserted.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # بستن ارتباط با دیتابیس
        cursor.close()
        mydb.close()

def insert_data_cost_building(data_list):
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        # کوئری برای وارد کردن داده‌ها به جدول building_cost
        insert_query = '''
            INSERT INTO building_cost (BuildingId, PropertyId, InitialValue, SecondValue)
            VALUES (%s, %s, %s, %s)
        '''

        # اجرای کوئری برای داده‌های متعدد
        cursor.executemany(insert_query, data_list)

        # تأیید تغییرات در دیتابیس
        mydb.commit()
        print(f"{cursor.rowcount} record(s) inserted.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # بستن ارتباط با دیتابیس
        cursor.close()
        mydb.close()

def insert_data_profit_building(data_list):
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        # کوئری برای وارد کردن داده‌ها به جدول profit_building
        insert_query = '''
            INSERT INTO profit_building (BuildingId, PropertyId, PrimaryProperty)
            VALUES (%s, %s, %s)
        '''

        # اجرای کوئری برای داده‌های متعدد
        cursor.executemany(insert_query, data_list)

        # تأیید تغییرات در دیتابیس
        mydb.commit()
        print(f"{cursor.rowcount} record(s) inserted.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # بستن ارتباط با دیتابیس
        cursor.close()
        mydb.close()

def insert_data_base_resource(resources, buildings):
    try:
        with mysql.connector.connect(
                host=config.host,
                user=config.user,
                password=config.password,
                database=config.database
        ) as mydb:
            with mydb.cursor() as cursor:

                # خالی کردن جداول
                cursor.execute("TRUNCATE TABLE property_city")
                cursor.execute("TRUNCATE TABLE building_city")

                # جستجوی شهرهای دارای ParentId
                tribe_query = '''
                    SELECT Id
                    FROM citytribe
                    WHERE ParentId IS NOT NULL
                '''
                cursor.execute(tribe_query)
                result = cursor.fetchall()

                if not result:
                    print("هیچ شهری با ParentId موجود نیست.")
                    return

                for city in result:
                    city_id = city[0]

                    # درج منابع در جدول property_city
                    insert_resource = '''
                        INSERT INTO property_city (CityId, PropertyId, Amount)
                        VALUES (%s, %s, %s)
                    '''
                    city_resources = [(city_id, resource[1], resource[2]) for resource in resources]
                    cursor.executemany(insert_resource, city_resources)

                    # درج ساختمان‌ها در جدول building_city
                    insert_building = '''
                        INSERT INTO building_city (CityId, BuildingId, Level)
                        VALUES (%s, %s, 1)
                    '''
                    city_buildings = [(city_id, building) for building in buildings]
                    cursor.executemany(insert_building, city_buildings)

                # تأیید نهایی عملیات در دیتابیس
                mydb.commit()
                print(f"{cursor.rowcount} record(s) inserted.")

    except mysql.connector.Error as err:
        print(f"خطای دیتابیس: {err}")

def insert_data_dragon(data_list):
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        # کوئری برای وارد کردن داده‌ها به جدول CityTribe
        insert_query = '''
            INSERT INTO dragon (Id,Title, ChatId)
            VALUES (%s, %s, 0)
        '''

        # اجرای کوئری برای داده‌های متعدد
        cursor.executemany(insert_query, data_list)

        # تأیید تغییرات در دیتابیس
        mydb.commit()
        print(f"{cursor.rowcount} record(s) inserted.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # بستن ارتباط با دیتابیس
        cursor.close()
        mydb.close()
#endregion

#region insert
# insert_data_city(data_city)
# insert_data_property(data_property)
# insert_data_building(data_building)
# insert_data_cost_building(data_cost_building)
# insert_data_profit_building(data_profit_building)
# insert_data_base_resource(resources, buildings)
# insert_data_dragon(data_dragon)
#endregion

#region save_data

def save_city(text,chat_id):
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
            # کوئری برای وارد کردن داده‌ها به جدول CityTribe
            city_query = '''
                         SELECT ChatId,Id
                         FROM citytribe
                         WHERE LOWER(Title) = LOWER(%s)
                         '''

            cursor.execute(city_query, (text,))
            city = cursor.fetchone()
            if city is None:
                return 'شهر یافت نشد'

        except mysql.connector.Error as err:
            return "خطا در پیدا کردن شهر"
        try:
            insert_query = '''
                UPDATE citytribe set ChatId = %s where Id = %s
            '''

            # اجرای کوئری
            cursor.execute(insert_query, (chat_id, city[1]))

            # تأیید تغییرات در دیتابیس
            mydb.commit()
        except mysql.connector.Error as err:
            print(err)
            return "خطا در تغییر ChatId"
        return "عملیات با موفقیت انجام شد"
    except mysql.connector.Error as err:
        return "خطای دیتابیس"
    finally:
        # بستن ارتباط با دیتابیس
        cursor.close()
        mydb.close()


def save_user(chat_id):
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()

        # کوئری درج داده‌ها
        insert_query = '''
            INSERT INTO userdata (ChatId)
            VALUES (%s)
        '''
        # اجرای کوئری با داده‌های ورودی
        cursor.execute(insert_query, (chat_id,))

        # اعمال تغییرات
        mydb.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        pass
    finally:
        if cursor:
            cursor.close()
        if mydb:
            mydb.close()

#endregion

def add_city_database(parent_id, city,family):
    try:
        # اتصال به دیتابیس
        mydb = mysql.connector.connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = mydb.cursor()
        print(parent_id, city, family)
        # کوئری برای وارد کردن داده‌ها به جدول CityTribe
        insert_query = '''
            INSERT INTO citytribe (Title, ParentId, ChatId,Family,Trade)
            VALUES (%s, %s, 0,%s,0)
        '''

        # اجرای کوئری
        cursor.execute(insert_query, (city,parent_id, family))

        # تأیید تغییرات در دیتابیس
        mydb.commit()
        return "شهر با موفقیت ایجاد شد"

    except mysql.connector.Error as err:
        return 'خطایی رخ داده است'

    finally:
        # بستن ارتباط با دیتابیس
        cursor.close()
        mydb.close()