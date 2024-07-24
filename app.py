import streamlit as st
from datetime import datetime
from cron_descriptor import get_description

# Set wide layout
st.set_page_config(layout="wide")

# Define the correct password
PASSWORD = "VeryFastAutomation1"

# Hide "Made with Streamlit" footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Password check
if "password_correct" not in st.session_state:
    st.session_state.password_correct = False

if "password_attempted" not in st.session_state:
    st.session_state.password_attempted = False

if not st.session_state.password_correct:
    with st.form("password_form"):
        password = st.text_input("Enter password", type="password")
        submit = st.form_submit_button("Submit")

        # Check for submission (button click OR Enter key in password field)
        if submit or (
            st.session_state.get("password_form")
            and st.session_state["password_form"]["submitted"]
        ):
            if password == PASSWORD:
                st.session_state.password_correct = True
            else:
                st.session_state.password_attempted = True
                st.error("Incorrect password")
else:
    st.sidebar.image("flipping-miracles-logo.png")
    header_html = """
        <div style="display: flex; align-items: center; padding: 10px;">
            <div style="font-size: 1em; font-family: 'Century Gothic', serif; line-height: 1;">
                <span style="font-weight: bold; color: rgb(67, 74, 79);">Flipping</span>
                <span style="font-weight: bold; color: rgb(24, 120, 200);">MIRACLES</span>
            </div>
        </div>
        <hr style="margin-bottom: 20px;">
    """
    st.sidebar.markdown(header_html, unsafe_allow_html=True)

    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigation", ["Scheduled Scrapes", "Manual Pull"], index=0
    )

    # Function to translate cron expression to readable format
    def translate_cron(cron_expression):
        try:
            description = get_description(cron_expression)
        except Exception as e:
            description = f"Invalid cron expression: {str(e)}"
        return description

    # Confirmation dialog function
    @st.dialog("Confirm Deletion")
    def confirm_deletion(index):
        st.write("Are you sure you want to delete this scheduled scrape?")
        confirmation_text = st.text_input(
            "Type DELETE to confirm", key=f"confirm_{index}"
        )
        if st.button("Delete", key=f"confirm_btn_{index}"):
            if confirmation_text == "DELETE":
                st.session_state.scheduled_scrapes.pop(index)
                st.rerun()
            else:
                st.write("You must type DELETE to confirm.")

    # Scheduled Scrapes Page
    if page == "Scheduled Scrapes":
        st.title("Scheduled Scrapes")

        st.subheader("Existing Scheduled Scrapes")
        if "scheduled_scrapes" not in st.session_state:
            st.session_state.scheduled_scrapes = [
                {"cron_expression": "0 0 * * 1-5"}  # Example: Every M-F at midnight
            ]

        for idx, scrape in enumerate(st.session_state.scheduled_scrapes):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{translate_cron(scrape['cron_expression'])}**")
            with col2:
                if st.button("Delete", key=f"delete_{idx}"):
                    confirm_deletion(idx)

        st.write(
            "### <span style='color:green'>Cron Job Scheduler</span>",
            unsafe_allow_html=True,
        )
        st.write(
            "Enter the cron expression fields below. If you're unsure how to format these, refer to the guide on the right."
        )
        col1, col2 = st.columns([2, 3])

        with col1:
            minute = st.text_input("Minute", value="0")
            hour = st.text_input("Hour", value="0")
            day_of_month = st.text_input("Day of month", value="1")
            month = st.text_input("Month", value="1")
            day_of_week = st.text_input("Day of week", value="0")

            cron_expression = f"{minute} {hour} {day_of_month} {month} {day_of_week}"
            cron_description = translate_cron(cron_expression)
            st.write(
                f"**<span style='color:green'>Schedule description:</span>** {cron_description}",
                unsafe_allow_html=True,
            )

            if st.button("Add"):
                new_schedule = {
                    "cron_expression": cron_expression,
                }
                st.session_state.scheduled_scrapes.append(new_schedule)
                st.rerun()

        with col2:
            st.markdown(
                """
                ### How to Write Cron Expressions
                A cron expression consists of five fields separated by spaces:
                - **Minute (0-59)**: The exact minute that the task should be executed.
                - **Hour (0-23)**: The hour of the day in 24-hour format.
                - **Day of the Month (1-31)**: The specific day of the month.
                - **Month (1-12)**: The month in the year.
                - **Day of the Week (0-6)**: The day of the week (0 = Sunday, 1 = Monday, ..., 6 = Saturday).

                Special characters you can use:
                - `*`: Matches any value.
                - `,`: Separates multiple values.
                - `-`: Specifies a range of values.
                - `/`: Specifies step values.

                **Examples:**
                - `0 0 * * 1-5`: At midnight, every Monday through Friday.
                - `15 14 1 * *`: At 2:15 PM on the first day of every month.
                - `0 */2 * * *`: Every 2 hours.

                Use these fields carefully to ensure tasks are scheduled correctly.
                """
            )

    # Manual Pull Page
    elif page == "Manual Pull":
        st.title("Manual Pull")
        st.write(
            "This tool allows you to manually pull foreclosure data from Orange county. "
            "To pull records, fill in the start and end date fields, and then click 'Get data'. "
            "You will receive an email when the data is available. (Not really, but as soon as I code the backend, you will)"
        )

        start_date = st.date_input("Start date", value=datetime.today())
        end_date = st.date_input("End date", value=datetime.today())

        if st.button("Get data"):
            # Logic for pulling data would go here
            st.write(
                "Data request submitted. You will receive an email when the data is ready. (Not really, but as soon as I code the backend, you will)"
            )
