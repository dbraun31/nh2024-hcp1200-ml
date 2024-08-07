#### Neurohackademy HCP-
## Author: Diana Hobbs, Melissa Hansen, and Yuxiang Wang 
## Date: August 2024

# import packages and load data
import pandas as pd
import numpy as np
data = pd.read_csv("./HCP_data_structural_from_Melissa.csv")

# filter out subjects with QC issues A B or C. ~ is for element-wise negation here.
data = data[(data['QC_Issue'] == "") | (~data['QC_Issue'].astype(str).str.contains("[ABC]", regex=True))]

# avg values for each ROI
data['Avg_Amygdala_Vol'] = (data['FS_L_Amygdala_Vol'] + data['FS_R_Amygdala_Vol']) / 2
data['Avg_Insula_Thck'] = (data['FS_L_Insula_Thck'] + data['FS_R_Insula_Thck']) / 2
data['Avg_Caudalanteriorcingulate_Thck'] = (data['FS_L_Caudalanteriorcingulate_Thck'] + data['FS_R_Caudalanteriorcingulate_Thck']) / 2
data['Avg_Caudalanteriorcingulate_Area'] = (data['FS_L_Caudalanteriorcingulate_Area'] + data['FS_R_Caudalanteriorcingulate_Area']) / 2
data['Avg_Rostralanteriorcingulate_Thck'] = (data['FS_L_Rostralanteriorcingulate_Thck'] + data['FS_R_Rostralanteriorcingulate_Thck']) / 2
data['Avg_Rostralanteriorcingulate_Area'] = (data['FS_L_Rostralanteriorcingulate_Area'] + data['FS_R_Rostralanteriorcingulate_Area']) / 2
data['Avg_Medialorbitofrontal_Thck'] = (data['FS_L_Medialorbitofrontal_Thck'] + data['FS_R_Medialorbitofrontal_Thck']) / 2
data['Avg_Medialorbitofrontal_Area'] = (data['FS_L_Medialorbitofrontal_Area'] + data['FS_R_Medialorbitofrontal_Area']) / 2

# Create age and sex dummy variables
data['Age_dummy'] = data['Age'].map({
    '22-25': 0,
    '26-30': 1,
    '31-35': 2,
    '36+': 3
})

data['Sex_dummy'] = data['Gender'].map({
    'M': 0,
    'F': 1
})

# Rename columns
data = data.rename(columns={'Gender': 'Sex'})

columns_to_select = [
    'Subject', 'Age', 'Age_dummy', 'Sex', 'Sex_dummy', 'QC_Issue',
    'FS_L_Amygdala_Vol', 'FS_R_Amygdala_Vol', 'Avg_Amygdala_Vol',
    'FS_L_Insula_Thck', 'FS_R_Insula_Thck', 'Avg_Insula_Thck',
    'FS_L_Caudalanteriorcingulate_Thck', 'FS_R_Caudalanteriorcingulate_Thck', 'Avg_Caudalanteriorcingulate_Thck',
    'FS_L_Caudalanteriorcingulate_Area', 'FS_R_Caudalanteriorcingulate_Area', 'Avg_Caudalanteriorcingulate_Area',
    'FS_L_Rostralanteriorcingulate_Thck', 'FS_R_Rostralanteriorcingulate_Thck', 'Avg_Rostralanteriorcingulate_Thck',
    'FS_L_Rostralanteriorcingulate_Area', 'FS_R_Rostralanteriorcingulate_Area', 'Avg_Rostralanteriorcingulate_Area',
    'FS_L_Medialorbitofrontal_Thck', 'FS_R_Medialorbitofrontal_Thck', 'Avg_Medialorbitofrontal_Thck',
    'FS_L_Medialorbitofrontal_Area', 'FS_R_Medialorbitofrontal_Area', 'Avg_Medialorbitofrontal_Area',
    'FS_BrainSeg_Vol_No_Vent'
]
data = data[columns_to_select]

# Remove rows with missing MRI data
data = data.dropna(subset=['FS_L_Amygdala_Vol'])

# Save the cleaned data to a new CSV file
data.to_csv("./structural_neuroimaging_.csv", index=False)
