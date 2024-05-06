import main
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
            f"The password to reset the bot is <code>{main.reset_pass}</code>. Send it to perform this operation.\n"
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
        "ask_args":
            "Usage: /ask ~Question~",
    },
    "arabic": {
        "hello":
            "مرحباً بك!\n"
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
            f"<code>{main.reset_pass}</code>. "
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
            "الاستخدام:"
            "\n/sendall ~الرسالة~",
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
        "verse_OTD":
            "اية اليوم:",
        "ask_args":
            "الاستخدام: /ask ~السؤال~"
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
