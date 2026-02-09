import streamlit as st
import re
from mashup import generate_mashup, send_email



st.title("Mashup Web Service")
st.subheader("Enter Mashup Details")

singer_name = st.text_input("Singer Name")

num_videos = st.number_input(
    "Number of Videos",
    min_value=1,
    step=1
)

duration = st.number_input(
    "Duration of each video (seconds)",
    min_value=1,
    step=1
)

email = st.text_input("Email ID")

submit = st.button("Submit")


def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email)


if submit:
    errors = []

    if not singer_name.strip():
        errors.append("Singer name cannot be empty.")

    if num_videos <= 10:
        errors.append("Number of videos must be greater than 10.")

    if duration <= 20:
        errors.append("Duration must be greater than 20 seconds.")

    if not is_valid_email(email):
        errors.append("Please enter a valid email ID.")

    if errors:
        for err in errors:
            st.error(err)
    else:
        with st.spinner("Generating mashup. Please wait..."):
            output_file = generate_mashup(
                singer_name,
                int(num_videos),
                int(duration)
            )
        try:
            zip_file = generate_mashup(
            singer_name,
            int(num_videos),
            int(duration)
            )
            send_email(email, zip_file)
            st.success("Mashup generated and sent to your email successfully!")
        except Exception as e:
            st.error(str(e))



        st.success("Mashup generated and zipped successfully!")
        st.write("ZIP file created at:")
        st.code(output_file)

