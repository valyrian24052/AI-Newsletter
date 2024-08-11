import streamlit as st
from utils import get_latest_results, summarize_text, send_email_mailgun

# Set page configuration
st.set_page_config(page_title="AutoNewsletter", page_icon="📰", layout="centered")

# Custom CSS for pitch-black background, styling, and animations
st.markdown(
    """
    <style>
    body {
        background-color: #000000;
        color: #ffffff;
    }
    .stTextInput label {
        color: #f2f2f2;
    }
    .stButton button {
        background-color: #1f77b4;
        color: #ffffff;
    }
    .stTextInput input {
        background-color: #333333;
        color: #ffffff;
    }
    .animated-title {
        font-size: 2.5rem;
        font-weight: bold;
        animation: bounce 2s infinite;
    }
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-20px);
        }
        60% {
            transform: translateY(-10px);
        }
    }
    .blink {
        animation: blinker 1.5s linear infinite;
        color: #ff5733;
    }
    @keyframes blinker {  
        50% { opacity: 0; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title with animation
st.markdown('<div class="animated-title">📰 AutoNewsletter</div>', unsafe_allow_html=True)

# Layout for API keys
with st.sidebar:
    st.markdown("## 🔑 Access Keys")
    serpapi_key = st.text_input("SerpAPI Key", type="password", help="Enter your SerpAPI key")
    openai_api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
    mailgun_domain = st.text_input("Mailgun Domain", help="Enter your Mailgun domain")
    mailgun_api = st.text_input("Mailgun API Key", type="password", help="Enter your Mailgun API key")
    st.markdown("---")

# Layout for newsletter information
st.markdown("## 📝 Newsletter Information")
user_query = st.text_input("Topic for the Newsletter", help="Enter a topic you'd like the newsletter to cover")
recipient_mail = st.text_input("Recipient Email", help="Enter the email address to send the newsletter to")
sending_mail = st.text_input("Sender Email", help="Enter the email address from which the newsletter will be sent")

if st.button('Generate and Send Newsletter'):
    if not user_query or not serpapi_key or not openai_api_key:
        st.error("Please fill in all required fields.")
    else:
        st.session_state.serpapi_key = serpapi_key
        st.session_state.user_query = user_query

        st.session_state.get_splitted_text = get_latest_results(user_query, serpapi_key)
        if not st.session_state.get_splitted_text:
            st.write("No results found.")
        else:
            st.session_state.summarized_texts = summarize_text(st.session_state.get_splitted_text, openai_api_key)
            
            email_body = ""
            for title, summarized_text, url in st.session_state.summarized_texts:
                st.markdown(f"### {title}")
                st.write(f"❇️ {summarized_text}")
                st.write(f"🔗 [Read more]({url})")
                st.markdown("\n\n")
                email_body += f"❇️{title}\n\n💬{summarized_text}\n\n🔗{url}\n\n"

            # Send the email
            send_email_mailgun(
                subject=f"🤖🤯 This week news about {user_query}",
                body=email_body, 
                to=recipient_mail, 
                from_email=sending_mail, 
                mailgun_domain=mailgun_domain, 
                mailgun_api_key=mailgun_api
            )
            st.success(f"Newsletter sent successfully to {recipient_mail}!")

# Animated footer text
st.markdown('<div class="blink">🌟 Powered by AI and Streamlit</div>', unsafe_allow_html=True)
