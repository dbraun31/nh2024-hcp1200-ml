import numpy as np
import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler
from pyprojroot import here
import os

os.chdir(here())

warnings.simplefilter(action='ignore', category=FutureWarning)

# Import
#d = pd.read_csv('data/general_data/clean_structural_behavioral_data.csv')
d = pd.read_csv('data/features/ivs/2024-08-09_features.csv')
y = pd.read_csv('data/features/dv/kmeans_subject_mapping.csv')
d.columns = ['subject'] + list(d.columns[1:])

# Sparse data (2024-08-09)
sparse_data = [
    "L_rostralanteriorcingulate_cortex_R_thalamus",
    "L_thalamus_R_rostralanteriorcingulate_cortex",
    "L_hippocampus_R_thalamus",
    "L_amygdala_R_rostralanteriorcingulate_cortex",
    "L_rostralanteriorcingulate_cortex_R_amygdala",
    "L_hippocampus_R_amygdala",
    "L_amygdala_R_hippocampus"
]

d = d[[x for x in d.columns if x not in sparse_data]]

# Code age bins
encoder = OrdinalEncoder(categories=list([d['Age'].unique()]))
d['age_encoded'] = encoder.fit_transform(d[['Age']])

# Effect coding sex
d['sex_effect'] = np.where(d['Sex'] == 'M', -.5, .5)

# Merge data together
d = pd.merge(d, y, on='subject', how='inner')

# Separate to features and outcome
drop = ['Age', 'Sex', 'cluster']
keep = [x for x in d.columns if x not in drop]
X = d[keep]
y = d['cluster']

# Save out X
X.to_csv('data/features/ivs/X_2024-08-09.csv', index=False)

# Drop subject
X = X[[x for x in X.columns if x != 'subject']]


def get_metrics(X, y):

	# Train test split
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,
														random_state=42)
	# Scale data
	nfeatures = X.shape[1]
	categorical_indices = list(range(nfeatures-2, nfeatures))
	numerical_indices = list(range(nfeatures - 2))
	preprocessor = ColumnTransformer(
			transformers = [
				('num', StandardScaler(), numerical_indices),
				('cat', 'passthrough', categorical_indices)
				])

	# Define pipeline
	pipeline = Pipeline(
			steps = [
				('imputer', SimpleImputer(strategy='mean')),
				('scaler', preprocessor),
				('classifier', LogisticRegression(multi_class='multinomial', 
												   solver='lbfgs'))])

	pipeline.fit(X_train, y_train)

	y_hat = pipeline.predict(X_test)

	accuracy = pipeline.score(X_test, y_test)


	# Get ROC score
	nclasses = len(set(y_test))
	y_prob = pipeline.predict_proba(X_test)
	roc_score = roc_auc_score(y_test, y_prob, multi_class='ovr')

	return (accuracy, roc_score)


# Brain only
X_brainonly = X.iloc[:, 12:]

# Get observed roc score
accuracy_brainonly, roc_score_brainonly = get_metrics(X_brainonly, y)
accuracy_all, roc_score_all = get_metrics(X, y)

# Generate null distributions
accuracy_dist = []
roc_score_dist = []
nsims = 1000

for sim in range(nsims):
    y_bs = np.random.choice([1,2,3], size = len(y))
    accuracy_trial, roc_score_trial = get_metrics(X, y_bs)
    accuracy_dist.append(accuracy_trial)
    roc_score_dist.append(roc_score_trial)









'''
# Cross validation
cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring='accuracy')  

print(f"Cross-validation scores: {cv_scores}")
print(f"Mean cross-validation score: {np.mean(cv_scores)}")


# MAKE ROC CURVE
nclasses = len(set(y_test))
y_prob = pipeline.predict_proba(X_test)
y_test_bin = label_binarize(y_test, classes=sorted(y_test.unique()))
dpi = 120
plt.figure(figsize=(1280/dpi, 720/dpi))

for i in range(nclasses):
    fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_prob[:, i])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f'Class {i} (area = {roc_auc:.2f})')

plt.plot([0, 1], [0, 1], 'k--', label='Random')

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristics (ROC) Curve')
plt.legend(loc='lower right')
plt.grid(True)
plt.rcParams['font.size'] = 14

out = 'scripts/ml/logistic-regression/lr_auc.png'
plt.savefig(out, dpi=dpi)
plt.clf()


# Feature importance
lr = pipeline.named_steps['classifier']
weights = lr.coef_
importance = np.mean(np.abs(weights), axis=0)
features = pd.DataFrame({
    'feature': X.columns,
    'importance': importance})


features = pd.DataFrame(sorted(features.to_numpy(), key=lambda x: -x[1]))
features.columns = ['Feature', 'MeanAbsoluteWeight']
'''
