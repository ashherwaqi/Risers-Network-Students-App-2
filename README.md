# Risers ClassDesk

A Streamlit MVP for small training institutes: student records, courses, attendance, fee collection and CSV reports.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Run:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```
4. Open the local URL shown by Streamlit.

## Publish free with Streamlit Community Cloud
1. Create a GitHub account and a new public repository named `risers-classdesk`.
2. Upload `app.py`, `requirements.txt`, `.gitignore`, `.streamlit/config.toml`, and this README.
3. Visit https://share.streamlit.io/ and sign in with GitHub.
4. Choose **Create app**, select the repository, branch `main`, and main file `app.py`.
5. Deploy. Your app will receive a public `*.streamlit.app` URL.

## Important production notes
This classroom MVP uses SQLite. Streamlit Community Cloud's local filesystem is not guaranteed to persist across redeploys or restarts. Do not use it for important live student records until you connect managed PostgreSQL (for example, Supabase or Neon), add authentication and role permissions, configure backups, and publish a privacy notice. Do not store sensitive identity documents or payment card details.

## MVP features
- Dashboard metrics and charts
- Student registration, search and updates
- Course catalogue
- Daily attendance with editable status per student/date
- Payment recording and history
- CSV exports for students, payments, attendance and courses
- Risers Network dark-and-gold branding

## Suggested validation
Interview five local institute owners or administrators. Ask how they currently track admissions, attendance and fee payments, and test whether ClassDesk saves time on a real administrative task.

## Assignment summary
**Problem:** Small institutes often manage student and fee information across notebooks and disconnected spreadsheets.
**Solution:** A simple browser-based workspace for core institute operations.
**Audience:** Small academies, tutors, coaching centres and vocational training providers.
**Business model hypothesis:** Free starter tier for one administrator, then a monthly subscription for multiple staff, cloud backups and automated reminders. Validate willingness to pay before building billing.
"# Risers-Network-Students-App-" 
<<<<<<< HEAD
"# Risers-Network-Students-App-" 
"# Risers-Network-Students-App-2" 
=======
>>>>>>> 8a3e15e9ece981222e3333f46d0d9dc01bcb5f53
"# Risers-Network-Students-App-2" 
