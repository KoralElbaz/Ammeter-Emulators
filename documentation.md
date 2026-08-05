# 📊 Ammeter Analysis System

## 📌 1. Overview

מערכת זו נועדה לבצע:

- דגימה של זרם ממספר אמפרמטרים  
- ניתוח סטטיסטי של המדידות  
- השוואה בין מכשירים  
- ניהול תוצאות  

המערכת בנויה בצורה מודולרית עם הפרדה ברורה של אחריות בין רכיבים.

---

## 🏗️ 2. Architecture
TEST_QA_EXPANDED/
│
├── Ammeters/                     # תקשורת עם מכשירים (Hardware Layer)
│   ├── base_ammeter.py           # מחלקת בסיס לכל אמפרמטר
│   ├── client.py                 # ניהול תקשורת socket
│   ├── Circutor_Ammeter.py       # מימוש מכשיר
│   ├── Entes_Ammeter.py          # מימוש מכשיר
│   └── Greenlee_Ammeter.py       # מימוש מכשיר
│
├── config/                       # קונפיגורציה
│   └── config.yaml
│
├── src/
│   │
│   ├── analyzers/                # לוגיקת ניתוח נתונים
│   │   ├── measurement_analyzer.py
│   │   └── multi_device_analyzer.py
│   │
│   ├── utils/                    # שירותים ותשתיות
│   │   ├── sampling_service.py   # איסוף דגימות
│   │   ├── config.py             # טעינת קונפיג
│   │   ├── logger.py             # לוגים
│   │   └── Utils.py
│   │
│   ├── visualization/            # הצגת נתונים
│   │   └── chart_printer.py
│   │
│   ├── results/                  # ניהול תוצאות (Requirement 4)
│   │   └── result_manager.py
│   
│
├── results/                      # תוצאות ריצה (JSON files)
│   ├── 2026-08-04_19-45-34.json
│   └── 2026-08-04_20-00-21.json
│
├── main.py                       # נקודת כניסה למערכת

## 🧩 3. Core Components

### 🔌 3.1 Client (Socket Communication)
**אחריות:**
- תקשורת עם האמפרמטרים דרך socket  
- שליחת פקודות  
- קבלת נתונים  



### 🔌 3.2 SamplingService
**אחריות:**
- איסוף דגימות ממכשיר
- ניהול זמן בין קריאות
- הפשטת הקריאה ל־float בלבד

### 🔌 3.3 MeasurementAnalyzer
**אחריות:**
- חישוב סטטיסטיקות על דגימות


### 🔌 3.4 MeasurementAnalyzer
**אחריות:**
- ניתוח מספר מכשירים
- השוואה ביניהם
- דירוג לפי יציבות (סטיית תקן)

### 🔌 3.5 Visualization
**אחריות:**
- מדפיס גרף טקסטואלי 
- משמש להבנה ויזואלית מהירה של התפלגות הערכים.


## 🗂️ 4. Result Management
**אחריות:**
- שמירת תוצאות ריצה
- זיהוי ייחודי לכל run
- שמירת metadata
- שליפה והשוואה


## ⚠️ 5. Challenges & Issues
בעת ההרצה הראשונית נתקלתי בבעיה:
No data received

**הסיבה:**

השרת מחזיר נתונים רק כאשר הפקודה שנשלחת תואמת בדיוק ל־command שהוגדר בכל Ammeter.

**הפתרון:**

לאחר ניתוח הקוד ב־base_ammeter.py הבנתי שיש השוואה ישירה בין ה־data לבין get_current_command, ולכן יש לשלוח את ה־bytes המדויקים.


חוסר התאמה בין main ל־config 
במהלך הפיתוח זיהיתי חוסר התאמה בין:
- ports
- commands

**הפתרון:**

שימוש בקובץ config.yaml כמקור אמת במקום ערכים hardcoded.


# שימוש בקובץ קונפיגורציה

פרטי האמפרמטרים (פורט ופקודות) מוגדרים בקובץ:
config/config.yaml

**יתרונות:**

- הפרדה בין לוגיקה להגדרות
- גמישות גבוהה
- תחזוקה קלה
- התאמה לפרויקטים אמיתיים


# שימוש בספריות

נעשה שימוש בספרייה:

- PyYAML — לקריאת YAML

# מימוש חישובים ידני

בדרישה 3 בחרתי לממש ידנית:

median
standard deviation

למה?

לצמצם dependencies
להראות שליטה באלגוריתמים בסיסיים


# איך להריץ?
pip install pyyaml
python main.py

## ✅ סיכום 
המערכת מספקת פתרון מלא ל:

- דגימה
- ניתוח
- השוואה
- ויזואליזציה
- ניהול תוצאות

תוך שימוש בארכיטקטורה מודולרית, ברורה ונוחה להרחבה.
