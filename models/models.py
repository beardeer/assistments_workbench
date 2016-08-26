from metrics import binary_classification_metrics
from sklearn.cross_validation import KFold, LabelKFold, LeavePOut, LeavePLabelOut, LabelShuffleSplit
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



def classification_model(model, data, predictors, label, categorical_features = None, cv_label_name = None, k = 5, test_size = 0.1, n_iter = 100, train_only = False):
    data_len = len(data)
    cv = None
    auc, r2, rmse, acc = [], [], [], []

    # print 'Predictors:', predictors
    predictors = [p.strip() for p in predictors]

    if cv_label_name is not None:
        cv_label = data[cv_label_name]
    else:
        cv_label = None


    if k is not None and cv_label is not None:
        cv = LabelKFold(cv_label, n_folds = k)
    elif k is not None and cv_label is None:
        cv = KFold(data_len, n_folds = k, shuffle = True)

    if k is None and test_size is not None and n_iter is not None and cv_label is not None:
        cv = LabelShuffleSplit(cv_label, n_iter = n_iter, test_size = test_size, random_state = 42)


    for train, test in cv:
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
