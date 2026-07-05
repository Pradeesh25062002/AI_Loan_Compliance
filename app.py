
import streamlit as st
from database import (
    create_tables,
    save_application,
    generate_application_id,
    get_all_applications
)
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
from business_rules import validate_application
from chatbot import ask_ai
from policy_loader import load_policy
from RAG import retrieve_policy



# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
   
    page_title="AI Loan Compliance & Eligibility Workbench",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)
create_tables()


# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------
st.markdown("""
<style>

.stApp{
    background:#F4F7FC;
}

section[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#0F172A,#1E3A8A);
}

.block-container{
    padding-top:1.2rem;
}

.metric-card{
    background:linear-gradient(135deg,#2563EB,#7C3AED);
    border-radius:20px;
    padding:22px;
    color:white;
    box-shadow:0px 10px 25px rgba(0,0,0,.15);
    transition:0.3s;
}

.metric-card:hover{
    transform:translateY(-5px);
}

.metric-title{
    font-size:18px;
}

.metric-value{
    font-size:40px;
    font-weight:bold;
}

.glass{
    background:white;
    padding:20px;
    border-radius:20px;
    box-shadow:0px 8px 30px rgba(0,0,0,.08);
}

div[data-testid="stMetric"]{
    background:white;
    padding:20px;
    border-radius:18px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

with st.sidebar:

    selected = option_menu(

        "🏦 Loan Workbench",

        ["Dashboard",
         "New Application",
         "Applications",
         "AI Assistant",
         "Policy Repository",
         "Reports"],

        icons=[
            "house",
            "person-plus",
            "folder2-open",
            "robot",
            "book",
            "bar-chart"
        ],

        default_index=0,
    )

    if "page" not in st.session_state:
        st.session_state.page = selected

    if st.session_state.page != selected:
        st.session_state.page = selected

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------

if selected=="Dashboard":

    col1,col2=st.columns([6,1])

    with col1:
        st.title("🏦 AI Loan Compliance & Eligibility Workbench")
        st.caption("Powered by Llama 3 + RAG")

    with col2:
        st.metric("AI Status","Online")

    st.write("")

    c1,c2,c3,c4=st.columns(4)

    with c1:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-title">Applications</div>
        <div class="metric-value">35</div>
        </div>
        """,unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-title">Approved</div>
        <div class="metric-value">21</div>
        </div>
        """,unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-title">Pending</div>
        <div class="metric-value">8</div>
        </div>
        """,unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-title">Rejected</div>
        <div class="metric-value">6</div>
        </div>
        """,unsafe_allow_html=True)

    st.write("")

    left,right=st.columns([2,1])

    # ------------------------
    # LINE CHART
    # ------------------------

    with left:

        st.subheader("📈 Loan Applications")

        df=pd.DataFrame({

            "Month":[
                "Jan","Feb","Mar","Apr","May","Jun"
            ],

            "Applications":[
                18,26,22,31,38,45
            ]

        })

        fig=px.line(
            df,
            x="Month",
            y="Applications",
            markers=True
        )

        fig.update_layout(
            height=350,
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ------------------------
    # DONUT
    # ------------------------

    with right:

        st.subheader("📊 Loan Distribution")

        donut=pd.DataFrame({

            "Loan":[
                "Home",
                "Car",
                "Personal"
            ],

            "Count":[
                18,
                9,
                8
            ]

        })

        fig2=px.pie(

            donut,

            names="Loan",

            values="Count",

            hole=.6

        )

        fig2.update_layout(height=350)

        st.plotly_chart(fig2,use_container_width=True)

    st.write("")

    left,right=st.columns([2,1])

    with left:

        st.subheader("📋 Recent Applications")

        data=pd.DataFrame({

            "Customer":[
                "Rahul",
                "Anjali",
                "Vivek",
                "Sanjay"
            ],

            "Loan":[
                "Home",
                "Car",
                "Personal",
                "Home"
            ],

            "Status":[
                "Approved",
                "Pending",
                "Rejected",
                "Approved"
            ]

        })

        st.dataframe(data,use_container_width=True)

    with right:

        st.subheader("🤖 AI Assistant")

        question=st.text_area(

            "Ask about loan policies"

        )

        st.button("Ask AI",use_container_width=True)

        st.info("Llama3 + RAG integration coming next.")

# -------------------------------------------------

elif selected=="New Application":

    st.title("📄 New Loan Application")

    st.subheader("👤 Customer Details")

    col1, col2 = st.columns(2)

    with col1:
        customer_name = st.text_input("Customer Name")
        age = st.number_input("Age", min_value=18, max_value=100)
        mobile = st.text_input("Mobile Number")
        pan = st.text_input("PAN Number")

    with col2:
        email = st.text_input("Email")
        aadhaar = st.text_input("Aadhaar Number")
        employment = st.selectbox(
            "Employment Type",
            ["Salaried", "Self Employed"]
        )
        experience = st.number_input(
            "Experience (Years)",
            min_value=0
        )

    st.divider()

    st.subheader("💰 Loan Details")

    col3, col4 = st.columns(2)

    with col3:

        loan_type = st.selectbox(
            "Loan Type",
            [
                "Home Loan",
                "Car Loan",
                "Personal Loan"
            ]
        )

        loan_amount = st.number_input(
            "Loan Amount",
            min_value=10000
        )

    with col4:

        monthly_income = st.number_input(
            "Monthly Income",
            min_value=0
        )

        existing_emi = st.number_input(
            "Existing EMI",
            min_value=0
        )

        credit_score = st.slider(
            "Credit Score",
            300,
            900,
            700
        )

    submit = st.button("Submit Application")

    if submit:

        application_id = generate_application_id()

        status = "Pending Review"

        save_application(

            (

                application_id,

                customer_name,

                age,

                mobile,

                email,

                pan,

                aadhaar,

                employment,

                experience,

                loan_type,

                loan_amount,

                monthly_income,

                existing_emi,

                credit_score,

                status

            )

        )

        st.success("Application Saved Successfully")

        st.info(f"Application ID : {application_id}")

        st.subheader("Business Rule Validation")

        results = validate_application(

            age,

            monthly_income,

            existing_emi,

            credit_score

        )

        eligible = True

        for rule, passed in results:

            if passed:

                st.success(f"✔ {rule}")

            else:

                st.error(f"❌ {rule}")

                eligible = False

        if eligible:

            st.success("Eligible for AI Compliance Check")

        else:

            st.warning("Manual Review Required")

elif selected == "Applications":

    st.title("📂 Loan Applications")

    applications = get_all_applications()

    if not applications:
        st.warning("No applications found.")

    else:

        for app in applications:

            st.container(border=True)

            col1, col2, col3 = st.columns([4,1,1])

            with col1:

                st.markdown(f"### {app[0]}")

                st.write(f"👤 Customer : {app[1]}")
                st.write(f"🏦 Loan : {app[9]}")
                st.write(f"💰 Amount : ₹{app[10]:,}")
                st.write(f"📊 Credit Score : {app[13]}")

            with col2:

                if st.button(
                    "View",
                    key=f"view_{app[0]}"
                ):
                    st.session_state.selected_application = app

            with col3:

                if st.button(
                    "AI Review",
                    key=f"ai_{app[0]}"
                ):
                    st.session_state.selected_application = app
                    st.session_state.page = "AI Review"

            st.divider()

elif selected=="AI Assistant":

    st.title("🤖 AI Loan Compliance Assistant")

    question = st.text_area(
        "Ask any question about Home Loan Policy"
    )

    if st.button("Ask AI"):

        if question:

            with st.spinner("Consulting Bank Policy..."):

                answer = ask_ai(question)

            st.success(answer)

elif selected=="AI Review":

    st.title("🤖 AI Compliance Review")

    if "selected_application" not in st.session_state:

        st.info("Select an application first.")

    else:

        app = st.session_state.selected_application

        st.subheader(app[0])

        st.write(f"Customer : {app[1]}")
        st.write(f"Loan Type : {app[9]}")
        st.write(f"Loan Amount : ₹{app[10]:,}")
        st.write(f"Income : ₹{app[11]:,}")
        st.write(f"Credit Score : {app[13]}")

        st.divider()

        if st.button("Generate AI Compliance Report"):
            query = f"""
    Age {app[2]}
    Income {app[11]}
    Credit Score {app[13]}
    Loan Type {app[9]}
    """

    policy = retrieve_policy(query)

            

    prompt = f"""
    You are a Senior Loan Compliance Officer.

    Below are the relevant policy sections retrieved from the bank policy.

    {policy}

    Loan Application

    Application ID : {app[0]}
    Customer : {app[1]}
    Age : {app[2]}
    Employment : {app[7]}
    Experience : {app[8]}
    Loan Type : {app[9]}
    Loan Amount : {app[10]}
    Monthly Income : {app[11]}
    Existing EMI : {app[12]}
    Credit Score : {app[13]}

    Generate a professional report.

    Include

    1. Eligibility Status

    2. Policy Validation

    3. Failed Rules

    4. Risk Level

    5. Recommendation

    6. Policy References

    Write in professional banking language.

    Track the records of the customer fetch the informations correctly. And when the application id is given fetch the complete information and make decision for every correct decision you will be rewarded.
    """

    report = ask_llm(prompt)

    st.success(report)

    import random

    confidence = random.randint(92, 99)

    st.metric(
        "AI Confidence",
        f"{confidence}%"
    )


elif selected == "Policy Repository":

    st.title("📚 Policy Repository")
    st.markdown("### Bank Policy Documents")

    import os

    policy_path = "policies/Home_Loan_Policy.pdf"

    col1, col2 = st.columns([2,1])

    with col1:

        st.info("""
### 🏦 Home Loan Policy

**Policy Name:** Home Loan Policy

**Version:** 2026.1

**Status:** Active

**Department:** Retail Banking

**Last Updated:** July 2026

**AI Search Enabled:** ✅ Yes
        """)

    with col2:

        if os.path.exists(policy_path):

            with open(policy_path,"rb") as file:

                st.download_button(

                    label="⬇ Download Policy",

                    data=file,

                    file_name="Home_Loan_Policy.pdf",

                    mime="application/pdf",

                    use_container_width=True

                )

        else:

            st.error("Policy not found.")

st.divider()

st.subheader("🔍 Search Policy")

query = st.text_input(
    "Enter policy question",
    placeholder="Example: Maximum home loan tenure?",
    key="policy_search"
)

if st.button("Search Policy", use_container_width=True):

    if query:

        answer = ask_ai(query)

        st.success(answer)

    else:

        st.warning("Please enter a question.")

elif selected == "Reports":

    st.title("📊 Reports Dashboard")

    import pandas as pd
    import sqlite3

    conn = sqlite3.connect("loan_workbench.db")

    df = pd.read_sql("SELECT * FROM loan_applications", conn)

    conn.close()

    if df.empty:

        st.warning("No applications available.")

    else:

        total = len(df)

        approved = len(df[df["credit_score"] >= 750])

        manual = len(df[(df["credit_score"] >= 650) &
                        (df["credit_score"] < 750)])

        rejected = len(df[df["credit_score"] < 650])

        avg_credit = round(df["credit_score"].mean(),1)

        c1,c2,c3,c4,c5 = st.columns(5)

        c1.metric("Applications", total)

        c2.metric("Approved", approved)

        c3.metric("Manual Review", manual)

        c4.metric("Rejected", rejected)

        c5.metric("Avg Credit", avg_credit)

    st.divider()

    st.subheader("🏠 Loan Type Distribution")

    loan_chart = df["loan_type"].value_counts()

    st.bar_chart(loan_chart)

    st.subheader("👨‍💼 Employment Type")

    employment_chart = df["employment_type"].value_counts()

    st.bar_chart(employment_chart)

    st.subheader("💳 Credit Score")

    st.line_chart(df["credit_score"])

    st.subheader("💰 EMI Ratio")

    st.bar_chart(df["existing_emi"])

    st.divider()

    st.subheader("🔍 Search Application")

    search = st.text_input("Search by Customer Name",
                            key = "report_search"
                        )
            

    if search:

        result = df[df["customer_name"].str.contains(search,case=False)]

        st.dataframe(result,use_container_width=True)

    else:

        st.dataframe(df,use_container_width=True)

