import numpy as np
import psycopg2
from hubway_features import hubway_station_features
from sklearn.externals import joblib
import pandas as pd
from sklearn import linear_model, metrics
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import scale
from sklearn.cross_validation import KFold, cross_val_score, train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.preprocessing import label_binarize
from time import time

from pylab import *

## load data
hubway_data = hubway_station_features(3)
print hubway_data.info()

model_features = ['minute_of_day', 'month', 'precip', 'num_bikes_st1', 'num_bikes_st2', 'num_bikes_st3']
X_data = scale(hubway_data[model_features].values)
Y_data = hubway_data['num_bikes'].values
y = label_binarize(Y_data, classes=np.arange(0, Y_data.max()))
X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=0.33, random_state=42)


def train_model(model, params=None, features=None, metric='roc_auc'):
    grid_search = GridSearchCV(model, param_grid=params)
    start = time()
    grid_search.fit(X_train, y_train)
    print("GridSearchCV took %.2f seconds for %d candidate parameter settings."
          % (time() - start, len(grid_search.grid_scores_)))
    print(grid_search.grid_scores_)
    # print(grid_search.grid_scores_[0])
    # print(grid_search.best_estimator_)
    # print(grid_search.best_score_)
    # print(grid_search.scorer_)
    # print 'predict'
    # print(grid_search.predict(X_test[0, :]))
    # print(grid_search.predict_proba(X_test[0, :]))
    # print(grid_search.score(X_train, y_train))
    return grid_search.best_estimator_
    # joblib.dump(grid.best_estimator_, 'filename.pkl', compress = 1)


# clf = linear_model.Lasso()
# clf = linear_model.Ridge()
# best = train_model(clf, params={'alpha': [0.1, 1.0]})



# clf = RandomForestClassifier(n_estimators=2, max_depth=1)
random_forest_params = {"max_depth": [1, 4],
                        "max_features": [3, None]}

                        # "min_samples_split": [1, 3, 10],
                        # "min_samples_leaf": [1, 3, 10],
                        # "bootstrap": [True, False],
                        # "criterion": ["gini", "entropy"]
clf = RandomForestRegressor()
best = train_model(clf, params=random_forest_params)
# print(best.score(X_train, y_train))

def pred_ints(model, X, percentile=95):
    err_down = []
    err_up = []
    for x in range(len(X)):
        preds = []
        for pred in model.estimators_:
            preds.append(pred.predict(X[x])[0])
        err_down.append(np.percentile(preds, (100 - percentile) / 2. ))
        err_up.append(np.percentile(preds, 100 - (100 - percentile) / 2.))
    return err_down, err_up

err_dwn, err_up = pred_ints(best, X_test[:10, :])
print err_dwn
print err_up

# best_lr = train_model(clf, params=random_forest_params)


# clf = linear_model.LogisticRegression(penalty='l2', multi_class='multinomial')
# logistic_regression_params = {'C': [100], #[0.001, 0.01, 0.1, 1, 10, 100, 1000]
#                                         'solver': ['lbfgs', 'newton-cg']}
# best_lr = train_model(clf, params=logistic_regression_params)


# clf = SVC()
# svc_regression_params = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000],
#                          'kernel': ['linear', 'rbf']}
# train_model(clf, params=svc_regression_params)


## calulate a metric
# figure()
# for index in xrange(12):
#     subplot(3, 4, index + 1)
#     probs = best_lr.predict_proba(X_test[index, :])[0]
#     weighted_probs = np.sum(probs * np.arange(len(probs))) / len(probs)
#     plot(probs)
#     print(weighted_probs)
# show()


# ## validation
# print 'Confusion Matrix'
# print(metrics.confusion_matrix(y_test, best_lr.predict(X_test)))
# print metrics.confusion_matrix(y_test, best_lr.predict(X_test)).shape
# figure()
# pcolor(metrics.confusion_matrix(y_test, best_lr.predict(X_test)))
# colorbar()
# show()
#
# print 'Accuracy'
# print(metrics.accuracy_score(y_test, best_lr.predict(X_test)))
#
# print 'Precision'
# print(metrics.precision_score(y_test, best_lr.predict(X_test)))
#
# print('Recall Score')
# print(metrics.recall_score(y_test, best_lr.predict(X_test)))

# print('ROC Curve')
# print(metrics.roc_curve(y_test, best_lr.predict(X_test)))

# print('ROC AUC Score')
# print(metrics.roc_auc_score(y_test, best_lr.predict(X_test)))

# ## check isnull()
# ## split data and scale scale()

#
#
# ## build model
# ## C = [0.01, 0.1, 1, 10, 100]
# ## multi_class = 'ovr' or 'multinomial' if multinomial solver 'lbfgs'; 'ovr' solver 'newton-cg', 'lbfgs'
# logreg = linear_model.LogisticRegression(penalty='l2', C=1, solver='lbfgs', multi_class='multinomial')
# logreg.fit(X_train, y_train)
#
# figure()
# index = 100
# subplot(1, 2, 1)
# print('Test Result: ', y_test[index])
# print('num of bins: ', len(logreg.predict_proba(X_test[index, :])[0]))
# print(hubway_data['num_bikes'].values.max())
# plot(logreg.predict_proba(X_test[index, :])[0], 'k-')
#
#
#
# clf = RandomForestClassifier(n_estimators=2, max_depth=1)
# clf.fit(X_train, y_train)
# print(clf.predict_proba(X_test[index, :]))
# print(clf.score(X_train, y_train))
# subplot(1, 2, 2)
# plot(clf.predict_proba(X_test[index, :])[0], 'k')
#
#
# y_score = clf.fit(X_train, y_train).decision_function(X_test)
# # Compute ROC curve and ROC area for each class
# fpr = dict()
# tpr = dict()
# roc_auc = dict()
# for i in range(n_classes):
#     fpr[i], tpr[i], _ = metrics.roc_curve(y_test[:, i], y_score[:, i])
#     roc_auc[i] = metrics.auc(fpr[i], tpr[i])
#
# # Compute micro-average ROC curve and ROC area
# fpr["micro"], tpr["micro"], _ = metrics.roc_curve(y_test.ravel(), y_score.ravel())
# roc_auc["micro"] = metrics.auc(fpr["micro"], tpr["micro"])
#
# # Plot of a ROC curve for a specific class
# plt.figure()
# plt.plot(fpr[2], tpr[2], label='ROC curve (area = %0.2f)' % roc_auc[2])
# plt.plot([0, 1], [0, 1], 'k--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('Receiver operating characteristic example')
# plt.legend(loc="lower right")
# plt.show()
#
# ## precision
#
# ## recall
#
# ## roc curve
#
# ## accuracy
#
# ## cross-validation
#
# print(logreg.score(X_test, y_test))
# print(metrics.precision_score(y_test, logreg.predict(X_test)))
# # print(metrics.average_precision_score(y_test, logreg.predict(X_test)))
#
#
#
#
#
# # figure()
# # subplot(1, 2, 1)
# # plot(logreg.predict(X_test), y_test, 'k.')
# # subplot(1, 2, 2)
# # plot(logreg.predict(X_test), y_test, 'k.')
# # show()
#
# ## cross-validate
# # from sklearn.ensemble import RandomForestClassifier
# # from sklearn.cross_validation import KFold, cross_val_score
# # clf = RandomForestClassifier(n_estimators=200, n_jobs=2,  )
# # kf = KFold(sk_frame.shape[0], n_folds=4, shuffle=True )
# # score = cross_val_score(clf, np.array(sk_frame), targets, cv=kf, n_jobs=2)
#
# ## roc curve
# ## look at features importance
# # feature_importances = logreg.feature_importances_
# # indices = np.argsort(feature_importances)[::-1]
# # print np.array(model_features)[indices]
#
