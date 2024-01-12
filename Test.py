import pandas as pd

def read_csv(file_path):
    # Read CSV file
    df = pd.read_csv(file_path)
    return df

def analyze_timecard(employee_data):
    employee_data['Time'] = pd.to_datetime(employee_data['Time'])
    employee_data['Time Out'] = pd.to_datetime(employee_data['Time Out'])

    #a) Who has worked for 7 consecutive days
    consecutive_days = 7
    seven_consecutive_days = employee_data.groupby('Employee Name')['Time'].apply(
        lambda x: x.diff().dt.total_seconds().div(60).ge(24 * 60 * consecutive_days)
    )
    employees_7_consecutive_days = seven_consecutive_days[seven_consecutive_days].index.tolist()

    #b) Who have less than 10 hours of time between shifts but greater than 1 hour
    time_between_shifts = employee_data.groupby('Employee Name')['Time'].diff().dt.total_seconds().div(60)
    between_1_and_10_hours = (time_between_shifts < 600) & (time_between_shifts > 60)
    employees_1_to_10_hours = between_1_and_10_hours[between_1_and_10_hours].index.tolist()

    #c) Who has worked for more than 14 hours in a single shift
    long_shifts = employee_data[employee_data['Time Out'].sub(employee_data['Time']).dt.total_seconds().div(3600) > 14]
    employees_long_shifts = long_shifts[['Employee Name', 'Position ID']].drop_duplicates()

    return employees_7_consecutive_days, employees_1_to_10_hours, employees_long_shifts

def main():
    file_path = 'C:/Users/aishs/Desktop/Test/Assignment_Timecard.xlsx - Sheet1.csv'
    employee_data = read_csv(file_path)

    # Analyzing the timecard data
    employees_7_consecutive_days, employees_1_to_10_hours, employees_long_shifts = analyze_timecard(employee_data)

    # Output results in tabular format to the console
    print("Employees who have worked for 7 consecutive days:")
    print(employee_data.loc[employees_7_consecutive_days, ['Employee Name', 'Position ID']].drop_duplicates().to_string(index=False))

    print("\nEmployees with less than 10 hours between shifts but greater than 1 hour:")
    print(employee_data.loc[employees_1_to_10_hours, ['Employee Name', 'Position ID']].drop_duplicates().to_string(index=False))

    print("\nEmployees who have worked for more than 14 hours in a single shift:")
    print(employees_long_shifts.to_string(index=False))

    #results to a file named 'output.txt'
    with open('output.txt', 'w') as output_file:
        output_file.write("1).Employees who have worked for 7 consecutive days:\n")
        output_file.write(employee_data.loc[employees_7_consecutive_days, ['Employee Name', 'Position ID']].drop_duplicates().to_string(index=False) + "\n\n")

        output_file.write("2).Employees with less than 10 hours between shifts but greater than 1 hour:\n")
        output_file.write(employee_data.loc[employees_1_to_10_hours, ['Employee Name', 'Position ID']].drop_duplicates().to_string(index=False) + "\n\n")

        output_file.write("3).Employees who have worked for more than 14 hours in a single shift:\n")
        output_file.write(employees_long_shifts.to_string(index=False) + "\n")

if __name__ == "__main__":
    main()
