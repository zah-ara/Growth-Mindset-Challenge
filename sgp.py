# Import necessary libraries
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up Streamlit app
st.set_page_config(page_title="💿 Data Sweeper", layout="wide")
st.title("💿 Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# File uploader
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)


import chardet  

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            raw_data = file.read()
            detected_encoding = chardet.detect(raw_data)['encoding']
            file.seek(0)  # Reset file pointer

            df = pd.read_csv(file, encoding=detected_encoding)
        
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)

        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue  # Skip processing for unsupported files

        # Display file information
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")

        # Show DataFrame preview
        st.write("🔍Preview of the DataFrame:")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("⚙️Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write(" Duplicates removed!")

            with col2:
                if st.button(f"Fill Missing Values For {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns  # Fixed 'numbers' to 'number'
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write(" Missing values have been filled!")


            # Choose Specific Columns To Keep Or Convert        
            st.subheader("🎯Select columns to convert")
            columns = st.multiselect(f"Choose Columns for {file.name}" , df.columns, default=df.columns)
            df = df[columns]


            #Create some visualizations
            st.subheader("📊 Data Visualization")
            if st.checkbox(f"Show Visualization for {file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

            # Convert th file -> CSV to EXCEL
            st.subheader("🔄️Conversion Options")    
            conversion_type  = st.radio(f"Convert {file.name}to:" , ["CSV","EXCEL"], key=file.name)
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer,index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"

                elif conversion_type == "Excel":
                    df.to_excel(buffer,index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)


                # Download Button
                st.download_button(
                    label=f"⬇️ Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )


st.success("🎉 All files processed!")                