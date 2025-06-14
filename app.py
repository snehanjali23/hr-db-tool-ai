import streamlit as st
import sqlite3
import os
from dotenv import load_dotenv
import openai  # using openai client for Groq API

load_dotenv()

# Get your Groq API key
openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

st.set_page_config(page_title="📊 AI HR Database Tool")

st.title("📊 Ask Your HR Database")
st.markdown("Ask in plain English (e.g., `Show average salary by department`)")

# Upload CSV and convert to DB
uploaded_file = st.file_uploader("Upload CSV to use as database", type="csv")
if uploaded_file:
    import pandas as pd
    df = pd.read_csv(uploaded_file)
    db_name = "hr_data.db"
    conn = sqlite3.connect(db_name)
    df.to_sql("employees", conn, if_exists="replace", index=False)
    st.success("CSV uploaded and converted to 'employees' table in SQLite.")

# Ask user question
user_question = st.text_input("Ask a question:")

if user_question:
    with st.spinner("Generating SQL..."):
        try:
            prompt = f"""Convert this natural language question into a valid SQLite SQL query for a table named 'employees':
Question: {user_question}
Only output the SQL query:"""

            response = openai.ChatCompletion.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
            generated_sql = response['choices'][0]['message']['content'].strip()
            st.code(generated_sql, language='sql')

            # Execute SQL
            try:
                conn = sqlite3.connect("hr_data.db")
                cur = conn.cursor()
                cur.execute(generated_sql)
                rows = cur.fetchall()
                columns = [desc[0] for desc in cur.description] if cur.description else []
                if rows:
                    df_result = pd.DataFrame(rows, columns=columns)
                    st.dataframe(df_result)
                else:
                    st.warning("✅ Query executed but no results found.")
            except Exception as e:
                st.error(f"⚠️ SQL Execution Error: {e}")
        except Exception as e:
            st.error(f"⚠️ LLM Error: {e}")
