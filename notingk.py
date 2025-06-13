import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="SAP vs GK Comparator", layout="centered")
st.title("📦 SAP vs GK Article Comparator")

uploaded_files = st.file_uploader(
    "Upload Excel files (with 'Articles in SAP' and 'Articles in GK')",
    type=["xlsx"],
    accept_multiple_files=True
)

def compare_articles(df, sap_col, gk_col):
    sap_articles = (
        df[sap_col]
        .astype(str)
        .str.strip()
        .replace(['', 'nan', 'None', 'NaN'], pd.NA)
        .dropna()
    )
    gk_articles = (
        df[gk_col]
        .astype(str)
        .str.strip()
        .replace(['', 'nan', 'None', 'NaN'], pd.NA)
        .dropna()
    )
    not_in_gk = sap_articles[~sap_articles.isin(gk_articles)].drop_duplicates()
    not_in_gk = not_in_gk[not_in_gk.notna() & (not_in_gk != '') & (not_in_gk != 'nan') & (not_in_gk != 'None')]
    return pd.DataFrame({sap_col: not_in_gk})


if uploaded_files:
    for uploaded_file in uploaded_files:
        st.subheader(f"🔍 Processing: {uploaded_file.name}")
        xls = pd.ExcelFile(uploaded_file)
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            found = False

            for sheet_name in xls.sheet_names:
                try:
                    df_raw = xls.parse(sheet_name, header=None)
                    # Look for the actual header row
                    for i in range(5):
                        if df_raw.iloc[i].str.contains("Articles in SAP", na=False).any():
                            header_row = i
                            break
                    else:
                        header_row = 0

                    df = xls.parse(sheet_name, header=header_row)
                    df.columns = df.columns.str.strip()

                    sap_col = next((col for col in df.columns if "SAP" in col), None)
                    gk_col = next((col for col in df.columns if "GK" in col), None)

                    if sap_col and gk_col:
                        result_df = compare_articles(df, sap_col, gk_col)
                        result_df.to_excel(writer, sheet_name="Not in GK", index=False)
                        st.success(f"✅ Found SAP & GK columns in '{sheet_name}' — wrote 'Not in GK'")
                        found = True
                        break
                except Exception as e:
                    st.warning(f"⚠️ Error reading sheet '{sheet_name}': {str(e)}")

            if not found:
                st.error("❌ Could not find valid SAP/GK columns in any sheet.")

            # Also write original sheets back
            for sheet_name in xls.sheet_names:
                df_original = xls.parse(sheet_name, header=header_row if found else 0)
                df_original.to_excel(writer, sheet_name=sheet_name, index=False)

        st.download_button(
            label="⬇️ Download Updated Excel",
            data=output.getvalue(),
            file_name=f"updated_{uploaded_file.name}",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
