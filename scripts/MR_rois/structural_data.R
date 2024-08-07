#### Neurohackademy HCP-
## Author: Diana Hobbs, Melissa Hansen, and Yuxiang Wang 
## Date: August 2024

#### Set Up Packages and Load Data ####
pacman::p_load(tidyverse,jtools,psych,cowplot,multcomp,gmodels,pscl, MASS)

data <- read.csv("./HCP_data_structural_from_Melissa.csv", header = TRUE)%>%
  # filter out any QC_Issue that has an A, B, or C within the string
  filter(QC_Issue == "" | !grepl("[ABC]", QC_Issue))%>%
  # create average vol, thck, area measures per ROI
  mutate(Avg_Amygdala_Vol = (FS_L_Amygdala_Vol + FS_R_Amygdala_Vol)/2,
         Avg_Insula_Thck = (FS_L_Insula_Thck + FS_R_Insula_Thck)/2,
         Avg_Caudalanteriorcingulate_Thck = (FS_L_Caudalanteriorcingulate_Thck + FS_R_Caudalanteriorcingulate_Thck)/2, 
         Avg_Caudalanteriorcingulate_Area = (FS_L_Caudalanteriorcingulate_Area + FS_R_Caudalanteriorcingulate_Area)/2, 
         Avg_Rostralanteriorcingulate_Thck = (FS_L_Rostralanteriorcingulate_Thck + FS_R_Rostralanteriorcingulate_Thck)/2,
         Avg_Rostralanteriorcingulate_Area = (FS_L_Rostralanteriorcingulate_Area + FS_R_Rostralanteriorcingulate_Area)/2, 
         Avg_Medialorbitofrontal_Thck = (FS_L_Medialorbitofrontal_Thck + FS_R_Medialorbitofrontal_Thck)/2,
         Avg_Medialorbitofrontal_Area = (FS_L_Medialorbitofrontal_Area + FS_R_Medialorbitofrontal_Area)/2)%>%
  # create age and sex dummy variables
  mutate(Age_dummy = case_when(Age == "22-25" ~ 0,
                             Age == "26-30" ~ 1,
                             Age == "31-35" ~ 2,
                             Age == "36+" ~ 3),
       Sex_dummy = case_when(Gender == "M" ~ 0,
                             Gender == "F" ~ 1))%>%
  rename(Sex = Gender)%>%
dplyr::select(Subject, Age, Age_dummy, Sex, Sex_dummy, QC_Issue, #Handedness, Race, Ethnicity, SSAGA_Income, SSAGA_Educ, ZygosityGT, ZygositySR
              FS_L_Amygdala_Vol, FS_R_Amygdala_Vol, Avg_Amygdala_Vol,
              FS_L_Insula_Thck, FS_R_Insula_Thck, Avg_Insula_Thck,
              FS_L_Caudalanteriorcingulate_Thck, FS_R_Caudalanteriorcingulate_Thck, Avg_Caudalanteriorcingulate_Thck,
              FS_L_Caudalanteriorcingulate_Area, FS_R_Caudalanteriorcingulate_Area, Avg_Caudalanteriorcingulate_Area,
              FS_L_Rostralanteriorcingulate_Thck, FS_R_Rostralanteriorcingulate_Thck, Avg_Rostralanteriorcingulate_Thck,
              FS_L_Rostralanteriorcingulate_Area,FS_R_Rostralanteriorcingulate_Area, Avg_Rostralanteriorcingulate_Area,
              FS_L_Medialorbitofrontal_Thck, FS_R_Medialorbitofrontal_Thck, Avg_Medialorbitofrontal_Thck,
              FS_L_Medialorbitofrontal_Area,FS_R_Medialorbitofrontal_Area, Avg_Medialorbitofrontal_Area,
              FS_BrainSeg_Vol_No_Vent,MRsession_Scanner_3T)%>%
  #remove anyone who doesn't have MRI data in FS ROI space
  na.omit(FS_BrainSeg_Vol_No_Vent)


write.csv(data,"./structural_neuroimaging.csv", row.names=FALSE)

  


