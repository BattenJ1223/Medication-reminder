import csv
import datetime
import sched
import time

class Reminder:
    def __init__(self, medicine, reminder_time, recurrence):
        self.medicine = medicine
        self.reminder_time = reminder_time
        self.recurrence = recurrence



def set_reminder():
    medicine = input("Enter the name of the medicine: ")
    reminder_time_str = input("Enter the reminder time (HH:MM AM/PM): ")
    recurrence = input("Enter the recurrence (daily, weekly, or custom): ").lower()

    try:
        reminder_time = datetime.datetime.strptime(reminder_time_str, '%I:%M %p').time()
    except ValueError:
        print("Invalid time format. Please use HH:MM AM/PM format.")
        return None, None

    return Reminder(medicine, reminder_time, recurrence), time.strptime(reminder_time_str, '%I:%M %p')



def read_reminders_from_csv():
    reminders = []
    with open("medicine_reminders.csv", "r") as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        for row in reader:
            medicine, reminder_time, recurrence = row
            reminder_time_struct = time.strptime(reminder_time, '%I:%M %p')
            reminders.append(Reminder(medicine, reminder_time_struct, recurrence))
    return reminders



def save_reminders_to_csv(reminders):
    with open("medicine_reminders.csv", "w", newline="") as file:
        header = ["Medicine", "Reminder Time", "Recurrence"]
        writer = csv.writer(file)
        writer.writerow(header)
        for reminder in reminders:
            reminder_time_struct = time.struct_time((0, 0, 0, reminder.reminder_time.hour, reminder.reminder_time.minute, 0, 0, 0, -1))
            writer.writerow([reminder.medicine, time.strftime('%I:%M %p', reminder_time_struct), reminder.recurrence])




def display_reminders():
    current_time = time.localtime()
    with open("medicine_reminders.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        all_reminders = []
        for row in reader:
            medicine, reminder_time, recurrence = row
            reminder_time_struct = time.strptime(reminder_time, '%I:%M %p')
            all_reminders.append((medicine, reminder_time_struct, recurrence))

        if not all_reminders:
            print("No reminders found.")
            return

        print("All Reminders:")
        for i, (medicine, reminder_time_struct, recurrence) in enumerate(all_reminders, 1):
            reminder_time = time.strftime('%I:%M %p', reminder_time_struct)
            print(f"{i}. Medicine: {medicine}, Reminder Time: {reminder_time}, Recurrence: {recurrence.capitalize()}")



def schedule_daily_reminder(reminder, reminder_time_struct):
    now = time.localtime()
    reminder_time = time.mktime(reminder_time_struct)

    if reminder.recurrence == "daily" or reminder_time < time.mktime(now):
        # If daily recurrence or the reminder time has already passed for the current day,
        # reschedule the reminder for the next day.
        reminder_time += 86400  # Add 24 hours (in seconds)
    elif reminder.recurrence == "weekly":
        # If weekly recurrence, schedule the reminder for the next week.
        reminder_time += 7 * 86400  # Add 7 days (in seconds)
    # Implement custom recurrence handling here, if desired.

    time_diff = reminder_time - time.mktime(now)

    if time_diff > 0:
        print(f"Scheduled reminder for {reminder.medicine} at {time.strftime('%I:%M %p', reminder_time_struct)}")
        time.sleep(time_diff)
        print(f"Reminder: Time to take {reminder.medicine}!")
    else:
        # Handle the case when the reminder time has already passed for the current day or recurrence is not set.
        if reminder.recurrence != "custom":
            print(f"The reminder for {reminder.medicine} will not be scheduled today due to its recurrence.")
        else:
            print(f"The reminder for {reminder.medicine} will not be scheduled today due to a past time.")






def delete_reminder():
    reminders = read_reminders_from_csv()
    if not reminders:
        print("No reminders to delete.")
        return

    print("Select the reminder to delete:")
    for i, reminder in enumerate(reminders, 1):
        print(f"{i}. Medicine: {reminder.medicine}, Reminder Time: {time.strftime('%H:%M', reminder.reminder_time)}")

    try:
        choice = int(input("Enter the number of the reminder to delete: "))

        if 1 <= choice <= len(reminders):
            del reminders[choice - 1]
            save_reminders_to_csv(reminders)
            print("Reminder deleted successfully!")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")



def main():
    if not open("medicine_reminders.csv", "a", newline=""):
        with open("medicine_reminders.csv", "w", newline="") as file:
            header = ["Medicine", "Reminder Time", "Recurrence"]
            writer = csv.writer(file)
            writer.writerow(header)

    while True:
        print("\nMedicine Reminder Menu:")
        print("1. Set a new reminder")
        print("2. View all reminders")
        print("3. Delete a reminder")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            reminder, reminder_time_struct = set_reminder()
            if reminder:
                schedule_daily_reminder(reminder, reminder_time_struct)
                save_reminders_to_csv([reminder])  # Corrected function call
                print("Reminder set successfully!")

        elif choice == "2":
            display_reminders()

        elif choice == "3":
            delete_reminder()

        elif choice == "4":
            print("Exiting Medicine Reminder. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
