#!/usr/bin/env python
# coding: utf-8

# In[34]:


import pandas as pd
df = pd.read_excel("data - sample.xlsx")
print(df.head())
print(df)


# In[35]:


def find_latest_absence(df):
    df["attendance_date"] = pd.to_datetime(df["attendance_date"])
    df = df[df["status"].str.lower() == "absent"].sort_values(["student_id", "attendance_date"])
    df["streak_group"] = df.groupby("student_id")["attendance_date"].diff().gt(pd.Timedelta(days=1)).cumsum()
    
    streaks = df.groupby(["student_id", "streak_group"]).agg(
        absence_start_date=("attendance_date", "first"),
        absence_end_date=("attendance_date", "last"),
        total_absent_days=("attendance_date", "count")
    ).reset_index()
    
    filtered_streaks = streaks[streaks["total_absent_days"] > 3]
    latest_streaks = filtered_streaks.loc[filtered_streaks.groupby("student_id")["absence_start_date"].idxmax()]
    
    return latest_streaks[["student_id", "absence_start_date", "absence_end_date", "total_absent_days"]]


# In[36]:


import pandas as pd
import numpy as np
import random
import seaborn as sns
import matplotlib.pyplot as plt


latest_absences = find_latest_absence(df)

latest_absences.to_csv("attendance_data.csv", index=False)


# In[37]:


df=pd.read_csv("attendance_data.csv")
df


# In[38]:


students_df = pd.DataFrame({
    "student_id": [101, 102, 103, 104, 105],
    "student_name": ["Alice Johnson", "Bob Smith", "Charlie Brown", "David Lee", "Eva White"],
    "parent_email": ["alice_parent@example.com", "bob_parent@example.com", "invalid.email.com", 
                     "invalid-email.com", "eva_white@example.com"]
})

attendance_df = pd.DataFrame({
    "student_id": [101, 102, 103],
    "absence_start_date": ["2024-03-01", "2024-03-02", "2024-03-05"],
    "absence_end_date": ["2024-03-04", "2024-03-05", "2024-03-09"],
    "total_absent_days": [4, 4, 5]
})


# In[39]:


attendance_df["absence_start_date"] = pd.to_datetime(attendance_df["absence_start_date"])
attendance_df["absence_end_date"] = pd.to_datetime(attendance_df["absence_end_date"])

def is_valid_email(email):
    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

merged_df = attendance_df.merge(students_df, on="student_id", how="left")

merged_df["email"] = merged_df["parent_email"].apply(lambda x: x if is_valid_email(str(x)) else None)

merged_df["msg"] = merged_df.apply(lambda row: 
    f"Dear Parent, your child {row['student_name']} was absent from {row['absence_start_date'].date()} to {row['absence_end_date'].date()} for {row['total_absent_days']} days. Please ensure their attendance improves." 
    if row["email"] else None, axis=1)

final_output = merged_df[["student_id", "absence_start_date", "absence_end_date", "total_absent_days", "email", "msg"]]

print(final_output)


# In[ ]:




