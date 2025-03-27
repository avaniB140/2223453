import pandas as pd

# Sample attendance data
attendance_data = {
    'id': [101, 101, 101, 101, 102, 102, 102, 102, 103, 103, 103, 103, 103],
    'missed_on': [
        '2024-03-01', '2024-03-02', '2024-03-03', '2024-03-04',
        '2024-03-02', '2024-03-03', '2024-03-04', '2024-03-05',
        '2024-03-05', '2024-03-06', '2024-03-07', '2024-03-08', '2024-03-09'
    ]
}

# Student info (id -> (name, parent email))
student_info = {
    101: ('Alice Johnson', 'alice_parent@example.com'),
    102: ('Bob Smith', 'bob_parent@example.com'),
    103: (None, None)  # No email for this one
}

# Convert to DataFrame
df = pd.DataFrame(attendance_data)
df['missed_on'] = pd.to_datetime(df['missed_on'])  # Convert dates properly

# Find first and last absent dates for each student
summary = df.groupby('id').agg(
    start_date=('missed_on', 'first'),
    end_date=('missed_on', 'last')
).reset_index()

# Figure out total days absent
summary['days_count'] = (summary['end_date'] - summary['start_date']).dt.days + 1

# Format dates nicely (DD-MM-YYYY)
summary['start_date'] = summary['start_date'].dt.strftime('%d-%m-%Y')
summary['end_date'] = summary['end_date'].dt.strftime('%d-%m-%Y')

# Show step 1 results
print("\nStep 1: Absence Summary")
print("+------------+------------------+----------------+------------------+")
print("| student_id | start_date       | end_date       | total_days_absent |")
print("+------------+------------------+----------------+------------------+")
for _, row in summary.iterrows():
    print(f"| {row['id']:10} | {row['start_date']:16} | {row['end_date']:14} | {row['days_count']:17} |")
print("+------------+------------------+----------------+------------------+\n")

# Add emails & messages
summary['email'] = summary['id'].map(lambda x: student_info[x][1])  # Map student IDs to emails

# Create messages for parents (if email exists)
summary['message'] = [
    f"Dear Parent, your child {student_info[row['id']][0]} was absent from {row['start_date']} to {row['end_date']} for {row['days_count']} days. Please ensure their attendance improves."
    if student_info[row['id']][1] else "No email available"
    for _, row in summary.iterrows()
]

# Final output
print("Step 2: Parent Notification Table")
print("+------------+------------------+----------------+------------------+------------------------+----------------------------------------------------------------------------------------------------------------------+")
print("| student_id | start_date       | end_date       | total_days_absent | email                  | message                                                                                                              |")
print("+------------+------------------+----------------+------------------+------------------------+----------------------------------------------------------------------------------------------------------------------+")

for _, row in summary.iterrows():
    email = row['email'] if row['email'] else "None"
    msg = row['message']

    # Print first line
    print(f"| {row['id']:10} | {row['start_date']:16} | {row['end_date']:14} | {row['days_count']:17} | {email:23} | {msg.split('.')[0]}. |")

    # If message is long, split it into multiple lines
    if msg != "No email available" and len(msg.split('.')) > 1:
        print(f"| {'':10} | {'':16} | {'':14} | {'':17} | {'':23} | {msg.split('.')[1]} |")

    print("+------------+------------------+----------------+------------------+------------------------+----------------------------------------------------------------------------------------------------------------------+")
