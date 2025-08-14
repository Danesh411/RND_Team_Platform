import requests
import streamlit as st
from datetime import datetime, date

theme_mode_col = st.columns(2)[1]
with theme_mode_col:

    is_dark = st.toggle("🌙 Dark Mode")

    if is_dark:
        st.markdown("<style>body { background-color: #000; color: #fff; }</style>", unsafe_allow_html=True)
    else:
        st.markdown("<style>body { background-color: #fff; color: #000; }</style>", unsafe_allow_html=True)

# country_list
country_lst = ["Please select the country", "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Côte d'Ivoire", "Croatia", "Cuba", "Cyprus", "Czechia (Czech Republic)", "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini (fmr. ""Swaziland"")", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Holy See", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (formerly Burma)", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine State", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States of America", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]

def convert_dates(obj):
    if isinstance(obj, dict):
        return {k: convert_dates(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_dates(elem) for elem in obj]
    elif isinstance(obj, (date, datetime)):
        return obj.isoformat()
    else:
        return obj

# Page configuration
st.set_page_config(page_title="R&D Team – Site/App Completion Status", layout="wide")
st.title("R&D Team – Site/App Completion Status")

# Initialize session state to hold form data
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

# Helper function to update session state
def update_form(key, value):
    st.session_state.form_data[key] = value


# Form fields
st.header("RND Team Form")


# For Site Name ....
site_namecol1= st.columns(1)[0]
with site_namecol1:
    site_name = st.text_input("Site Name", placeholder="Please enter the site name", key="site_name")


# For Country || Feasible For || Site URL || Approx Volume  ....
col1, col2 = st.columns(2)
with col1:
    country = st.selectbox("Country", options=country_lst[1:], key="country", index=None,placeholder="Select a country")
    feasible_for = st.selectbox("Feasible For", options=["Web", "App", "Both", "Not Checked"], index=0, key="feasible_for")
with col2:
    site_url = st.text_input("Site URL", placeholder="Please enter the url if available", key="site_url")
    approx_volume = st.number_input("Approx Volume", min_value=0, value=0, step=1, key="approx_volume")

# For Method ....
methodcol = st.columns(1)[0]
with methodcol:
    method = st.selectbox("Method", options=["Direct Request", "Browser Automation"], index=0, key="method")


# For Is Proxy Used || Proxy Name || Credits ....
proxycol1 = st.columns(1)[0]
with proxycol1:
    is_proxy_used = st.checkbox("Is Proxy Used", value=True, key="is_proxy_used")

proxy_name_val = ""
credits_val = 0
if is_proxy_used:
    proxycol2, creditcol2 = st.columns(2)
    with proxycol2:
        proxy_name = st.selectbox("Proxy Name", options=["ScraperApi", "SmartProxy", "ScrapeDo", "ZyteProxy", "StromProxy"], key="proxy_name")

    with creditcol2:
        credits = st.number_input("Credits", min_value=1, value=10, step=1, key="credits")

    proxy_name_val = st.session_state.proxy_name
    credits_val = st.session_state.credits


# For Complexity || GitHub Code Link || Last Checked Date || Choose a file
col3, col4 = st.columns(2)
with col3:
    if feasible_for == "Not Checked":
        complexity = st.selectbox("Complexity", options=["Not Checked"], index=0, key="complexity")
    else:
        complexity = st.selectbox("Complexity", options=["Low", "Medium", "High"], index=0, key="complexity")

    if complexity == "Not Checked":
        github_link = st.text_input("GitHub Code Link", value="", disabled=True, key="github_link")
    else:
        github_link = st.text_input("GitHub Code Link", placeholder="Please enter the github link", key="github_link")
with col4:
    last_checked_date = st.date_input("Last Checked Date", value=datetime.today().now(), max_value=datetime.today().date(), format="YYYY/MM/DD", key="last_checked_date")
    updated_last_checked_date = convert_dates(last_checked_date)

    sow_doc = st.file_uploader("Choose a file", accept_multiple_files=True)
    if sow_doc:
        for uploaded_file in sow_doc:
            st.write("filename:", uploaded_file.name)

# Submit button
st.markdown("---")
if st.button("Submit"):
    is_valid = True

    #TODO::site_name validation ....
    if not site_name.strip():
        st.error("Site Name is required. Please enter a value.")
        is_valid = False

    # TODO::site_url validation ....
    if site_url:
        if not (site_url.startswith("http://") or site_url.startswith("https://")):
            st.error("Invalid Site Url")
            is_valid = False

    #TODO:: Country validation ....
    if country == "Please select the country":
        st.error("Country selection is required. Please select the country.")
        is_valid = False

    # TODO:: Github validation ....
    if github_link:
        if not ("github.com" in github_link and github_link.startswith("http")):
            st.error("Invalid GitHub link")
            is_valid = False

    if not is_valid:
        st.warning("Please correct the errors above.")

    else:
        # Collect form data
        submitted_data = {
            "site_name": st.session_state.site_name,
            "site_url": st.session_state.site_url if method != "Browser Automation" else "",
            "country": st.session_state.country,
            "feasible_for": st.session_state.feasible_for,
            "approx_volume": st.session_state.approx_volume if feasible_for != "Not Checked" else "0",
            "method": st.session_state.method if feasible_for != "Not Checked" else "",
            "is_proxy_used": st.session_state.is_proxy_used if feasible_for != "Not Checked" else "",
            "proxy_name": proxy_name_val,
            "credits": credits_val,
            "complexity": st.session_state.complexity,
            "last_checked_date": updated_last_checked_date if feasible_for != "Not Checked" else "",
            "gitHub_code_link": st.session_state.github_link if feasible_for != "Not Checked" else "",
            "sow_doc": [f.name for f in sow_doc] if sow_doc else ""
        }

        # Display submitted data
        st.success("Form submitted successfully!")
        st.json(submitted_data)  # Or display as table

        try:
            # === Send POST Request to Google Apps Script ===
            response = requests.post(
                "https://script.google.com/macros/s/AKfycbwVWOOeqUZlB2bUhc6-5YdSRC-hUx4Ai4v_tgS3-UEzMz2DBj16OaFU0-8B1ypNMQu-/exec",
                json=submitted_data,
                timeout=10
            )

            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get("status") == "success":
                        st.success("✅ Data saved to Google Sheet!")
                        # st.balloons()
                        st.toast()
                    else:
                        st.error(f"❌ Script error: {result.get('message', 'Unknown error')}")
                except:
                    st.success("✅ Data sent successfully! (Response not JSON)")
            else:
                st.error(f"❌ Failed to save data. HTTP {response.status_code}")
                st.code(response.text)

        except Exception as e:
            st.error("⚠️ Network error. Could not send data.")
            st.exception(e)