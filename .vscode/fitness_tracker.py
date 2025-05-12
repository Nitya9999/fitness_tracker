import csv
import datetime
import streamlit as st
import matplotlib.pyplot as plt
import os

data_file = "fitness_tracker.csv"
weight_goal_file = "weight_goal.csv"

def initialize_csv():
    if not os.path.exists(data_file):
        with open(data_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Age", "Gender", "Height (cm)", "Weight (kg)", "Workout Type", "Duration (mins)", "Calories Burned", "BMI"])

def initialize_goal_csv():
    if not os.path.exists(weight_goal_file):
        with open(weight_goal_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Target Weight (kg)", "Current Weight (kg)", "Height (cm)", "Start Date"])

def calculate_bmi(height, weight):
    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:
        status = "Underweight"
    elif 18.5 <= bmi < 24.9:
        status = "Normal weight"
    elif 25 <= bmi < 29.9:
        status = "Overweight"
    else:
        status = "Obese"
    return bmi, status

def log_workout(age, gender, height, weight, workout_type, duration, calories):
    date = datetime.date.today().strftime("%Y-%m-%d")
    bmi, _ = calculate_bmi(height, weight)
    with open(data_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, age, gender, height, weight, workout_type, duration, calories, round(bmi, 2)])
    st.success("Workout logged successfully!")

def view_history():
    if not os.path.exists(data_file):
        return []
    with open(data_file, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)[1:]
        return data

def generate_progress_report():
    data = view_history()
    if not data:
        st.write("No data available.")
        return
    total_calories = sum([float(row[7]) for row in data])
    total_duration = sum([float(row[6]) for row in data])
    st.write(f"**Total Calories Burned:** {total_calories:.2f} cal")
    st.write(f"**Total Workout Duration:** {total_duration:.2f} mins")

    dates = [row[0] for row in data]
    weights = [float(row[4]) for row in data]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, weights, marker='o', label="Weight")
    plt.xlabel("Date")
    plt.ylabel("Weight (kg)")
    plt.title("Weight Progress Over Time")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)

def generate_bmi_report():
    data = view_history()
    if not data:
        return
    dates = [row[0] for row in data]
    bmis = [float(row[8]) for row in data if row[8]]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, bmis, marker='x', color='orange', label="BMI")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.title("BMI Trend Over Time")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)

def set_weight_goal(target_weight, current_weight, height):
    date = datetime.date.today().strftime("%Y-%m-%d")
    with open(weight_goal_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Target Weight (kg)", "Current Weight (kg)", "Height (cm)", "Start Date"])
        writer.writerow([target_weight, current_weight, height, date])
    st.success("Weight gain goal saved.")

def view_weight_goal():
    if not os.path.exists(weight_goal_file):
        return None
    with open(weight_goal_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            return {
                "target": float(row[0]),
                "current": float(row[1]),
                "height": float(row[2]),
                "start_date": row[3]
            }
    return None

def display_goal_progress():
    goal = view_weight_goal()
    if goal:
        current = goal["current"]
        target = goal["target"]
        if current < target:
            progress = (current / target) * 100
        else:
            progress = 100
        st.write(f"📈 Progress Towards Goal: {progress:.2f}%")

def main():
    initialize_csv()
    initialize_goal_csv()
    st.title("🏋️ Personal Fitness Tracker")
    menu = ["Log Workout", "View History", "Show Statistics", "BMI Calculator", "Progress Report", "Set Weight Gain Goal"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Log Workout":
        st.subheader("Log Your Workout")
        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, step=0.1)
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=200.0, step=0.1)
        workout_type = st.text_input("Workout Type (e.g., Running, Cycling, Yoga)")
        duration = st.number_input("Duration (mins)", min_value=1.0, max_value=300.0, step=1.0)
        calories = st.number_input("Estimated Calories Burned", min_value=1.0, max_value=2000.0, step=1.0)
        if st.button("Log Workout"):
            log_workout(age, gender, height, weight, workout_type, duration, calories)

    elif choice == "View History":
        st.subheader("Workout History")
        history = view_history()
        if history:
            st.table(history)
        else:
            st.write("No workout history found. Start logging workouts!")

    elif choice == "Show Statistics":
        st.subheader("Workout Statistics")
        generate_progress_report()

    elif choice == "BMI Calculator":
        st.subheader("BMI Calculator")
        height = st.number_input("Enter your height (cm)", min_value=50.0, max_value=250.0, step=0.1)
        weight = st.number_input("Enter your weight (kg)", min_value=20.0, max_value=200.0, step=0.1)
        if st.button("Calculate BMI"):
            bmi, status = calculate_bmi(height, weight)
            st.write(f"**Your BMI:** {bmi:.2f}")
            st.write(f"**Health Status:** {status}")

    elif choice == "Progress Report":
        st.subheader("Progress Report")
        generate_progress_report()
        generate_bmi_report()
        goal = view_weight_goal()
        if goal:
            st.write(f"🎯 Target Weight: {goal['target']} kg")
            st.write(f"📅 Goal Set On: {goal['start_date']}")
            st.write(f"📊 Starting Weight: {goal['current']} kg")
            display_goal_progress()

    elif choice == "Set Weight Gain Goal":
        st.subheader("Set Your Weight Gain Target")
        current_weight = st.number_input("Current Weight (kg)", min_value=20.0, max_value=200.0)
        target_weight = st.number_input("Target Weight (kg)", min_value=current_weight, max_value=300.0)
        height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0)
        if st.button("Save Goal"):
            set_weight_goal(target_weight, current_weight, height)

if __name__ == "__main__":
    main()
