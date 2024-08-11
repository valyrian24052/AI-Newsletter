import streamlit as st
from utils import get_latest_results, summarize_text, send_email_mailgun

# Set page configuration
st.set_page_config(page_title="AutoNewsletter", page_icon="📰", layout="wide")

# Inject the particles.js configuration and background styling
st.markdown("""
    <style>
        /* The canvas element created by particles.js */
        #particles-js {
            position: fixed;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: -1;
            background-color: #000000;
        }
        
        /* Content container to ensure it stays above the particles.js background */
        .content {
            position: relative;
            z-index: 1;
            color: #ffffff;
            padding: 2rem;
        }

        /* Custom styles for your Streamlit app with transparency */
        .stButton button {
            background-color: rgba(31, 119, 180, 0.7);
            color: #ffffff;
        }
        .stTextInput input {
            background-color: rgba(51, 51, 51, 0.7);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .stTextInput label {
            color: #f2f2f2;
        }
        .stMarkdown {
            background-color: rgba(0, 0, 0, 0.7);
            color: #ffffff;
            padding: 1rem;
            border-radius: 5px;
        }
    </style>
    
    <!-- Div element for the particles.js background -->
    <div id="particles-js"></div>

    <!-- Load the particles.js library -->
    <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
    
    <!-- particles.js config -->
    <script>
    particlesJS("particles-js", {
      "particles": {
        "number": {
          "value": 100,
          "density": {
            "enable": true,
            "value_area": 800
          }
        },
        "color": {
          "value": "#ffffff"
        },
        "shape": {
          "type": "circle",
          "stroke": {
            "width": 0,
            "color": "#000000"
          },
          "polygon": {
            "nb_sides": 5
          },
          "opacity": {
            "value": 0.5,
            "random": false,
            "anim": {
              "enable": false,
              "speed": 1,
              "opacity_min": 0.2,
              "sync": false
            }
          },
          "size": {
            "value": 3,
            "random": true,
            "anim": {
              "enable": false,
              "speed": 40,
              "size_min": 0.1,
              "sync": false
            }
          },
          "line_linked": {
            "enable": true,
            "distance": 150,
            "color": "#ffffff",
            "opacity": 0.4,
            "width": 1
          },
          "move": {
            "enable": true,
            "speed": 3,
            "direction": "none",
            "random": false,
            "straight": false,
            "out_mode": "out",
            "bounce": false,
            "attract": {
              "enable": false,
              "rotateX": 600,
              "rotateY": 1200
            }
          }
        },
        "interactivity": {
          "detect_on": "canvas",
          "events": {
            "onhover": {
              "enable": true,
              "mode": "grab"
            },
            "onclick": {
              "enable": true,
              "mode": "push"
            },
            "resize": true
          },
          "modes": {
            "grab": {
              "distance": 140,
              "line_linked": {
                "opacity": 1
              }
            },
            "bubble": {
              "distance": 400,
              "size": 40,
              "duration": 2,
              "opacity": 8,
              "speed": 3
            },
            "repulse": {
              "distance": 200,
              "duration": 0.4
            },
            "push": {
              "particles_nb": 4
            },
            "remove": {
              "particles_nb": 2
            }
          }
        },
        "retina_detect": true
      }
    });
    </script>
""", unsafe_allow_html=True)

# Streamlit content
st.markdown("<div class='content'><h1>AutoNewsletter</h1></div>", unsafe_allow_html=True)

# Layout for API keys and newsletter input
col1, col2 = st.columns(2)

with col1:
    st.markdown("## 🔑 Access Keys")
    serpapi_key = st.text_input("SerpAPI Key", type="password", help="Enter your SerpAPI key")
    openai_api_key = st.text_input("OpenAI API Key", type="password", help="Enter your OpenAI API key")
    mailgun_domain = st.text_input("Mailgun Domain", help="Enter your Mailgun domain")
    mailgun_api = st.text_input("Mailgun API Key", type="password", help="Enter your Mailgun API key")

with col2:
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
