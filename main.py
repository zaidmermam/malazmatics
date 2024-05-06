### الحمدلله if you can see me its working
import mimetypes
import subprocess
import data

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, Bot, BotCommand, ParseMode
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
TOKEN = "6885894371:AAGNeZK41ncT01_hTYCrKzodSDdyCzROHyk"
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
    message = data.messages[context.user_data["language"]]["help"]
    if context.user_data["admin"]:
        x = message.split("^", maxsplit=1)
        update.message.reply_text(
            x[0] + data.messages[context.user_data["language"]]["admin_help"] +
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
            data.messages[context.user_data["language"]]["unworthy"],
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
                data.messages[context.user_data["language"]]["upset_past"],
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
            data.messages[context.user_data["language"]]["upcoming_set"].format(
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
            data.messages[context.user_data["language"]]["upcoming_args"],
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
        message += data.messages[
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
            data.messages[context.user_data["language"]]["no_events"],
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
                data.messages[context.user_data["language"]]["sendall_args"],
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
            data.messages[context.user_data["language"]]["unworthy"],
            parse_mode=ParseMode.HTML)


def subscribe(update: Update, context: CallbackContext):
    global bot, subscribers
    check_data(update, context)
    user = context.user_data["id"]
    unsubscribers.discard(user)
    subscribers.add(user)
    save()
    update.message.reply_text(
        data.messages[context.user_data["language"]]["subbed"],
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
        data.messages[context.user_data["language"]]["unsubbed"],
        parse_mode=ParseMode.HTML)
    log.info(
        f"user: {bot.get_chat(user).username} has unsubscribed..",
        extra={"action": "USER_UNSUB"},
    )


def reset(update: Update, context: CallbackContext):
    check_data(update, context)
    if context.user_data["admin"]:
        update.message.reply_text(
            data.messages[context.user_data["language"]]["reset_pass"],
            parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(
            data.messages[context.user_data["language"]]["unworthy"],
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
            data.messages[context.user_data["language"]]["try_again"],
            parse_mode=ParseMode.HTML)
        return
    if context.user_data["admin"]:
        update.message.reply_text(
            data.messages[context.user_data["language"]]["add_remove_prompt"],
            parse_mode=ParseMode.HTML)
        return ADD_REMOVE
    else:
        update.message.reply_text(
            data.messages[context.user_data["language"]]["unworthy"],
            parse_mode=ParseMode.HTML)
        return


def receive_button_name(update: Update, context: CallbackContext):
    if check_data(update, context):
        update.message.reply_text(
            data.messages[context.user_data["language"]]["try_again"],
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
                data.messages[context.user_data["language"]]["cancelled"],
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
                data.messages[context.user_data["language"]]["button_added"].format(
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
                data.messages[context.user_data["language"]]
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
        data.messages[context.user_data["language"]]["update_success"],
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def upload_file(update: Update, context: CallbackContext):
    global file_id_counter, name_convert
    if check_data(update, context):
        update.message.reply_text(data.messages[context.user_data["language"]]["try_again"], parse_mode=ParseMode.HTML)
        return
    if not context.user_data["admin"]:
        update.message.reply_text(data.messages[context.user_data["language"]]["unworthy"], parse_mode=ParseMode.HTML)
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
        data.messages[context.user_data["language"]]["file_downloaded"], parse_mode=ParseMode.HTML
    )
    log.info(
        f"File {context.user_data['state'] + '_' + file_name} uploaded by {update.message.from_user.username}",
        extra={"action": "ADMIN_UPLOAD"},
    )
    save()


def button_press(update: Update, context: CallbackContext):
    if check_data(update, context):
        update.message.reply_text(
            data.messages[context.user_data["language"]]["try_again"],
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
                data.messages[context.user_data["language"]]["unworthy"],
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
            data.messages[context.user_data["language"]]["reset"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML)
        save()
        return
    elif pressed_button == "Download File":
        if context.user_data["state"] not in name_convert['state_to_idfilename']:
            update.message.reply_text(
                data.messages[context.user_data["language"]]["no_file_for_state"],
                parse_mode=ParseMode.HTML)
            return
        file_id = name_convert['state_to_idfilename'][
            context.user_data["state"]]
        if not os.path.exists(file_id):
            update.message.reply_text(
                data.messages[context.user_data["language"]]["no_file_for_state"],
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
            data.messages[context.user_data["language"]]["choose_option"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(
            data.messages[context.user_data["language"]]["button_pressed"].format(
                pressed_button=pressed_button),
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML)


def select_language(update: Update, context: CallbackContext):
    selected_language = update.message.text.lower()
    if selected_language in data.messages:
        context.user_data["language"] = selected_language
        update.message.reply_text(
            data.messages[context.user_data["language"]]["lang_changed"],
            reply_markup=get_keyboard_markup(context),
            parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(
            data.messages[context.user_data["language"]]["lang_not_supported"],
            reply_markup=get_keyboard_markup(context),
            parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def set_language(update: Update, context: CallbackContext):
    check_data(update, context)
    update.message.reply_text(
        data.messages[context.user_data["language"]]["choose_lang"],
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
    commands = []
    if user_role:
         commands
    elif user_role:
         print("show admin commands.")
    bot.set_my_commands(commands)

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
    update.message.reply_text(data.messages[context.user_data["language"]]["hello"],
                              reply_markup=reply_markup,
                              parse_mode=ParseMode.HTML)
    update.message.reply_text(
        data.messages[context.user_data["language"]]["choose_option"],
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
