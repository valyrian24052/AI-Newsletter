import streamlit as st
from utils import get_latest_results, summarize_text, send_email_mailgun

def main():
    """Main function to run the Streamlit app."""
    st.title('AutoNewsletter')
    st.markdown("## Please input your API keys")

    # API keys input
    serpapi_key = st.text_input("Insert your SerpAPI key here: ", type="password")
    openai_api_key = st.text_input("Insert your OpenAI API key: ", type="password")

    # User input for keyword
    user_query = st.text_input("Make me a newsletter about: ")

    st.markdown("## Info necessary for the MailGun to work")

    # Email settings
    recipient_mail = st.text_input("Email To: ")
    sending_mail = st.text_input("Email from: ") 
    mailgun_domain = st.text_input("Enter your Mailgun Domain here: ")
    mailgun_api = st.text_input("Enter your Mailgun API key here: ", type="password")

    if st.button('Submit'):
        st.session_state.serpapi_key = serpapi_key
        st.session_state.user_query = user_query

        st.session_state.get_splitted_text = get_latest_results(user_query, serpapi_key)
        if not st.session_state.get_splitted_text:
            st.write("No results found.")
            return

        st.session_state.summarized_texts = summarize_text(st.session_state.get_splitted_text, openai_api_key)
        
        email_body = ""
        for title, summarized_text, url in st.session_state.summarized_texts:
            st.title(title)
            st.write(f"❇️ {summarized_text}")
            st.write(f"🔗 {url}")
            st.markdown("\n\n")
            email_body += f"❇️{title}\n\n"
            email_body += f"💬{summarized_text}\n\n"
            email_body += f"🔗{url}\n\n"

        # Send the email
        send_email_mailgun(
            subject=f"🤖🤯 This week news about {user_query}",
            body=email_body, 
            to=recipient_mail, 
            from_email=sending_mail, 
            mailgun_domain=mailgun_domain, 
            mailgun_api_key=mailgun_api
        )

if __name__ == "__main__":
    main()
