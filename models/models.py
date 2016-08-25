from metrics import binary_classification_metrics
from sklearn.cross_validation import KFold
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from scipy import stats
from tqdm import tqdm

def majority_model(data, label):

    mean_label = np.mean(data[label])
    if mean_label >= 0.5:
        data['majority'] = 1
    else:
        data['majority'] = 0

    return binary_classification_metrics(data[label], data['majority'], data['majority'])



def classification_model(model, data, predictors, label, categorical_features = None, k = 5, train_only = False):
    data_len = len(data)
    auc, r2, rmse, acc = [], [], [], []

    # print 'Predictors:', predictors
    predictors = [p.strip() for p in predictors]

    kf = KFold(data_len, n_folds = k, shuffle = True)
    for train, test in tqdm(kf):
        x_train = (data[predictors].iloc[train,:])
        y_train = data[label].iloc[train]
        x_test = (data[predictors].iloc[test,:])
        y_test = data[label].iloc[test]

        if categorical_features is not None:
            feature_idxs = [x_train.columns.get_loc(name) for name in categorical_features]
            encoder = OneHotEncoder(categorical_features = feature_idxs)
            encoder.fit(np.vstack((x_train, x_test)))
            x_train = encoder.transform(x_train)
            x_test = encoder.transform(x_test)

        model.fit(x_train, y_train)
        if train_only:
            x_test = x_train
            y_test = y_train
        y_pred_p = model.predict_proba(x_test)[:, 1]
        y_pred_c = model.predict(x_test)

        a,b,c,d = binary_classification_metrics(y_test, y_pred_p, y_pred_c)

        auc.append(a)
        r2.append(b)
        rmse.append(c)
        acc.append(d)

    # print 'auc:', a
    # print 'r2:', b
    # print 'rmse:', c
    # print 'accuracy:', d

    return np.mean(auc), np.mean(r2), np.mean(rmse), np.mean(acc)
