import streamlit as st
import google.generativeai as genai
from datetime import datetime
import random

# Configure the Gemini AI key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Streamlit App Configuration
st.set_page_config(page_title="CollabSphere", layout="wide")
st.title("\U0001F91D CollabSphere: Anonymous Collaboration Platform")

# Anonymous User Login
username = st.text_input("Enter a pseudonym to join anonymously:", placeholder="E.g., CreativeSoul123")
if not username:
    st.warning("Please enter a pseudonym to proceed.")
    st.stop()

st.success(f"Welcome, {username}! Let's start collaborating!")

# Workspace Selection
workspace = st.text_input("Enter or create a workspace name:", placeholder="E.g., TeamAlpha")
if not workspace:
    st.warning("Please provide a workspace name.")
    st.stop()

st.info(f"You are in the workspace: {workspace}")

# Sidebar for AI Tools
st.sidebar.header("\U0001F916 Gemini AI Assistant")
ai_tool = st.sidebar.selectbox("Choose an AI Tool:", [
    "Brainstorm Ideas",
    "Summarize Text",
    "Task Prioritization",
    "Custom Prompt"
])

# AI Tools Logic
if ai_tool == "Brainstorm Ideas":
    prompt = st.sidebar.text_area("Describe what you need ideas for:", placeholder="E.g., Marketing strategies for product launch")
    if st.sidebar.button("Generate Ideas"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            st.sidebar.write(response.text)
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

elif ai_tool == "Summarize Text":
    text_to_summarize = st.sidebar.text_area("Enter text to summarize:", placeholder="Paste a long document or text here")
    if st.sidebar.button("Summarize"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"Summarize this: {text_to_summarize}")
            st.sidebar.write(response.text)
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

elif ai_tool == "Task Prioritization":
    tasks = st.sidebar.text_area("Enter your tasks (separated by commas):", placeholder="Task 1, Task 2, Task 3")
    if st.sidebar.button("Prioritize Tasks"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"Prioritize these tasks: {tasks}")
            st.sidebar.write(response.text)
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

elif ai_tool == "Custom Prompt":
    custom_prompt = st.sidebar.text_area("Enter your custom prompt for Gemini AI:", placeholder="Ask anything!")
    if st.sidebar.button("Get Response"):
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(custom_prompt)
            st.sidebar.write(response.text)
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

# Main Collaboration Workspace
st.header("\U0001F4C2 Collaboration Board")

# Shared Notes Section
st.subheader("\U0001F4DD Shared Notes")
if "notes" not in st.session_state:
    st.session_state.notes = ""
st.session_state.notes = st.text_area("Collaborative Notes:", st.session_state.notes, height=200)

# Task Management Section
st.subheader("\U00002705 Task Management")
if "tasks" not in st.session_state:
    st.session_state.tasks = []

task_input = st.text_input("Add a new task:", placeholder="E.g., Complete project proposal")
if st.button("Add Task"):
    st.session_state.tasks.append({"task": task_input, "status": "Pending", "assigned": username})
    st.success("Task added!")

if st.session_state.tasks:
    for idx, task in enumerate(st.session_state.tasks):
        col1, col2, col3 = st.columns([6, 2, 2])
        col1.write(f"{task['task']} (Assigned: {task['assigned']})")
        col2.write(task['status'])
        if col3.button("Mark Complete", key=f"complete_{idx}"):
            task['status'] = "Completed"
            st.experimental_rerun()

# Gamification Section
st.subheader("\U0001F3C6 Leaderboard")
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = {}

# Update leaderboard points
def update_points(username, points):
    if username in st.session_state.leaderboard:
        st.session_state.leaderboard[username] += points
    else:
        st.session_state.leaderboard[username] = points

update_points(username, random.randint(1, 5))  # Simulate earning points
leaderboard_sorted = sorted(st.session_state.leaderboard.items(), key=lambda x: x[1], reverse=True)

for rank, (user, points) in enumerate(leaderboard_sorted, start=1):
    st.write(f"{rank}. {user}: {points} points")

# File Sharing Section
st.subheader("\U0001F4C4 File Sharing")
uploaded_files = st.file_uploader("Upload files for the workspace:", accept_multiple_files=True)
if uploaded_files:
    for file in uploaded_files:
        st.write(f"File uploaded: {file.name}")

# Footer
st.write("\n---\n")
st.write("\U0001F4A1 Powered by Gemini AI and built with Streamlit.")
