

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=(n > 1);
    if (typeof(v) == 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  var newcatalog = {
    "#%(position)s": "#%(position)s", 
    "%(count)s language matches your query.": [
      "So\u2018rovingiz bo\u2018yicha %(count)s ta til topildi"
    ], 
    "%(count)s project matches your query.": [
      "So\u2018rovingiz bo\u2018yicha %(count)s ta natija topildi."
    ], 
    "%(count)s user matches your query.": [
      "So\u2018rovingiz bo\u2018yicha %(count)s ta natija topildi."
    ], 
    "%(timeSince)s via file upload": "%(timeSince)s orqali fayl yuklab qo\u2018yish", 
    "%s word": [
      "%s ta so\u2018z"
    ], 
    "%s's accepted suggestions": "%s's tavsiyalarni qabul qildi", 
    "%s's overwritten submissions": "%s'ning almashtirilgan tarjimalari", 
    "%s's pending suggestions": "%s's tavsiyalar jo\u2018natmoqda", 
    "%s's rejected suggestions": "%s's tavsiyalarni rad qildi", 
    "%s's submissions": "%s's tarjimalari", 
    "(registered tasks)": "(ro\u2018yxatdan o\u2018tgan vazifalar)", 
    "Accept": "Qabul qilish", 
    "Account Activation": "Hisobni faollashtirish", 
    "Account Inactive": "Hisob to\u2018xtatib qo\u2018yilgan", 
    "Action": "Amal", 
    "Active": "Faol", 
    "Add Language": "Til qo\u2018shish", 
    "Add Project": "Loyiha qo\u2018shish", 
    "Add User": "Foydalanuvchi qo\u2018shish", 
    "Administrator": "Administrator", 
    "After changing your password you will sign in automatically.": "Parolni o\u2018zgartirganingizdan so\u2018ng avtomatik tarzda tizimga kirasiz.", 
    "All Languages": "Barcha tillar", 
    "All Projects": "Barcha loyihalar", 
    "Amount": "Miqdori", 
    "An error occurred while attempting to sign in via %s.": "%s orqali kirishga urinishda xatolik yuz berdi.", 
    "An error occurred while attempting to sign in via your social account.": "ijtimoiy hisobingiz orqali kirishga urinishda xatolik yuz berdi.", 
    "Avatar": "Avatar", 
    "Cancel": "Bekor qilish", 
    "Clear all": "Barchasini tozalash", 
    "Clear value": "Qiymatni tozalash", 
    "Close": "Yopish", 
    "Code": "Kod", 
    "Collapse details": "Tafsilotlarni yig\u02bbish", 
    "Comment": "Fikr", 
    "Comment on it": "Unga fikr bildirish", 
    "Congratulations! You have completed this task!": "Tabriklaymiz! Siz bu vazifani bajarib bo\u2018ldingiz!", 
    "Contact Us": "Biz bilan bog\u2018laning", 
    "Creating new user accounts is prohibited.": "Yangi hisob yaratish taqiqlangan.", 
    "Datetime": "Oy kuni", 
    "Delete": "O\u2018chirish", 
    "Deleted successfully.": "Muvaffaqiyatli ravishda o\u2018chirildi.", 
    "Didn't receive an email? Check if it was accidentally filtered out as spam, or try requesting another copy of the email.": "Xat olmadingizmi? Uni spam jildidan izlab ko\u2018ring yoki xatning boshqa nusxasini so\u2018rab ko\u2018ring.", 
    "Disabled": "O\u2018chirilgan", 
    "Discard changes.": "O\u2018zgarishlardan voz kechish", 
    "Edit Language": "Tilni tahrirlash", 
    "Edit My Public Profile": "Ommaviy profilni tahrirlash", 
    "Edit Project": "Loyihani tahrirlash", 
    "Edit User": "Foydalanuvchini tahrirlash", 
    "Edit the suggestion before accepting, if necessary": "Tavsiyalarni qabul qilishdan oldin tahrir qiling (agar zarur bo\u2018lsa)", 
    "Email": "E-pochta", 
    "Email Address": "E-pochta manzili", 
    "Email Confirmation": "E-pochtani tasdiqlash", 
    "Enter your email address, and we will send you a message with the special link to reset your password.": "E-pochta manzilingizni kiriting. Biz esa sizga parolingizni tiklash uchun maxsus havola berilgan xatni jo\u2018natamiz.", 
    "Entire Project": "Butun loyiha", 
    "Error while connecting to the server": "Server bilan bog'lanishda xatolik", 
    "Expand details": "Tafsilotlarni yoyish", 
    "File types": "Fayl turi", 
    "Find language by name, code": "Tilni nomi, kodi bo\u2018yicha toping", 
    "Find project by name, code": "Loyihani nomi va kodi bo\u2018yicha topish", 
    "Find user by name, email, properties": "Foydalanuvchini nomi, e-pochta manzili va xossalari bo\u2018yicha topish", 
    "Full Name": "To\u2018liq ismi", 
    "Go back to browsing": "Ko\u2018rish uchun orqaga qaytish", 
    "Go to the next string (Ctrl+.)<br/><br/>Also:<br/>Next page: Ctrl+Shift+.<br/>Last page: Ctrl+Shift+End": "Keyingi qatorga (Ctrl+.) bilan o\u2018tish mumkin<br/><br/>Shuningdek,<br/>Keyingi sahifaga: Ctrl+Shift+.<br/>So\u2018nggi sahifaga: Ctrl+Shift+End tugmalari bilan o\u2018tish mumkin", 
    "Go to the previous string (Ctrl+,)<br/><br/>Also:<br/>Previous page: Ctrl+Shift+,<br/>First page: Ctrl+Shift+Home": "Oldingi qatorga (Ctrl+,) bilan o\u2018tish mumkin<br/><br/>Shuningdek,</br>Oldingi sahifaga: Ctrl+Shift+,<br/>Birinchi sahifaga: Ctrl+Shift+Home tugmalari bilan o\u2018tish mumkin.", 
    "Hide": "Yashirish", 
    "Hide disabled": "Yashirish o\u2018chirib qo\u2018yilgan", 
    "I forgot my password": "Parolimni unutdim", 
    "Ignore Files": "Fayllarni e\u2019tiborsiz qoldirish", 
    "Languages": "Tillar", 
    "Less": "Kamroq", 
    "LinkedIn": "LinkedIn", 
    "LinkedIn profile URL": "LinkedIn profil URL manzili", 
    "Load More": "Ko\u2018proq yuklash", 
    "Loading...": "Yuklanmoqda...", 
    "Login / Password": "Login / Parol", 
    "More": "Ko\u02bbproq", 
    "More...": "Ko\u02bbproq\u2026", 
    "My Public Profile": "Ommaviy profilim", 
    "No": "Yo\u2018q", 
    "No activity recorded in a given period": "Berilgan muddatda hech qanday faoliyat yozilmagan", 
    "No results found": "Hech qanday natija topilmadi", 
    "No results.": "Natijalarsiz.", 
    "No, thanks": "Yo\u2018q, rahmat, kerak emas", 
    "Not found": "Topilmadi", 
    "Note: when deleting a user their contributions to the site, e.g. comments, suggestions and translations, are attributed to the anonymous user (nobody).": "Diqqat: foydalanuvchini o\u2018chirsangiz, uning saytga qo\u2018shgan hissalari, masalan, mulohazalari, tavsiyalari va tarjimalari noma\u2019lum foydalanuvchiga (hech kimga) tegishli deb ko\u2018rsatiladi.", 
    "Number of Plurals": "Ko\u2018plik soni", 
    "Oops...": "Obbo...", 
    "Overview": "Umumiy ko\u2018rinishi", 
    "Password": "Parol", 
    "Password changed, signing in...": "Parol o\u2018zgartirildi, tizimga kirilmoqda...", 
    "Period": "Vaqt", 
    "Permissions": "Huquqlar", 
    "Personal description": "Shaxsiy ta\u2019rifi", 
    "Personal website URL": "Shaxsiy veb sayt URL manzili", 
    "Please follow that link to continue the account creation.": "Hisob yaratishda davom etish uchun ushbu havolaga o\u2018ting.", 
    "Please follow that link to continue the password reset procedure.": "Parolni tiklash jarayonini davom ettirish uchun quyidagi havolaga o\u2018ting.", 
    "Please select a valid user.": "To\u2018g\u2018ri foydalanuvchini tanlang.", 
    "Plural Equation": "Ko\u2018plik ifodasi", 
    "Preview will be displayed here.": "Umumiy ko\u2018rinishi shu yerda ko\u2018rinadi.", 
    "Project / Language": "Loyiha / Til", 
    "Project Tree Style": "Loyiha daraxt uslubi", 
    "Provide optional comment (will be publicly visible)": "Fikr bildiring (hammaga ko\u2018rinadi)", 
    "Public Profile": "Hammaga ko\u2018rinadigan profil", 
    "Quality Checks": "Sifatini tekshirish", 
    "Rate": "Baho", 
    "Registered Tasks": "Ro\u2018yxatdan o\u2018tgan vazifalar", 
    "Reject": "Rad qilish", 
    "Reload page": "Sahifani qayta yuklash", 
    "Remove task": "Vazifani olib tashlash", 
    "Repeat Password": "Parolni qayta kiriting", 
    "Resend Email": "Xatni qayta jo\u2018natish", 
    "Reset Password": "Parolni tiklash", 
    "Reset Your Password": "Parolni tiklash", 
    "Reviewed": "Ko\u2018rib chiqildi", 
    "Save": "Saqlash", 
    "Saved successfully.": "Muvaffaqiyatli ravishda saqlandi.", 
    "Score Change": "Tarjima o\u2018zgarishi", 
    "Screenshot Search Prefix": "Ekran rasmi qidiruvi old qo\u2018shimchasi", 
    "Search Languages": "Tillarni izlash", 
    "Search Projects": "Loyihalarni izlash", 
    "Search Users": "Foydalanuvchilarni izlash", 
    "Select...": "Tanlash...", 
    "Send Email": "Xat jo\u2018natish", 
    "Sending email to %s...": "%s\u2019ga xat jo\u2018natilmoqda...", 
    "Server error": "Server xatoligi", 
    "Set New Password": "Yangi parolni o\u2018rnatish", 
    "Set a new password": "Yangi parol o\u2018rnatish", 
    "Settings": "Moslamalar", 
    "Short Bio": "Qisqacha biografiya", 
    "Show": "Ko\u02bbrsatish", 
    "Show disabled": "Ko\u2018rsatish o\u2018chirib qo\u2018yilgan", 
    "Sign In": "Kirish", 
    "Sign In With %s": "%s bilan kirish", 
    "Sign In With...": "Ushbu yordamida kirish...", 
    "Sign Up": "Ro\u2018yxatdan o\u2018tish", 
    "Sign in as an existing user": "Mavjud foydalanuvchi sifatida kirish", 
    "Sign up as a new user": "Yangi foydalanuvchi sifatida ro\u2018yxatdan o\u2018tish", 
    "Signed in. Redirecting...": "Kirildi. Qayta yo\u2018naltirilmoqda...", 
    "Signing in with an external service for the first time will automatically create an account for you.": "Tashqi xizmatlardan birinchi marta kirganingizda, avtomatik tarzda siz uchun hisob yaratiladi.", 
    "Similar translations": "Bir xil tarjimalar", 
    "Social Services": "Ijtimoiy xizmatlar", 
    "Social Verification": "Ijtimoiy tasdiqlash", 
    "Source Language": "Manba til", 
    "Special Characters": "Maxsus belgilar", 
    "String Errors Contact": "Kontakt xatoliklari qatori", 
    "Subtotal": "Oraliq natija", 
    "Suggested": "Tavsiya qilindi", 
    "Summary": "Xulosa", 
    "The password reset link was invalid, possibly because it has already been used. Please request a new password reset.": "Parolni tiklash havolasi noto\u2018g\u2018ri, undan oldin foydalanilgan bo\u2018lishi mumkin. Qaytadan yangi parolni tiklash so\u2018rovini amalga oshiring.", 
    "The server seems down. Try again later.": "Server ishlamayapti. Keyinroq harakat qilib ko'ring.", 
    "There are unsaved changes. Do you want to discard them?": "Saqlanmagan o\u2018zgartirishlar bor. Ularni rad qilishni xohlaysizmi?", 
    "There is %(count)s language.": [
      "%(count)s ta til topildi.%(count)s ta til topildi. Quyida eng so\u2018nggi qo\u2018shilganlar keltirilgan."
    ], 
    "There is %(count)s project.": [
      "%(count)s ta loyiha mavjud. So\u2018nggi qo\u2018shilganlari quyida keltirilgan."
    ], 
    "There is %(count)s user.": [
      "%(count)s ta foydalanuvchi mavjud. Quyida eng so\u2018nggi qo\u2018shilganlari keltirilgan."
    ], 
    "This email confirmation link expired or is invalid.": "Ushbu e-pochtani tasdiqlash havolasi eskirgan yoki noto\u2018g\u2018ri.", 
    "This string no longer exists.": "Ushbu qator mavjud emas.", 
    "To set or change your avatar for your email address (%(email)s), please go to gravatar.com.": "E-pochta manzilingiz (%(email)s) uchun avatar o\u2018rnatish yoki o\u2018zgartirish uchun gravatar.com saytiga tashrif buyuring.", 
    "Total (%(currency)s)": "Jami (%(currency)s)", 
    "Translated": "Tarjima qilindi", 
    "Translated by %(fullname)s in &ldquo;<span title=\"%(path)s\">%(project)s</span>&rdquo; project": "Tarjimon: %(fullname)s \u2013 &ldquo;<span title=\"%(path)s\">%(project)s</span>&rdquo; project", 
    "Translated by %(fullname)s in &ldquo;<span title=\"%(path)s\">%(project)s</span>&rdquo; project %(time_ago)s": "Tarjimon: %(fullname)s in &ldquo;<span title=\"%(path)s\">%(project)s</span>&rdquo; loyiha %(time_ago)s", 
    "Try again": "Yana urinib ko\u2018ring", 
    "Twitter": "Twitter", 
    "Twitter username": "Twitter tarmog\u2018idagi nomi", 
    "Type to search": "Izlash uchun yozing", 
    "Use the search form to find the language, then click on a language to edit.": "Tilni topish uchun izlash shaklidan foydalaning. So\u2018ngra tahrirlash uchun til ustiga bosing.", 
    "Use the search form to find the project, then click on a project to edit.": "Loyihani topish uchun izlash shaklidan foydalaning. So\u2018ngra tahrirlash uchun loyiha ustiga bosing.", 
    "Use the search form to find the user, then click on a user to edit.": "Foydalanuvchini topish uchun izlash shaklidan foydalaning, so\u2018ngra tahrirlash uchun foydalanuvchi nomining ustiga bosing.", 
    "Username": "Foydalanuvchi", 
    "We have sent an email containing the special link to <span>%s</span>": "Biz<span>%s</span>ga maxsus havola berilgan xatni sizga jo\u2018natdik", 
    "Website": "Veb sayt", 
    "Why are you part of our translation project? Describe yourself, inspire others!": "Siz nega tarjima loyihamizning ishtirokchisiga aylandingiz? Bu haqida batafsil ma\u2019lumot bering va boshqalarni ham ruhlantiring!", 
    "Yes": "Ha", 
    "You have unsaved changes in this string. Navigating away will discard those changes.": "Ushbu qatorda siz kiritgan, lekin saqlanmagan o\u2018zgarishlar bor. Keyingi yoki oldinga tarjimaga o\u2018tsangiz, ushbu o\u2018zgartirishlar saqlanmaydi.", 
    "Your Full Name": "To\u2018liq ismingiz", 
    "Your LinkedIn profile URL": "LinkedIn tarmog\u2018idagi profilingiz URL manzili", 
    "Your Personal website/blog URL": "Shaxsiy veb sahifanigz/blogingiz URL manzili", 
    "Your Twitter username": "Twitter tarmog\u2018idagi nomingiz", 
    "Your account is inactive because an administrator deactivated it.": "Hisobingiz to\u2018xtatib qo\u2018yilgan, chunki administrator buni amalga oshirgan.", 
    "Your account needs activation.": "Hisobingizni faollashtirishingiz kerak.", 
    "disabled": "o\u2018chirib qo\u2018yilgan", 
    "some anonymous user": "anonim foydalanuvchi", 
    "someone": "kimdir"
  };
  for (var key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      var value = django.catalog[msgid];
      if (typeof(value) == 'undefined') {
        return msgid;
      } else {
        return (typeof(value) == 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      var value = django.catalog[singular];
      if (typeof(value) == 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value[django.pluralidx(count)];
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      var value = django.gettext(context + '\x04' + msgid);
      if (value.indexOf('\x04') != -1) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      var value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.indexOf('\x04') != -1) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "N j, Y, P", 
    "DATETIME_INPUT_FORMATS": [
      "%Y-%m-%d %H:%M:%S", 
      "%Y-%m-%d %H:%M:%S.%f", 
      "%Y-%m-%d %H:%M", 
      "%Y-%m-%d", 
      "%m/%d/%Y %H:%M:%S", 
      "%m/%d/%Y %H:%M:%S.%f", 
      "%m/%d/%Y %H:%M", 
      "%m/%d/%Y", 
      "%m/%d/%y %H:%M:%S", 
      "%m/%d/%y %H:%M:%S.%f", 
      "%m/%d/%y %H:%M", 
      "%m/%d/%y"
    ], 
    "DATE_FORMAT": "N j, Y", 
    "DATE_INPUT_FORMATS": [
      "%Y-%m-%d", 
      "%m/%d/%Y", 
      "%m/%d/%y", 
      "%b %d %Y", 
      "%b %d, %Y", 
      "%d %b %Y", 
      "%d %b, %Y", 
      "%B %d %Y", 
      "%B %d, %Y", 
      "%d %B %Y", 
      "%d %B, %Y"
    ], 
    "DECIMAL_SEPARATOR": ".", 
    "FIRST_DAY_OF_WEEK": "0", 
    "MONTH_DAY_FORMAT": "F j", 
    "NUMBER_GROUPING": "0", 
    "SHORT_DATETIME_FORMAT": "m/d/Y P", 
    "SHORT_DATE_FORMAT": "m/d/Y", 
    "THOUSAND_SEPARATOR": ",", 
    "TIME_FORMAT": "P", 
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S", 
      "%H:%M:%S.%f", 
      "%H:%M"
    ], 
    "YEAR_MONTH_FORMAT": "F Y"
  };

    django.get_format = function(format_type) {
      var value = django.formats[format_type];
      if (typeof(value) == 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }

}(this));

