import streamlit as st
def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
         <div style="background: white; border-left: 8px solid #8B459E; padding: 25px; border-radius: 20px; border: 1px solid black; margin-top:35px; margin-bottom:15px;">
         <h3 style="margin:0; color: #1E293B; font-size: 1.5rem">{name.upper()}</h3>
         <p style="color: #64748B; margin:10px 0;">Code : <span style="background-color:#E0E3FF; color:#5865F2; padding:2px 8px; border-radius: 5px">{code.upper()}</span> | Section : {section.upper()}</p>
         """
    
    if stats:
        html += """
         <div style="display:flex; gap:8px; flex-wrap:wrap;">
        """
        for icon, label, value in stats:
            html += f'<div style="background-color: #EB459E10; padding: 5px 12px; border-radius: 12px; font-size: 0.9rem">{icon} <b>{value}</b> {label} </div>'


        html += "</div>"


    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()