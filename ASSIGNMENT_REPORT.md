# AI for Everyone – Batch I
## SaaS Product Launch Assignment
### Product: Risers ClassDesk
**Brand:** Risers Network  
**Category:** Education technology / SaaS  
**Prototype:** Streamlit web application

### 1. Problem domain research
Small academies, coaching centres and vocational training providers need to coordinate admissions, attendance, course information and fee collection. In early-stage institutes, these records are often spread across paper registers, spreadsheets and messaging apps. This can make it difficult to find a student's latest status, reconcile payments or prepare a monthly report.

### 2. Target users
- Small private academies and coaching centres
- Independent tutors and training providers
- Vocational and skills-development institutes
- Institute administrators handling admissions and fees

### 3. Proposed solution
Risers ClassDesk provides a single lightweight workspace for student records, course catalogue, daily attendance, payment history and CSV exports.

### 4. MVP functionality
1. Dashboard with student and fee collection metrics
2. Student registration, search and editing
3. Course creation and catalogue
4. Daily attendance (Present, Absent, Late)
5. Payment recording with date, period, method and reference
6. CSV exports and basic revenue summaries

### 5. Technology stack
- Python: application logic
- Streamlit: user interface and hosting workflow
- SQLite: prototype database
- Pandas: tables, summaries and CSV export
- GitHub: source control and deployment source
- Streamlit Community Cloud: public deployment

### 6. AI-assisted development
AI assistance was used to structure the product scope, propose a practical MVP, generate the initial Streamlit application, and prepare deployment and documentation materials. The developer should test every workflow with sample records before public demonstration.

### 7. Business model hypothesis
A freemium model may suit small institutes: a free starter plan for a single administrator, with paid plans for multiple staff accounts, cloud backups, automated reminders and advanced reporting. Pricing should be decided only after interviews and pilot testing.

### 8. Validation plan
Interview at least five institute owners or administrators. Ask:
- How do you currently record admissions and student contact details?
- How do you mark daily attendance?
- How do you track fee due dates and payments?
- What reports take the most time to prepare?
- Would a shared dashboard solve a recurring problem, and what would you pay for it?

### 9. Deployment
The app is prepared for GitHub and Streamlit Community Cloud. Follow README.md to publish and add the live URL to the final submission.

### 10. Limitations and next steps
The current MVP uses local SQLite. Streamlit Community Cloud does not guarantee persistence of local files, so this version is for demonstration and controlled testing. Before handling real student data, integrate managed PostgreSQL, secure authentication, role-based access, backups, privacy controls and a retention policy.

### Conclusion
Risers ClassDesk turns a common administrative problem into a small, testable software product. Its scope is intentionally focused so the product can be deployed quickly, demonstrated clearly and improved using feedback from actual institute operators.
