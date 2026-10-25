import sqlite3
import streamlit as st
# 1. Database Connection Setup
conn = sqlite3.connect("school_crud.db", check_same_thread=False)
cursor = conn.cursor()
# Table Creation (Database madhe table banavne)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        city TEXT
    )
""")
conn.commit()
st.title("🎓 Advanced Student Management App")
# --- LOGIN SESSION STATE SETUP ---
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
if not st.session_state.logged_in:
  st.subheader("🔐 Please Login")
  username = st.text_input("Username")
  password = st.text_input("Password", type="password")
  if st.button("Login"):
    if username == "Admin" and password == "Akash@1234":
      st.session_state.logged_in = True
      st.success("Login Successful! 🎉")
      st.rerun()
    else:
      st.error("❌ Invalid Username or Password!")
else:
  # --- MAIN APP WITH FULL ENGLISH UI & CRUD ---
  if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()
  # Sidebar Menu (Navigation)
  menu = st.sidebar.selectbox(
      "Navigation",
      [
          "📊 Dashboard (Statistics)",
          "➕ Add New Student",
          "📋 View & Delete Students",
          "✏️ Update Student",
      ],
  )
  # 1. DASHBOARD / STATISTICS
  if menu == "📊 Dashboard (Statistics)":
    st.subheader("📊 App Overview & Statistics")
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]
    cursor.execute("SELECT AVG(age) FROM students")
    avg_age_result = cursor.fetchone()[0]
    avg_age = round(avg_age_result, 1) if avg_age_result else 0
    col1, col2 = st.columns(2)
    with col1:
      st.metric(label="Total Students", value=total_students)
    with col2:
      st.metric(label="Average Age", value=avg_age)
    st.info(
        "💡 Tip: You can add, edit, or delete students using the sidebar menu!"
    )
  # 2. ADD STUDENT
  elif menu == "➕ Add New Student":
    st.subheader("➕ Add a New Student")
    with st.form("add_form"):
      name = st.text_input("Student Name:")
      age = st.number_input("Age:", min_value=15, max_value=100, value=18)
      city = st.text_input("City:")
      submit = st.form_submit_button("Save to Database")
      if submit:
        if name and city:
          cursor.execute(
              "INSERT INTO students (name, age, city) VALUES (?, ?, ?)",
              (name, age, city),
          )
          conn.commit()
          st.success(f"✅ {name} successfully saved to the database! 🎉")
        else:
          st.warning("⚠️ Please fill in all the required fields!")
  # 3. VIEW & DELETE STUDENTS
  elif menu == "📋 View & Delete Students":
    st.subheader("📋 Student List & Management")
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    if rows:
      for row in rows:
        col1, col2 = st.columns([4, 1])
        with col1:
          st.write(
              f"🆔 **ID:** {row[0]} | 👤 **Name:** {row[1]} | 🎂 **Age:**"
              f" {row[2]} | 🏙️ **City:** {row[3]}"
          )
        with col2:
          if st.button("Delete", key=f"del_{row[0]}"):
            cursor.execute("DELETE FROM students WHERE id = ?", (row[0],))
            conn.commit()
            st.success(f"Student ID {row[0]} deleted successfully!")
            st.rerun()
    else:
      st.info("No students found in the database yet.")
  # 4. UPDATE / EDIT STUDENT
  elif menu == "✏️ Update Student":
    st.subheader("✏️ Update Student Information")
    cursor.execute("SELECT id, name FROM students")
    student_list = cursor.fetchall()
    if student_list:
      student_dict = {f"{row[1]} (ID: {row[0]})": row[0] for row in student_list}
      selected_option = st.selectbox(
          "Select a student to update:", list(student_dict.keys())
      )
      selected_id = student_dict[selected_option]
      cursor.execute(
          "SELECT name, age, city FROM students WHERE id = ?", (selected_id,)
      )
      student_data = cursor.fetchone()
      with st.form("update_form"):
        new_name = st.text_input("New Name:", value=student_data[0])
        new_age = st.number_input(
            "New Age:", min_value=15, max_value=100, value=student_data[1]
        )
        new_city = st.text_input("New City:", value=student_data[2])
        update_submit = st.form_submit_button("Update Information")
        if update_submit:
          cursor.execute(
              "UPDATE students SET name = ?, age = ?, city = ? WHERE id = ?",
              (new_name, new_age, new_city, selected_id),
          )
          conn.commit()
          st.success(f"✅ Student ID {selected_id} updated successfully!")
          st.rerun()
    else:
      st.info("No students available to update.")