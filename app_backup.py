import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="PlacementPro AI",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #07111f;
    color: #e8f3ff;
}
h1, h2, h3, p, label {
    color: #e8f3ff !important;
}
div[data-testid="stMetric"] {
    background: #10243a;
    border: 1px solid #00d9e8;
    padding: 18px;
    border-radius: 12px;
}
.stButton > button {
    background-color: #00d9e8;
    color: #07111f;
    border-radius: 8px;
    font-weight: bold;
    width: 100%;
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

    st.caption(
        "Prototype score based on a fixed formula, not a trained ML model."
    )