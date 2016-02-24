from sklearn import metrics
from sklearn.cross_validation import KFold
from sklearn.preprocessing import OneHotEncoder
import numpy as np

def classification_model(model, data, predictors, label, categorical_features = None, k = 5):
    data_len = len(data)
    auc, r2, rmse = [], [], []

    kf = KFold(data_len, n_folds = k)
    for train, test in kf:
        x_train = (data[predictors].iloc[train,:])
        y_train = data[label].iloc[train]
        x_test = (data[predictors].iloc[test,:])
        y_test = data[label].iloc[test]

        if categorical_features is not None:
            feature_idxs = []
            for name in categorical_features:
                feature_idxs.append(x_train.columns.get_loc(name))
            encoder = OneHotEncoder(categorical_features = feature_idxs)
            encoder.fit(np.vstack((x_train, x_test)))
            x_train = encoder.transform(x_train)
            x_test = encoder.transform(x_test)

        model.fit(x_train, y_train)
        y_pred = model.predict_proba(x_test)[:, 1]

        auc.append(metrics.roc_auc_score(y_test, y_pred))
        r2.append(metrics.r2_score(y_test, y_pred))
        rmse.append(metrics.mean_squared_error(y_test, y_pred)**0.5)

    print 'auc:', np.mean(auc)
    print 'r2:', np.mean(r2)
    print 'rmse:', np.mean(rmse)
