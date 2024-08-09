# Helper functions for the task-based MRI
# Purpose: Access the fMRI data and calculate functional connectivity from the HCP database
# Data: task-based fMRI (HCP-YA-S1200), emotional processing task
# Contributor: Jiayue Yang
# Time: August 2024

# Functions referred to notebooks from Dr. Ariel Rokem and Dr. Noah Benson


# import libraries
from pathlib import Path
from cloudpathlib import S3Path, S3Client
import pandas as pd
import neuropythy as ny
import nibabel as nib
import numpy as np

# Function 1
# Access the tfMRI data using cloudpathlib
# input: subject id (string)
# output: tfMRI surface data (numpy data array)
def extract_tfMRI(subject_id):
    # make sure that we have a cache path:
    cache_path = Path('/tmp/cache')
    if not cache_path.exists():
        cache_path.mkdir()
    
    hcp_base_path = S3Path(
        's3://hcp-openaccess/HCP_1200/',
        client=S3Client(
            local_cache_dir=cache_path,
            profile_name='hcp'))
    # subject pathway
    subject_path = hcp_base_path/subject_id
    # emotional tfMRI pathway
    emo_tfMRI_path = subject_path/'MNINonLinear'/'Results'/'tfMRI_EMOTION_LR'
    emo_subdirs = list(emo_tfMRI_path.iterdir())
    
    # open the functional data of left hemisphere
    func_file = 'tfMRI_EMOTION_LR.L.native.func.gii'
    gii = nib.load((emo_tfMRI_path/func_file).fspath)
    
    # access the surface data
    surface_data = np.transpose([arr.data for arr in gii.darrays])

    return surface_data


# Function 2
# Extract the time series of ROIs from the tfMRI GIFTI file
# input: subject id (string), left or right hemisphere (string), parcellation atlas (string), regional_rois (numpy array)
# output: mean roi time series (dict)
def extract_time_series(subject_id, hemis, parc_atlas, regional_rois, surface_data):
    # get the number of vertex from the left hemisphere data
    sub = ny.hcp_subject(int(subject_id))
    n_vertices_L = sub.lh.vertex_count
    # get the unilateral data
    if hemis == "left":
        # extract the cortical parcellation of the left hemisphere (i.e. rois)
        surf_parc = sub.lh.properties[parc_atlas]
    else:
        # extract the cortical parcellation of the right hemisphere (i.e. rois)
        surf_parc = sub.rh.properties[parc_atlas]
    
    # based on the rois
    # extract time series data for each ROI
    roi_time_series = {}
    # iterate through each regions (ROI)
    for label in regional_rois:
        # if the current vertex is the current iterated region
        vertices = np.where(surf_parc == label)[0]
        # ensure that the vertex contains information
        if vertices.size > 0:
            mean_time_series = np.mean(surface_data[vertices, :], axis=0)
            if not np.any(np.isnan(mean_time_series)):  # Check if there are NaNs
                roi_time_series[label] = mean_time_series
    
    return roi_time_series


# Function 3
# Calculate the functional connectivity from the time series of ROIs
# Between the vertices within one ROI
# input: ROI time series (dict)
# output: connectivity matrix (data frame)
def calculate_within_roi_FC(roi_time_series):
    # create functional connectivity matrix
    # keys = roi labels
    roi_keys = list(roi_time_series.keys())
    n_rois = len(roi_keys)
    connectivity = np.zeros((n_rois, n_rois))
    
    # iterate through each roi
    for i in range(n_rois):
        # calculate its connectivity with the other rois
        for j in range(n_rois):
            # ensure that different regions are calculated
            if i != j:
                time_i = roi_time_series[roi_keys[i]]
                time_j = roi_time_series[roi_keys[j]]
                # estimate connectivity by correlation between 2 rois
                if np.std(time_i) > 0 and np.std(time_j) > 0:  
                    connectivity[i, j] = np.corrcoef(time_i, time_j)[0, 1]
                # otherwise NaN
                else:
                    connectivity[i, j] = np.nan  
            # if the same regions, denote as 1 (fully correlated)
            else:
                connectivity[i, j] = 1  
    
    # convery connectivity to dataframe
    FC = pd.DataFrame(connectivity, index=roi_keys, columns=roi_keys)

    return FC


# Function 4
# Calculate the functional connectivity from the time series of ROIs
# Between the ROIs
# input: ROI time series (dict)
# output: connectivity matrix (data frame)
def calculate_between_roi_FC(time_series_region1, time_series_region2):
    # calculate the functional connectivity between the two regions using Pearson correlation
    FC_value = np.corrcoef(time_series_region1, time_series_region2)[0, 1]

    return FC_value



# Function 5
# Convert the nxn dataframe to a 1xn dataframe to save data
# input: nxn dataframe, roi_names (list)
# output: 1xn dataframe
def convert_df(n_dim_dataframe, roi_names, subject_id):
    # rename row and column
    n_dim_dataframe.index = roi_names
    n_dim_dataframe.columns = roi_names

    # create the new dataframe
    new_data = {}
    # iterate through old df
    for i in range(len(n_dim_dataframe)):
        for j in range(i+1, len(n_dim_dataframe)):
            new_data[f"{n_dim_dataframe.index[i]}-{n_dim_dataframe.columns[j]}"] = n_dim_dataframe.iloc[i, j]

    
    # convert the new_data dictionary into a 1x3 DataFrame
    new_df = pd.DataFrame([new_data])

    # add the subject name
    new_df.insert(0, 'Subject', subject_id)
    

    return new_df