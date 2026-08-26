import streamlit as st

def style_base_layout():
    st.markdown("""

    <style>
                
            @import url('https://fonts.googleapis.com/css2?family=Audiowide&family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');
            
            /* Hide Top Bar of streamlit */
                #MainMenu, footer, header {
                     visibility: hidden
                }

                .block-container{
                    padding-top:1.5rem !important;
                    padding-bottom:0rem !important;
                } 

                h1{
                    font-family: "Audiowide", sans-serif !important;
                    font-size: 3.5rem !important;
                    line-height: 1.1 !important;
                    margin-bottom:0rem !important;
                    color:  #D3D3D3   !important;  
            
                    }    

                h2 {
                    font-family: "Audiowide", sans-serif !important;
                    font-size: 1.75rem !important;
                    line-height: 0.9 !important;
                    margin-bottom:0rem !important;
                    color:  #28282B   !important;        
                    }     
                
                h3, h4, p{
                    font-family: "Outfit", sans-serif,color:#28282B   !important;
                }

                button[kind="secondary"]{
                   border-radius: 1.5rem !important;
                   background-color: #EB459E !important;
                   color: white ! important;
                   padding: 10px 20px !important;
                   border: none !important;
                   transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
                }

                button[kind="tertiary"]{
                   border-radius: 1.5rem !important;
                   background-color: black !important;
                   color: white ! important;
                   padding: 10px 20px !important;
                   border: none !important;
                   transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
                }

                button {
                        border-radius: 1.5rem !important;
                        background-color: #5865F2 !important;
                        color: white !important;
                        padding: 10px 20px !important;
                        border: none !important;

                       transition:
                           transform 0.2s ease-out,
                          box-shadow 0.2s ease-out !important;

                        animation: slideUp 0.5s ease-out !important;
                    }

                button:hover {
                       transform: translateY(-3px);
                        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.25) !important;
                }

                button:active {
                       transform: translateY(0) scale(0.97) !important;
                }

                @keyframes slideUp {
                      from {
                          transform: translateY(20px);
                          opacity: 0;
                      }

                     to {
                         transform: translateY(0);
                         opacity: 1;
                     }
                }
 

    </style>

     """,unsafe_allow_html=True)
    


def style_background_home():
    st.markdown("""

    <style>
            .stApp{
                 background: #4052D6  !important
            }
                
            .stApp div[data-testid="stColumn"] {
                background-color: #E0E3FF !important;
                padding: 2.5rem 1rem 2.5rem 4.5rem !important;
                border-radius: 5rem !important;
            }


    </style>

     """,unsafe_allow_html=True)    
    


def style_background_dashboard():

    st.markdown("""

    <style>
            .stApp{
                  background: #E0E3FF !important;
                }


    </style>

     """,unsafe_allow_html=True)        