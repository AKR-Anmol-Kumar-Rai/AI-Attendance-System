import streamlit as st

from supabase import create_client, Client


# Creating the Supabase client
# This basically says: "Connect my Python application to this Supabase project using its URL and API key."
supabase: Client = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)