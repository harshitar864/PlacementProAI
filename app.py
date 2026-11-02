import streamlit as st
import pandas as pd
import pickle 
import numpy as np
with open("placement_model.pkl", "rb") as file:
    saved_model = pickle.load(file)

model = saved_model["model"]
model_features = saved_model["features"]

st.set_page_config(
    page_title="PlacementPro AI",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1020, #17142e, #211642);
    color: #f1f5f9;
}

h1, h2, h3 {
    color: #c4b5fd !important;
    font-weight: 700;
}

p, label, span {
    color: #e2e8f0;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #252044, #35265c);
    border: 1px solid #7655b7;
    padding: 20px;
    border-radius: 15px;
}

.stButton > button {
    background: linear-gradient(90deg, #7c3aed, #a855f7);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px;
    font-weight: bold;
}

.stButton > button:hover {
    background: #9333ea;
    color: white;
    border: 1px solid #c4b5fd;
}

[data-testid="stSidebar"] {
    background: #111329;
}

input, textarea {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🎓 PlacementPro AI")
st.subheader("Your Smart Campus Placement Dashboard")
st.write("Understand your readiness. Improve your future.")

st.divider()
st.header("👤 Student Profile")

name = st.text_input("Student Name")

col1, col2 = st.columns(2)

with col1:
    cgpa = st.slider("CGPA", 0.0, 10.0, 7.0, 0.1)
    attendance = st.slider("Attendance (%)", 0, 100, 75)
    aptitude = st.slider("Aptitude Score (%)", 0, 100, 60)

with col2:
    coding = st.slider("Coding Score (%)", 0, 100, 50)
    communication = st.slider(
        "Communication Score (%)", 0, 100, 60
    )
    internship = st.selectbox(
        "Internship Experience", ["No", "Yes"]
    )

if st.button("Analyze My Readiness"):
    score = (
        cgpa / 10 * 25
        + attendance * 0.15
        + aptitude * 0.20
        + coding * 0.20
        + communication * 0.20
    )

    if internship == "Yes":
        score = min(score + 5, 100)

    st.divider()
    st.header("📊 Your Placement Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric("Readiness Score", f"{score:.1f}/100")
    c2.metric("CGPA", f"{cgpa:.1f}/10")
    c3.metric("Attendance", f"{attendance}%")

    st.progress(int(score) / 100)

    if score >= 75:
        st.success("Good preparation! Keep improving your skills.")
    elif score >= 50:
        st.warning("You are progressing. Work on weaker skills.")
    else:
        st.info("Focus on fundamentals and regular practice.")

    skills = pd.DataFrame({
        "Skill": [
            "Aptitude", "Coding", "Communication", "Attendance"
        ],
        "Score": [
            aptitude, coding, communication, attendance
        ]
    })

    st.subheader("📈 Skill Performance")
    st.bar_chart(skills.set_index("Skill"))

    st.subheader("🎯 Personalized Recommendations")

    if coding < 60:
        st.write("- Practice Python and coding problems.")
    if aptitude < 60:
        st.write("- Practice quantitative aptitude.")
    if communication < 60:
        st.write("- Practice English and interview questions.")
    if attendance < 75:
        st.write("- Try to improve class attendance.")
    if all(x >= 60 for x in
           [coding, aptitude, communication]):
        st.write("- Continue mock interviews and placement practice.")


        
    

    st.divider()
    st.subheader("📄 Download Your Placement Report")

    report = f"""
    PLACEMENTPRO AI - STUDENT REPORT
    =================================
    Student Name: {name}
    Readiness Score: {score:.1f}/100
    CGPA: {cgpa}/10
    Attendance: {attendance}%
    Aptitude Score: {aptitude}%
    Coding Score: {coding}%
    Communication Score: {communication}%
    Internship Experience: {internship}

    PERSONALIZED RECOMMENDATIONS
    - Practice coding and problem-solving.
    - Improve aptitude and communication.
    - Continue mock interviews and placement practice.

    Note: This is a prototype readiness score,
    not a guaranteed placement prediction.
    """

    st.download_button(
        label="⬇️ Download My Placement Report",
        data=report,
        file_name=f"{name}_placement_report.txt",
        mime="text/plain"
    )

    st.divider()
    st.subheader("🤖 AI Placement Prediction")

    student_data = pd.DataFrame([{
        "CGPA": cgpa,
        "Attendance": attendance,
        "Aptitude Score": aptitude,
        "Coding Score": coding,
        "Communication Score": communication,
        "Internship Experience": 1 if internship == "Yes" else 0
    }])

    student_data = student_data[model_features]

    prediction = model.predict(student_data)[0]

    if prediction == "Placed":
        st.success("Predicted Outcome: Placed")
    else:
        st.warning("Predicted Outcome: Not Placed")

    st.caption(
        "Demo prediction using a small synthetic dataset. "
        
        "Not a reliable real-world placement forecast."
    )
    st.divider()
st.header("🎯 Smart Skill Gap Analysis")

required_skills = {
    "Data Analyst": ["Python", "SQL", "Excel", "Power BI", "Statistics"],
    "Software Developer": ["Python", "Java", "DSA", "SQL", "Git"],
    "AI Engineer": ["Python", "Machine Learning", "SQL", "Statistics", "Deep Learning"]
}

role = st.selectbox(
    "Select your target career",
    list(required_skills.keys())
)

student_skills = st.multiselect(
    "Select your current skills",
    ["Python", "SQL", "Excel", "Power BI", "Statistics",
     "Java", "DSA", "Git", "Machine Learning",
     "Deep Learning"]
)

if st.button("Analyze My Skills"):
    missing = [
        skill for skill in required_skills[role]
        if skill not in student_skills
    ]

    st.subheader("Your Skill Analysis")

    st.write("Target Role:", role)
    st.write("Skills Matched:", len(required_skills[role]) - len(missing))

    if missing:
        st.warning("Skills you need to improve:")
        for skill in missing:
            st.write("📌", skill)
    else:
        st.success("You have all the listed skills for this role!")
