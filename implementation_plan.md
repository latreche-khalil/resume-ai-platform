# خطة تنفيذ منصة تحليل السيرة الذاتية (Resume Analysis Platform)

## الهدف (Goal Description)

بناء منصة ويب ذكية (MVP) تطبق مفاهيم "Explainable AI Recruitment" كما وردت في مذكرة التخرج. تهدف المنصة لمساعدة الباحثين عن عمل من خلال تحليل دقيق يكشف "الفجوة الدلالية" بينهم وبين الوظائف، وليس مجرد مطابقة كلمات.

## التوافق مع مذكرة التخرج (Thesis Alignment) 🎓

تم تصميم هذه الخطة لتطبيق المفاهيم النظرية الواردة في المذكرة حرفياً:

1.  **المشكلة (Research Problem - 1.2):** غياب الشفافية للمرشحين ("Black Box").
    - _الحل التقني:_ استخدام **Explainable AI (XAI)** لتوليد نصوص تشرح سبب القبول/الرفض بدلاً من الأرقام الصماء (كما هو مطلوب للإجابة على Figure 2.4).
2.  **المنهجية (Methodology - 2.1 & 2.2):** الانتقال من الكلمات المفتاحية (Keyword Matching) إلى الفهم الدلالي (Semantic Understanding).
    - _الحل التقني:_ استخدام **Vector Embeddings** و **Cosine Similarity** لقياس التشابه المعنوي (مثلاً: ريادة الأعمال ≈ الإدارة) في فضاء متعدد الأبعاد (High-dimensional Vector Space).
3.  **الهدف (Purpose - 1.3):** تحسين ملف المرشح (Upskilling).
    - _الحل التقني:_ ميزة **Roadmap Generation** لاقتراح مهارات محددة ترفع نسبة القبول للمرات القادمة.

## التقنيات والأدوات (Tech Stack)

تم اختيار "Hybrid Architecture" لدمج أفضل ما في العالمين:

### 1. الواجهة الأمامية (Frontend & UX)

- **Framework:** **Next.js 14** (App Router)
  - لتوفير واجهة مستخدم تفاعلية تعرض الرسوم البيانية (Charts) لوصف الـ Resume Features بوضوح.
- **Styling:** **Tailwind CSS**
  - لتصميم واجهة نظيفة واحترافية (Dark Mode preferred).

### 2. الخلفية والذكاء الاصطناعي (Backend & AI - Python) 🐍

- **Framework:** **FastAPI**
  - الخيار الأمثل للسرعة (High Performance) وسهولة التعامل مع البيانات.
- **AI Logic & NLP:**
  - **OpenAI Embeddings:** لتحويل النصوص (Resume & Job Description) إلى Vectors.
  - **Scikit-learn / NumPy:** لحساب **Cosine Similarity** بدقة رياضية (تطبيق للمعادلة في الشكل 2.3).
  - **GPT-4o:** للعمل كـ "XAI Explainer" لشرح النتائج للمستخدم بلغة طبيعية.

## الهيكلة المقترحة (Proposed Structure)

### [Backend] `api/` (Python/FastAPI)

- `main.py`: نقطة الدخول (Entry Point).
- `endpoints/analyze.py`: يستقبل كافة الصيغ (PDF, DOCX, IMG, TXT).
- `services/parser.py`: مركز استخراج النصوص المتطور (يدعم OCR للصور + ملفات Word/PDF).
- `services/ai_engine.py`: حساب التوافق (Vectors) وتوليد الشرح (LLM).

### [Frontend] `web/` (Next.js)

- `components/Upload.tsx`: واجهة الرفع وحقل إدخال "الوصف الوظيفي" (Job Description).
- `components/Results/ScoreGauge.tsx`: عداد النسبة المئوية للتطابق.
- `components/Results/XAIExplanation.tsx`: صندوق "لماذا حصلت على هذه النتيجة؟".
- `components/Results/InterviewPrep.tsx`: بطاقات تعرض أسئلة المقابلة المتوقعة وكيفية الإجابة عليها.
- `components/Results/BiasChecker.tsx`: تنبيهات حول التحيز.
- `components/Results/HeatmapOverlay.tsx`: طبقة شفافة تلون السيرة الذاتية (أحمر/أزرق) حسب أهمية المحتوى.
- `components/Results/SkillsGraph.tsx`: رسم بياني تفاعلي للمهارات.
- `components/Results/RecruiterChat.tsx`: مساعد ذكي (Chatbot) لمناقشة النتائج.
- `components/Results/Roadmap.tsx`: خطوات التحسين المقترحة.

## منهجية العمل (Workflow)

1. يقوم المستخدم بلصق **الوصف الوظيفي (Job Description)**.
2. يرفع المستخدم السيرة الذاتية (بأي صيغة: **PDF, Word, أو حتى صورة PNG/JPG**).
3. يقوم النظام بالتعرف على الصيغة واستخراج النص (باستخدام **OCR** إذا كان ملف صورة).
4. يقوم `FastAPI` بتحويل (السيرة الذاتية + الوصف الوظيفي) إلى **Vectors**.
5. تتم مقارنة المتجهين باستخدام **Cosine Similarity** لكشف مدى التطابق الدلالي.
6. يعود النظام بـ JSON يحتوي على:
   - `match_score`: (0-100%).
   - `explanation`: نص تفسيري (XAI).
   - `missing_skills`: قائمة المهارات المفقودة دلالياً.
   - `interview_questions`: 5 أسئلة متوقعة للمقابلة بناءً على الفجوات والخبرات.
   - `bias_report`: تقرير عن المخالفات الأخلاقية المحتملة.
   - `skills_graph`: بيانات الشبكة التفاعلية.
   - `heatmap_data`: إحداثيات المناطق (Hot/Cold) لتلوين السيرة الذاتية بصرياً.
   - `chat_session_id`: معرف الجلسة لبدء المحادثة مع "AI Recruiter".
