#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import glob
from sklearn.ensemble import IsolationForest
import plotly.express as px
from PIL import Image
from fpdf import FPDF
import os

# Define the path to the directory containing CSV files
directory_path = 'C://Users//Asus//Downloads//Telegram Desktop//computing-usage-dataset//computing-usage-dataset//'

# Use glob to get a list of all CSV files in the directory
csv_files = glob.glob(directory_path + '*.csv')

# Directory to save images temporarily
images_dir = 'temp_images'
os.makedirs(images_dir, exist_ok=True)

# Function to process each CSV file and save Plotly visualizations as images
def process_file(file_path, image_path):
    try:
        # Load the dataset
        data = pd.read_csv(file_path, parse_dates=['timestamp'], index_col='timestamp')

        # Fill missing values if needed
        data.fillna(method='ffill', inplace=True)

        # Anomaly Detection
        model = IsolationForest(contamination=0.01)  # Adjust contamination rate if needed
        data['anomaly'] = model.fit_predict(data[['value']])
        data['is_anomaly'] = data['anomaly'].apply(lambda x: 1 if x == -1 else 0)

        # Categorize anomalies
        def categorize_anomalies(data):
            data['rolling_mean'] = data['value'].rolling(window=5).mean()
            data['rolling_std'] = data['value'].rolling(window=5).std()

            def get_category(row):
                if row['is_anomaly'] == 1:
                    if row['value'] > row['rolling_mean'] + 2 * row['rolling_std']:
                        return 'spike'
                    elif row['value'] < row['rolling_mean'] - 2 * row['rolling_std']:
                        return 'drop'
                    else:
                        return 'drift'
                return 'normal'

            data['category'] = data.apply(get_category, axis=1)
            return data

        data = categorize_anomalies(data)

        # Optional: Severity Scoring
        data['severity_score'] = abs(data['value'] - data['rolling_mean'])
        data.fillna(0, inplace=True)

        # Plotly visualization
        fig = px.scatter(data, x=data.index, y='value', color='category', title=f'Anomalies and Categories for {file_path}')
        fig.update_layout(yaxis_title='Value', xaxis_title='Timestamp')

        # Save figure as PNG
        fig.write_image(image_path)
        
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Process each file and save images
image_paths = []
for file in csv_files:
    image_path = os.path.join(images_dir, f"{os.path.basename(file).replace('.csv', '.png')}")
    image_paths.append(image_path)
    process_file(file, image_path)

# Convert images to PDF
pdf_path = 'combined_visualizations.pdf'
pdf = FPDF()

# Set PDF page size to A4 (you can adjust as needed)
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Add images to PDF
for image_path in image_paths:
    try:
        # Open image and add to PDF
        with Image.open(image_path) as img:
            img_width, img_height = img.size
            
            # Convert pixels to millimeters
            img_width_mm = img_width * 0.264583
            img_height_mm = img_height * 0.264583
            
            # Fit image within A4 page (210mm x 297mm)
            max_width_mm = 190  # Adjust as needed
            max_height_mm = 270  # Adjust as needed
            
            # Calculate scaling factor
            scale = min(max_width_mm / img_width_mm, max_height_mm / img_height_mm)
            
            # Scale image dimensions
            width_mm = img_width_mm * scale
            height_mm = img_height_mm * scale
            
            # Add new page if image exceeds page size
            if pdf.page_no() > 1 and pdf.get_y() + height_mm > 297:
                pdf.add_page()
            
            # Add image to PDF
            pdf.image(image_path, x=10, y=pdf.get_y(), w=width_mm)
            
            # Move cursor down for next image
            pdf.ln(height_mm + 10)  # Adjust space as needed
            
    except Exception as e:
        print(f"Error adding image {image_path} to PDF: {e}")

# Save the PDF
try:
    pdf.output(pdf_path)
    print(f'Successfully saved combined visualizations to {pdf_path}')
except Exception as e:
    print(f"Error saving PDF file: {e}")

# Clean up temporary images
for image_path in image_paths:
    os.remove(image_path)
os.rmdir(images_dir)


# In[ ]:




