# گیم آریا base
from telebot import types
import telebot
from threading import Thread
import time
#local
from city import (get_all_city,get_city_by_parent_id,get_campaign_confirm,get_city_by_chat_id,get_city_by_id,
                  get_my_dragon,get_dragon_by_id)
from property import (get_property,get_trade,get_product_detail,get_product,get_all_resource,resource_add,resource_costs
                    ,promotion,get_all_dragon,get_add_dragon,get_remove_property)
from building import (get_all_building_costs_and_profits,get_cost,get_confirm_cost,get_economic,get_military,get_all_building,
                      get_up_level,get_down_level)
from data_sql import save_city,save_user,add_city_database
from making import (get_all_ship,get_config_ship,get_cost_ship,get_cost_tools,get_all_tools,get_config_tools,get_all_army
                    ,get_cost_army,get_config_army)
from upgrate import cost_food,cost_casualties,get_negative_supply,get_resource_efficiency,get_up_city
admin_chat_id = '1889589121'
admin_chat_second_id ='6968676246'
admin_chat_tree_id = '0'
BOT_TOKEN = '7573605568:AAFAatB0133sDm5KkuK3Wxezxn6cipNdfGo'
campaign_chat_id = '-1002832253797'
bot = telebot.TeleBot(BOT_TOKEN)

campaign_messages={} # مقدار ارتش انتخابی
last_click_time = {}

file_id_dragon = {
    105: "AgACAgQAAxkBAAObZ3fIzBUI5ZZKryq_5UFiLhv4ruoAAjLDMRsBRcFTlwdGZx4DNSUBAAMCAAN4AAM2BA",
    106: "AgACAgQAAxkBAAIJI2d-EtF36h94FvYgP-JePeYDrSYqAAK7wjEb5KzxU13hHc-AAiv-AQADAgADeAADNgQ",

}

file_id_campaign = {
    105: "AgACAgQAAxkBAAM3aNGOQdepYKQZRjHO6EvaX4qECtkAAmPLMRtYGpBS_tcDd8FYzOABAAMCAAN5AAM2BA",
    106: "AgACAgQAAxkBAAM2aNGN6wr8WQn5OzFYz_rV_ya0vvsAAmHLMRtYGpBScOws-EbIu8MBAAMCAAN5AAM2BA",
}
file_id_naval_campaign = {
    105: "AgACAgQAAxkBAAM7aNLWxo6Vc_xaBZgtPTSVOYkLiU8AAo3IMRuzD5lSnWG8LNW0qFEBAAMCAAN4AAM2BA",
    106: "AgACAgQAAxkBAAM7aNLWxo6Vc_xaBZgtPTSVOYkLiU8AAo3IMRuzD5lSnWG8LNW0qFEBAAMCAAN4AAM2BA",

}
file_id_attack_naval_campaign = 'AgACAgQAAxkBAAM8aNLW32SoYkNI-ZpwfRsjIVxramAAAo7IMRuzD5lSqXVXMpMBKRMBAAMCAAN4AAM2BA'
file_id_siege = 'AgACAgQAAxkBAAM0aNGNKcSR4sF69uEJVm0EQJBeGrIAAlPLMRtYGpBS4SsxlugkQVkBAAMCAAN5AAM2BA'
file_id_attack = 'AgACAgQAAxkBAAM1aNGNf4xOTt_JNfn2fnpAju-stkMAAlXLMRtYGpBSH7QAAbiP81DGAQADAgADeQADNgQ'
group_chat_id = '@BloodyThrone_Main'
tweet_chat_id = '@BloodyThrone_Tweet'
admin_panel = '-4786037295'
def send_admin(text, error, user_id):
    try:
        bot.send_message(chat_id=admin_chat_id, text=f'مکان خطا :'
                                                     f'\n'
                                                     f'{text}'
                                                     f'\n'
                                                     f'{error} '
                                                     f'\n'
                                                     f' @{user_id}', parse_mode='Markdown')
    except Exception as e:
        pass
def is_spamming(user_id):
    current_time = time.time()
    if user_id in last_click_time:
        if current_time - last_click_time[user_id] < 1:  # فاصله زمانی 1 ثانیه
            return True
    last_click_time[user_id] = current_time
    return False
def run_in_thread(func, *args, **kwargs):
    thread = Thread(target=func, args=args, kwargs=kwargs)
    thread.start()

#region start
@bot.message_handler(func=lambda message: 'پنل' in message.text.lower())
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        if message.chat.type == "private":
            bot.send_message(message.chat.id, f'کونی تو اینجا چه گهی میخوری ')
            bot.send_message(admin_chat_id, f' {message.from_user.first_name} \n @{message.from_user.username} \n'
                                            f'قصد استارت روبات از داخل خود بات را داشت')
            save_user(message.chat.id)
            return
        markup = types.InlineKeyboardMarkup(row_width=2)
        row1 = [types.InlineKeyboardButton("🔀 لشکرکشی", callback_data="campaign_message")]
        row2 = [types.InlineKeyboardButton("🗡️ حمله", callback_data="attack_message"),
                types.InlineKeyboardButton("⚔️ محاصره", callback_data="siege_message")]
        row3 = [types.InlineKeyboardButton("ساخت نیرو", callback_data="make_message"),
                types.InlineKeyboardButton("📨 ارسال توئیت", callback_data="tweet_message")]
        row4 = [types.InlineKeyboardButton("📦 تجارت", callback_data="business_message")]
        row5 = [types.InlineKeyboardButton("🪙 دارایی", callback_data="property_message")]
        # row6 = [types.InlineKeyboardButton("حرکت اژدها", callback_data="dragon_message")]

        markup.add(*row1)
        markup.add(*row2)
        markup.add(*row3)
        markup.add(*row4)
        markup.add(*row5)
        # markup.add(*row6)
        bot.send_message(message.chat.id, "دستور خود را وارد کنید", reply_markup=markup)
    except Exception as e:
        bot.send_message(admin_chat_id, e)

#endregion

#region لشکر کشی
@bot.callback_query_handler(func=lambda call: call.data=="campaign_message")
def chose_send_type_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(chose_send_type, call)
def chose_send_type(call):
    try:
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        item1 = types.InlineKeyboardButton("⚓ دریایی", callback_data="campaign_type_2")
        item3 = types.InlineKeyboardButton("🐎 زمینی", callback_data="campaign_type_1")
        markup.add(item3, item1, item2)
        bot.edit_message_text('نوع لشکر کشی خود را انتخاب نمایید', chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=markup)
    except Exception as e:
        send_admin('chose_send_type', e, call.message.from_user.username)
@bot.callback_query_handler(func=lambda call: call.data.startswith("campaign_type_"))
def send_army_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(send_army, call)
def send_army(call):
    try:
        bot.answer_callback_query(call.id)

        data = call.data.split('_')
        campaign_type = data[2]

        bot.edit_message_text("ارتش خود را وارد نمایید : ", chat_id=call.message.chat.id,
                              message_id=call.message.message_id)
        bot.register_next_step_handler(call.message, lambda message : campaign_message(message, campaign_type))
    except Exception as e:
        send_admin('send_army', e, call.from_user.username)
def campaign_message(message,campaign_type):
    try:
        continent, status = get_all_city()
        if not status:
            try:
                bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, f' \n {e}پیام حذف نشد از لشکر کشی')
            bot.send_message(chat_id='1889589121', text=continent)
            send_welcome(message)
            return
        campaign_messages[message.chat.id] = {
            'text': message.text,
        }
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup_list = []
        for item in continent:
            markup_list.append(
                types.InlineKeyboardButton(text=item[1], callback_data=f'send_continent_{item[0]}_{campaign_type}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        item1 = types.InlineKeyboardButton("سایر", callback_data=f"desired_campaign_{campaign_type}")
        markup.add(*markup_list, item1, item2)

        bot.send_message(chat_id=message.chat.id, text='مبدا حرکتی خود را انتخاب کنید', reply_markup=markup)
    except Exception as e:
        send_admin('campaign_message', e, message.from_user.username)
@bot.callback_query_handler(func=lambda call: call.data.startswith("send_continent_"))
def chose_send_city_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(chose_send_city, call)
def chose_send_city(call):
    try:
        bot.answer_callback_query(call.id)

        data = call.data.split('_')
        parent_id = data[2]
        campaign_type = data[3]
        city, status = get_city_by_parent_id(parent_id)
        if not status:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از لشکر کشی')
            bot.send_message(chat_id='1889589121', text=city)
            send_welcome(call.message)
            return

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup_list = []
        for item in city:
            markup_list.append(types.InlineKeyboardButton(text=item[1], callback_data=f'send_city_{item[0]}_{campaign_type}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        item1 = types.InlineKeyboardButton("سایر", callback_data=f"desired_campaign_{campaign_type}")
        markup.add(*markup_list, item1, item2)
        bot.edit_message_text('قلعه حرکتی خود را انتخاب کنید', chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=markup)
    except Exception as e:
        send_admin('send_army', e, call.from_user.username)
@bot.callback_query_handler(func=lambda call: call.data.startswith("send_city_"))
def send_city_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(send_city, call)
def send_city(call):
    try:
        bot.answer_callback_query(call.id)
        data = call.data.split('_')
        send_city = data[2]
        campaign_type = data[3]
        continent, status = get_all_city()
        if (status == False):
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از لشکر کشی')
            bot.send_message(chat_id='1889589121', text=continent)
            send_welcome(call.message)
            return
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup_list = []
        for item in continent:
            markup_list.append(
                types.InlineKeyboardButton(text=item[1], callback_data=f'send_destination_{item[0]}_{send_city}_{campaign_type}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        item1 = types.InlineKeyboardButton("سایر", callback_data=f"desired_campaign_{campaign_type}")
        markup.add(*markup_list, item1, item2)

        bot.edit_message_text('مقصد حرکتی خود را انتخاب کنید', chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=markup)
    except Exception as e:
        send_admin('send_city', e, call.from_user.username)
@bot.callback_query_handler(func=lambda call: call.data.startswith("send_destination_"))
def send_destination_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(send_destination, call)
def send_destination(call):
    try:
        bot.answer_callback_query(call.id)

        data = call.data.split('_')
        parent_id = data[2]
        send_city = data[3]
        campaign_type = data[4]
        country, status = get_city_by_parent_id(parent_id)
        if not status:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, f'{e}\nپیام حذف نشد از لشکر کشی')
            bot.send_message(chat_id=admin_chat_id, text=country)
            send_welcome(call.message)
            return

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup_list = []
        for item in country:
            markup_list.append(types.InlineKeyboardButton(text=item[1], callback_data=f'campaign_confirm_{item[0]}_{send_city}_{campaign_type}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        item1 = types.InlineKeyboardButton("سایر", callback_data=f"desired_campaign_{campaign_type}")
        markup.add(*markup_list, item1, item2)
        bot.edit_message_text('قلعه مقصد خود را انتخاب کنید', chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=markup)
    except Exception as e:
        send_admin('send_destination', e, call.from_user.username)
@bot.callback_query_handler(func=lambda call: call.data.startswith("campaign_confirm_"))
def ask_duration_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(ask_duration, call)
def ask_duration(call):
    try:
        bot.answer_callback_query(call.id)

        data = call.data.split('_')  # دریافت داده‌ها از CallbackQuery
        destination_id = data[2]
        origin_id = data[3]
        campaign_type = data[4]
        bot.edit_message_text("زمان رسیدن ارتش خود را وارد نمایید:", chat_id=call.message.chat.id,
                              message_id=call.message.message_id)

        bot.register_next_step_handler(call.message, lambda message : campaign_confirm(message, destination_id, origin_id, campaign_type))  # انتظار پیام بعدی برای دریافت زمان
    except Exception as e:
        send_admin('ask_duration', e, call.from_user.username)
def campaign_confirm(message, destination_id, origin_id, campaign_type):
    try:
        duration = message.text  # زمان وارد شده توسط کاربر را از متن پیام بگیرید

        # فراخوانی تابع تایید لشکرکشی
        property_text, status, city_id = get_campaign_confirm(origin_id, destination_id, message.chat.id, duration,campaign_type)
        if not status:
            try:
                bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از لشکر کشی')
            bot.send_message(chat_id='1889589121', text=property_text)
            send_welcome(message)
            return

        property_text += '\n\nآیا از لشکر کشی خود اطمینان دارید؟'
        markup = types.InlineKeyboardMarkup(row_width=2)

        item1 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        item2 = types.InlineKeyboardButton("تایید",
                                           callback_data=f"campaign_send_{origin_id}_{destination_id}_{duration}_{campaign_type}")
        markup.add(item1, item2)
        if campaign_type == "1":
            image = file_id_campaign[city_id]
        else:
            image = file_id_naval_campaign[city_id]
        bot.send_photo(chat_id=message.chat.id, photo=image, caption=property_text,reply_markup=markup)
    except Exception as e:
        send_admin('campaign_confirm', e, message.from_user.username)
@bot.callback_query_handler(func=lambda call: call.data.startswith("campaign_send_"))
def campaign_confirm_send_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(campaign_confirm_send, call)
def campaign_confirm_send(call):
    try:
        bot.answer_callback_query(call.id)

        data = call.data.split('_')
        destination_id = data[3]
        origin_id = data[2]
        duration = data[4]
        campaign_type = data[5]
        username = call.from_user.username
        first_name = call.from_user.first_name

        property_text, status, city_id = get_campaign_confirm(origin_id, destination_id, call.message.chat.id, duration, campaign_type)
        if not status:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از لشکر کشی')
            bot.send_message(chat_id='1889589121', text=property_text)
            send_welcome(call.message)
            return

        # بررسی موجود بودن داده‌ها
        if call.message.chat.id not in campaign_messages:
            bot.send_message(call.message.chat.id, "هیچ داده‌ای برای این کاربر موجود نیست.")
            return

        if campaign_type == "1":
            image = file_id_campaign[city_id]
        else:
            image = file_id_naval_campaign[city_id]

        property_text += f"\n\n\nفرمانده {first_name}\n@{username}"

        data_campaign = campaign_messages[call.message.chat.id]
        campaign = data_campaign['text']

        bot.send_message(chat_id=campaign_chat_id, text=f'{property_text} \n \n لشکر ها \n \n {campaign}')
        bot.send_photo(chat_id=group_chat_id, photo=image, caption=property_text)
        bot.send_message(chat_id=call.message.chat.id, text='لشکر کشی با موفقیت انجام شد')
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            bot.send_message(call.message.chat.id,"@mohammadtazar پیام لشکر کشیش حذف نشد یک پیگیزی بکن")
        send_welcome(call.message)
    except Exception as e:
        send_admin('campaign_confirm_send', e, call.from_user.username)
@bot.callback_query_handler(func=lambda call: call.data.startswith("desired_campaign_"))
def desired_campaign_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(desired_campaign, call)
def desired_campaign(call):
    try:
        bot.answer_callback_query(call.id)
        data = call.data.split('_')
        campaign_type = data[2]
        campaign_type = int(campaign_type)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # اندازه دکمه‌ها را تغییر می‌دهد
        button = types.KeyboardButton("لغو لشکر کشی")
        markup.add(button)
        text = ('نام خاندان شهر مبدا ، مقصد و زمان رسیدن ارتش خود را به شکل صحیح ارسال نمایید نمونه :'
                '\n\n'
                'لشکران خاندان stark از Winterfell به به سمت کمپ شورشیان حرکت کردند زمان رسیدن 2 ساعت')
        # ویرایش پیام برای درخواست زمان لشکرکشی
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            bot.send_message(admin_chat_id, 'پیام حذف نشد از دستور آخر لشکر کشی')
        bot.send_message(chat_id=call.message.chat.id,text=text,reply_markup=markup)
        bot.register_next_step_handler(call.message, lambda  message : send_desired_campaign(message,campaign_type))  # انتظار پیام بعدی برای دریافت زمان
    except Exception as e:
        send_admin('desired_campaign', e, call.from_user.username)
def send_desired_campaign(message,campaign_type):
    try:
        empty_markup = types.ReplyKeyboardRemove()
        username = message.from_user.username
        first_name = message.from_user.first_name
        if message.text == "لغو لشکر کشی":
            bot.send_message(chat_id=message.chat.id, text='لشکر کشی لغو شد', reply_markup=empty_markup)
            send_welcome(message)
            return
        city,status = get_city_by_chat_id(message.chat.id)

        if campaign_type == 1:
            image = file_id_campaign[city[0][2]]
        else:
            image = file_id_naval_campaign[city[0][2]]

        text = message.text
        text += (f"\n"
                 f"\n"
                 f"\n"
                 f"فرمانده {first_name}\n"
                 f"@{username}")
        data_campaign = campaign_messages[message.chat.id]
        campaign = data_campaign['text']

        bot.send_message(chat_id=campaign_chat_id, text=f'{text} \n \n لشکر ها \n \n {campaign}')
        bot.send_photo(chat_id=group_chat_id, photo=image, caption=text)
        bot.send_message(chat_id=message.chat.id, text='لشکر کشی با موفقیت انجام شد', reply_markup=empty_markup)
        send_welcome(message)
    except Exception as e:
        send_admin('send_desired_campaign', e, message.from_user.username)
#endregion

#region حمله

@bot.callback_query_handler(func=lambda call: call.data == "attack_message")
def attack_type_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(attack_type, call)
def attack_type(call):
    try:
        bot.answer_callback_query(call.id)

        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("🐎 زمینی", callback_data="attack_type_1")
        item2 = types.InlineKeyboardButton("⚓ دریایی", callback_data="attack_type_2")
        item3 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(item1, item2, item3)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="نوع حمله خود را انتخاب کنید", reply_markup=markup)
    except Exception as e:
        send_admin('attack_type', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("attack_type_"))
def attack_message_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(attack_message, call)
def attack_message(call):
    try:
        bot.answer_callback_query(call.id)

        data = call.data.split('_')
        type_attack = data[2]

        continent, status = get_all_city()

        if not status:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از خطای دیتابی حمله')
            bot.send_message(chat_id='1889589121', text=continent)
            send_welcome(call.message)
            return

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup_list = []
        for item in continent:
            markup_list.append(
                types.InlineKeyboardButton(text=item[1], callback_data=f'attack_continent_{item[0]}_{type_attack}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        item1 = types.InlineKeyboardButton("سایر", callback_data=f"desired_attack_{type_attack}")
        markup.add(*markup_list, item1, item2)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="مکان حمله خود را انتخاب کنید", reply_markup=markup)
    except Exception as e:
        send_admin('attack_message', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("attack_continent_"))
def attack_continent_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(attack_continent, call)
def attack_continent(call):
    try:
        bot.answer_callback_query(call.id)

        data = call.data.split('_')
        parent_id = data[2]
        type_attack = data[3]

        city, status = get_city_by_parent_id(parent_id)
        if not status:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از خطای دیتابی حمله')
            bot.send_message(chat_id='1889589121', text=city)
            send_welcome(call.message)
            return

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup_list = []
        for item in city:
            markup_list.append(types.InlineKeyboardButton(text=item[1], callback_data=f'chose_at_co_{item[1]}_{type_attack}'))
        item1 = types.InlineKeyboardButton("سایر", callback_data=f"desired_attack_{type_attack}")
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(*markup_list, item1, item2)

        bot.edit_message_text('قلعه مورد حمله را انتخاب کنید', chat_id=call.message.chat.id,
                              message_id=call.message.message_id, reply_markup=markup)
    except Exception as e:
        send_admin('attack_continent', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("chose_at_co_"))
def chose_attack_confirm_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(chose_attack_confirm, call)
def chose_attack_confirm(call):
    try:
        bot.answer_callback_query(call.id)

        data = call.data.split('_')
        city,statuse = get_city_by_chat_id(call.message.chat.id)
        destination = data[3]
        type_attack = data[4]

        if type_attack == "1":
            text_type = 'لشکریان'
        else:
            text_type = "نیروی دریایی"

        text = (f'{text_type} {city[0][1]} دستور حمله به سمت {destination} را صادر کردند\n\n'
                f'آیا از حمله اطمینان دارید؟')

        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        item2 = types.InlineKeyboardButton("تایید", callback_data=f"attack_confirm_{destination}_{type_attack}")
        markup.add(item1, item2)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, reply_markup=markup)
    except Exception as e:
        send_admin('chose_attack_confirm', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("attack_confirm_"))
def attack_confirm_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(attack_confirm, call)
def attack_confirm(call):
    try:
        bot.answer_callback_query(call.id)

        username = call.from_user.username
        first_name = call.from_user.first_name

        data = call.data.split('_')
        city,status = get_city_by_chat_id(call.message.chat.id)
        destination = data[2]
        type_attack = data[3]

        if type_attack == "1":
            text_type = "لشکریان"
            image = file_id_attack
        else:
            text_type = "نیروی دریایی"
            image = file_id_attack_naval_campaign

        text = (f'{text_type} {city[0][1]} دستور حمله به سمت {destination} را صادر کردند\n\n'
                f'فرصت ارسال سنا تا فردا ساعت 1\n\n'
                f'فرمانده {first_name}\n'
                f'@{username}')

        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            bot.send_message(admin_chat_id, 'پیام حذف نشد از حمله')
        bot.send_photo(chat_id=group_chat_id, photo=image, caption=text)
        bot.send_message(chat_id=call.message.chat.id, text='دستور حمله با موفقیت صادر شد')
        send_welcome(call.message)
    except Exception as e:
        send_admin('attack_confirm', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("desired_attack_"))
def desired_attack_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(desired_attack, call)

def desired_attack(call):
    try:
        bot.answer_callback_query(call.id)

        data = call.data.split('_')
        type_attack = data[2]

        text = ('نام خاندان مقصد و مکان مورد حمله را به صورت دقیق ذکر نمایید.\n'
                'نمونه: لشکران خاندان Stark به سمت کمپ شورشیان حمله کردند.\n'
                'جهت لغو عملیات بنویسید: انصراف')

        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            bot.send_message(admin_chat_id, 'پیام حذف نشد از حمله')
        bot.send_message(chat_id=call.message.chat.id, text=text)
        bot.register_next_step_handler(call.message, lambda message: send_desired_attack(message, type_attack))
    except Exception as e:
        send_admin('desired_attack', e, call.from_user.username)
def send_desired_attack(message, type_attack):
    try:

        username = message.from_user.username
        first_name = message.from_user.first_name

        text = message.text
        if text =="انصراف":
            bot.send_message(message.chat.id,"عملیات با لغو شد")
            send_welcome(message)
            return
        if type_attack == "1":
            image = file_id_attack
        else:
            image = file_id_attack_naval_campaign
        text += (f"\n\n\n"
                 f"فرصت ارسال سنا تا فرساد ساعت 1"
                 f"\n"
                 f"\n"
                 f"فرمانده {first_name}\n"
                 f"{username}")
        bot.send_photo(chat_id=group_chat_id, photo=image, caption=text)
        bot.send_message(chat_id=message.chat.id, text='دستور حمله با موفقیت انجام شد')
        send_welcome(message)
    except Exception as e:
        send_admin('desired_attack', e, message.from_user.username)

#endregion

#region محاصره
@bot.callback_query_handler(func=lambda call: call.data=="siege_message")
def siege_message_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(siege_message, call)
def siege_message(call):
    try:
        bot.answer_callback_query(call.id)

        continent, status = get_all_city()
        if not status:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از خطای دیتابی محاصره')
            bot.send_message(chat_id='1889589121', text=continent)
            send_welcome(call.message)
            return
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup_list = []
        for item in continent:
            markup_list.append(
                types.InlineKeyboardButton(text=item[1], callback_data=f'siege_continent_{item[0]}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(*markup_list, item2)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="مکان محاصره خود را انتخاب کنید", reply_markup=markup)
    except Exception as e:
        send_admin('siege_message', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("siege_continent_"))
def siege_co_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(siege_co, call)
def siege_co(call):
    try:
        bot.answer_callback_query(call.id)

        data = call.data.split('_')
        parent_id = data[2]
        city, status = get_city_by_parent_id(parent_id)
        if not status:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از خطای دیتابی محاصره')
            bot.send_message(chat_id='1889589121', text=city)
            send_welcome(call.message)
            return
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup_list = []
        for item in city:
            markup_list.append(types.InlineKeyboardButton(text=item[1], callback_data=f'chose_siege_co_{item[1]}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(*markup_list, item2)
        bot.edit_message_text('قلعه مورد محاصره را انتخاب کنید', chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup)
    except Exception as e:
        send_admin('siege_co', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("chose_siege_co_"))
def chose_siege_co_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(chose_siege_co, call)
def chose_siege_co(call):
    try:
        bot.answer_callback_query(call.id)

        data = call.data.split('_')
        city, status = get_city_by_chat_id(call.message.chat.id)
        destination = data[3]

        text = (f'نیرو های {city[0][1]} دستور محاصره قلعه {destination} را صادر کردند '
                f'\n\n'
                f'آیا از محاصره خود اطمینان دارید ؟')

        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        item2 = types.InlineKeyboardButton("تایید",
                                           callback_data=f"siege_confirm_{destination}_{city[0][1]}")
        markup.add(item1, item2)

        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=text, reply_markup=markup)
    except Exception as e:
        send_admin('chose_siege_co', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("siege_confirm_"))
def siege_confirm_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(siege_confirm, call)
def siege_confirm(call):
    try:
        bot.answer_callback_query(call.id)
        username = call.from_user.username
        first_name = call.from_user.first_name

        data = call.data.split('_')
        city = data[3]
        destination = data[2]

        text = (f' لشکریان  {city} دستور محاصره قلعه  {destination} را صادر کردند '
                f'\n'
                f'\n'
                f'فرمانده{first_name}\n'
                f'@{username}')
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            bot.send_message(admin_chat_id, 'پیام حذف نشد از  محاصره')

        bot.send_photo(chat_id=group_chat_id, photo=file_id_siege, caption=text)
        bot.send_message(chat_id=call.message.chat.id, text='محاصره با موفقیت انجام شد')
        send_welcome(call.message)

    except Exception as e:
        send_admin('siege_confirm', e, call.from_user.username)
#endregion

#region دارایی
@bot.callback_query_handler(func=lambda call: call.data=="property_message")
def property_message_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(property_message, call)
def property_message(call):
    try:
        bot.answer_callback_query(call.id)

        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("⬆️ ارتقا", callback_data="upgrade")
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(item1, item2)
        author = call.from_user.first_name

        property_text,status = get_property(call.message.chat.id,author)
        if not status:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از دارایی')
            bot.send_message(chat_id='1889589121', text=property_text)
            send_welcome(call.message)
            return

        bot.edit_message_text(property_text, chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=markup)
    except Exception as e:
        send_admin('property_message', e, call.from_user.username)
#endregion

#region تجارت
@bot.callback_query_handler(func=lambda call: call.data=="business_message")
def business_message_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(business_message, call)
def business_message(call):
    try:
        bot.answer_callback_query(call.id)
        if call.message.chat.type == "private":
            bot.send_message(call.message.chat.id, f'خوب به گا رفتی الان به بابام میگم دهنت رو سرویس کنه')
            bot.send_message(admin_chat_id, f' {call.message.from_user.first_name} \n @{call.from_user.username} \n'
                                            f'استارت دارایی از داخل بات رو زد')
            return

        continent, status = get_all_city()
        if not status:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از خطای دیتابی تجارت')
            bot.send_message(chat_id='1889589121', text=continent)
            send_welcome(call.message)
            return
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup_list = []
        for item in continent:
            markup_list.append(
                types.InlineKeyboardButton(text=item[1], callback_data=f'business_continent_{item[0]}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(*markup_list, item2)

        bot.edit_message_text("خاندان مورد نظر را انتخاب نمایید", chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=markup)
    except Exception as e:
        send_admin('business_message', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("business_continent_"))
def business_continent_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(business_continent, call)
def business_continent(call):
    try:
        bot.answer_callback_query(call.id)

        data = call.data.split('_')
        parent_id = data[2]
        city, status = get_city_by_parent_id(parent_id)
        if not status:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از خطای دیتابی تجارت')
            bot.send_message(chat_id='1889589121', text=city)
            send_welcome(call.message)
            return
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup_list = []
        for item in city:
            markup_list.append(types.InlineKeyboardButton(text=item[1], callback_data=f'business_city_{item[0]}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(*markup_list, item2)
        bot.edit_message_text('قلعه مورد نظر برای ارسال کالا را انتخاب نمایید', chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup)
    except Exception as e:
        send_admin('business_continent', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("business_city_"))
def business_city_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(business_city, call)
def business_city(call):
    try:
        bot.answer_callback_query(call.id)

        data = call.data.split('_')
        city = data[2]
        product, status = get_product()
        if not status:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از خطای دیتابی تجارت')
            bot.send_message(chat_id='1889589121', text=product)
            send_welcome(call.message)
            return
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup_list = []
        for item in product:
            markup_list.append(types.InlineKeyboardButton(text=item[0], callback_data=f'production_city_{city}_{item[1]}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(*markup_list, item2)
        bot.edit_message_text('محصول مورد نظر برای تجارت را انتخاب کنید', chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=markup)

    except Exception as e:
        send_admin('business_city', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("production_city_"))
def production_city_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(production_city, call)
def production_city(call):
    try:
        bot.answer_callback_query(call.id)

        data = call.data.split('_')
        city = data[2]
        product = data[3]

        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            bot.send_message(admin_chat_id, f' {e}پیام حذف نشد از تجارت')
        bot.send_message(chat_id=call.message.chat.id, text="تعداد مورد نظر را به صورت صحیح وارد نمایید\n"
                                                            "\n"
                                                            "فقط تعداد را وارد نمایید بدون هیچ کلمه اضافه ای")
        bot.register_next_step_handler(call.message, lambda message: confirm_business(message, city,product))
    except Exception as e:
        send_admin('production_city', e, call.from_user.username)
def confirm_business(message, city_id, product_id):
    try:
        amount = message.text
        if not amount.isdigit():
            bot.send_message(message.chat.id, "گاوی مگه نمیفهمی که میگم فقط عدد وارد کن")
            return
        amount = int(amount)
        product_title, status = get_product_detail(product_id)
        if not status:
            try:
                bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از خطای دیتابی تجارت')
            bot.send_message(chat_id='1889589121', text=product_title)
            send_welcome(message)
            return
        city_title,status = get_city_by_id(city_id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("ارسال", callback_data=f"se_bu_{amount}_{product_id}_{city_id}")
        item2 = types.InlineKeyboardButton("انصراف", callback_data="cansel")
        markup.add(item1, item2)
        property_text = (f"تعداد {amount} {product_title[0]} به سمت قلعه {city_title[0][1]} ارسال شود \n"
                         f"\n"
                         f"\n"
                         f"آیا از تجارت خود اطمینان دارید؟")
        bot.send_message(message.chat.id, text=property_text, reply_markup=markup)
    except Exception as e:
        send_admin('confirm_business', e, message.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("se_bu_"))
def se_bu_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(se_bu, call)
def se_bu(call):
    try:
        bot.answer_callback_query(call.id)
        data = call.data.split('_')
        amount = data[2]
        product_id = data[3]
        city_id = data[4]
        amount = int(amount)

        city_title,status = get_city_by_chat_id(call.message.chat.id)
        resource_title,status = get_product_detail(product_id)
        chat_id_send,status = get_city_by_id(city_id)
        text, status = get_trade(product_id,amount,city_id,call.message.chat.id)
        if not status:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از خطای دیتابی تجارت')
            bot.send_message(chat_id='1889589121', text=text)
            send_welcome(call.message)
            return
        if text == 'تعداد دارایی شما کمتر از میزان ارسالی می باشد':
            bot.send_message(chat_id=call.message.chat.id, text=text)
            return
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            bot.send_message(admin_chat_id, 'پیام حذف نشد از تجارت')
        bot.send_message(chat_id=call.message.chat.id, text=f'{text} \n مقدار {amount} {resource_title[0]}\n مقصد {chat_id_send[0][1]} ارسال شد')
        time.sleep(1)
        bot.send_message(chat_id=chat_id_send[0][3], text=f"مقدار {amount} {resource_title[0]} از قلعه {city_title[0][1]} ارسال شد")
        send_welcome(call.message)
    except Exception as e:
        send_admin('se_bu', e, call.from_user.username)
#endregion

#region تویئت
@bot.callback_query_handler(func=lambda call: call.data=="tweet_message")
def tweet_message_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(tweet_message, call)
def tweet_message(call):
    try:
        bot.answer_callback_query(call.id)

        markup = types.InlineKeyboardMarkup(row_width=2)

        property_text = ('توئیت خود را ارسال نمایید '
                         '\n'
                         '\n'
                         'برای لغو عملیات کلمه انصراف را بنویسید')

        bot.edit_message_text(property_text, chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=markup)
        bot.register_next_step_handler(call.message, tweet_send)
    except Exception as e:
        send_admin('tweet_message', e, call.from_user.username)
def tweet_send(message):
    try:
        if message.text == 'انصراف':
            send_welcome(message)
            return

        # دریافت نام ارسال‌کننده
        author = message.from_user.username if message.from_user.username else message.from_user.first_name

        # بررسی نوع پیام
        if message.photo:
            file_id = message.photo[-1].file_id
            message_content = message.caption if message.caption else ""
            send_type = "photo"
        elif message.video:
            file_id = message.video.file_id
            message_content = message.caption if message.caption else ""
            send_type = "video"
        elif message.animation:  # ویدیو گیف
            file_id = message.animation.file_id
            message_content = message.caption if message.caption else ""
            send_type = "animation"
        elif message.text:
            file_id = None
            message_content = message.text
            send_type = "text"
        else:
            bot.send_message(chat_id=message.chat.id, text="فرمت پیام پشتیبانی نمی‌شود.")
            return

        # ایجاد متن توئیت
        property_text = ('#توئیت'
                         '\n\n'
                         f'{message_content}'
                         '\n\n'
                         f'@{author}')

        # ارسال پیام بر اساس نوع آن
        if send_type == "photo":
            bot.send_photo(chat_id=tweet_chat_id, photo=file_id, caption=property_text)
        elif send_type == "video":
            bot.send_video(chat_id=tweet_chat_id, video=file_id, caption=property_text)
        elif send_type == "animation":
            bot.send_animation(chat_id=tweet_chat_id, animation=file_id, caption=property_text)
        else:
            bot.send_message(chat_id=tweet_chat_id, text=property_text)

        # ارسال پیام تأیید برای کاربر
        bot.send_message(chat_id=message.chat.id, text='✅ توئیت ارسال شد!')
        send_welcome(message)

    except Exception as e:
        send_admin('tweet_send', e, message.from_user.username)
#endregion

#region ارتقا
@bot.callback_query_handler(func=lambda call: call.data=="upgrade")
def upgrade_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(upgrade, call)
def upgrade(call):
    try:
        bot.answer_callback_query(call.id)

        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("🪙 اقتصادی", callback_data="upgrade_economic")
        item3 = types.InlineKeyboardButton("⚔️ نظامی", callback_data="upgrade_military")
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(item1, item3, item2)

        bot.edit_message_text('نوع ارتقا خود را انتخاب نمایید', chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=markup)
    except Exception as e:
        send_admin('upgrade', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("upgrade_military"))
def upgrade_military_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(upgrade_military, call)
def upgrade_military(call):
    try:
        bot.answer_callback_query(call.id)

        all_economic_build, status = get_military()
        if not status:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از خطای دیتابی ارتقا')
            bot.send_message(chat_id='1889589121', text=all_economic_build)
            send_welcome(call.message)
            return
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup_list = []
        for item in all_economic_build:
            markup_list.append(
                types.InlineKeyboardButton(text=item[1], callback_data=f'economic_upgrade_{item[0]}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(*markup_list, item2)

        bot.edit_message_text('ساختمون مورد نظر برای ارتقا را مشخص کنید', chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=markup)
    except Exception as e:
        send_admin('upgrade_military', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("upgrade_economic"))
def upgrade_economic_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(upgrade_economic, call)
def upgrade_economic(call):
    try:
        bot.answer_callback_query(call.id)

        all_economic_build, status = get_economic()
        if not status:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از خطای دیتابی ارتقا')
            bot.send_message(chat_id='1889589121', text=all_economic_build)
            send_welcome(call.message)
            return
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup_list = []
        for item in all_economic_build:
            markup_list.append(
                types.InlineKeyboardButton(text=item[1], callback_data=f'economic_upgrade_{item[0]}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(*markup_list, item2)

        bot.edit_message_text('ساختمان مورد نظر برای ارتقا را انتخاب کنید . ', chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=markup)
    except Exception as e:
        send_admin('upgrade_economic', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("economic_upgrade_"))
def economic_upgrade_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(economic_upgrade, call)
def economic_upgrade(call):
    try:
        bot.answer_callback_query(call.id)

        data = call.data.split('_')
        build_id = data[2]

        cost_text, status = get_cost(build_id,call.message.chat.id)
        if not status:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از خطای دیتابی ارتقا')
            bot.send_message(chat_id='1889589121', text=cost_text)
            send_welcome(call.message)
            return
        if cost_text == 1 :
            bot.send_message(chat_id=call.message.chat.id,text='شما حداکثر سطح را بدست آوردید')
            return
        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("تایید", callback_data=f"con_upgrade_{build_id}")
        item2 = types.InlineKeyboardButton("انصراف", callback_data="cansel")
        markup.add(item1, item2)
        bot.edit_message_text(cost_text,chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=markup)

    except Exception as e:
        send_admin('economic_upgrade', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("con_upgrade_"))
def con_upgrade_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(con_upgrade, call)
def con_upgrade(call):
    try:
        bot.answer_callback_query(call.id)

        data = call.data.split('_')
        build_id = data[2]

        cost_text, status = get_confirm_cost(build_id,call.message.chat.id)
        if not status:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, 'پیام حذف نشد از خطای دیتابی ارتقا')
            bot.send_message(chat_id=admin_chat_id, text=cost_text)
            send_welcome(call.message)
            return
        bot.send_message(chat_id=call.message.chat.id, text=cost_text)
        property_message(call)

    except Exception as e:
        send_admin('con_upgrade', e, call.from_user.username)
#endregion

#region اضافه کردن شهر
@bot.message_handler(commands=['add_city'])
def add_city(message):
    try:
        # بررسی ادمین بودن کاربر
        if message.from_user.id not in [int(admin_chat_id), int(admin_chat_second_id), int(admin_chat_tree_id)]:
            bot.send_message(chat_id=message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن")
            return

        bot.send_message(chat_id=message.chat.id, text="شهر مورد نظر را وارد نمایید.")
        bot.register_next_step_handler(message, save_add_city)
    except Exception as e:
        bot.send_message(admin_chat_id, str(e))
def save_add_city(message):
    try:
        # بررسی ادمین بودن کاربر
        if message.from_user.id not in [int(admin_chat_id), int(admin_chat_second_id), int(admin_chat_tree_id)]:
            bot.send_message(chat_id=message.chat.id, text="تو کاری که به شما مربوط نیست دخالت نکن.")
            return

        text = message.text
        property_text = save_city(text, message.chat.id)
        bot.send_message(message.chat.id, property_text)
    except Exception as e:
        bot.send_message(admin_chat_id, str(e))
#endregion

#region ساخت نیرو
@bot.callback_query_handler(func=lambda call: call.data=="make_message")
def make_message_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(make_message, call)
def make_message(call):
    try:
        bot.answer_callback_query(call.id)

        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("🛶 کشتی", callback_data="ship")
        item2 = types.InlineKeyboardButton("ادوات", callback_data="tools")
        item3 = types.InlineKeyboardButton("سرباز", callback_data="army")
        item4 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(item1, item2, item3, item4)
        bot.edit_message_text(text='نوع نیروی خود را وارد نمایید', chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=markup)
    except Exception as e:
        send_admin('make_message', e, call.from_user.username)

#region کشتی
@bot.callback_query_handler(func=lambda call: call.data=="ship")
def ship_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(ship, call)
def ship(call):
    try:
        bot.answer_callback_query(call.id)

        all_resource, status = get_all_ship()
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup_list = []
        for item in all_resource:
            markup_list.append(
                types.InlineKeyboardButton(text=item[1], callback_data=f'add_ship_{item[0]}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(*markup_list, item2)

        bot.edit_message_text(text='نوع کشتی را انتخاب کنید',chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=markup)
    except Exception as e:
        send_admin('ship', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_ship_"))
def add_ship_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(add_ship, call)
def add_ship(call):
    try:
        bot.answer_callback_query(call.id)
        data = call.data.split('_')
        ship_id = data[2]
        markup = types.InlineKeyboardMarkup(row_width=2)
        property_text, code, status = get_cost_ship(call.message.chat.id, ship_id)
        if status == False:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, str(e))
            bot.send_message(admin_chat_id, property_text)
            send_welcome(call.message)
            return
        if code == 0:
            bot.send_message(chat_id=call.message.chat.id, text = property_text)

            return
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        item1 = types.InlineKeyboardButton("تایید", callback_data=f"ship_config_{ship_id}")
        markup.add(item1, item2)

        bot.edit_message_text(property_text, chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=markup)

    except Exception as e:
        send_admin('add_ship', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("ship_config_"))
def ship_config_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(ship_config, call)
def ship_config(call):
    try:
        bot.answer_callback_query(call.id)
        data = call.data.split('_')
        ship_id = data[2]

        property_text, code, status = get_config_ship(call.message.chat.id, ship_id)
        if status == False:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, str(e))
            bot.send_message(call.message.chat.id, 'خطایی رخ داده است')
            bot.send_message(admin_chat_id, property_text)

            send_welcome(call.message)
            return
        if code == 0:
            bot.send_message(chat_id=call.message.chat.id, text = property_text)
            return
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id, text = property_text)
        send_welcome(call.message)
    except Exception as e:
        send_admin('ship_config', e, call.from_user.username)
#endregion

#region ساخت ادوات
@bot.callback_query_handler(func=lambda call: call.data=="tools")
def tools_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(tools, call)
def tools(call):
    try:
        bot.answer_callback_query(call.id)

        all_resource, status = get_all_tools()
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup_list = []
        for item in all_resource:
            markup_list.append(
                types.InlineKeyboardButton(text=item[1], callback_data=f'add_tools_{item[0]}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(*markup_list, item2)

        bot.edit_message_text(text='ادوات خود را انتخاب کنید',chat_id=call.message.chat.id, message_id=call.message.message_id,reply_markup=markup)
    except Exception as e:
        send_admin('tools', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_tools_"))
def add_tools_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(add_tools, call)
def add_tools(call):
    try:
        bot.answer_callback_query(call.id)
        data = call.data.split('_')
        tools_id = data[2]

        markup = types.InlineKeyboardMarkup(row_width=2)
        property_text, code, status = get_cost_tools(call.message.chat.id, tools_id)
        if status == False:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, str(e))
            bot.send_message(admin_chat_id, property_text)
            send_welcome(call.message)
            return
        if code == 0:
            bot.send_message(chat_id=call.message.chat.id, text=property_text)

            return
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        item1 = types.InlineKeyboardButton("تایید", callback_data=f"tools_config_{tools_id}")
        markup.add(item1, item2)

        bot.edit_message_text(property_text, chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=markup)
    except Exception as e:
        send_admin('add_tools', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("tools_config_"))
def tools_config_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(tools_config, call)
def tools_config(call):
    try:
        bot.answer_callback_query(call.id)
        data = call.data.split('_')
        ship_id = data[2]
        property_text, code, status = get_config_tools(call.message.chat.id, ship_id)
        if status == False:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, str(e))
            bot.send_message(call.message.chat.id, 'خطایی رخ داده است')
            bot.send_message(admin_chat_id, property_text)

            send_welcome(call.message)
            return
        if code == 0:
            bot.send_message(chat_id=call.message.chat.id, text = property_text)
            return
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id, text = property_text)
        send_welcome(call.message)
    except Exception as e:
        send_admin('tools_config', e, call.from_user.username)
#endregion
# region ساخت سرباز
@bot.callback_query_handler(func=lambda call: call.data == "army")
def army_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(army, call)
def army(call):
    try:
        bot.answer_callback_query(call.id)

        all_resource, status = get_all_army()
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup_list = []
        for item in all_resource:
            markup_list.append(
                types.InlineKeyboardButton(text=item[1], callback_data=f'add_army_{item[0]}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(*markup_list, item2)

        bot.edit_message_text(
            text='⚔️ سرباز خود را انتخاب کنید',
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )
    except Exception as e:
        send_admin('army', e, call.from_user.username)

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_army_"))
def add_army_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(add_army, call)
def add_army(call):
    try:
        bot.answer_callback_query(call.id)
        weapon_id = int(call.data.split('_')[2])

        # از کاربر تعداد بپرسیم
        msg = bot.edit_message_text(
            text=f"🔢 تعداد را وارد کنید:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )

        # ذخیره weapon_id و گرفتن تعداد
        bot.register_next_step_handler(msg, process_army_count, weapon_id)
    except Exception as e:
        send_admin('add_army', e, call.from_user.username)

def process_army_count(message, weapon_id):
    try:
        count = int(message.text)

        markup = types.InlineKeyboardMarkup(row_width=2)
        property_text, code, status = get_cost_army(weapon_id,count)
        if status == False:
            try:
                bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, str(e))
            bot.send_message(admin_chat_id, property_text)
            send_welcome(message)
            return
        if code == 0:
            bot.send_message(chat_id=message.chat.id, text=property_text)

            return
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        item1 = types.InlineKeyboardButton("تایید", callback_data=f"army_config_{weapon_id}_{count}")
        markup.add(item1, item2)

        bot.send_message(
            message.chat.id,
            f"{property_text}\n\nآیا تایید می‌کنید؟",
            reply_markup=markup
        )

    except ValueError:
        bot.send_message(message.chat.id, "⚠️ لطفاً یک عدد صحیح وارد کنید.")


@bot.callback_query_handler(func=lambda call: call.data.startswith("army_config_"))
def army_config_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(army_config, call)
def army_config(call):
    try:
        bot.answer_callback_query(call.id)
        _, _, wid, count = call.data.split("_")
        wid, count = int(wid), int(count)

        property_text, code, status = get_config_army(call.message.chat.id, wid,count)
        if status == False:
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except Exception as e:
                bot.send_message(admin_chat_id, str(e))
            bot.send_message(call.message.chat.id, 'خطایی رخ داده است')
            bot.send_message(admin_chat_id, property_text)

            send_welcome(call.message)
            return
        if code == 0:
            bot.send_message(chat_id=call.message.chat.id, text=property_text)
            return
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id, text=property_text)
        send_welcome(call.message)
    except Exception as e:
        send_admin('tools_config', e, call.from_user.username)
# endregion

#endregion

#region پنل مدیریت
@bot.message_handler(func=lambda message: 'مدیریت' in message.text.lower())
@bot.callback_query_handler(func=lambda call: call.data=="cansel_manager")
def handle_panel_message(message):
    try:
        if message.chat.id != int(admin_panel):
            author = message.from_user.username if message.from_user.username else message.from_user.first_name
            bot.send_message(chat_id=admin_chat_id, text=f"@{author} \n"
                                                     f"تلاش کرد که به پنل ادمین دسترسی پیدا کند")
            return
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("بازدهی", callback_data="resource_efficiency")
        item2 = types.InlineKeyboardButton("کم کردن آذوغه", callback_data="food")
        item3 = types.InlineKeyboardButton("زدن تلفات", callback_data="Casualties")
        item4 = types.InlineKeyboardButton("قلعه ها دارای دارایی آذوغه منفی", callback_data="negative_supply")
        markup.add(item1, item2,item3,item4)
        bot.send_message(message.chat.id, "دستور خود را وارد کنید", reply_markup=markup)
    except Exception as e:
        bot.send_message(admin_chat_id, e)
#region بازدهی
@bot.callback_query_handler(func=lambda call: call.data == "resource_efficiency")
def resource_efficiency(call):
    bot.answer_callback_query(call.id)

    if call.from_user.id != int(admin_chat_id) and call.from_user.id != int(admin_chat_second_id) and call.from_user.id != int(admin_chat_tree_id):
        bot.send_message(chat_id=call.message.chat.id, text="خسته ام کردید")
        return

    try:
        markup = types.InlineKeyboardMarkup(row_width=2)

        item1 = types.InlineKeyboardButton("تایید بازدهی", callback_data="config_resource_efficiency")
        item2 = types.InlineKeyboardButton("انصراف", callback_data="cansel_manager")
        markup.add(item1,item2)
        bot.edit_message_text(text='حتما قبل از بازدهی خبر بده تا از داده ها بکاپ بگیرم مشکلی پیش نیاد ',message_id=call.message.message_id,chat_id=call.message.chat.id, reply_markup=markup)
    except Exception as e:
        bot.send_message(admin_chat_id, e)
@bot.callback_query_handler(func=lambda call: call.data == "config_resource_efficiency")
def config_resource_efficiency(call):
    bot.answer_callback_query(call.id)
    if call.from_user.id != int(admin_chat_id) and call.from_user.id != int(admin_chat_second_id) and call.from_user.id != int(admin_chat_tree_id):
        bot.send_message(chat_id=call.message.chat.id, text="خسته ام کردید")
        return

    try:
        property_text, status = get_resource_efficiency()
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=property_text)
    except Exception as e:
        bot.send_message(admin_chat_id, e)
#endregion
#region کم کردن آذوغه
@bot.callback_query_handler(func=lambda call: call.data == "food")
def food(call):
    if call.from_user.id != int(admin_chat_id) and call.from_user.id != int(
            admin_chat_second_id) and call.from_user.id != int(admin_chat_tree_id):
        bot.send_message(chat_id=call.message.chat.id, text="خسته ام کردید")
        return
    bot.answer_callback_query(call.id)
    try:
        markup = types.InlineKeyboardMarkup(row_width=2)

        item1 = types.InlineKeyboardButton("تایید", callback_data="costfood")
        item2 = types.InlineKeyboardButton("انصراف", callback_data="cansel_manager")
        markup.add(item1, item2)
        bot.edit_message_text(text='حتما قبل از کم کردن غلات خبر بده تا از داده ها بکاپ بگیرم مشکلی پیش نیاد ',
                              message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=markup)
    except Exception as e:
        bot.send_message(admin_chat_id, e)
@bot.callback_query_handler(func=lambda call: call.data == "costfood")
def costfood(call):
    if call.from_user.id != int(admin_chat_id) and call.from_user.id != int(
            admin_chat_second_id) and call.from_user.id != int(admin_chat_tree_id):
        bot.send_message(chat_id=call.message.chat.id, text="خسته ام کردید")
        return
    bot.answer_callback_query(call.id)
    try:
        property_text, status = cost_food()
        bot.send_message(call.message.chat.id, property_text)
    except Exception as e:
        bot.send_message(admin_chat_id, e)
# endregion
#region زدن تلفات
@bot.callback_query_handler(func=lambda call: call.data == "Casualties")
def Casualties(call):
    if call.from_user.id != int(admin_chat_id) and call.from_user.id != int(
            admin_chat_second_id) and call.from_user.id != int(admin_chat_tree_id):
        bot.send_message(chat_id=call.message.chat.id, text="خسته ام کردید")
        return
    bot.answer_callback_query(call.id)
    try:
        markup = types.InlineKeyboardMarkup(row_width=2)

        item1 = types.InlineKeyboardButton("تایید", callback_data="costCasualties")
        item2 = types.InlineKeyboardButton("انصراف", callback_data="cansel_manager")
        markup.add(item1, item2)
        bot.edit_message_text(text='حتما قبل از زدن تلفات خبر بده تا از داده ها بکاپ بگیرم مشکلی پیش نیاد ',
                              message_id=call.message.message_id, chat_id=call.message.chat.id, reply_markup=markup)
    except Exception as e:
        bot.send_message(admin_chat_id, e)

@bot.callback_query_handler(func=lambda call: call.data == "costCasualties")
def costCasualties(call):

    bot.answer_callback_query(call.id)
    try:
        property_text, status = cost_casualties()
        bot.send_message(call.message.chat.id, property_text)
    except Exception as e:
        bot.send_message(admin_chat_id, e)
#endregion
#region قلعه های آذوغه منفی
@bot.callback_query_handler(func=lambda call: call.data == "negative_supply")
def negative_supply(call):

    bot.answer_callback_query(call.id)
    try:
        property_text = get_negative_supply()
        bot.send_message(call.message.chat.id, property_text)
    except Exception as e:
        bot.send_message(admin_chat_id, e)
#endregion
#endregion

#region حرکت اژدها
# @bot.callback_query_handler(func=lambda call: call.data=="dragon_message")
# def dragon_message_thread(call):
#     bot.answer_callback_query(call.id, "در حال پردازش...")
#     if is_spamming(call.message.chat.id):
#         bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
#         return
#     run_in_thread(dragon_message, call)
# def dragon_message(call):
#     try:
#         dragon,status = get_my_dragon(call.message.chat.id)
#         if not status:
#             try:
#                 bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
#             except Exception as e:
#                 bot.send_message(admin_chat_id, 'پیام حذف نشد از دارایی')
#             bot.send_message(chat_id='1889589121', text=dragon)
#             send_welcome(call.message)
#             return
#         markup = types.InlineKeyboardMarkup(row_width=1)
#         property_text = 'یکی از اژدها های خود را وارد نمایید'
#         markup_list = []
#         for item in dragon:
#             markup_list.append(
#                 types.InlineKeyboardButton(text=item[1], callback_data=f'dragon_country_{item[0]}'))
#         item1 = types.InlineKeyboardButton("تغییر مسیر", callback_data="other_desired_dragon")
#         item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
#         markup.add(*markup_list, item2, item1)
#         bot.edit_message_text(property_text, chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               reply_markup=markup)
#     except Exception as e:
#         send_admin('property_message', e, call.from_user.username)
# @bot.callback_query_handler(func=lambda call: call.data.startswith("dragon_country_"))
# def dragon_country_thread(call):
#     bot.answer_callback_query(call.id, "در حال پردازش...")
#     if is_spamming(call.message.chat.id):
#         bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
#         return
#     run_in_thread(dragon_country, call)
# def dragon_country(call):
#     try:
#         bot.answer_callback_query(call.id)
#
#         data = call.data.split('_')
#         dragon_id = data[2]
#         country, status = get_all_city()
#         if not status:
#             try:
#                 bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
#             except Exception as e:
#                 bot.send_message(admin_chat_id, 'پیام حذف نشد از لشکر کشی')
#             bot.send_message(chat_id='1889589121', text=country)
#             send_welcome(call.message)
#             return
#
#         markup = types.InlineKeyboardMarkup(row_width=2)
#         markup_list = []
#         for item in country:
#             markup_list.append(types.InlineKeyboardButton(text=item[1], callback_data=f'send_dragon_continent_{item[0]}_{dragon_id}'))
#         item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
#         markup.add(*markup_list, item2)
#         bot.edit_message_text('قاره حرکتی خود را انتخاب کنید', chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               reply_markup=markup)
#     except Exception as e:
#         send_admin('send_army', e, call.from_user.username)
# @bot.callback_query_handler(func=lambda call: call.data.startswith("send_dragon_continent_"))
# def send_dragon_continent_thread(call):
#     bot.answer_callback_query(call.id, "در حال پردازش...")
#     if is_spamming(call.message.chat.id):
#         bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
#         return
#     run_in_thread(send_dragon_continent, call)
# def send_dragon_continent(call):
#     try:
#         bot.answer_callback_query(call.id)
#
#         data = call.data.split('_')
#         parent_id = data[3]
#         dragon_id = data[4]
#         parent_id = int(parent_id)
#         city, status = get_city_by_parent_id(parent_id)
#         if not status:
#             try:
#                 bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
#             except Exception as e:
#                 bot.send_message(admin_chat_id, 'پیام حذف نشد از لشکر کشی')
#             bot.send_message(chat_id='1889589121', text=city)
#             send_welcome(call.message)
#             return
#
#         markup = types.InlineKeyboardMarkup(row_width=2)
#         markup_list = []
#         for item in city:
#             markup_list.append(types.InlineKeyboardButton(text=item[1], callback_data=f'send_dragon_city_{item[0]}_{dragon_id}'))
#         item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
#         markup.add(*markup_list, item2)
#         bot.edit_message_text('قلعه حرکتی خود را انتخاب کنید', chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               reply_markup=markup)
#     except Exception as e:
#         send_admin('send_army', e, call.from_user.username)
# @bot.callback_query_handler(func=lambda call: call.data.startswith("send_dragon_city_"))
# def send_dragon_city_thread(call):
#     bot.answer_callback_query(call.id, "در حال پردازش...")
#     if is_spamming(call.message.chat.id):
#         bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
#         return
#     run_in_thread(send_dragon_city, call)
# def send_dragon_city(call):
#     try:
#         bot.answer_callback_query(call.id)
#         data = call.data.split('_')
#         send_city = data[3]
#         dragon_id = data[4]
#         continent, status = get_all_city()
#         if (status == False):
#             try:
#                 bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
#             except Exception as e:
#                 bot.send_message(admin_chat_id, 'پیام حذف نشد از لشکر کشی')
#             bot.send_message(chat_id='1889589121', text=continent)
#             send_welcome(call.message)
#             return
#         markup = types.InlineKeyboardMarkup(row_width=2)
#         markup_list = []
#         for item in continent:
#             markup_list.append(
#                 types.InlineKeyboardButton(text=item[1], callback_data=f'send_dragon_destination_{item[0]}_{send_city}_{dragon_id}'))
#         item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
#         markup.add(*markup_list,  item2)
#
#         bot.edit_message_text('مقصد حرکتی خود را انتخاب کنید', chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               reply_markup=markup)
#     except Exception as e:
#         send_admin('send_city', e, call.from_user.username)
# @bot.callback_query_handler(func=lambda call: call.data.startswith("send_dragon_destination"))
# def send_dragon_destination_thread(call):
#     bot.answer_callback_query(call.id, "در حال پردازش...")
#     if is_spamming(call.message.chat.id):
#         bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
#         return
#     run_in_thread(send_dragon_destination, call)
# def send_dragon_destination(call):
#     try:
#         bot.answer_callback_query(call.id)
#
#         data = call.data.split('_')
#         parent_id = data[3]
#         send_city = data[4]
#         dragon_id = data[5]
#         country, status = get_city_by_parent_id(parent_id)
#         if not status:
#             try:
#                 bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
#             except Exception as e:
#                 bot.send_message(admin_chat_id, f'{e}\nپیام حذف نشد از لشکر کشی')
#             bot.send_message(chat_id=admin_chat_id, text=country)
#             send_welcome(call.message)
#             return
#
#         markup = types.InlineKeyboardMarkup(row_width=2)
#         markup_list = []
#         for item in country:
#             markup_list.append(types.InlineKeyboardButton(text=item[1], callback_data=f'campaign_dragon_confirm_{item[0]}_{send_city}_{dragon_id}'))
#         item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
#         markup.add(*markup_list,  item2)
#         bot.edit_message_text('قلعه مقصد خود را انتخاب کنید', chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               reply_markup=markup)
#     except Exception as e:
#         send_admin('send_destination', e, call.from_user.username)
# @bot.callback_query_handler(func=lambda call: call.data.startswith("campaign_dragon_confirm_"))
# def campaign_dragon_confirm_thread(call):
#     bot.answer_callback_query(call.id, "در حال پردازش...")
#     if is_spamming(call.message.chat.id):
#         bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
#         return
#     run_in_thread(campaign_dragon_confirm, call)
# def campaign_dragon_confirm(call):
#     try:
#         bot.answer_callback_query(call.id)
#
#         data = call.data.split('_')
#         city_id = data[3]
#         send_city = data[4]
#         dragon_id = data[5]
#         bot.edit_message_text('زمان رسیدن خود را وارد نمایید', chat_id=call.message.chat.id,message_id=call.message.message_id)
#         bot.register_next_step_handler(call.message,
#                                        lambda message: campaign_dragon_time_confirm(message, city_id, send_city,dragon_id))
#     except Exception as e:
#         send_admin('send_army', e, call.from_user.username)
# def campaign_dragon_time_confirm(message, city_id,send_city, dragon_id):
#     try:
#         duration = message.text  # زمان وارد شده توسط کاربر را از متن پیام بگیرید
#
#         property_text = 'آیا از حرکت اژدها خود اطمینان دارید؟'
#         markup = types.InlineKeyboardMarkup(row_width=2)
#
#         item1 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
#         item2 = types.InlineKeyboardButton("تایید",
#                                            callback_data=f"1campaign_send_dragon_{duration}_{city_id}_{send_city}_{dragon_id}")
#         markup.add(item1, item2)
#         bot.send_message(chat_id=message.chat.id, text=property_text,reply_markup=markup)
#     except Exception as e:
#         send_admin('campaign_confirm', e, message.from_user.username)
# @bot.callback_query_handler(func=lambda call: call.data.startswith("1campaign_send_dragon_"))
# def campaign_send_dragon_thread(call):
#     bot.answer_callback_query(call.id, "در حال پردازش...")
#     if is_spamming(call.message.chat.id):
#         bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
#         return
#     run_in_thread(campaign_send_dragon, call)
# def campaign_send_dragon(call):
#     try:
#         bot.answer_callback_query(call.id)
#         data = call.data.split('_')
#         duration = data[3]
#         city_des_id = int(data[4])
#         send_city = int(data[5])
#         dragon_id = int(data[6])
#         destanation_title, status = get_city_by_id(city_des_id)
#         send_title, status = get_city_by_id(send_city)
#         dragon_title,status = get_dragon_by_id(dragon_id)
#         image = file_id_dragon[dragon_id]
#         property_text = (f'اژدها {dragon_title[0][1]} از مبدا {send_title[0][1]} به پرواز درآمد. '
#                          f'\n'
#                          f' مقصد {destanation_title[0][1]}'
#                          f'\n\n'
#                          f' زمان رسیدن :{duration}')
#         username = call.from_user.username
#         first_name = call.from_user.first_name
#         property_text += f"\n\n\nفرمانده {first_name}\n@{username}"
#         bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
#         bot.send_photo(chat_id=group_chat_id, photo=image,caption= property_text)
#
#     except Exception as e:
#         print(e)
#         send_admin('send_army', e, call.from_user.username)
# @bot.callback_query_handler(func=lambda call: call.data=="other_desired_dragon")
# def other_desired_dragon_thread(call):
#     bot.answer_callback_query(call.id, "در حال پردازش...")
#     if is_spamming(call.message.chat.id):
#         bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
#         return
#     run_in_thread(other_desired_dragon, call)
# def other_desired_dragon(call):
#     try:
#         property_text = 'برای بک و یا تغییر مسیر لژدهای خود متن خود را مانند متن نمونه وارد نمایید'
#         property_text += '\n\n '
#         property_text += 'اژدها کراکسیس که از مبدا Winterfell به پرواز درآمده بود مسیر خود را به طرف Oldcastle تغییر داد \n زمان رسیدن 20:30. '
#         property_text += 'برای لغو انصراف بنویسید'
#         bot.edit_message_text(property_text, chat_id=call.message.chat.id, message_id=call.message.message_id,)
#         bot.register_next_step_handler(call.message,
#                                        lambda message: send_other_desired_dragon(message))
#     except Exception as e:
#         send_admin('property_message', e, call.from_user.username)
# def send_other_desired_dragon(message):
#     try:
#         empty_markup = types.ReplyKeyboardRemove()
#         username = message.from_user.username
#         first_name = message.from_user.first_name
#         if message.text == "انصراف":
#             bot.send_message(chat_id=message.chat.id, text='حرکت اژدها لغو شد', reply_markup=empty_markup)
#             send_welcome(message)
#             return
#         dragon_id,status = get_my_dragon(message.chat.id)
#         image = file_id_dragon[dragon_id[0][0]]
#         text = message.text
#         text += (f"\n"
#                  f"\n"
#                  f"\n"
#                  f"فرمانده {first_name}\n"
#                  f"@{username}")
#         bot.send_photo(chat_id=group_chat_id, photo=image, caption=text)
#         bot.send_message(chat_id=message.chat.id, text='لشکر کشی با موفقیت انجام شد', reply_markup=empty_markup)
#         send_welcome(message)
#     except Exception as e:
#         send_admin('send_desired_campaign', e, message.from_user.username)
#endregion

#region اضافه کردن منابع و ساختمان
@bot.message_handler(commands=['add_resource'])
def add_resource(message):
    try:
        # بررسی کنید که کاربر ادمین باشد
        if message.from_user.id != int(admin_chat_id) and message.from_user.id != int(admin_chat_second_id) and message.from_user.id != int(admin_chat_tree_id):
            bot.send_message(chat_id=message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن بیا موزم 🍌رو بگیر")
            bot.send_message(chat_id=admin_chat_id,
                             text=f' {message.from_user.first_name} \n @{message.from_user.username} \n دسترسی غیر مجاز برای کم یا زیاد کردن دارایی')
            return

        all_resource, status = get_all_resource()
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup_list = []
        for item in all_resource:
            markup_list.append(
                types.InlineKeyboardButton(text=item[1], callback_data=f'add_resource_{item[0]}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(*markup_list, item2)

        bot.send_message(chat_id=message.chat.id, text='نوع دارایی را انتخاب نمایید',
                         reply_markup=markup)

    except Exception as e:
        bot.send_message(admin_chat_id, str(e))

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_resource_"))
def handle_add_resource(call):
    try:
        if call.from_user.id != int(admin_chat_id) and call.from_user.id != int(admin_chat_second_id) and call.from_user.id != int(admin_chat_tree_id):
            bot.send_message(chat_id=call.message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن بیا موزم 🍌رو بگیر")
            bot.send_message(chat_id=admin_chat_id,
                             text=f' {call.from_user.first_name} \n @{call.from_user.username} \n دسترسی غیر مجاز برای کم یا زیاد کردن دارایی')
            return
        bot.answer_callback_query(call.id)
        data = call.data.split('_')
        resource_id = data[2]

        bot.send_message(chat_id=call.message.chat.id, text='تعداد را وارد نمایید')
        # استفاده از lambda برای پاس دادن resource_id
        bot.register_next_step_handler(call.message, lambda message: add_resource_config(message, resource_id))


    except Exception as e:
        bot.send_message(admin_chat_id, str(e))
def add_resource_config(message, resource_id):
    try:
        # بررسی کنید که کاربر ادمین باشد
        if message.from_user.id != int(admin_chat_id) and message.from_user.id != int(admin_chat_second_id) and message.from_user.id != int(admin_chat_tree_id):
            bot.send_message(chat_id=message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن بیا موزم🍌 رو بگیر")
            bot.send_message(chat_id=admin_chat_id,
                             text=f' {message.from_user.first_name} \n @{message.from_user.username} \n دسترسی غیر مجاز برای کم یا زیاد کردن دارایی')
            return
        text, status = resource_add(message.chat.id, resource_id, message.text)

        bot.send_message(message.chat.id, text)

    except Exception as e:
        bot.send_message(admin_chat_id, str(e))

@bot.message_handler(commands=['cost_resource'])
def costs_resource(message):
    try:

        # بررسی کنید که کاربر ادمین باشد
        if message.from_user.id != int(admin_chat_id) and message.from_user.id != int(admin_chat_second_id) and message.from_user.id != int(admin_chat_tree_id):
            bot.send_message(chat_id=message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن بیا موزم 🍌رو بگیر")
            bot.send_message(chat_id=admin_chat_id,
                             text=f' {message.from_user.first_name} \n @{message.from_user.username} \n دسترسی غیر مجاز برای کم یا زیاد کردن دارایی')
            return

        all_resource, status = get_all_resource()
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup_list = []
        for item in all_resource:
            markup_list.append(
                types.InlineKeyboardButton(text=item[1], callback_data=f'costs_resource_{item[0]}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(*markup_list, item2)

        bot.send_message(chat_id=message.chat.id, text='نوع دارایی برای کم شدن را انتخاب کنید',
                         reply_markup=markup)

    except Exception as e:
        bot.send_message(admin_chat_id, str(e))

@bot.callback_query_handler(func=lambda call: call.data.startswith("costs_resource_"))
def costs_resource(call):
    try:
        # اصلاح دسترسی به شناسه کاربر
        if call.from_user.id != int(admin_chat_id) and call.from_user.id != int(admin_chat_second_id) and call.from_user.id != int(admin_chat_tree_id):
            bot.send_message(chat_id=call.message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن بیا موزم🍌 رو بگیر")
            bot.send_message(chat_id=admin_chat_id,
                             text=f' {call.from_user.first_name} \n @{call.from_user.username} \n دسترسی غیر مجاز برای کم یا زیاد کردن دارایی')
            return
        bot.answer_callback_query(call.id)
        data = call.data.split('_')
        resource_id = data[2]

        bot.send_message(chat_id=call.message.chat.id, text='تعداد مد نظر برای کم شدن را وارد نمایید')
        # استفاده از lambda برای پاس دادن resource_id
        bot.register_next_step_handler(call.message, lambda message: costs_resource_config(message, resource_id))


    except Exception as e:
        bot.send_message(admin_chat_id, str(e))
def costs_resource_config(message, resource_id):
    try:
        # بررسی کنید که کاربر ادمین باشد
        if message.from_user.id != int(admin_chat_id) and message.from_user.id != int(admin_chat_second_id) and message.from_user.id != int(admin_chat_tree_id):
            bot.send_message(chat_id=message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن بیا موزم🍌 رو بگیر")
            bot.send_message(chat_id=admin_chat_id, text=f' {message.from_user.first_name} \n @{message.from_user.username} \n دسترسی غیر مجاز برای کم یا زیاد کردن دارایی')
            return
        text, status = resource_costs(message.chat.id, resource_id, message.text)

        bot.send_message(message.chat.id, text)

    except Exception as e:
        bot.send_message(admin_chat_id, str(e))

@bot.message_handler(commands=['building_up'])
def add_building(message):
    try:
        # بررسی کنید که کاربر ادمین باشد
        if message.from_user.id != int(admin_chat_id) and message.from_user.id != int(admin_chat_second_id) and message.from_user.id != int(admin_chat_tree_id):
            bot.send_message(chat_id=message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن بیا موزم 🍌رو بگیر")
            bot.send_message(chat_id=admin_chat_id,
                             text=f' {message.from_user.first_name} \n @{message.from_user.username} \n دسترسی غیر مجاز برای کم یا زیاد کردن دارایی')
            return

        all_resource, status = get_all_building()
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup_list = []
        for item in all_resource:
            markup_list.append(
                types.InlineKeyboardButton(text=item[1], callback_data=f'building_up_{item[0]}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(*markup_list, item2)

        bot.send_message(chat_id=message.chat.id, text='نوع ساختمان برای بالابردن را انتخاب نمایید',
                         reply_markup=markup)

    except Exception as e:
        bot.send_message(admin_chat_id, str(e))
@bot.callback_query_handler(func=lambda call: call.data.startswith("building_up"))
def up_level(call):
    try:
        if call.from_user.id != int(admin_chat_id) and call.from_user.id != int(admin_chat_second_id) and call.from_user.id != int(admin_chat_tree_id):
            bot.send_message(chat_id=call.message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن بیا موزم 🍌رو بگیر")
            bot.send_message(chat_id=admin_chat_id,
                             text=f' {call.from_user.first_name} \n @{call.from_user.username} \n دسترسی غیر مجاز برای کم یا زیاد کردن دارایی')
            return
        bot.answer_callback_query(call.id)
        data = call.data.split('_')
        building_id = data[2]
        property_text = get_up_level(call.message.chat.id, building_id)
        bot.send_message(chat_id=call.message.chat.id, text=property_text)

    except Exception as e:
        bot.send_message(admin_chat_id, str(e))
@bot.message_handler(commands=['building_down'])
def cost_building(message):
    try:
        # بررسی کنید که کاربر ادمین باشد
        if message.from_user.id != int(admin_chat_id) and message.from_user.id != int(admin_chat_second_id) and message.from_user.id != int(admin_chat_tree_id):
            bot.send_message(chat_id=message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن بیا موزم 🍌رو بگیر")
            bot.send_message(chat_id=admin_chat_id,
                             text=f' {message.from_user.first_name} \n @{message.from_user.username} \n دسترسی غیر مجاز برای کم یا زیاد کردن دارایی')
            return

        all_resource, status = get_all_building()
        markup = types.InlineKeyboardMarkup(row_width=3)
        markup_list = []
        for item in all_resource:
            markup_list.append(
                types.InlineKeyboardButton(text=item[1], callback_data=f'building_down_{item[0]}'))
        item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
        markup.add(*markup_list, item2)

        bot.send_message(chat_id=message.chat.id, text='نوع ساختمان برای کم کردن واحد را انتخاب نمایید',
                         reply_markup=markup)

    except Exception as e:
        bot.send_message(admin_chat_id, str(e))
@bot.callback_query_handler(func=lambda call: call.data.startswith("building_down"))
def down_level(call):
    try:
        if call.from_user.id != int(admin_chat_id) and call.from_user.id != int(admin_chat_second_id) and call.from_user.id != int(admin_chat_tree_id):
            bot.send_message(chat_id=call.message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن بیا موزم 🍌رو بگیر")
            bot.send_message(chat_id=admin_chat_id,
                             text=f' {call.from_user.first_name} \n @{call.from_user.username} \n دسترسی غیر مجاز برای کم یا زیاد کردن دارایی')
            return
        bot.answer_callback_query(call.id)
        data = call.data.split('_')
        building_id = data[2]
        property_text = get_down_level(call.message.chat.id, building_id)
        bot.send_message(chat_id=call.message.chat.id, text=property_text)

    except Exception as e:
        bot.send_message(admin_chat_id, str(e))
#endregion

#region داریی شاپ
@bot.message_handler(commands=['promotion_1'])
def add_city(message):
    try:
        # بررسی کنید که کاربر ادمین باشد
        if message.from_user.id not in [int(admin_chat_id), int(admin_chat_second_id), int(admin_chat_tree_id)]:
            bot.send_message(chat_id=message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن")
            return
        text = promotion(message.chat.id,1)
        bot.send_message(message.chat.id, text)
        bot.send_message(admin_chat_id,text='تاسیس الماس انجام شد')

    except Exception as e:
        bot.send_message(admin_chat_id, str(e))
@bot.message_handler(commands=['promotion_2'])
def add_city(message):
    try:
        # بررسی کنید که کاربر ادمین باشد
        if message.from_user.id not in [int(admin_chat_id), int(admin_chat_second_id), int(admin_chat_tree_id)]:
            bot.send_message(chat_id=message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن")
            return
        text = promotion(message.chat.id,2)
        bot.send_message(message.chat.id, text)
        bot.send_message(admin_chat_id,text='تاسیس طلایی ای انجام شد')

    except Exception as e:
        bot.send_message(admin_chat_id, str(e))
@bot.message_handler(commands=['promotion_3'])
def add_city(message):
    try:
        # بررسی کنید که کاربر ادمین باشد
        if message.from_user.id not in [int(admin_chat_id), int(admin_chat_second_id), int(admin_chat_tree_id)]:
            bot.send_message(chat_id=message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن")
            return
        text = promotion(message.chat.id,3)
        bot.send_message(message.chat.id, text)
        bot.send_message(admin_chat_id,text='تاسیس نقره ای انجام شد')
    except Exception as e:
        bot.send_message(admin_chat_id, str(e))
@bot.message_handler(commands=['base_property'])
def add_city(message):
    try:
        # بررسی کنید که کاربر ادمین باشد
        if message.from_user.id not in [int(admin_chat_id), int(admin_chat_second_id), int(admin_chat_tree_id)]:
            bot.send_message(chat_id=message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن")
            return
        text = promotion(message.chat.id,4)
        bot.send_message(message.chat.id, text)

    except Exception as e:
        bot.send_message(admin_chat_id, str(e))
@bot.message_handler(commands=['remove_property'])
def remove_city(message):
    try:
        # بررسی کنید که کاربر ادمین باشد
        if message.from_user.id not in [int(admin_chat_id), int(admin_chat_second_id), int(admin_chat_tree_id)]:
            bot.send_message(chat_id=message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن")
            return
        text = get_remove_property(message.chat.id)
        bot.send_message(message.chat.id, text)

    except Exception as e:
        bot.send_message(admin_chat_id, str(e))
@bot.message_handler(commands=['up_city'])
def up_city(message):
    try:
        # بررسی کنید که کاربر ادمین باشد
        if message.from_user.id not in [int(admin_chat_id), int(admin_chat_second_id), int(admin_chat_tree_id)]:
            bot.send_message(chat_id=message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن")
            return
        text = get_up_city(message.chat.id)
        bot.send_message(message.chat.id, text)

    except Exception as e:
        bot.send_message(admin_chat_id, str(e))
#endregion

#region تشخیص اژدها
# @bot.message_handler(commands=['add_dragon'])
# def add_dragon(message):
#     try:
#         # بررسی کنید که کاربر ادمین باشد
#         if message.from_user.id not in [int(admin_chat_id), int(admin_chat_second_id), int(admin_chat_tree_id)]:
#             bot.send_message(chat_id=message.chat.id, text="تو کاری که بهت مربوط نیست دخالت نکن")
#             return
#         continent, status = get_all_dragon()
#         markup = types.InlineKeyboardMarkup(row_width=2)
#         markup_list = []
#         for item in continent:
#             markup_list.append(
#                 types.InlineKeyboardButton(text=item[1], callback_data=f'add_chat_dragon_{item[0]}'))
#         item2 = types.InlineKeyboardButton("🔙 بازگشت", callback_data="cansel")
#         markup.add(*markup_list, item2)
#         text = 'یکی از اژدها های زیر را انتخاب کنید'
#         bot.send_message(message.chat.id, text,reply_markup=markup)
#
#     except Exception as e:
#         bot.send_message(admin_chat_id, str(e))
#
# @bot.callback_query_handler(func=lambda call: call.data.startswith("add_chat_dragon_"))
# def ship_thread(call):
#     try:
#         bot.answer_callback_query(call.id)
#         data = call.data.split('_')
#         dragon_id = data[3]
#         dragon_id = int(dragon_id)
#         text = get_add_dragon(dragon_id,call.message.chat.id)
#         bot.send_message(call.message.chat.id, text)
#         bot.delete_message(call.message.chat.id, call.message.message_id)
#     except Exception as e:
#         bot.send_message(admin_chat_id, str(e))
#endregion

#region 🔙 بازگشت
@bot.callback_query_handler(func=lambda call: call.data=="cansel")
def cansel_thread(call):
    bot.answer_callback_query(call.id, "در حال پردازش...")
    if is_spamming(call.message.chat.id):
        bot.send_message(call.message.chat.id, "ّبین هر کلیک 1 ثانیه فاصله بده")
        return
    run_in_thread(cansel, call)
def cansel(call):
    try:
        bot.answer_callback_query(call.id)

        markup = types.InlineKeyboardMarkup(row_width=2)
        row1 = [types.InlineKeyboardButton("🔀 لشکرکشی", callback_data="campaign_message")]
        row2 = [types.InlineKeyboardButton("🗡️ حمله", callback_data="attack_message"),
                types.InlineKeyboardButton("⚔️ محاصره", callback_data="siege_message")]
        row3 = [types.InlineKeyboardButton("ساخت نیرو", callback_data="make_message"),
                types.InlineKeyboardButton("📨 ارسال توئیت", callback_data="tweet_message")]
        row4 = [types.InlineKeyboardButton("📦 تجارت", callback_data="business_message")]
        row5 = [types.InlineKeyboardButton("🪙 دارایی", callback_data="property_message")]
        # row6 = [types.InlineKeyboardButton("حرکت اژدها", callback_data="dragon_message")]


        markup.add(*row1)
        markup.add(*row2)
        markup.add(*row3)
        markup.add(*row4)
        markup.add(*row5)
        # markup.add(*row6)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="دستور خود را وارد نمایید", reply_markup=markup)
    except Exception as e:
        send_admin('cansel', e, call.from_user.username)
#endregion

#region اضافه کردن شهر به دیتابیس
@bot.message_handler(commands=['add_database'])
def add_database(message):
    try:
        # بررسی کنید که کاربر ادمین باشد
        if message.chat.id != int(admin_panel):
            author = message.from_user.username if message.from_user.username else message.from_user.first_name
            bot.send_message(chat_id=admin_chat_id, text=f"@{author} \n"
                                                         f"تلاش کرد که به پنل ادمین دسترسی پیدا کند")
            return

        all_city, status = get_all_city()
        if not status or not all_city:  # بررسی اگر شهرها دریافت نشدند
            bot.send_message(message.chat.id, "❌ خطا در دریافت لیست اقلیم‌ها.")
            return

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup_list = [types.InlineKeyboardButton(text=item[1], callback_data=f'city_add_{item[0]}') for item in
                       all_city]
        markup.add(*markup_list, types.InlineKeyboardButton(" 🔙 بازگشت", callback_data="cancel"))

        bot.send_message(chat_id=message.chat.id, text='🌍 اقلیم مورد نظر را انتخاب کنید:',
                         reply_markup=markup)

    except Exception as e:
        bot.send_message(admin_chat_id, f"❌ خطا در اجرای `add_database`:\n{str(e)}")


@bot.callback_query_handler(func=lambda call: call.data.startswith("city_add_"))
def city_add(call):
    try:
        data = call.data.split('_')
        if len(data) < 3:  # بررسی تعداد داده‌های دریافت‌شده
            bot.send_message(call.message.chat.id, "❌ خطا: مقدار `parent_id` نامعتبر است.")
            return

        parent_id = data[2]
        bot.send_message(chat_id=call.message.chat.id, text='🏰 نام قلعه را وارد نمایید:')

        # استفاده از lambda برای پاس دادن parent_id
        bot.register_next_step_handler(call.message, lambda message: add_city_config(message, parent_id))

    except Exception as e:
        bot.send_message(admin_chat_id, f"❌ خطا در `city_add`:\n{str(e)}")


def add_city_config(message, parent_id):
    try:
        title = message.text.strip()
        if not title:  # بررسی اگر ورودی خالی باشد
            bot.send_message(message.chat.id, "❌ نام قلعه نمی‌تواند خالی باشد. لطفاً دوباره وارد کنید.")
            bot.register_next_step_handler(message, lambda msg: add_city_config(msg, parent_id))
            return

        bot.send_message(chat_id=message.chat.id, text='👑 خاندان خود را وارد نمایید:')
        bot.register_next_step_handler(message, lambda msg: add_family_config(msg, parent_id, title))

    except Exception as e:
        bot.send_message(admin_chat_id, f"❌ خطا در `add_city_config`:\n{str(e)}")


def add_family_config(message, parent_id, title):
    try:
        family = message.text.strip()
        if not family:  # بررسی اگر ورودی خالی باشد
            bot.send_message(message.chat.id, "❌ نام خاندان نمی‌تواند خالی باشد. لطفاً دوباره وارد کنید.")
            bot.register_next_step_handler(message, lambda msg: add_family_config(msg, parent_id, title))
            return

        text = add_city_database(parent_id, title, family)
        bot.send_message(message.chat.id, text)

    except Exception as e:
        bot.send_message(admin_chat_id, f"❌ خطا در `add_family_config`:\n{str(e)}")


#endregion

@bot.message_handler(func=lambda message: 'هزینه ارتقا' in message.text.lower())
def all_building_costs(message):
    try:
       text = get_all_building_costs_and_profits()
       bot.send_message(chat_id=message.chat.id, text=text)
    except Exception as e:
        bot.send_message(admin_chat_id, e)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        # بزرگترین اندازه تصویر ارسال شده را انتخاب کنید
        file_id = message.photo[-1].file_id
        print(file_id)
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")
def main():
    try:
        bot.polling(non_stop=True, interval=0, timeout=30)
    except Exception:
        time.sleep(5)
        main()

if __name__ == "__main__":
    main()
