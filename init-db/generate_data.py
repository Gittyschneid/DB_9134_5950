import random
from datetime import datetime, timedelta

# הגדרות
num_records = 20000
num_staff = 500  # מניח שיש לך 500 עובדים בטבלת Staff
num_shifts = 3   # בוקר, ערב, לילה
start_date = datetime(2024, 1, 1)

with open('insert_20k_shifts.sql', 'w') as f:
    for i in range(1, num_records + 1):
        staff_id = random.randint(1, num_staff)
        shift_id = random.randint(1, num_shifts)
        # יצירת תאריך אקראי לאורך שנה
        random_days = random.randint(0, 365)
        current_date = (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
        
        sql = f"INSERT INTO Staff_Shift (staff_shift_id, staff_id, shift_id, shift_date) " \
              f"VALUES ({i}, {staff_id}, {shift_id}, '{current_date}');\n"
        f.write(sql)

print(f"Success! Created a file with {num_records} insert commands.")