### الحمدلله
import mimetypes
import subprocess

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, Bot, ParseMode
import os
import logging
from datetime import datetime, timedelta
import yaml
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    ConversationHandler,
)

keyboard_layout = {
    "start": [],
}
TOKEN = "7118089972:AAGeuHugpqcbDPNqVptKxtBdb66EcSaOEmY"
bot = Bot(TOKEN)
SAVE_FILE = "savefile.yaml"
LOGGING_FILE = "bot_logs.yaml"
ADD_REMOVE = 1
file_id_counter = 1
SET_LANGUAGE = 2
password = "Lime"
reset_pass = "ResetMe420UwU"
unsubscribers = set()
subscribers = set()
regular_user_commands = ['/start', '/help', '/upcoming']
admin_commands = ['/start', '/help', '/upcoming', '/upset', '/sendall']
preserved_names = [
    "cancel",
    "add/remove",
    "عودة",
    "download file",
    password,
    reset_pass,
]
upcoming_events = [{
    "date": datetime(1980, 1, 1),
    "name": "??!?",
    "dayofweek": 0
}]
name_convert = {
    "state_to_idfilename": {"start.": "0.ext"},
    "idfilename_to_orname": {"0.ext": "0.ext"},
}
messages = {
    "english": {
        "hello":
            "Hello!\nI am a bot made to help you study any subject with ease, with work sheets, explanations, and "
            "exam papers prepared by the best of our teachers. Navigate using the button keyboard on the right "
            "side of your text box. To learn more you can use /help",
        "choose_option":
            "Choose an option:",
        "cancelled":
            "Operation cancelled.",
        "file_downloaded":
            "File uploaded successfully.",
        "no_file_found":
            "No file found.",
        "button_removed":
            "Button <code>{button_name}</code> removed successfully.",
        "button_added":
            "Button <code>{button_name}</code> added successfully.",
        "button_pressed":
            "You entered <code>{pressed_button}</code>.",
        "no_file_for_state":
            "This file hasn't been added yet.",
        "unworthy":
            "Please enter admin mode to continue with this action.",
        "lang_changed":
            "Language set to English.",
        "add_remove_prompt":
            "Please enter the name of the button you want to add or remove. Type <code>cancel</code> to cancel "
            "this update.",
        "reset":
            "Operation BOMB has been done agent 69.",
        "reset_pass":
            f"The password to reset the bot is <code>{reset_pass}</code>. Send it to perform this operation.\n"
            f"Warning: This will reset the entire bot, including all uploaded files and remove all buttons.",
        "choose_lang":
            "Choose your language:",
        "lang_not_supported":
            "This language is not supported.",
        "help":
            '''💫 Welcome to Syrian Stars School's bot!
This bot will help you get our latest news, and find all you need in terms of work sheets, explanations, past exam papers, and more!

💫 Main commands:

🌟 /start - to restart the bot
🌟 /setlang - to change the bot's language
🌟 /sub - to subscribe to our news and announcements
🌟 /unsub - to unsubscribe from our news and announcements
🌟 /upcoming - to show upcoming events
^
📌 Facebook: 
https://www.facebook.com/profile.php?id=100071613814495
📌 Mobile:
+963 959 303 022
📌 Location: 
https://maps.app.goo.gl/iVrceWoGB4xksFiA8
We are open from 8:00 until 13:00 on work days.

📌 The bot's developers:
@Sir_Lime @SimaSandouk @ZaidKhorsi @Abdullah_Kassar
Feel free to contact us to report a bug or request a new feature.''',
        "admin_help": '''
🛠 Admin Mode commands:

⚙️ Add/Remove
To add a button: Enter the name of the button you want to add. This name should be unique among the rest of the buttons in the current subcategory. You can add more than one button to the same row by separating their names with commas <code>,</code>.
To remove a button: Enter the name of the button you want to remove from the subcategory. All buttons and files inside this button will be deleted. Names must completely match for the removal operation to work. 
To cancel this operation, type and send <code>cancel</code>.

⚙️ /sendall ~Message~
To send the specified message to all subscribed users.

⚙️ /upset ~Event date in format: <b>YYYY-MM-DD</b>~ ~Event name~
To set an upcoming event on the specified date.
Example:
<code>/upset 2025-04-17 عطلة عيد الجلاء</code>

⚙️ /reset
To reset the bot. Be careful and 100% sure you want to delete all files and buttons before proceeding with this operation.

🛠 To upload a file:
1 - Add the button which you want to send the file in the desired destination with its name followed by a period <code>.</code>.
2 - Enter the newly added button ending with a <code>.</code> and send the desired file.
3 - File can now be retrieved using the <code>Download File</code> button.

''',
        "subbed":
            "You subscribed to our news and announcements successfully.",
        "unsubbed":
            "You unsubscribed from our news and announcements successfully.",
        "sendall_args":
            "Usage: /sendall ~Message~",
        "upcoming_event":
            "<b>{day_of_week} {event_date} ({days_left} day(s)):</b>\n"
            "{event_name}",
        "upset_past":
            "You can't add an event in the past.",
        "upcoming_set":
            "Upcoming event set: {event_name} on {day_of_week} {event_date}.",
        "upcoming_args":
            "Usage: /upset ~date <b>YYYY-MM-DD</b>~ ~event~.",
        "no_events":
            "No upcoming events to show.",
        "update_success":
            "Update applied successfully",
        "try_again":
            "User has no data. Please try again.",
    },
    "arabic": {
        "hello":
            "مرحباً!\n"
            " انا بوت سيقوم بمساعدتك بدراسة أي مادة بسهولة عن طريق اوراق العمل, الشروحات, و النماذج "
            "الامتحانية من قبل نخبة معلمينا. يمكنك التنقل عبر البوت من خلال كيبورد الأزرار على يمين مساحة"
            " الكتابة. لمعرفة المزيد يمكنك استخدام"
            " /help",
        "choose_option":
            "اختر خيارًا:",
        "cancelled":
            "تم الغاء العملية.",
        "file_downloaded":
            "تم رفع الملف بنجاح.",
        "no_file_found":
            "لم يتم العثور على ملف.",
        "button_removed":
            "تمت إزالة الزر <code>{button_name}</code> بنجاح.",
        "button_added":
            "تمت إضافة الزر <code>{button_name}</code> بنجاح.",
        "button_pressed":
            "لقد دخلت الى <code>{pressed_button}</code>.",
        "no_file_for_state":
            "لم تتم اضافة هذا الملف بعد.",
        "unworthy":
            "يرجى دخول وضع الادارة للقيام بهذا العمل.",
        "lang_changed":
            "تم تعيين اللغة إلى العربية.",
        "add_remove_prompt":
            "الرجاء إدخال اسم الزر الذي تريد إضافته أو إزالته. اكتب "
            "<code>cancel</code> "
            "من اجل الغاء هذا التعديل.",
        "reset":
            "تمت إعادة الضبط, عميل 47.",
        "reset_pass":
            f"كلمة المرور لإعادة ضبط البوت هي "
            f"<code>{reset_pass}</code>. "
            f" أرسلها للقيام بهذه العملية.\n"
            f"تحذير: هذه العملية تعيد ضبط البوت بأكمله و من ضمن ذلك الملفات"
            f" المرفوعة و الأزرار.",
        "choose_lang":
            "اختر لغتك:",
        "lang_not_supported":
            "هذه اللغة غير مدعومة.",
        "help":
            '''💫 اهلاً بك في بوت مدرسة نجوم سورية! 
هذا البوت سيساعدك في الحصول على أحدث أخبارنا، و إيجاد كل ما تحتاجه من أوراق العمل، شرح للدروس، أسئلة دورات, وأكثر!

💫 الأوامر الأساسية:

🌟 /start - لإعادة تشغيل البوت
🌟 /setlang - لتغيير لغة البوت
🌟 /sub - للاشتراك بأخبارنا وإعلاناتنا
🌟 /unsub - لإلغاء الاشتراك بأخبارنا وإعلاناتنا
🌟 /upcoming - لإظهار قائمة بالأحداث المقبلة
^
📌 فيسبوك: 
https://www.facebook.com/profile.php?id=100071613814495
📌 موبايل:
+963 959 303 022
📌 الموقع: 
https://maps.app.goo.gl/iVrceWoGB4xksFiA8
نفتح بين الساعة 8 صباحاً و ال1 ظهراً في أيام الدوام.

📌 مبرمجو البوت:
@Sir_lime @SimaSandouk @ZaidKhorsi @Abdullah_Kassar
يمكنك التواصل معنا للإبلاغ عن مشكلة او طلب ميزة جديدة.
''',
        "admin_help": ''' 🛠 أوامر وضع الإدارة:

⚙️ Add/Remove
لإضافة زر: ادخل اسم الزر الجديد الذي تريد إضافته, هذا الاسم يجب أن يكون مختلفاً عن باقي الأسماء في القائمة الحالية, يمكنك إضافة أكثر من زر إلى نفس الصف من خلال كتابة أسمائهم مع وضع فاصلة <code>,</code> بينهم.
 لحذف زر: ادخل اسم الزر الذي تريد حذفه في القائمة الحالية, سيتم حذف الزر مع جميع الأزرار التي بداخل هذا الزر, يجب أن تتطابق الأسماء لتتم عملية الحذف.
للخروج من هذه التعليمة: قم بإرسال: <code>cancel</code>

⚙️ /sendall ~الرسالة التي تريد ارسالها~
لإرسال الرسالة المحددة إلى جميع المستخدمين المشتركين في الأخبار.

⚙️ /upset ~تاريخ الحدث بصيغة <b>YYYY-MM-DD</b>~ ~اسم الحدث~
لتعيين حدث جديد في التاريخ المعين.
مثال:
<code>/upset 2025-04-17 عطلة عيد الجلاء</code>

⚙️ /reset
لإعادة ضبط البوت. كن حذراً وواثقاً تماماً أنك تريد حذف جميع الأزرار و الملفات قبل القيام بهذه العملية.

🛠 لرفع ملف:
1 - أضف الزر الذي تريد أن يُرسِل الملف في المكان المطلوب مع اسمه ملحوقاً بنقطة <code>.</code> .
2 - ادخل إلى الزر الجديد المنتهي اسمه بنقطة ثم أرسل الملف المطلوب.
 3 - يمكنك الآن تنزيل الملف من خلال زر <code>Download File</code>.

''',
        "subbed":
            "تم الاشتراك باخبارنا و اعلاناتنا بنجاح.",
        "unsubbed":
            "تم الغاء الاشتراك باخبارنا و اعلاناتنا بنجاح.",
        "sendall_args":
            "الاستخدام:\n/sendall <النص>",
        "upcoming_event":
            "<b>{day_of_week} {event_date} (بعد {days_left} أيام):</b>\n"
            "{event_name}",
        "upset_past":
            "لا يمكنك اضافة حدث في الماضي.",
        "upcoming_set":
            "تم تحديد حدث: {event_name} يوم {day_of_week} {event_date}.",
        "upcoming_args":
            "الاستخدام:"
            "\n /upset ~<b>YYYY-MM-DD</b> الحدث~ ~التاريخ~",
        "no_events":
            "لا توجد احداث قادمة.",
        "update_success":
            "تم التعديل بنجاح.",
        "try_again":
            "لا توجد بيانات للمستخدم. ترجى اعادة المحاولة.",
    },
}
week_days = {
    "english": {
        0: "Sunday",
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday",
    },
    "arabic": {
        0: "الاحد",
        1: "الاثنين",
        2: "الثلاثاء",
        3: "الاربعاء",
        4: "الخميس",
        5: "الجمعة",
        6: "السبت",
    },
}


def help_message(update, context):
    check_data(update, context)
    message = messages[context.user_data["language"]]["help"]
    if context.user_data["admin"]:
        x = message.split("^", maxsplit=1)
        update.message.reply_text(
            x[0] + messages[context.user_data["language"]]["admin_help"] +
            x[1], parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(message.replace("^", ""), parse_mode=ParseMode.HTML)


def setup_logger(log_filename):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    class CustomYamlFormatter(logging.Formatter):

        def format(self, record):
            log_entry = {
                "Timestamp": self.formatTime(record),
                "Level": record.levelname,
                "Module": record.module,
                "Message": record.getMessage(),
            }
            standard_attributes = set(vars(logging.LogRecord('', 0, '', 0, '', (), None)))
            extra_attributes = {
                key: value for key, value in record.__dict__.items()
                if key not in standard_attributes
            }
            log_entry.update(extra_attributes)

            return yaml.dump(log_entry,
                             default_flow_style=False,
                             indent=4,
                             sort_keys=False)

    yaml_formatter = CustomYamlFormatter()
    file_handler.setFormatter(yaml_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def set_upcoming(update, context):
    global upcoming_events
    upcoming_events = list(upcoming_events)
    check_data(update, context)
    if not context.user_data["admin"]:
        update.message.reply_text(
            messages[context.user_data["language"]]["unworthy"],
            parse_mode=ParseMode.HTML)
        return
    try:
        message_parts = update.message.text.split(" ")
        temp = {
            "name": " ".join(message_parts[2:]),
            "date": datetime.strptime(message_parts[1], "%Y-%m-%d")
        }
        if temp["date"].strftime('%Y-%m-%d') < datetime.today().strftime('%Y-%m-%d'):
            update.message.reply_text(
                messages[context.user_data["language"]]["upset_past"],
                parse_mode=ParseMode.HTML)
            return
        temp["dayofweek"] = int(temp["date"].strftime('%w'))
        left = 0
        right = len(upcoming_events) - 1
        while left <= right:
            mid = int((left + right) / 2)
            if upcoming_events[mid]["date"] > temp["date"]:
                right = mid - 1
            else:
                left = mid + 1
        upcoming_events.insert(left, temp)
        update.message.reply_text(
            messages[context.user_data["language"]]["upcoming_set"].format(
                event_name=upcoming_events[left]["name"],
                event_date=upcoming_events[left]["date"].strftime("%Y-%m-%d"),
                day_of_week=week_days[context.user_data["language"]][
                    upcoming_events[left]["dayofweek"]],
            ),
            parse_mode=ParseMode.HTML)
        log.info(
            f"User: {update.message.from_user.username} set upcoming event: {upcoming_events[left]['name']}",
            extra={"action": "EVENT_SET"})
    except Exception as e:
        print(e)
        update.message.reply_text(
            messages[context.user_data["language"]]["upcoming_args"],
            parse_mode=ParseMode.HTML)
    save()


def upcoming(update, context):
    global upcoming_events
    check_data(update, context)
    message = ""
    toremove = []
    cnt = 0
    for i, event in enumerate(upcoming_events):
        if event["date"].strftime('%Y-%m-%d') < datetime.today().strftime(
                '%Y-%m-%d'):
            if event["name"] != "??!?":
                toremove.append(i)
            continue
        cnt += 1
        delta = event["date"] - datetime.today() + timedelta(days=1)
        message += messages[
            context.user_data["language"]]["upcoming_event"].format(
            event_name=event["name"],
            day_of_week=week_days[context.user_data["language"]][
                event["dayofweek"]],
            event_date=event["date"].strftime('%d/%m/%Y'),
            days_left=delta.days,
        )
        message += '\n\n'
    for i in reversed(range(len(toremove))):
        upcoming_events.pop(toremove[i])
    if cnt == 0:
        update.message.reply_text(
            messages[context.user_data["language"]]["no_events"],
            parse_mode=ParseMode.HTML)
        return
    update.message.reply_text(message, parse_mode=ParseMode.HTML)


def send_all(update: Update, context: CallbackContext):
    global subscribers
    check_data(update, context)
    user = context.user_data["id"]
    if context.user_data["admin"] is True:
        message_parts = update.message.text.split(" ", 1)
        if len(message_parts) <= 1:
            update.message.reply_text(
                messages[context.user_data["language"]]["sendall_args"],
                parse_mode=ParseMode.HTML)
            return
        message = message_parts[1]
        log.info(
            f"User {bot.get_chat(user).username} has sent a global message. message='{message}'",
            extra={"action": "GLOBAL_MES"},
        )
        for ID in subscribers:
            try:
                context.bot.send_message(chat_id=ID,
                                         text=message,
                                         parse_mode=ParseMode.HTML)
            except Exception as e:
                print(e)
                pass
    else:
        update.message.reply_text(
            messages[context.user_data["language"]]["unworthy"],
            parse_mode=ParseMode.HTML)


def subscribe(update: Update, context: CallbackContext):
    global bot, subscribers
    check_data(update, context)
    user = context.user_data["id"]
    unsubscribers.discard(user)
    subscribers.add(user)
    save()
    update.message.reply_text(
        messages[context.user_data["language"]]["subbed"],
        parse_mode=ParseMode.HTML)
    log.info(
        f"user: {bot.get_chat(user).username} has subscribed!",
        extra={"action": "USER_SUB"},
    )


def unsubscribe(update: Update, context: CallbackContext):
    global bot
    check_data(update, context)
    user = context.user_data["id"]
    subscribers.discard(user)
    unsubscribers.add(user)
    save()
    update.message.reply_text(
        messages[context.user_data["language"]]["unsubbed"],
        parse_mode=ParseMode.HTML)
    log.info(
        f"user: {bot.get_chat(user).username} has unsubscribed..",
        extra={"action": "USER_UNSUB"},
    )


def reset(update: Update, context: CallbackContext):
    check_data(update, context)
    if context.user_data["admin"]:
        update.message.reply_text(
            messages[context.user_data["language"]]["reset_pass"],
            parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(
            messages[context.user_data["language"]]["unworthy"],
            parse_mode=ParseMode.HTML)


def save():
    global SAVE_FILE, unsubscribers, subscribers, upcoming_events, keyboard_layout, name_convert
    file_path = SAVE_FILE

    serializable_keyboard_configurations = {
        state: [[button.text for button in button_row]
                for button_row in buttons]
        for state, buttons in keyboard_layout.items()
    }

    serializable_configurations = {
        "keyboard": serializable_keyboard_configurations,
        "unsubs": unsubscribers,
        "subs": subscribers,
        "upcoming": upcoming_events,
        "name_convert": name_convert,
        "file_id_counter": file_id_counter,
    }

    with open(file_path, "w") as file:
        yaml.dump(serializable_configurations, file, default_flow_style=False)


def load():
    global SAVE_FILE, unsubscribers, subscribers, upcoming_events, keyboard_layout, file_id_counter, name_convert, log
    try:
        file_path = SAVE_FILE
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)

        keyboard_configurations = data.get("keyboard", {})
        keyboard_configurations_original = {}
        for state, buttons in keyboard_configurations.items():
            original_buttons = [[KeyboardButton(text) for text in button_row]
                                for button_row in buttons]
            keyboard_configurations_original[state] = original_buttons
        keyboard_layout = keyboard_configurations_original

        unsubscribers = set(data.get("unsubs", {}))
        subscribers = set(data.get("subs", {}))
        upcoming_events = data.get("upcoming", {})
        name_convert = data.get("name_convert", {})
        file_id_counter = data.get("file_id_counter", 1)
    except Exception as e:
        log.warning(
            f"Error loading configurations: {e}",
            extra={"Note": "Possibly resolved with a restart."},
        )
        keyboard_layout = {"start": []}
        unsubscribers = set()
        subscribers = set()
        upcoming_events = [{
            "date": datetime(1980, 1, 1),
            "name": "??!?",
            "dayofweek": 0
        }]
        name_convert = {
            "state_to_idfilename": {"start.": "0.ext"},
            "idfilename_to_orname": {"0.ext": "0.ext"}
        }
        file_id_counter = 1
        save()


def remove_branches(branch_state):
    for row in keyboard_layout[branch_state]:
        for button in row:
            remove_branches(branch_state + '_' + button.text)
    if branch_state in name_convert['state_to_idfilename']:
        script_directory = os.path.dirname(os.path.realpath(__file__))
        file_name = name_convert['state_to_idfilename'][branch_state]
        if os.path.exists(os.path.join(script_directory, file_name)):
            os.remove(os.path.join(script_directory, file_name))
        name_convert['state_to_idfilename'].pop(branch_state, None)
        name_convert['idfilename_to_orname'].pop(file_name, None)
    keyboard_layout.pop(branch_state, None)


def add_remove(update: Update, context: CallbackContext):
    if check_data(update, context):
        update.message.reply_text(
            messages[context.user_data["language"]]["try_again"],
            parse_mode=ParseMode.HTML)
        return
    if context.user_data["admin"]:
        update.message.reply_text(
            messages[context.user_data["language"]]["add_remove_prompt"],
            parse_mode=ParseMode.HTML)
        return ADD_REMOVE
    else:
        update.message.reply_text(
            messages[context.user_data["language"]]["unworthy"],
            parse_mode=ParseMode.HTML)
        return


def receive_button_name(update: Update, context: CallbackContext):
    if check_data(update, context):
        update.message.reply_text(
            messages[context.user_data["language"]]["try_again"],
            parse_mode=ParseMode.HTML)
        return
    global password
    global keyboard_layout
    state = context.user_data["state"]
    user_input = update.message.text.split(",")
    updated = False
    keyboard_layout[state].append([])
    for name in user_input:
        name = name.strip()
        if name == "":
            continue
        if name.lower() in preserved_names:
            update.message.reply_text(
                messages[context.user_data["language"]]["cancelled"],
                parse_mode=ParseMode.HTML)
            continue
        updated = True
        ind = 0
        row = 0
        found = False
        for i, buttons in enumerate(keyboard_layout[state]):
            for j, button in enumerate(buttons):
                if button.text == name:
                    ind = j
                    row = i
                    found = True
                    break
        if not found:  # no such button, add it
            keyboard_layout[state][-1].append(KeyboardButton(name))
            keyboard_layout[state + "_" + name] = []
            update.message.reply_text(
                messages[context.user_data["language"]]["button_added"].format(
                    button_name=name),
                parse_mode=ParseMode.HTML)
            log.info(
                f"Button configurations changed by {update.message.from_user.username}",
                extra={
                    "action": "ADD",
                    "button": name
                },
            )
            save()
        else:  # remove this button from its place
            removed_button_name = keyboard_layout[state][row].pop(ind).text
            if len(keyboard_layout[state]
                   [row]) == 0:  # if row becomes empty remove it
                keyboard_layout[state].pop(row)
            removed_state = context.user_data["state"] + '_' + removed_button_name
            remove_branches(removed_state)
            update.message.reply_text(
                messages[context.user_data["language"]]
                ["button_removed"].format(button_name=removed_button_name),
                parse_mode=ParseMode.HTML)
            log.info(
                f"Button configurations changed by {update.message.from_user.username}",
                extra={
                    "action": "REMOVE",
                    "button": name
                },
            )
            save()
    while len(keyboard_layout[state]) and len(keyboard_layout[state][-1]) == 0:
        keyboard_layout[state].pop()
        log.info(
            f"Button configurations changed by system",
            extra={
                "action": "REMOVE",
                "button": "Empty rows"
            },
        )
        save()
    if not updated:
        return ConversationHandler.END
    reply_markup = get_keyboard_markup(context)
    update.message.reply_text(
        messages[context.user_data["language"]]["update_success"],
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def upload_file(update: Update, context: CallbackContext):
    global file_id_counter, name_convert
    if check_data(update, context):
        update.message.reply_text(messages[context.user_data["language"]]["try_again"], parse_mode=ParseMode.HTML)
        return
    if not context.user_data["admin"]:
        update.message.reply_text(messages[context.user_data["language"]]["unworthy"], parse_mode=ParseMode.HTML)
        return
    file_id = ""
    file_name = ""
    needs_extension = False
    extension = ""
    if update.message.photo:
        needs_extension = True
        file_id = update.message.photo[-1].file_id
        file_name = str(file_id_counter)
    elif update.message.video:
        needs_extension = True
        file_id = update.message.video.file_id
        file_name = str(file_id_counter)
    elif update.message.audio:
        file_id = update.message.audio.file_id
        file_name = update.message.audio.file_name
    elif update.message.document:
        file_id = update.message.document.file_id
        file_name = update.message.document.file_name
    elif update.message.voice:
        needs_extension = True
        file_id = update.message.voice.file_id
        extension = ".mp3"
        file_name = str(file_id_counter)
    elif update.message.sticker:
        needs_extension = True
        file_id = update.message.sticker.file_id
        file_name = str(file_id_counter)
    elif update.message.video_note:
        needs_extension = True
        file_id = update.message.sticker.file_id
        extension = ".mp4"
        file_name = str(file_id_counter)
    else:
        update.message.reply_text("File type currently not supported", parse_mode=ParseMode.HTML)
        return
    file = context.bot.get_file(file_id)
    if extension == "":
        extension = os.path.splitext(file.file_path)[1]
    if needs_extension:
        file_name = file_name + extension
    if context.user_data["state"] in name_convert['state_to_idfilename']:  # delete the old file before adding this one
        old_file_name = name_convert['state_to_idfilename'][context.user_data["state"]]
        script_directory = os.path.dirname(os.path.realpath(__file__))
        if os.path.exists(os.path.join(script_directory, old_file_name)):
            os.remove(os.path.join(script_directory, old_file_name))
        name_convert['idfilename_to_orname'].pop(old_file_name, None)
    name_convert['state_to_idfilename'][context.user_data["state"]] = str(file_id_counter) + extension
    name_convert['idfilename_to_orname'][str(file_id_counter) + extension] = file_name
    file.download(str(file_id_counter) + extension)
    file_id_counter += 1
    update.message.reply_text(
        messages[context.user_data["language"]]["file_downloaded"], parse_mode=ParseMode.HTML
    )
    log.info(
        f"File {context.user_data['state'] + '_' + file_name} uploaded by {update.message.from_user.username}",
        extra={"action": "ADMIN_UPLOAD"},
    )
    save()


def button_press(update: Update, context: CallbackContext):
    if check_data(update, context):
        update.message.reply_text(
            messages[context.user_data["language"]]["try_again"],
            parse_mode=ParseMode.HTML)
        return
    pressed_button = update.message.text
    global password, reset_pass, keyboard_layout, name_convert, file_id_counter
    if pressed_button == password:
        context.user_data["admin"] = True
        log.info(
            f"User: {update.message.from_user.username} is now admin",
            extra={"action": "USER_ADMIN"},
        )
    elif pressed_button == reset_pass:
        if not context.user_data["admin"]:
            update.message.reply_text(
                messages[context.user_data["language"]]["unworthy"],
                parse_mode=ParseMode.HTML)
            return
        context.user_data["state"] = "start"
        script_directory = os.path.dirname(os.path.realpath(__file__))
        for file in os.listdir(script_directory):
            if file.endswith(".py") or file.endswith(".yaml"):
                continue
            os.remove(os.path.join(script_directory, file))
        file_id_counter = 1
        name_convert = {
            "state_to_idfilename": {"start.": "0.ext"},
            "idfilename_to_orname": {"0.ext": "0.ext"}
        }
        keyboard_layout = {"start": []}
        reply_markup = get_keyboard_markup(context)
        update.message.reply_text(
            messages[context.user_data["language"]]["reset"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML)
        save()
        return
    elif pressed_button == "Download File":
        if context.user_data["state"] not in name_convert['state_to_idfilename']:
            update.message.reply_text(
                messages[context.user_data["language"]]["no_file_for_state"],
                parse_mode=ParseMode.HTML)
            return
        file_id = name_convert['state_to_idfilename'][
            context.user_data["state"]]
        if not os.path.exists(file_id):
            update.message.reply_text(
                messages[context.user_data["language"]]["no_file_for_state"],
                parse_mode=ParseMode.HTML)
            return
        original_name = name_convert['idfilename_to_orname'][file_id]
        os.rename(file_id, original_name)
        file_type, _ = mimetypes.guess_type(original_name)
        if file_type and file_type.startswith('image'):
            update.message.reply_photo(photo=open(original_name, 'rb'))
        elif file_type and file_type.startswith('video'):
            update.message.reply_video(video=open(original_name, 'rb'))
        elif file_type and file_type.startswith('audio'):
            update.message.reply_audio(audio=open(original_name, 'rb'))
        elif file_type and file_type.startswith('sticker'):
            update.message.reply_sticker(sticker=open(original_name, 'rb'))
        elif file_type:
            update.message.reply_document(document=open(original_name, 'rb'))
        os.rename(original_name, file_id)
        log.info(
            f"File '{file_id}' downloaded by {update.message.from_user.username}",
            extra={"action": "USER_DOWNLOAD"},
        )
        return
    elif pressed_button == "عودة":
        context.user_data["state"] = "start"
    else:
        context.user_data[
            "state"] = context.user_data["state"] + "_" + pressed_button

    if context.user_data["state"] not in keyboard_layout:
        context.user_data["state"] = "start"

    reply_markup = get_keyboard_markup(context)
    if context.user_data["state"] == "start":
        update.message.reply_text(
            messages[context.user_data["language"]]["choose_option"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(
            messages[context.user_data["language"]]["button_pressed"].format(
                pressed_button=pressed_button),
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML)


def select_language(update: Update, context: CallbackContext):
    selected_language = update.message.text.lower()
    if selected_language in messages:
        context.user_data["language"] = selected_language
        update.message.reply_text(
            messages[context.user_data["language"]]["lang_changed"],
            reply_markup=get_keyboard_markup(context),
            parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(
            messages[context.user_data["language"]]["lang_not_supported"],
            reply_markup=get_keyboard_markup(context),
            parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def set_language(update: Update, context: CallbackContext):
    check_data(update, context)
    update.message.reply_text(
        messages[context.user_data["language"]]["choose_lang"],
        reply_markup=get_language_markup(),
        parse_mode=ParseMode.HTML)
    return SET_LANGUAGE


def get_language_markup():
    languages = ["English", "Arabic"]
    keyboard = [[KeyboardButton(lang)] for lang in languages]
    return ReplyKeyboardMarkup(keyboard,
                               resize_keyboard=True,
                               one_time_keyboard=True)


def get_keyboard_markup(context: CallbackContext):
    global keyboard_layout
    state = context.user_data["state"]
    keyboard = keyboard_layout[state].copy()
    if state == "start":
        if context.user_data["admin"]:
            keyboard.append([KeyboardButton("Add/Remove")])
    else:
        if state.endswith("."):
            if context.user_data["admin"]:
                keyboard.append([KeyboardButton("Download File")])
                keyboard.append(
                    [KeyboardButton("Add/Remove"),
                     KeyboardButton("عودة")])
            else:
                keyboard.append(
                    [KeyboardButton("Download File"),
                     KeyboardButton("عودة")])
        else:
            if context.user_data["admin"]:
                keyboard.append(
                    [KeyboardButton("Add/Remove"),
                     KeyboardButton("عودة")])
            else:
                keyboard.append([KeyboardButton("عودة")])

    return ReplyKeyboardMarkup(keyboard,
                               resize_keyboard=True,
                               one_time_keyboard=True)


def check_data(update: Update, context: CallbackContext):
    if ("language" not in context.user_data or "admin" not in context.user_data
            or "id" not in context.user_data
            or "state" not in context.user_data):
        start(update, context)
        return True
    return False

# Function to handle user commands
def handle_command_list(user_role):
    if user_role:
         print("show user commands.")
    elif user_role:
         print("show admin commands.")

def start(update: Update, context: CallbackContext):
    global unsubscribers, subscribers, keyboard_layout, log
    log.info(
        f"Bot started by {update.message.from_user.username}",
        extra={"action": "USER_START"},
    )
    if "language" not in context.user_data:
        context.user_data["language"] = "arabic"
    context.user_data["id"] = update.message.from_user.id
    context.user_data["admin"] = False
    context.user_data["state"] = "start"
    handle_command_list(context.user_data["admin"], );
    if (context.user_data["id"] not in unsubscribers
            and context.user_data["id"] not in subscribers):
        subscribe(update, context)
        log.info(
            f"user: {update.message.from_user.username} added",
            extra={"action": "USER_ADD"},
        )
    reply_markup = get_keyboard_markup(context)
    update.message.reply_text(messages[context.user_data["language"]]["hello"],
                              reply_markup=reply_markup,
                              parse_mode=ParseMode.HTML)
    update.message.reply_text(
        messages[context.user_data["language"]]["choose_option"],
        parse_mode=ParseMode.HTML)

# /update command
def update_bot(update, context):
    # Send a message indicating the update process
    try:
        subprocess.run(['/home/zaid/update_bot.sh'])
        context.bot.send_message(chat_id=update.effective_chat.id, text="Updating bot's code...")
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You don't seem to be hosting the bot on the linux server.")


def main():
    updater = Updater(TOKEN)
    load()
    dp = updater.dispatcher
    global log, LOGGING_FILE
    log.debug("Bot is running...", extra={"action": "BOT_START"})
    conv_handler = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex(r"^Add/Remove$"), add_remove),
            CommandHandler("setlang", set_language),
        ],
        states={
            ADD_REMOVE: [
                MessageHandler(Filters.text & ~Filters.command,
                               receive_button_name)
            ],
            SET_LANGUAGE:
                [MessageHandler(Filters.text & ~Filters.command, select_language)],
        },
        fallbacks=[],
    )
    update_handler = CommandHandler('update_code', update_bot)
    dp.add_handler(
        MessageHandler(Filters.document | Filters.photo | Filters.audio | Filters.video | Filters.voice |
                       Filters.animation | Filters.sticker | Filters.video_note, upload_file))
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(update_handler)
    dp.add_handler(CommandHandler("unsub", unsubscribe))
    dp.add_handler(CommandHandler("sub", subscribe))
    dp.add_handler(CommandHandler("help", help_message))
    dp.add_handler(CommandHandler("sendall", send_all))
    dp.add_handler(CommandHandler("reset", reset))
    dp.add_handler(CommandHandler("upset", set_upcoming))
    dp.add_handler(CommandHandler("upcoming", upcoming))
    dp.add_handler(
        MessageHandler(Filters.text & ~Filters.command, button_press))

    updater.start_polling()
    updater.idle()


log = setup_logger(LOGGING_FILE)

if __name__ == "__main__":
    main()
