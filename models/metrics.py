from sklearn import metrics
from scipy import stats


def binary_classification_metrics(label, pred, pred_c):

	auc = metrics.roc_auc_score(label, pred)
	r, _ = stats.pearsonr(label, pred)
	r2 = (r**2)
	rmse = metrics.mean_squared_error(label, pred)**0.5
	acc = metrics.accuracy_score(label, pred_c)
	return auc, r2, rmse, acc