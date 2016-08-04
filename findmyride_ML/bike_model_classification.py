import psycopg2
from hubway_features import hubway_station_features
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from pylab import *
import pickle



## load data
model_features = ['minute_of_day', 'month', 'day_of_week', 'holidays', 'temp_avg', 'precip'] #, 'num_bikes_st1', 'num_bikes_st2', 'num_bikes_st3']


def get_station_ids():
    con = psycopg2.connect(database='hubway_db', user='dianeivy')
    sql_query = "SELECT * FROM station_count;"
    station_info = pd.read_sql_query(sql_query, con)
    return station_info[(station_info['event_count'] > 1000)]['station_id'].values


def bin_data(hubway_row):
    if hubway_row['num_bikes'] == 0:
        return 0
    elif hubway_row['num_bikes'] >= 1 and hubway_row['num_bikes'] <= 3:
        return 1
    else:
        return 2


def split_train_test(station_data):
    station_data['binned_bikes'] = station_data.apply(bin_data, axis=1)
    idx = np.random.permutation(np.arange(31))
    idx_train = idx[:17]
    idx_validate = idx[17:24]
    idx_test = idx[24:31]
    return station_data[station_data['day'].isin(idx_train)], \
           station_data[station_data['day'].isin(idx_validate)], \
           station_data[station_data['day'].isin(idx_test)]


def train_model(train_data, validation_data):
    all_classifiers = []
    all_scores = []
    all_recall = []
    for n_est in [5, 10]:
        clf = RandomForestClassifier(n_estimators=n_est, max_depth=None, n_jobs=2)
        all_classifiers.append(clf)
        clf.fit(train_data[model_features].values, train_data['binned_bikes'].values)
        all_scores.append(clf.score(validation_data[model_features].values,
                                    validation_data['binned_bikes'].values))
        all_recall.append(metrics.recall_score(validation_data['binned_bikes'].values,
                                               clf.predict(validation_data[model_features].values),
                                               average=None)[0])
    print('recall', all_recall)
    return all_classifiers[np.argmax(all_recall)]


for station_number in get_station_ids():
    hubway_data = hubway_station_features(station_number)
    hubway_train, hubway_validate, hubway_test = split_train_test(hubway_data)
    best_rf_clf = train_model(hubway_train, hubway_validate)
    conf_matrix = metrics.confusion_matrix(hubway_test['binned_bikes'].values,
                                           best_rf_clf.predict(hubway_test[model_features].values))
    with open('../findmyride_models/rfc2_%d.pkl' %(station_number), 'wb') as f:
        pickle.dump(best_rf_clf, f)
    with open('../findmyride_models/rfc2_cm_%d.pkl' %(station_number), 'wb') as f:
        pickle.dump(conf_matrix, f)