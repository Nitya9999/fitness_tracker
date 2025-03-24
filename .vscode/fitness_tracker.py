import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

data_file = "fitness_tracker.csv"

def initialize_csv():
    """Creates the CSV file if it doesn't exist."""
    try:
        with open(data_file, 'x', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Age", "Gender", "Height (cm)", "Weight (kg)", "Workout Type", "Duration (mins)", "Calories Burned"])
    except FileExistsError:
        pass

def log_workout(age, gender, height, weight, workout_type, duration, calories):
    """Logs a workout session."""
    date = datetime.date.today().strftime("%Y-%m-%d")
    
    with open(data_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, age, gender, height, weight, workout_type, duration, calories])
    
    st.success("Workout logged successfully!")

def view_history():
    """Displays workout history."""
    try:
        with open(data_file, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
            if len(data) > 1:
                return data[1:]
            else:
                return []
    except FileNotFoundError:
        return []

def calculate_bmi(height, weight):
    """Calculates BMI and provides health status."""
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

def show_statistics():
    """Displays workout statistics and generates graphs."""
    try:
        data = view_history()
        if not data:
            st.warning("No data available. Start logging workouts!")
            return
        
        dates = [row[0] for row in data]
        durations = np.array([float(row[6]) for row in data])
        calories = np.array([float(row[7]) for row in data])
        workout_types = {}
        
        for row in data:
            workout_types[row[5]] = workout_types.get(row[5], 0) + float(row[7])
        
        avg_duration = np.mean(durations)
        total_calories = np.sum(calories)
        
        st.write(f"**Average Workout Duration:** {avg_duration:.2f} mins")
        st.write(f"**Total Calories Burned:** {total_calories:.2f} cal")
        
        st.line_chart({"Date": dates, "Duration (mins)": durations})
        st.bar_chart(workout_types)
        
    except Exception as e:
        st.error(f"Error generating statistics: {e}")

def main():
    initialize_csv()
    st.title("🏋️ Personal Fitness Tracker")
    menu = ["Log Workout", "View History", "Show Statistics", "BMI Calculator", "Set Fitness Goals"]
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
        show_statistics()
    
    elif choice == "BMI Calculator":
        st.subheader("BMI Calculator")
        height = st.number_input("Enter your height (cm)", min_value=50.0, max_value=250.0, step=0.1)
        weight = st.number_input("Enter your weight (kg)", min_value=20.0, max_value=200.0, step=0.1)
        if st.button("Calculate BMI"):
            bmi, status = calculate_bmi(height, weight)
            st.write(f"**Your BMI:** {bmi:.2f}")
            st.write(f"**Health Status:** {status}")
    
    elif choice == "Set Fitness Goals":
        st.subheader("Set Your Fitness Goals")
        goal_calories = st.number_input("Target Calories Burned (weekly)", min_value=100, max_value=10000, step=100)
        goal_duration = st.number_input("Target Workout Duration (weekly, in mins)", min_value=10, max_value=1000, step=10)
        
        if st.button("Save Goals"):
            st.success(f"Goal set: Burn {goal_calories} calories & Workout for {goal_duration} mins per week!")
    
if __name__ == "__main__":
    main()
    