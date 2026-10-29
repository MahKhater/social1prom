import random
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'ser_el_tafouk_secret_key' # مفتاح الجلسة لتخزين الأسئلة والإجابات

QUESTIONS_DB = {
    "id": 1,
        "type": "multiple choice",
        "prompt": "تعد قارة إفريقيا ثاني أكبر قارات العالم من حيث المساحة بعد قارة:",
        "options": ["أوروبا", "أمريكا الشمالية", "آسيا", "أستراليا"],
        "answer": "آسيا"
    },
  {
        "id": 2,
        "type": "true/false",
        "prompt": "تبلغ مساحة قارة إفريقيا حوالي 30.4 مليون كم٢.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
   {
        "id": 3,
        "type": "multiple choice",
        "prompt": "تمثل مساحة قارة إفريقيا من مساحة قارات العالم نسبة:",
        "options": ["10%", "20%", "25%", "30%"],
        "answer": "20%"
    },
{
        "id": 4,
        "type": "true/false",
        "prompt": "تقع قارة إفريقيا في وسط قارات العالم القديم.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 5,
        "type": "multiple choice",
        "prompt": "تتصل قارة إفريقيا بقارة آسيا عن طريق:",
        "options": ["مضيق باب المندب", "شبه جزيرة سيناء", "مضيق جبل طارق", "قناة السويس"],
        "answer": "شبه جزيرة سيناء"
    },
    {
        "id": 6,
        "type": "multiple choice",
        "prompt": "تقترب قارة إفريقيا من قارة أوروبا عند مضيق:",
        "options": ["باب المندب", "هرمز", "موزمبيق", "جبل طارق"],
        "answer": "جبل طارق"
    },
    {
        "id": 7,
        "type": "true/false",
        "prompt": "يحد قارة إفريقيا من جهة الشمال البحر الأحمر.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 8,
        "type": "multiple choice",
        "prompt": "المسطح المائي الذي يفصل قارة إفريقيا عن قارتي أمريكا الشمالية والجنوبية هو:",
        "options": ["المحيط الهندي", "المحيط الأطلنطي", "البحر المتوسط", "المحيط القطبي"],
        "answer": "المحيط الأطلنطي"
    },
    {
        "id": 9,
        "type": "true/false",
        "prompt": "يمر مدار السرطان في النصف الشمالي من قارة إفريقيا.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 10,
        "type": "multiple choice",
        "prompt": "يمر خط الطول الرئيسي (جرينتش) في قارة إفريقيا جهة:",
        "options": ["الشرق", "الغرب", "الشمال", "الجنوب"],
        "answer": "الغرب"
    },
    {
        "id": 11,
        "type": "true/false",
        "prompt": "يقع نحو ثلثي مساحة قارة إفريقيا في نصف الكرة الأرضية الجنوبي.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 12,
        "type": "multiple choice",
        "prompt": "الموقع بالنسبة لدوائر العرض وخطوط الطول يُقصد به:",
        "options": ["الموقع الجغرافي", "الموقع الفلكي", "الموقع الاستراتيجي", "الموقع الاقتصادي"],
        "answer": "الموقع الفلكي"
    },
    {
        "id": 13,
        "type": "true/false",
        "prompt": "الأهمية الاستراتيجية هي أهمية المكان وقت الحروب والأزمات والسلم.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 14,
        "type": "multiple choice",
        "prompt": "أدى الموقع الفلكي لقارة إفريقيا بشكل مباشر إلى تنوع:",
        "options": ["الممرات المائية", "الموقع الاستراتيجي", "المناخ", "الحدود السياسية"],
        "answer": "المناخ"
    },
    {
        "id": 15,
        "type": "true/false",
        "prompt": "نشأت حضارة قرطاج القديمة على أرض دولة تونس الحالية.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 16,
        "type": "multiple choice",
        "prompt": "نشأت حضارة أكسوم القديمة في قارة إفريقيا على أرض:",
        "options": ["السودان", "تونس", "إريتريا وإثيوبيا", "مصر"],
        "answer": "إريتريا وإثيوبيا"
    },
    {
        "id": 17,
        "type": "true/false",
        "prompt": "نشأت حضارة كوش القديمة في دولة ليبيا.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 18,
        "type": "multiple choice",
        "prompt": "مجموع الإنتاج الثقافي والمادي الذي يميز مجتمعاً عن غيره يُعرف بـ:",
        "options": ["التاريخ", "الحضارة", "الجغرافيا", "العادات"],
        "answer": "الحضارة"
    },
    {
        "id": 19,
        "type": "true/false",
        "prompt": "انتقلت الثقافة والحضارة الإسلامية من آسيا إلى إفريقيا عبر شبه جزيرة سيناء.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 20,
        "type": "multiple choice",
        "prompt": "من أوائل المصريين القدماء الذين قاموا بأربع رحلات نحو الجنوب واكتشفوا أجزاء من إفريقيا:",
        "options": ["الملك نخاو الثاني", "الرحالة حرخوف", "محمد علي باشا", "الخديو إسماعيل"],
        "answer": "الرحالة حرخوف"
    },
    {
        "id": 21,
        "type": "true/false",
        "prompt": "أرسل الملك نخاو الثاني بعثة من الفينيقيين للدوران حول إفريقيا استمرت لمدة 3 سنوات.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 22,
        "type": "multiple choice",
        "prompt": "بدأت رحلة بعثة الملك نخاو الثاني للدوران حول إفريقيا من:",
        "options": ["البحر المتوسط", "البحر الأحمر", "مضيق جبل طارق", "المحيط الأطلنطي"],
        "answer": "البحر الأحمر"
    },
    {
        "id": 23,
        "type": "true/false",
        "prompt": "انتهت رحلة بعثة الملك نخاو الثاني وعادت إلى مصر عبر مضيق باب المندب.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 24,
        "type": "multiple choice",
        "prompt": "في العصر الحديث، أرسل محمد علي باشا رحلات لاكتشاف منابع النيل عام 1839م وانتهت باكتشاف:",
        "options": ["النيل الأزرق", "نهر عطبرة", "النيل الأبيض", "بحيرة تانا"],
        "answer": "النيل الأبيض"
    },
    {
        "id": 25,
        "type": "true/false",
        "prompt": "وصل حكم الخديو إسماعيل إلى جنوب دائرة الاستواء أثناء اهتمامه باكتشاف منابع النيل.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 26,
        "type": "multiple choice",
        "prompt": "رحالة عربي قام برحلات مهمة في شمال وغرب إفريقيا واخترق الصحراء الكبرى حتى وصل إلى مالي:",
        "options": ["المسعودي", "ابن بطوطة", "ابن خلدون", "الإدريسي"],
        "answer": "ابن بطوطة"
    },
    {
        "id": 27,
        "type": "true/false",
        "prompt": "يعد الرحالة العربي المسعودي من أوائل الذين زاروا إفريقيا وكتبوا عنها.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 28,
        "type": "multiple choice",
        "prompt": "بدأ البرتغاليون محاولاتهم لاكتشاف إفريقيا في القرن الـ 15 الميلادي في عهد الأمير:",
        "options": ["فاسكو دي جاما", "بارتولوميو دياس", "هنري الملاح", "جون سبيك"],
        "answer": "هنري الملاح"
    },
    {
        "id": 29,
        "type": "true/false",
        "prompt": "أسس البرتغاليون الموانئ والمراكز التجارية على طول طريق رأس الرجاء الصالح لتأمين الملاحة والتجارة.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 30,
        "type": "multiple choice",
        "prompt": "تصارعت الدول الاستعمارية الأوروبية على إفريقيا لنهب خيراتها، مما نتج عنه تقسيمها إلى:",
        "options": ["22 دولة", "44 دولة", "54 دولة", "64 دولة"],
        "answer": "54 دولة"
         }
],
"متوسط": [
          {
                 "id": 301,
        "type": "multiple choice",
        "prompt": "يمر خط الاستواء في قارة إفريقيا بالطرف الجنوبي من دولة:",
        "options": ["مصر", "الصومال", "السودان", "ليبيا"],
        "answer": "الصومال"
    },
    {
        "id": 302,
        "type": "true/false",
        "prompt": "تتميز هضبة شمال إفريقيا بأنها عظيمة الاتساع وقليلة الارتفاع مقارنة بهضبة الحبشة.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 303,
        "type": "multiple choice",
        "prompt": "تنحدر هضبة شمال إفريقيا تدريجياً نحو الشمال حتى تلتقي بسواحل البحر:",
        "options": ["الأحمر", "المتوسط", "الأسود", "العربي"],
        "answer": "المتوسط"
    },
    {
        "id": 304,
        "type": "true/false",
        "prompt": "يعد جبل العوينات من المظاهر التضاريسية التي تقع بالكامل داخل الحدود الجغرافية لدولة مصر.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 305,
        "type": "multiple choice",
        "prompt": "من أمثلة الواحات التي تقع في دولة ليبيا وتنتشر فوق هضبة شمال إفريقيا واحة:",
        "options": ["سيوة", "القطارة", "الجوف", "عين صالح"],
        "answer": "الجوف"
    },
    {
        "id": 306,
        "type": "true/false",
        "prompt": "تمتاز هضبة الحبشة بخصوبة تربتها العالية نتيجة لتعرضها القديم للطفوح البركانية.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 307,
        "type": "multiple choice",
        "prompt": "تعد هضبة الحبشة :",
        "options": ["أقل هضاب القارة ارتفاعاً", "أعلى هضاب القارة ارتفاعاً", "أكثر هضاب القارة اتساعاً", "أقرب الهضاب للمحيط الأطلنطي"],
        "answer": "أعلى هضاب القارة ارتفاعاً"
    },
    {
        "id": 308,
        "type": "true/false",
        "prompt": "تتميز هضبة البحيرات الاستوائية في وسط القارة بأنها تنحدر بشكل عام من الشمال إلى الجنوب.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 309,
        "type": "multiple choice",
        "prompt": "تعلو هضبة البحيرات الاستوائية في وسط قارة إفريقيا مجموعة من القمم الجبلية:",
        "options": ["الالتوائية", "الانكسارية", "البركانية", "التصدعية"],
        "answer": "البركانية"
    },
    {
        "id": 310,
        "type": "true/false",
        "prompt": "يقع الأخدود الإفريقي العظيم في الجزء الشرقي من الهضبة الجنوبية لقارة إفريقيا.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 311,
        "type": "multiple choice",
        "prompt": "يتجه الامتداد الجغرافي العام للأخدود الإفريقي العظيم شرق القارة من:",
        "options": ["الشمال إلى الجنوب", "الشرق إلى الغرب", "الجنوب إلى الشمال", "الغرب إلى الشرق"],
        "answer": "الجنوب إلى الشمال"
    },
    {
        "id": 312,
        "type": "true/false",
        "prompt": "تُصنف جبال أطلس وجبال الكاب في إفريقيا على أنهما جبال انكسارية نشأت نتيجة تصدع الصخور الصلبة.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 313,
        "type": "multiple choice",
        "prompt": "أعلى قمة جبلية في سلسلة جبال أطلس الالتوائية في شمال غرب إفريقيا هي جبل:",
        "options": ["شايب البنات", "كينيا", "توبقال", "كلمنجارو"],
        "answer": "توبقال"
    },
    {
        "id": 314,
        "type": "true/false",
        "prompt": "تحصر سلسلتا جبال أطلس التل وأطلس الصحراء بينهما هضبة الشطوط في دولة الجزائر.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 315,
        "type": "multiple choice",
        "prompt": "تعد جبال البحر الأحمر جبالاً انكسارية، وأعلى قمة جبلية في سلسلتها داخل مصر هي جبل:",
        "options": ["توبقال", "شايب البنات", "العوينات", "كلمنجارو"],
        "answer": "شايب البنات"
    },
    {
        "id": 316,
        "type": "true/false",
        "prompt": "تمتد جبال البحر الأحمر الانكسارية عبر أراضي ثلاث دول إفريقية هي مصر والسودان وإريتريا.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 317,
        "type": "multiple choice",
        "prompt": "يتطابق سبب النشأة التكوينية البركانية لجبل كلمنجارو مع سبب نشأة جبل:",
        "options": ["أطلس", "الكاب", "كينيا", "شايب البنات"],
        "answer": "كينيا"
    },
    {
        "id": 318,
        "type": "true/false",
        "prompt": "يتكون الجليد فوق قمة جبل كلمنجارو نتيجة لموقعه الفلكي في العروض القطبية الباردة.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 319,
        "type": "multiple choice",
        "prompt": "يتكون الجليد فوق قمة جبل كلمنجارو بالرغم من وقوعه في المنطقة الاستوائية الحارة بسبب:",
        "options": ["اقترابه من مياه المحيط", "شدة ارتفاعه وعلو قمته", "كثرة الأمطار الشتوية", "تأثير الحركات الانكسارية"],
        "answer": "شدة ارتفاعه وعلو قمته"
    },
    {
        "id": 320,
        "type": "true/false",
        "prompt": "تساهم المناطق الجبلية في إفريقيا في دعم نشاط التعدين والصناعة لأنها غنية بالثروات المعدنية كالحديد والذهب.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 321,
        "type": "multiple choice",
        "prompt": "تتميز سهول وادي النيل بخصوبة تربتها العالية نتيجة لتكونها من الطمي المنقول من هضبة:",
        "options": ["شمال إفريقيا", "البحيرات الاستوائية", "الحبشة", "الهضبة الجنوبية"],
        "answer": "هضبة الحبشة"
    },
    {
        "id": 322,
        "type": "true/false",
        "prompt": "تضيق السهول الساحلية للبحر المتوسط في بلاد المغرب العربي بسبب اقتراب جبال أطلس من الساحل.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 323,
        "type": "multiple choice",
        "prompt": "تتميز السهول الساحلية المطلة على المحيط الهندي باتساعها في دولة تنزانيا بينما تضيق في دولة:",
        "options": ["مصر", "كينيا", "السودان", "الجزائر"],
        "answer": "كينيا"
    },
    {
        "id": 324,
        "type": "true/false",
        "prompt": "تعد سهول المحيط الأطلنطي في غرب القارة سهولاً ضيقة وغير صالحة للاستغلال الزراعي.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 325,
        "type": "multiple choice",
        "prompt": "أكبر جزر القارة الإفريقية مساحة وتقع في مياه المحيط الهندي هي جزيرة:",
        "options": ["جزر القمر", "مدغشقر", "سيشل", "موريشيوس"],
        "answer": "مدغشقر"
    },
    {
        "id": 326,
        "type": "true/false",
        "prompt": "يفصل جزيرة مدغشقر عن الساحل الشرقي للقارة الإفريقية ممر مائي مهم هو مضيق موزمبيق.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 327,
        "type": "multiple choice",
        "prompt": "المصطلح الجغرافي الذي يُقصد به (المساحة التي يجري بها نهر النيل وروافده) هو:",
        "options": ["السهل الفيضي للنيل", "المجرى الدولي", "حوض نهر النيل", "الدلتا الطبيعية"],
        "answer": "حوض نهر النيل"
    },
    {
        "id": 328,
        "type": "true/false",
        "prompt": "تشغل مساحة حوض نهر النيل إجمالاً نحو 10% من المساحة الكلية لقارة إفريقيا.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 329,
        "type": "multiple choice",
        "prompt": "يُصنف نهر النيل كونه نهراً دولياً بسبب امتداد مجراه وروافده داخل أراضي كم دولة إفريقية؟",
        "options": ["9 دول", "10 دول", "11 دولة", "12 دولة"],
        "answer": "11 دولة"
    },
    {
        "id": 330,
        "type": "true/false",
        "prompt": "اقترحت مصر على دول حوض النيل إنشاء تجمع إقليمي عام 1983م أطلق عليه اسم تجمع الأندوجو.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
      }
],
 "محترف": [
        { 
    "id": 730,
        "type": "true/false",
        "prompt": "تقع واحة الجوف كإحدى الظاهرات التضاريسية لهضبة شمال إفريقيا داخل دولة مصر.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 731,
        "type": "multiple choice",
        "prompt": "من المظاهر التضاريسية المنتشرة فوق هضبة شمال إفريقيا في دولة ليبيا واحة:",
        "options": ["سيوة", "القطارة", "الجوف", "عين صالح"],
        "answer": "الجوف"
    },
    {
        "id": 732,
        "type": "true/false",
        "prompt": "تتميز الهضبة الجنوبية لقارة إفريقيا بأنها تنحدر بشدة نحو السواحل الغربية للقارة.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 733,
        "type": "multiple choice",
        "prompt": "مجموعة انكسارات طولية تمتد شرق قارة إفريقيا وتتجه بشكل عام من الجنوب إلى الشمال هي:",
        "options": ["حوض نهر النيل", "الأخدود الإفريقي العظيم", "السهول الفيضية للنيل", "سلاسل جبال أطلس"],
        "answer": "الأخدود الإفريقي العظيم"
    },
    {
        "id": 734,
        "type": "true/false",
        "prompt": "يُعد كل من البحر الأحمر وخليج عدن وخليج العقبة من الأجزاء التابعة للأخدود الإفريقي العظيم شرق القارة.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 735,
        "type": "multiple choice",
        "prompt": "تحصر سلسلتا جبال أطلس المتوازيتان (أطلس التل وأطلس الصحراء) في شمال غرب القارة بينهما هضبة:",
        "options": ["شمال إفريقيا", "الحبشة", "الشطوط", "البحيرات الاستوائية"],
        "answer": "الشطوط"
    },
    {
        "id": 736,
        "type": "true/false",
        "prompt": "تُصنف جبال أطلس في شمال غرب القارة وجبال الكاب في جنوبها على أنهما جبال انكسارية صلبة.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 737,
        "type": "multiple choice",
        "prompt": "أعلى قمة جبلية في سلسلة جبال البحر الأحمر الانكسارية وتوجد داخل حدود مصر هي جبل:",
        "options": ["توبقال", "شايب البنات", "كينيا", "كلمنجارو"],
        "answer": "شايب البنات"
    },
    {
        "id": 738,
        "type": "true/false",
        "prompt": "يتكون الجليد فوق قمة جبل كلمنجارو بالرغم من وقوعه في المنطقة الاستوائية الحارة بسبب شدة ارتفاعه وعلو قمته.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 739,
        "type": "multiple choice",
        "prompt": "تساهم المناطق الجبلية في قارة إفريقيا في دعم الأنشطة الاقتصادية الهامة مثل قطاعي التعدين والصناعة و:",
        "options": ["الرعي الجاف", "صيد الأسماك النهرية", "السياحة", "استصلاح الصحاري الملحية"],
        "answer": "السياحة"
    },
    {
        "id": 740,
        "type": "true/false",
        "prompt": "تتميز السهول الفيضية في إفريقيا بصلاحيتها التامة للزراعة نتيجة للمواد والترسبات الطمية التي كونتها الأنهار.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 741,
        "type": "multiple choice",
        "prompt": "تضيق السهول الساحلية للبحر المتوسط في بلاد المغرب العربي بسبب اقتراب جبال:",
        "options": ["البحر الأحمر", "الكاب", "أطلس", "دراكنزبرج"],
        "answer": "أطلس"
    },
    {
        "id": 742,
        "type": "true/false",
"prompt": "تتميز السهول الساحلية المطلة على البحر الأحمر في مصر والسودان بالاتساع الكبير والخلو من الحواجز الجبلية.",
"options": ["صح", "خطأ"],
"answer": "خطأ"
},
{
"id": 743,
"type": "multiple choice",
"prompt": "تتميز السهول الساحلية للمحيط الهندي باتساعها الواضح في دولة تنزانيا بينما تضيق في دولة:",
"options": ["مصر", "السودان", "كينيا", "الصومال"],
"answer": "كينيا"
},
{
"id": 744,
"type": "true/false",
"prompt": "يفصل جزيرة مدغشقر (أكبر جزر القارة في المحيط الهندي) عن الساحل الشرقي لإفريقيا مضيق موزمبيق.",
"options": ["صح", "خطأ"],
"answer": "صح"
},
{
"id": 745,
"type": "multiple choice",
"prompt": "من الجزر الإفريقية التي تقع في المحيط الهندي وتتميز بأنها تقع شمال غرب جزيرة مدغشقر جزر:",
"options": ["سيشل", "القمر", "موريشيوس", "زنجبار"],
"answer": "القمر"
},
{
"id": 746,
"type": "true/false",
"prompt": "تشغل مساحة حوض نهر النيل الإجمالية نحو 10% من المساحة الكلية لقارة إفريقيا.",
"options": ["صح", "خطأ"],
"answer": "صح"
},
{
"id": 747,
"type": "multiple choice",
"prompt": "يمتد مجرى نهر النيل وروافده داخل أراضي إحدى عشرة دولة إفريقية، ولذلك يُصنف بأنه نهر:",
"options": ["محلي", "إقليمي", "دولي", "ساحلي"],
"answer": "دولي"
},
{
"id": 748,
"type": "true/false",
"prompt": "تقع منابع نهر النيل الدائمة (الاستوائية) في نطاق تضاريس هضبة البحيرات الاستوائية وتتميز بسقوط الأمطار طوال العام.",
"options": ["صح", "خطأ"],
"answer": "صح"
},
{
"id": 749,
"type": "multiple choice",
"prompt": "من الروافد الموسمية الإثيوبية التي تمد النيل بمياهه وتساعده على الجريان شمالاً نحو المصب نهر عطبرة ونهر:",
"options": ["كاجيرا", "بحر الغزال", "النيل الأزرق", "بحر العرب"],
"answer": "النيل الأزرق"
},
{
"id": 750,
"type": "true/false",
"prompt": "قامت مصر بحفر عشرات الآبار لتوفير المياه النقية في دولة كينيا كأحد جهود التنمية المائية المستدامة.",
"options": ["صح", "خطأ"],
"answer": "صح"
},
{
"id": 751,
"type": "multiple choice",
"prompt": "السد المائي الذي قامت مصر بالمساهمة الكاملة في إنشائه وتشييده في دولة أوغندا لدعم التنمية المستدامة هو سد:",
"options": ["سنار", "أوين", "جبل الأولياء", "العالي"],
"answer": "أوين"
},
{
"id": 752,
"type": "true/false",
"prompt": "ساهمت جمهورية مصر العربية في تطهير بحيرتي فيكتوريا وكيوجا من الحشائش والنباتات المائية الضارة المانعة للجريان.",
"options": ["صح", "خطأ"],
"answer": "صح"
},
{
"id": 753,
"type": "multiple choice",
"prompt": "من مشروعات مصر المائية المستدامة الموثقة لدعم البحث العلمي المائي إنشاء مركز للبحوث المائية في دولة:",
"options": ["كينيا", "تنزانيا", "السودان", "أوغندا"],
"answer": "تنزانيا"
},
{
"id": 754,
"type": "true/false",
"prompt": "نصت اتفاقية المبادئ عام 2015م بين مصر وإثيوبيا والسودان على مبدأ التعاون والتنمية وعدم التسبب في ضرر والاستخدام المنصف.",
"options": ["صح", "خطأ"],
"answer": "صح"
},
{
"id": 755,
        "type": "multiple choice",
        "prompt": "يحد قارة افريقيا من جهة الشرق مسطحان مائيان هما المحيط الهندي و:",
        "options": ["البحر المتوسط", "البحر الأحمر", "المحيط الأطلنطي", "خليج غينيا"],
        "answer": "البحر الأحمر"
    },
    {
        "id": 756,
        "type": "true/false",
        "prompt": "تقترب قارة إفريقيا من قارة آسيا جغرافياً عند ممر مائي استراتيجي هو مضيق جبل طارق.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 757,
        "type": "multiple choice",
        "prompt": "الدولتان العربيتان الإفريقيتان اللتان تقعان بأكملهما في النصف الكروي الغربي وفقاً لخريطة المنهج هما المغرب و:",
        "options": ["الجزائر", "تونس", "موريتانيا", "ليبيا"],
        "answer": "موريتانيا"
    },
    {
        "id": 758,
        "type": "true/false",
        "prompt": "تتقاطع دائرة الاستواء الفلكية مباشرة في وسط القارة مع هضبة الحبشة وجبل كينيا.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 759,
        "type": "multiple choice",
        "prompt": "أي من الدول العربية الإفريقية التالية يتقاطع فيها مدار السرطان الفلكي مع خط الطول الرئيسي جرينتش؟",
        "options": ["مصر", "ليبيا", "تونس", "الجزائر"],
        "answer": "الجزائر"
    },
    {
        "id": 760,
        "type": "true/false",
        "prompt": "تعد دولة الصومال الدولة العربية الوحيدة في القارة الإفريقية التي تمر بها دائرة الاستواء.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 761,
        "type": "multiple choice",
        "prompt": "نشأت على أرض القارة الإفريقية قديماً حضارة أكسوم، وتقع أراضيها التاريخية حالياً في دولتي:",
        "options": ["مصر والسودان", "تونس والجزائر", "إريتريا وإثيوبيا", "ليبيا وتشاد"],
        "answer": "إريتريا وإثيوبيا"
    },
    {
        "id": 762,
        "type": "true/false",
        "prompt": "تطابقت جبال كينيا وكلمنجارو في وسط القارة من حيث سبب النشأة، حيث تكونتا نتيجة الثورانات البركانية.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
        }
  ]
}


@app.route('/', methods=['GET', 'POST'])
def index():
    level = request.form.get('level', 'متوسط')
    num_questions = int(request.form.get('num_questions', 5))
    action = request.form.get('action', 'select')
   
    pool = QUESTIONS_DB.get(level, QUESTIONS_DB.get("متوسط", []))
   
    if request.method == 'GET' or action == 'select':
        return render_template_string(MAIN_TEMPLATE, level=level, num_questions=num_questions)
       
    elif action == 'generate':
        selected_questions = random.sample(pool, min(num_questions, len(pool))) if pool else []
        session['questions'] = selected_questions
        session['level'] = level
        session['current_index'] = 0
        session['user_answers'] = {}
        return redirect(url_for('quiz_step'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz_step():
    questions = session.get('questions', [])
    current_index = session.get('current_index', 0)
    level = session.get('level', 'متوسط')
   
    if not questions:
        return redirect(url_for('index'))
       
    if request.method == 'POST':
        ans = request.form.get('current_answer')
        
        user_answers = session.get('user_answers', {})
        user_answers[str(current_index)] = {
            "prompt": questions[current_index]['prompt'],
            "user_ans": ans if ans else "لم تتم الإجابة",
            "correct_ans": questions[current_index]['answer'],
            "is_correct": (ans == questions[current_index]['answer'])
        }
        session['user_answers'] = user_answers
       
        current_index += 1
        session['current_index'] = current_index
       
    if current_index >= len(questions):
        return redirect(url_for('results'))
       
    current_question = questions[current_index]
   
    return render_template_string(
        QUIZ_TEMPLATE,
        level=level,
        question=current_question,
        current_num=current_index + 1,
        total_questions=len(questions),
        num_questions=len(questions)
    )

@app.route('/results')
def results():
    user_answers = session.get('user_answers', {})
    level = session.get('level', 'متوسط')
   
    score = 0
    total = len(user_answers)
    results_list = []
   
    for idx, data in sorted(user_answers.items(), key=lambda x: int(x[0])):
        if data['is_correct']:
            score += 1
        results_list.append({
            "id": int(idx) + 1,
            "prompt": data['prompt'],
            "user_ans": data['user_ans'],
            "correct_ans": data['correct_ans'],
            "is_correct": data['is_correct']
        })
       
    return render_template_string(
        RESULT_TEMPLATE,
        level=level,
        score=score,
        total=total,
        results=results_list
    )

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة سر التفوق - تصميم الامتحان</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        .header-badge { text-align: center; color: #d4a373; font-size: 14px; font-weight: bold; margin-bottom: 5px; }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .subtitle { text-align: center; color: #666; font-size: 14px; margin-bottom: 25px; }
        .section-title { font-weight: bold; color: #222; font-size: 15px; margin-bottom: 10px; }
        .levels-container { display: flex; gap: 10px; margin-bottom: 20px; }
        .level-btn { flex: 1; padding: 12px; border: 2px solid #e0e0e0; border-radius: 12px; background: #fff; cursor: pointer; text-align: center; font-weight: bold; font-size: 14px; transition: 0.3s; }
        .level-btn input { display: none; }
        .level-btn.active, .level-btn:hover { border-color: #114b3e; background: #e8f5e9; color: #114b3e; }
        .slider-container { margin-bottom: 25px; background: #f9f9f9; padding: 15px; border-radius: 12px; border: 1px solid #eee; }
        .slider-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; font-weight: bold; color: #114b3e; }
        input[type=range] { width: 100%; accent-color: #114b3e; cursor: pointer; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        .whatsapp-link-btn { display: block; width: 100%; background: #25d366; color: white; padding: 13px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 15px; text-decoration: none; box-shadow: 0 4px 10px rgba(37,211,102,0.3); transition: 0.3s; margin-top: 15px; box-sizing: border-box; }
        .whatsapp-link-btn:hover { background: #1ebe57; }
    </style>
</head>
<body>
    <div class="main-card">
        <div class="header-badge">منصة سر التفوق التعليمية ✨</div>
        <h2>صمّم امتحانك</h2>
        <div class="subtitle">اختبر معلوماتك الآن بكل سهولة ⏱️</div>
       
        <form method="POST">
            <input type="hidden" name="action" value="generate">
            <div class="section-title">اختيار مستوى الصعوبة الوحدة الاولى اولى اعدادي تاريخ </div>
            <div class="levels-container">
                <label class="level-btn {% if level == 'مبتدئ' %}active{% endif %}">
                    <input type="radio" name="level" value="مبتدئ" {% if level == 'مبتدئ' %}checked{% endif %} onchange="updateActive(this)"> مبتدئ
                </label>
                <label class="level-btn {% if level == 'متوسط' %}active{% endif %}">
                    <input type="radio" name="level" value="متوسط" {% if level == 'متوسط' %}checked{% endif %} onchange="updateActive(this)"> متوسط
                </label>
                <label class="level-btn {% if level == 'محترف' %}active{% endif %}">
                    <input type="radio" name="level" value="محترف" {% if level == 'محترف' %}checked{% endif %} onchange="updateActive(this)"> محترف ⏱️
                </label>
            </div>
           
            <div class="slider-container">
                <div class="slider-header">
                    <span>عدد الأسئلة بالاختبار</span>
                    <span id="range-val" style="background: #114b3e; color: white; padding: 2px 10px; border-radius: 20px; font-size: 13px;">{{ num_questions }} أسئلة</span>
                </div>
                <input type="range" name="num_questions" min="5" max="15" value="{{ num_questions }}" oninput="document.getElementById('range-val').innerText = this.value + ' أسئلة'">
            </div>
           
            <button type="submit" class="start-btn">ابدأ مع سر التفوق 🚀</button>
        </form>
       
        <a href="https://wa.me/201221581154?s=t" class="whatsapp-link-btn" target="_blank">💬 للاشتراك اضغط هنا</a>
    </div>
    <script>
        function updateActive(radio) {
            document.querySelectorAll('.level-btn').forEach(b => b.classList.remove('active'));
            radio.closest('.level-btn').classList.add('active');
        }
    </script>
</body>
</html>
"""

QUIZ_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة سر التفوق - حل الاختبار</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .question-box { background: #fdfdfd; border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 10px; border-right: 5px solid #114b3e; }
        .options-list { margin-top: 10px; display: flex; flex-direction: column; gap: 8px; }
        .option-item { background: #f9f9f9; border: 1px solid #e0e0e0; padding: 10px 12px; border-radius: 8px; cursor: pointer; font-size: 14px; }
        .option-item:hover { background: #e8f5e9; border-color: #114b3e; }
        .option-item input { margin-left: 10px; }
        .badge-type { display: inline-block; background: #e8f5e9; color: #114b3e; padding: 2px 8px; border-radius: 6px; font-size: 12px; font-weight: bold; margin-bottom: 8px; }
        .hint { color: #555; font-size: 13px; margin-top: 10px; background: #f1f8f6; padding: 8px; border-radius: 6px; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        #timer-box { background: #ffebee; color: #c62828; border: 1px solid #ef9a9a; padding: 10px; border-radius: 10px; text-align: center; font-weight: bold; margin-bottom: 15px; font-size: 16px; display: none; }
        @media print {
            body { display: none !important; }
        }
    </style>
</head>
<body>
    <div class="main-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; border-bottom: 2px solid #eee; padding-bottom: 10px;">
            <span style="font-size: 14px; color: #555;">المستوى: <strong style="color: #114b3e;">{{ level }}</strong></span>
            <span style="font-size: 14px; color: #555;">السؤال: <strong style="color: #114b3e;">{{ current_num }} من {{ total_questions }}</strong></span>
        </div>

        <h2>اختبار الدرس الأول الشامل</h2>
       
        <form method="POST" action="{{ url_for('quiz_step') }}" id="quiz-form">
            <div class="question-box">
                <span class="badge-type">اختيار من متعدد</span>
                <p><strong>سؤال {{ current_num }}:</strong> {{ question.prompt }}</p>
               
                <div class="options-list">
                    {% for opt in question.options %}
                        <label class="option-item">
                            <input type="radio" name="current_answer" value="{{ opt }}" required> {{ opt }}
                        </label>
                    {% endfor %}
                </div>
                <div class="hint">💡 <em>{{ question.hint }}</em></div>
            </div>
           
            <button type="submit" class="start-btn">السؤال التالي ←</button>
        </form>
    </div>
</body>
</html>
"""

RESULT_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نتيجة الامتحان - سر التفوق</title>
    <style>
        body { font-family: 'Tahoma', sans-serif; background-color: #114b3e; color: #333; margin: 0; padding: 20px; direction: rtl; text-align: right; }
        .main-card { max-width: 600px; margin: auto; background: white; padding: 25px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        h2 { text-align: center; color: #114b3e; margin-top: 0; font-size: 26px; }
        .score-box { background: #e8f5e9; border: 2px solid #2e7d32; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 25px; }
        .score-num { font-size: 32px; font-weight: bold; color: #1b5e20; }
        .res-item { background: #f9f9f9; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 10px; }
        .correct { border-right: 5px solid #2e7d32; }
        .wrong { border-right: 5px solid #c62828; }
        .start-btn { display: block; width: 100%; background: #114b3e; color: white; padding: 14px; text-align: center; border-radius: 12px; font-weight: bold; font-size: 16px; border: none; cursor: pointer; box-shadow: 0 4px 10px rgba(17,75,62,0.3); transition: 0.3s; text-decoration: none; box-sizing: border-box; }
        .start-btn:hover { background: #0d382f; }
        .wa-btn { background: #25d366; margin-top: 10px; display: block; text-align: center; }
        .wa-btn:hover { background: #1ebe57; }
    </style>
</head>
<body>
    <div class="main-card">
        <h2>نتيجة اختبارك</h2>
       
        <div class="score-box">
            <p style="margin: 0 0 5px 0; font-size: 16px; color: #333;">لقد أتممت الاختبار بنجاح!</p>
            <div class="score-num">{{ score }} / {{ total }}</div>
            <p style="margin: 5px 0 0 0; font-size: 14px; color: #555;">المستوى: {{ level }}</p>
        </div>

        <h3>تفاصيل الإجابات:</h3>
        <div style="margin-top: 15px;">
            {% for r in results %}
                <div class="res-item {% if r.is_correct %}correct{% else %}wrong{% endif %}">
                    <p><strong>سؤال {{ r.id }}:</strong> {{ r.prompt }}</p>
                    <p style="margin: 5px 0; font-size: 14px;">إجابتك: <span style="font-weight: bold; color: {% if r.is_correct %}#2e7d32{% else %}#c62828{% endif %};">{{ r.user_ans }} {% if r.is_correct %}✅{% else %}❌{% endif %}</span></p>
                    {% if not r.is_correct %}
                        <p style="margin: 5px 0; font-size: 14px; color: #2e7d32;">الإجابة الصحيحة هي: <strong>{{ r.correct_ans }}</strong></p>
                    {% endif %}
                </div>
            {% endfor %}
        </div>

        <button type="button" class="start-btn print-btn" onclick="window.print()" style="background: #455a64; margin-top: 15px;">🖨️ طباعة النتيجة</button>
        <a href="/" class="start-btn" style="text-align: center; margin-top: 10px;">🔄 تصميم امتحان جديد</a>
        <a href="https://wa.me/201221581154?s=t" class="start-btn wa-btn" target="_blank">تواصل عبر الواتساب للاشتراك 💬</a>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
