import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression

# This must match validation.py
# feature_1 ∈ [0,100]
# feature_2 ∈ [0,1]
# feature_3 ∈ [0,1000]

np.random.seed(42)

N = 5000

X = np.column_stack([
    np.random.uniform(0, 100, N),
    np.random.uniform(0, 1, N),
    np.random.uniform(0, 1000, N)
])

# Simple decision boundary:
# Higher feature_1 + feature_3 → more likely positive
y = ((X[:, 0] * 0.4 + X[:, 2] * 0.001 + X[:, 1] * 2) > 30).astype(int)

model = LogisticRegression()
model.fit(X, y)

with open("data/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved to data/model.pkl")