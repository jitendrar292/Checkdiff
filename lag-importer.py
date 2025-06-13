import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile

st.title("📊 Lag Tracker from Grafana CSV Files")

uploaded_files = st.file_uploader("Upload CSV files from Grafana", type=["csv"], accept_multiple_files=True)

def extract_lag_periods(df, franchise):
    df["timestamp"] = pd.to_datetime(df["Time"])
    df["lag"] = pd.to_numeric(df.iloc[:, 1], errors='coerce').fillna(0).astype(int)
    df["date"] = df["timestamp"].dt.date
    results = []

    for date, group in df.groupby("date"):
        group = group.sort_values("timestamp").reset_index(drop=True)
        max_lag = group["lag"].max()
        if max_lag == 0:
            continue

        max_lag_row = group[group["lag"] == max_lag].iloc[0]
        max_lag_index = max_lag_row.name

        # Find start of max lag window
        start_idx = max_lag_index
        while start_idx > 0 and group.loc[start_idx - 1, "lag"] > 0:
            start_idx -= 1
        start_time = group.loc[start_idx, "timestamp"]

        # Find end of lag window
        end_idx = max_lag_index
        while end_idx < len(group) - 1 and group.loc[end_idx + 1, "lag"] > 0:
            end_idx += 1
        end_time = group.loc[end_idx, "timestamp"]
        duration = end_time - start_time

        results.append({
            "Day": date,
            "Franchise": franchise,
            "Start Time": start_time.strftime('%H:%M:%S'),
            "End Time": end_time.strftime('%H:%M:%S'),
            "Duration": duration,
            "Max Lag": max_lag,
            "Max Lag Timestamp": max_lag_row["timestamp"].strftime('%H:%M:%S')
        })
    return results

if uploaded_files:
    all_data = []

    for file in uploaded_files:
        filename = file.name
        df = pd.read_csv(file)
        franchise = filename.split("-data")[0].replace("Consumer Lag", "").strip()
        records = extract_lag_periods(df, franchise)
        all_data.extend(records)

    if all_data:
        final_df = pd.DataFrame(all_data)

        # 🔧 Convert duration to total seconds for clarity
        final_df["Duration (minutes)"] = final_df["Duration"].dt.total_seconds() / 60

        st.success("✅ Processed Successfully!")
        st.dataframe(final_df)

        # Save to Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            final_df.to_excel(writer, index=False, sheet_name="Lag Tracker")

        st.download_button(
            label="📥 Download Lag Tracker Excel",
            data=output.getvalue(),
            file_name="lag_tracker.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("No lag data found with non-zero values.")
