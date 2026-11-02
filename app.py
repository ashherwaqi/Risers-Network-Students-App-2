import streamlit as st
import sqlite3
import pandas as pd
from datetime import date, datetime
from pathlib import Path

APP_DIR = Path(__file__).parent
DB_PATH = Path("classdesk.db")  # For production, use persistent external PostgreSQL storage.

st.set_page_config(page_title="Risers ClassDesk", page_icon="🎓", layout="wide")

GOLD = "#D6B15E"
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
html, body, [class*="css"] {{ font-family: 'DM Sans', sans-serif; }}
.stApp {{ background: #0B0D12; color: #F5F1E8; }}
[data-testid="stSidebar"] {{ background: #11151D; border-right: 1px solid #29251B; }}
h1,h2,h3 {{ color: #F5F1E8; }}
.brand {{ color:{GOLD}; font-family:'Playfair Display',serif; letter-spacing:.4px; }}
.metric-card {{ background:linear-gradient(145deg,#171C26,#11151D); border:1px solid #34302A; border-radius:14px; padding:18px; }}
.metric-label {{ color:#A9A49A; font-size:13px; }}
.metric-value {{ color:{GOLD}; font-size:28px; font-weight:700; }}
div.stButton > button {{ border-radius:9px; border:1px solid {GOLD}; }}
</style>
""", unsafe_allow_html=True)

def connect():
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.execute("PRAGMA foreign_keys = ON")
    return con

def init_db():
    with connect() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS courses(
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL,
            duration TEXT DEFAULT '', fee REAL DEFAULT 0, active INTEGER DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, phone TEXT,
            email TEXT, course_id INTEGER, admission_date TEXT, monthly_fee REAL DEFAULT 0,
            scholarship REAL DEFAULT 0, status TEXT DEFAULT 'Active', notes TEXT,
            FOREIGN KEY(course_id) REFERENCES courses(id)
        );
        CREATE TABLE IF NOT EXISTS attendance(
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL,
            attendance_date TEXT NOT NULL, status TEXT NOT NULL,
            UNIQUE(student_id, attendance_date),
            FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS payments(
            id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL,
            amount REAL NOT NULL, payment_date TEXT NOT NULL, period TEXT,
            method TEXT DEFAULT 'Cash', reference TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id) ON DELETE CASCADE
        );
        """)
        count = con.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
        if count == 0:
            con.executemany("INSERT INTO courses(name,duration,fee) VALUES(?,?,?)", [
                ("IELTS Preparation","8 weeks",25000),
                ("Data Analytics with AI","12 weeks",35000),
                ("Forex & Commodity Trading","8 weeks",30000),
                ("Digital Marketing with AI","8 weeks",25000),
                ("English Language","12 weeks",18000)
            ])

def query(sql, params=()):
    with connect() as con:
        return pd.read_sql_query(sql, con, params=params)

def execute(sql, params=()):
    with connect() as con:
        cur = con.execute(sql, params)
        con.commit()
        return cur.lastrowid

def money(x):
    return f"PKR {float(x or 0):,.0f}"

init_db()
courses = query("SELECT * FROM courses WHERE active=1 ORDER BY name")
students = query("""SELECT s.*, c.name course_name FROM students s
                    LEFT JOIN courses c ON s.course_id=c.id ORDER BY s.id DESC""")
payments = query("""SELECT p.*, s.name student_name FROM payments p
                    JOIN students s ON p.student_id=s.id ORDER BY p.payment_date DESC, p.id DESC""")

with st.sidebar:
    st.markdown('<div class="brand" style="font-size:27px">RISERS NETWORK</div>', unsafe_allow_html=True)
    st.caption("THE PLEDGE (ALLEGIANCE) IS FOR ALLAH")
    st.markdown("---")
    page = st.radio("WORKSPACE", ["Dashboard","Students","Attendance","Fee Management","Courses","Reports & Export","About Project"])
    st.markdown("---")
    st.caption("ClassDesk • Institute Operations")
    st.caption("Built for learning and productive support.")

st.markdown('<div class="brand">RISERS NETWORK</div>', unsafe_allow_html=True)
st.title("ClassDesk")
st.caption("A simple operating system for growing training institutes.")

if page == "Dashboard":
    total = len(students)
    active = int((students.status == "Active").sum()) if total else 0
    collected = float(payments.amount.sum()) if len(payments) else 0
    pending = 0.0
    if total:
        pending = float(((students.monthly_fee - students.scholarship).clip(lower=0)).sum())
        this_month = date.today().strftime("%Y-%m")
        paid_month = query("SELECT COALESCE(SUM(amount),0) total FROM payments WHERE substr(payment_date,1,7)=?", (this_month,)).iloc[0]["total"]
    else:
        paid_month = 0
    c1,c2,c3,c4 = st.columns(4)
    for col,label,value in [
        (c1,"Total students",f"{total}"),
        (c2,"Active students",f"{active}"),
        (c3,"Total collected",money(collected)),
        (c4,"Collected this month",money(paid_month))
    ]:
        with col:
            st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)
    st.subheader("Recent admissions")
    st.dataframe(students[["id","name","course_name","phone","admission_date","status"]].head(8) if total else pd.DataFrame(columns=["id","name","course_name","phone","admission_date","status"]), use_container_width=True, hide_index=True)
    left,right = st.columns(2)
    with left:
        st.subheader("Fee collection by month")
        if len(payments):
            p = payments.copy()
            p["month"] = pd.to_datetime(p.payment_date).dt.strftime("%Y-%m")
            chart = p.groupby("month",as_index=False).amount.sum().sort_values("month")
            st.bar_chart(chart.set_index("month"))
        else: st.info("Payment activity will appear here after you record a fee.")
    with right:
        st.subheader("Course enrolments")
        if total:
            st.bar_chart(students.groupby("course_name").size())
        else: st.info("Add students to see course enrolments.")

elif page == "Students":
    st.subheader("Student directory")
    with st.expander("＋ Register a student", expanded=False):
        with st.form("new_student", clear_on_submit=True):
            a,b = st.columns(2)
            name = a.text_input("Full name *")
            phone = b.text_input("Phone / WhatsApp")
            email = a.text_input("Email")
            course_options = {r["name"]:int(r["id"]) for _,r in courses.iterrows()}
            course_name = b.selectbox("Course", list(course_options) or ["No active courses"])
            admission = a.date_input("Admission date", value=date.today())
            monthly_fee = b.number_input("Monthly / course fee (PKR)", min_value=0.0, step=500.0)
            scholarship = a.number_input("Scholarship discount (PKR)", min_value=0.0, step=500.0)
            status = b.selectbox("Status", ["Active","Completed","Paused","Withdrawn"])
            notes = st.text_area("Notes")
            submitted = st.form_submit_button("Save student", type="primary")
            if submitted:
                if not name.strip(): st.error("Please enter the student's name.")
                elif not course_options: st.error("Create a course before registering a student.")
                elif scholarship > monthly_fee: st.error("Scholarship cannot exceed the listed fee.")
                else:
                    execute("""INSERT INTO students(name,phone,email,course_id,admission_date,monthly_fee,scholarship,status,notes)
                               VALUES(?,?,?,?,?,?,?,?,?)""",
                            (name.strip(),phone,email,course_options[course_name],admission.isoformat(),monthly_fee,scholarship,status,notes))
                    st.success("Student registered.")
                    st.rerun()
    if len(students):
        search = st.text_input("Search by name, phone or course")
        view = students.copy()
        if search:
            mask = view[["name","phone","course_name"]].fillna("").astype(str).apply(lambda c:c.str.contains(search,case=False)).any(axis=1)
            view = view[mask]
        st.dataframe(view[["id","name","phone","email","course_name","admission_date","monthly_fee","scholarship","status"]], use_container_width=True, hide_index=True)
        with st.expander("Edit or update a student"):
            sid = st.selectbox("Select student ID", view.id.tolist())
            row = students[students.id==sid].iloc[0]
            with st.form("edit_student"):
                en = st.text_input("Name",row["name"])
                ep = st.text_input("Phone",row["phone"] or "")
                ee = st.text_input("Email",row["email"] or "")
                ec = st.selectbox("Course",list(course_options),index=list(course_options.values()).index(int(row["course_id"])) if int(row["course_id"]) in course_options.values() else 0)
                ef = st.number_input("Fee (PKR)",min_value=0.0,value=float(row["monthly_fee"]),step=500.0)
                es = st.number_input("Scholarship (PKR)",min_value=0.0,value=float(row["scholarship"]),step=500.0)
                est = st.selectbox("Status",["Active","Completed","Paused","Withdrawn"],index=["Active","Completed","Paused","Withdrawn"].index(row["status"]))
                if st.form_submit_button("Update student"):
                    if es > ef: st.error("Scholarship cannot exceed fee.")
                    else:
                        execute("UPDATE students SET name=?,phone=?,email=?,course_id=?,monthly_fee=?,scholarship=?,status=? WHERE id=?",(en,ep,ee,course_options[ec],ef,es,est,int(sid)))
                        st.success("Student updated."); st.rerun()
    else: st.info("No students yet. Register your first learner above.")

elif page == "Attendance":
    st.subheader("Daily attendance")
    if len(students):
        active_students = students[students.status=="Active"]
        chosen_date = st.date_input("Attendance date",date.today())
        if len(active_students):
            with st.form("attendance_form"):
                marks = {}
                for _,r in active_students.iterrows():
                    marks[int(r.id)] = st.selectbox(f'{r["name"]} • {r["course_name"]}',["Present","Absent","Late"],key=f'att_{r.id}')
                if st.form_submit_button("Save attendance",type="primary"):
                    for sid,status in marks.items():
                        execute("""INSERT INTO attendance(student_id,attendance_date,status) VALUES(?,?,?)
                                    ON CONFLICT(student_id,attendance_date) DO UPDATE SET status=excluded.status""",(sid,chosen_date.isoformat(),status))
                    st.success("Attendance saved.")
        st.subheader("Attendance register")
        att = query("""SELECT a.attendance_date, s.name, c.name course, a.status
                       FROM attendance a JOIN students s ON s.id=a.student_id
                       LEFT JOIN courses c ON c.id=s.course_id
                       ORDER BY a.attendance_date DESC, s.name""")
        st.dataframe(att, use_container_width=True, hide_index=True)
    else: st.info("Register students before taking attendance.")

elif page == "Fee Management":
    st.subheader("Record a payment")
    if len(students):
        with st.form("payment_form",clear_on_submit=True):
            opts = {f'{r["name"]} (ID {r["id"]})':int(r["id"]) for _,r in students.iterrows()}
            who = st.selectbox("Student",list(opts))
            amount = st.number_input("Amount received (PKR)",min_value=1.0,step=500.0)
            pdate = st.date_input("Payment date",date.today())
            period = st.text_input("Fee period / month",date.today().strftime("%B %Y"))
            method = st.selectbox("Payment method",["Cash","Bank transfer","JazzCash","Easypaisa","Other"])
            ref = st.text_input("Receipt / transaction reference")
            if st.form_submit_button("Record payment",type="primary"):
                execute("INSERT INTO payments(student_id,amount,payment_date,period,method,reference) VALUES(?,?,?,?,?,?)",(opts[who],amount,pdate.isoformat(),period,method,ref))
                st.success("Payment recorded."); st.rerun()
        st.subheader("Payment history")
        st.dataframe(payments[["payment_date","student_name","amount","period","method","reference"]] if len(payments) else pd.DataFrame(),use_container_width=True,hide_index=True)
        st.download_button("Download payment history CSV",payments.to_csv(index=False).encode("utf-8"),"classdesk_payments.csv","text/csv")
        st.caption("Note: outstanding balances are estimates based on the fee entered for each student. Record each billing period's charge separately in your accounting process.")
    else: st.info("Register a student before recording payments.")

elif page == "Courses":
    st.subheader("Course catalogue")
    with st.form("course_form",clear_on_submit=True):
        n = st.text_input("Course name")
        d = st.text_input("Duration",placeholder="e.g. 8 weeks")
        f = st.number_input("Standard fee (PKR)",min_value=0.0,step=500.0)
        if st.form_submit_button("Add course"):
            if n.strip():
                try:
                    execute("INSERT INTO courses(name,duration,fee) VALUES(?,?,?)",(n.strip(),d,f))
                    st.success("Course added."); st.rerun()
                except sqlite3.IntegrityError: st.error("A course with that name already exists.")
            else: st.error("Enter a course name.")
    st.dataframe(courses[["id","name","duration","fee"]] if len(courses) else pd.DataFrame(),use_container_width=True,hide_index=True)

elif page == "Reports & Export":
    st.subheader("Institute reports")
    st.markdown("Export your working data for backup, analysis or sharing with authorized staff.")
    datasets = {
        "Students":("students.csv",students),
        "Payments":("payments.csv",payments),
        "Attendance":("attendance.csv",query("SELECT * FROM attendance ORDER BY attendance_date DESC")),
        "Courses":("courses.csv",query("SELECT * FROM courses"))
    }
    for label,(filename,df) in datasets.items():
        c1,c2 = st.columns([2,1])
        c1.write(f"**{label}** · {len(df)} records")
        c2.download_button(f"Export {label}",df.to_csv(index=False).encode("utf-8"),filename,"text/csv",key=f"dl_{label}")
    if len(payments):
        st.subheader("Revenue summary")
        st.metric("Lifetime recorded collections",money(payments.amount.sum()))
        monthly=payments.copy()
        monthly["month"]=pd.to_datetime(monthly.payment_date).dt.strftime("%Y-%m")
        st.dataframe(monthly.groupby("month",as_index=False).amount.sum().sort_values("month",ascending=False),use_container_width=True,hide_index=True)

else:
    st.subheader("About Risers ClassDesk")
    st.markdown("""
    **Risers ClassDesk** is a lightweight student and institute operations tool created as an AI for Everyone practical SaaS project.

    **Problem researched:** Small training centres often coordinate admissions, attendance and fee collection using disconnected notebooks and spreadsheets.

    **Target users:** Independent tutors, coaching centres, vocational training providers and small academies.

    **Value proposition:** Keep core learner and payment records in one accessible workspace, reduce repetitive administration and make basic reporting easier.

    **MVP scope:** Student directory, course catalogue, attendance register, payment history and CSV reporting.

    **Future roadmap:** Secure staff accounts, role-based access, automated receipts, WhatsApp reminders, scholarship applications, cloud database, parent/student portal and subscription billing.

    **Brand:** Risers Network | Financial Education & Technology
    """)
    st.warning("Deployment note: Streamlit Community Cloud's local filesystem is not durable storage. This MVP uses SQLite for demonstration. For real institute records and multiple users, connect a managed PostgreSQL database and add authentication, backups and privacy controls before production use.")
    st.markdown("**Suggested validation:** Interview 5 local institute owners or administrators. Ask how they currently track admissions, attendance, fees and scholarships, then use their feedback to prioritize the next release.")

st.markdown("---")
st.caption("© Risers Network • ClassDesk • Prototype for AI for Everyone – Batch I")
