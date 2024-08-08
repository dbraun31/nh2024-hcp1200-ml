import numpy as np
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from pyprojroot import here
import os

os.chdir(here())


# Import
d = pd.read_csv('data/general_data/clean_structural_behavioral_data.csv')
y = pd.read_csv('data/features/dv/kmeans_subject_mapping.csv')
d.columns = ['subject'] + list(d.columns[1:])


# Code age bins
encoder = OrdinalEncoder(categories=list([d['Age'].unique()]))
d['age_encoded'] = encoder.fit_transform(d[['Age']])

# Effect coding sex
d['sex_effect'] = np.where(d['Sex'] == 'M', -.5, .5)

# Merge data together
d = pd.merge(d, y, on='subject', how='inner')
d = d.dropna()

# Separate to features and outcome
X = d.iloc[:, 3:21]
y = d['cluster']

# Normalizing 
# (may need to consider ratios between brain volumes)


# Train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
                                                    random_state=42)


lr = LogisticRegression(multi_class='multinomial', solver='lbfgs',
                        random_state=42)

lr.fit(X_train, y_train)

y_pred = lr.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

