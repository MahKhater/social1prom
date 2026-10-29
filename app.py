import random
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'ser_el_tafouk_secret_key' # مفتاح الجلسة لتخزين الأسئلة والإجابات

QUESTIONS_DB = {
  "مبتدئ": [
           {
"id": 114,
        "type": "true/false",
        "prompt": "تكونت بعض الممالك الإسلامية التاريخية أيضاً في غرب قارة إفريقيا وفقاً لما ورد في المنهج.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 115,
        "type": "multiple choice",
        "prompt": " إذا قمت برحلة بحرية من الإسكندرية بمصر إلى موريتانيا، فإنك ستعبر مضيق:",
        "options": ["موزمبيق", "باب المندب", "جبل طارق", "هرمز"],
        "answer": "مضيق جبل طارق"
    },
    {
        "id": 116,
        "type": "true/false",
        "prompt": "تعد دولة الصومال الدولة العربية الوحيدة بالقارة الإفريقية التي يمر بها دائرة الاستواء وفقاً لتدريبات الأضواء.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 117,
        "type": "multiple choice",
        "prompt": " أي من الدول التالية يتقاطع بها مدار السرطان مع خط جرينتش؟",
        "options": ["ليبيا", "مصر", "الجزائر", "تونس"],
        "answer": "الجزائر"
    },
    {
        "id": 118,
        "type": "true/false",
        "prompt": " تم رسم خريطة للنيل حتى جنوب السودان في عهد محمد علي باشا.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 119,
        "type": "multiple choice",
        "prompt": "تتوزع القوافل العربية التاريخية الاستكشافية في إفريقيا حيث وصلت إلى السودان وجزر القمر وبلاد:",
        "options": ["المغرب العربي", "الحبشة", "بونت القديمة", "جنوب إفريقيا"],
        "answer": "الحبشة"
    },
    {
        "id": 120,
        "type": "true/false",
        "prompt": "تضم قارة إفريقيا دولاً عربية يبلغ عددها إجمالاً 10 دول مختلفة المساحة.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 121,
        "type": "multiple choice",
        "prompt": "تم اكتشاف النيل الأبيض في العصر الحديث خلال عهد:",
        "options": ["الخديو إسماعيل", "محمد علي باشا", "الملك نخاو الثاني", "الأمير هنري الملاح"],
        "answer": "محمد علي باشا"
    },
    {
        "id": 122,
        "type": "true/false",
        "prompt": "يعد جبل كينيا من الجبال الانكسارية التي نشأت في وسط القارة الإفريقية.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 123,
        "type": "multiple choice",
        "prompt": "يتطابق سبب نشأة التكوين الجغرافي لجبل كلمنجارو مع سبب نشأة جبل:",
        "options": ["أطلس", "كينيا", "الكاب", "شايب البنات"],
        "answer": "كينيا"
    },
    {
        "id": 124,
        "type": "true/false",
        "prompt": "جبال دراكنزبرج وجبال الكاب تقعان معاً في الجزء الجنوبي من القارة الإفريقية.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 125,
        "type": "multiple choice",
        "prompt": "تتميز السهول الساحلية المطلة على البحر المتوسط في شمال مصر بوجود محاصيل زراعية ونباتات تعتمد على الأمطار:",
        "options": ["الشتوية", "الصيفية طوال العام", "الموسمية الغزيرة", "المدارية المتطرفة"],
        "answer": "الشتوية"
    },
    {
        "id": 126,
        "type": "true/false",
        "prompt": " يقع جبل شايب البنات (أعلى قمة في جبال البحر الأحمر) في جمهورية مصر العربية.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 127,
        "type": "multiple choice",
        "prompt": " ما هو العامل المشترك التكويني بين هضبة الحبشة والهضبة الجنوبية؟",
        "options": ["وجود بحيرات عذبة", "وجود انكسارات طولية", "تعرضهما لثورانات بركانية واسعة", "وجود صحارى رملية"],
        "answer": "وجود انكسارات طولية"
    },
    {
        "id": 128,
        "type": "true/false",
        "prompt": "يقطع مدار الجدي في قارة إفريقيا تضاريس الهضبة الجنوبية وفقاً لأسئلة مستوى القمة.",
        "options": ["صح", "خطأ"],
        "answer": "صح"    }
],
"متوسط": [
          {
"id": 448,
"type": "true/false",
"prompt": "تتميز جبال البحر الأحمر الانكسارية بأنها تمتد داخل أراضي مصر والسودان ودولة إريتريا.",
"options": ["صح", "خطأ"],
"answer": "صح"
},
{
"id": 449,
"type": "multiple choice",
"prompt": "أعلى قمة جبلية في سلسلة جبال البحر الأحمر الانكسارية وتوجد داخل مصر هي جبل:",
"options": ["توبقال", "شايب البنات", "كينيا", "كلمنجارو"],
"answer": "شايب البنات"
},
{
"id": 450,
"type": "true/false",
"prompt": "تعد جبال كينيا وكلمنجارو في وسط إفريقيا وجبال دراكنزبرج في جنوبها من الجبال البركانية التكوين.",
"options": ["صح", "خطأ"],
"answer": "صح"
},
{
"id": 451,
"type": "multiple choice",
"prompt": "المصطلح الجغرافي الذي يُعبر عن (مجموعة انكسارات طولية تمتد شرق قارة إفريقيا وتتجه بشكل عام من الجنوب إلى الشمال) هو:",
"options": ["حوض نهر النيل", "الأخدود الإفريقي العظيم", "السهول الفيضية", "سلاسل جبال أطلس"],
"answer": "الأخدود الإفريقي العظيم"
},
{
"id": 452,
"type": "true/false",
"prompt": "يُعد كل من البحر الأحمر وخليج عدن وخليج العقبة من الأجزاء التابعة للأخدود الإفريقي العظيم شرق القارة.",
"options": ["صح", "خطأ"],
"answer": "صح"
},
{
"id": 453,
"type": "multiple choice",
"prompt": "تساهم المناطق الجبلية في قارة إفريقيا في دعم العديد من الأنشطة الاقتصادية الهامة مثل التعدين والصناعة و:",
"options": ["الرعي الجاف", "السياحة", "صيد الأسماك النهرية", "استصلاح الصحاري الملحية"],
"answer": "السياحة"
},
{
"id": 454,
"type": "true/false",
"prompt": "تتميز السهول الفيضية الخصبة في إفريقيا بصلاحيتها التامة لحرفة الزراعة نتيجة للمواد والترسبات الطمية التي كونتها الأنهار.",
"options": ["صح", "خطأ"],
"answer": "صح"
},
{
"id": 455,
        "type": "multiple choice",
        "prompt": "يمتد اليابس الإفريقي فلكياً عبر عدد من الدوائر العرضية يبلغ حوالي:",
        "options": ["51 دائرة عرضية", "68 دائرة عرضية", "70 دائرة عرضية", "72 دائرة عرضية"],
        "answer": "70 دائرة عرضية"
    },
    {
        "id": 456,
        "type": "true/false",
        "prompt": "يمر خط الطول الرئيسي جرينتش في الجزء الشرقي من القارة الإفريقية.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 457,
        "type": "multiple choice",
        "prompt": "المسطح المائي الذي يحد قارة إفريقيا من جهة الغرب ويفصلها عن قارتي أمريكا الشمالية والجنوبية هو:",
        "options": ["المحيط الهندي", "المحيط الأطلنطي", "البحر المتوسط", "خليج عدن"],
        "answer": "المحيط الأطلنطي"
    },
    {
        "id": 458,
        "type": "true/false",
        "prompt": "تقع دولة الجزائر كأكبر دول القارة الإفريقية مساحة في نطاق تضاريس الهضبة الجنوبية.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 459,
        "type": "multiple choice",
        "prompt": "من أمثلة الدول الحبيسة التي لا تطل على مسطحات مائية ومذكورة في الخريطة السياسية للدرس دولة:",
        "options": ["مصر", "المغرب", "الصومال", "مالي"],
        "answer": "مالي"
    },
    {
        "id": 460,
        "type": "true/false",
        "prompt": "تُصنف دولة الصومال ودولة المغرب كأمثلة للدول الساحلية في قارة إفريقيا.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 461,
        "type": "multiple choice",
        "prompt": "أحد الجغرافيين والرحالة العرب الذي زار إفريقيا وكتب عنها وكان من أوائل الرحالة هو:",
        "options": ["ابن خلدون", "ابن سينا", "المسعودي", "ابن الهيثم"],
        "answer": "المسعودي"
    },
    {
        "id": 462,
        "type": "true/false",
        "prompt": "نجح الرحالة العربي ابن بطوطة في اختراق الصحراء الكبرى من الشمال إلى الجنوب حتى وصل إلى مالي.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 463,
        "type": "multiple choice",
        "prompt": "بدأ البرتغاليون محاولاتهم لاكتشاف إفريقيا في القرن الخامس عشر الميلادي خلال عهد الأمير:",
        "options": ["فاسكو دي جاما", "بارتولوميو دياس", "هنري الملاح", "جون سبيك"],
        "answer": "هنري الملاح"
    },
    {
        "id": 464,
        "type": "true/false",
        "prompt": "أسس البرتغاليون الموانئ والمراكز التجارية على طول طريق رأس الرجاء الصالح بهدف تأمين الملاحة والتجارة.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 465,
        "type": "multiple choice",
        "prompt": "في العصر الحديث، أرسل محمد علي باشا رحلات لاكتشاف منابع النيل عام 1839م وانتهت باكتشاف النيل:",
        "options": ["الأزرق", "الأبيض", "المباركي", "الفيضي"],
        "answer": "النيل الأبيض"
    },
    {
        "id": 466,
        "type": "true/false",
        "prompt": "وصل المد الحضاري والحكم المصري في عهد الخديو إسماعيل إلى جنوب دائرة الاستواء أثناء اكتشاف منابع النيل.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
}
],
 "محترف": [
        { 
"id": 796,
"type": "true/false",
"prompt": "قامت مصر بحفر عشرات الآبار لتوفير المياه النقية في دولة كينيا كأحد جهود التنمية المائية المستدامة الصديقة للبيئة.",
"options": ["صح", "خطأ"],
"answer": "صح"
},
{
"id": 797,
"type": "multiple choice",
"prompt": "السد المائي الذي قامت مصر بالمساهمة الكاملة في إنشائه وتشييده في دولة أوغندا لدعم التنمية المستدامة هو سد:",
"options": ["سنار", "أوين", "جبل الأولياء", "العالي"],
"answer": "أوين"
},
{
"id": 798,
"type": "true/false",
"prompt": "ساهمت مصر في إنشاء وتأسيس خزان سنار التاريخي على مجرى النيل الأزرق لخدمة دولة السودان.",
"options": ["صح", "خطأ"],
"answer": "صح"
},
{
"id": 799,
"type": "multiple choice",
"prompt": "تحملت مصر تكاليف إنشاء خزان مائي لتوليد الطاقة الكهربائية وتخزين المياه بدولة السودان هو خزان:",
"options": ["سد أوين", "جبل الأولياء", "خزان سنار الجديد", "السد العالي"],
"answer": "جبل الأولياء"
},
{
"id": 800,
"type": "true/false",
"prompt": "ساهمت جمهورية مصر العربية في تطهير بحيرتي فيكتوريا وكيوجا من الحشائش والنباتات المائية الضارة المانعة للجريان المائي.",
"options": ["صح", "خطأ"],
"answer": "صح"
},
{
"id": 801,
"type": "multiple choice",
"prompt": "من مشروعات مصر المائية المستدامة الموثقة لدعم البحث العلمي المائي في دول الحوض إنشاء مركز للبحوث المائية في دولة:",
"options": ["كينيا", "تنزانيا", "السودان", "أوغندا"],
"answer": "تنزانيا"
},
{
"id": 802,
"type": "true/false",
"prompt": "نصت اتفاقية المبادئ عام 2015م بين مصر وإثيوبيا والسودان على مبدأ التعاون والتنمية وعدم التسبب في ضرر والاستخدام المنصف والمناسب.",
"options": ["صح", "خطأ"],
"answer": "صح"
},
{
"id": 803,
"type": "multiple choice",
"prompt": "من أمثلة الدول الحبيسة التي لا تطل على مسطحات مائية دولة النيجر ودولة:",
"options": ["الصومال", "المغرب", "تشاد", "مصر"],
"answer": "تشاد"
},
{
"id": 804,
"type": "true/false",
"prompt": "تم انتخاب مصر لرئاسة الاتحاد الإفريقي عام 2019م مما ساهم في تعميق دورها الريادي في قارة إفريقيا وتدعيم علاقاتها بشعوبها.",
"options": ["صح", "خطأ"],
"answer": "صح"
},
{
"id": 805,
        "type": "multiple choice",
        "prompt": "يحد افريقيا من جهة الشمال مسطح مائي يفصلها عن أوروبا وهو:",
        "options": ["البحر الأحمر", "البحر المتوسط", "المحيط الأطلنطي", "المحيط الهندي"],
        "answer": "البحر المتوسط"
    },
    {
        "id": 806,
        "type": "true/false",
        "prompt": "تقترب قارة إفريقيا من قارة أوروبا جغرافياً عند ممر مائي استراتيجي هو مضيق باب المندب.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 807,
        "type": "multiple choice",
        "prompt": "الدولتان العربيتان الإفريقيتان اللتان تقعان بأكملهما في النصف الكروي الغربي وفقاً لخريطة المنهج هما المغرب و:",
        "options": ["الجزائر", "تونس", "موريتانيا", "ليبيا"],
        "answer": "موريتانيا"
    },
    {
        "id": 809,
        "type": "multiple choice",
        "prompt": "أي من الدول العربية الإفريقية التالية يتقاطع فيها مدار السرطان الفلكي مع خط الطول الرئيسي جرينتش؟",
        "options": ["مصر", "ليبيا", "تونس", "الجزائر"],
        "answer": "الجزائر"
    },
    {
        "id": 810,
        "type": "true/false",
        "prompt": "تعد دولة الصومال الدولة العربية الوحيدة في القارة الإفريقية التي تمر بها دائرة الاستواء في ممرها الشرقي.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 811,
        "type": "multiple choice",
        "prompt": "نشأت على أرض القارة الإفريقية قديماً حضارة أكسوم، وتقع أراضيها التاريخية حالياً في دولتي:",
        "options": ["مصر والسودان", "تونس والجزائر", "إريتريا وإثيوبيا", "ليبيا وتشاد"],
        "answer": "إريتريا وإثيوبيا"
    },
    {
        "id": 812,
        "type": "true/false",
        "prompt": "تطابقت جبال كينيا وكلمنجارو في وسط القارة من حيث سبب النشأة، حيث تكونتا نتيجة الحركات الالتوائية الباطنية.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 813,
        "type": "multiple choice",
        "prompt": "يتشابه سبب النشأة التكوينية الباطنية لجبال أطلس في الشمال الغربي مع جبال الكاب في الجنوب بوصفهما جبالاً:",
        "options": ["انكسارية", "التوائية", "بركانية", "تصدعية"],
        "answer": "التوائية"
    },
    {
        "id": 814,
        "type": "true/false",
        "prompt": "تتميز جبال البحر الأحمر بأنها جبال انكسارية تمتد على طول ساحل البحر الأحمر في مصر والسودان ودولة إريتريا.",
        "options": ["صح", "خطأ"],
        "answer": "صح"
    },
    {
        "id": 815,
        "type": "multiple choice",
        "prompt": "أعلى قمة جبلية في سلاسل جبال البحر الأحمر الانكسارية وتقع داخل الحدود الجغرافية لمصر هي جبل:",
        "options": ["العوينات", "شايب البنات", "توبقال", "كلمنجارو"],
        "answer": "شايب البنات"
    },
    {
        "id": 816,
        "type": "true/false",
        "prompt": "تحصر سلسلتا جبال أطلس المتوازيتان (أطلس التل وأطلس الصحراء) بينهما هضبة الشطوط بدولة المغرب.",
        "options": ["صح", "خطأ"],
        "answer": "خطأ"
    },
    {
        "id": 817,
        "type": "multiple choice",
        "prompt": "يتكون الجليد فوق قمة جبل كلمنجارو بالرغم من وقوعه في المنطقة الاستوائية الحارة بسبب عامل:",
        "options": ["الموقع الفلكي القطبي", "شدة الارتفاع وعلو القمة", "القرب من المحيط الهندي", "تأثير الرياح التجارية"],
        "answer": "شدة الارتفاع وعلو القمة"
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
            <div class="section-title">اختيار مستوى الصعوبة الدرس الاول دراسات اجتماعية اولى اعدادي    </div>
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
