from pylab import *
from plot_figures import plot_data_parameters
from my_colormaps import *
import pickle
import glob


model_features = ['minute_of_day', 'month', 'day_of_week', 'holidays', 'temp_avg', 'precip']
model_feature_labels = ['time (min)', 'month', 'day', 'holidays', 'temp', 'precip']


plot_data_parameters(fs_offset=-6)
## load data
def load_model(station_file):
    with open(station_file, 'rb') as f:
        rf_classifier = pickle.load(f)
    return rf_classifier

def load_cm(station_file):
    with open(station_file, 'rb') as f:
        rf_cm = pickle.load(f)
    return rf_cm


def get_features():
    model_files = sort(glob.glob('../findmyride_models/rfc2_*.pkl'))
    all_feature_importance = []
    for model_file in model_files[:10]:
        all_feature_importance.append(load_model(model_file).feature_importances_)
    return ma.array(all_feature_importance)

def get_cm():
    cm_files = sort(glob.glob('../findmyride_models/confusion_matrix/*.pkl'))
    all_cms = []
    for cm_file in cm_files:
        tmp_cm =load_cm(cm_file)
        if len(tmp_cm) == 3:
            all_cms.append(tmp_cm)
    return all_cms


def fix_axes(ax):
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

rcParams['xtick.major.width'] = 0
rcParams['ytick.major.width'] = 0
rcParams['xtick.minor.width'] = 0
rcParams['ytick.minor.width'] = 0
rcParams['axes.linewidth'] = 3
rcParams['axes.edgecolor'] = 'w'
rcParams['ytick.major.pad'] = '5'
rcParams['xtick.major.pad'] = '5'

def plot_features():
    all_features = get_features()

    figure(figsize=(5, 3))
    ax = subplot(1, 1, 1)
    feature_importance = ma.mean(all_features, axis=0)
    indices = np.argsort(feature_importance)[::-1]
    bar(np.arange(len(feature_importance)), feature_importance[indices], color=np.array([0, 221, 221]) / 255., edgecolor=[1, 1, 1], linewidth=2)
    xticks(np.arange(len(feature_importance)) + 0.4, [model_feature_labels[index] for index in indices], color='w') #, rotation='vertical')
    xlim(-0.2,)
    yticks(np.arange(0, 0.41, 0.1), color='w')
    tight_layout()
    fix_axes(ax)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    rcParams['axes.linewidth'] = 3
    savefig('features.png', transparent=True, dpi=300)
    show()


def plot_average_cm():
    rf_cms = get_cm()
    figure(figsize=(5, 4))
    ax = subplot(111)
    avg_cm = ma.mean(ma.array(rf_cms), axis=0)
    norm_avg_cm = avg_cm.astype('float') / avg_cm.sum(axis=1)[:, None]
    pcolor(norm_avg_cm, cmap=get_cmap('plasma_r'), vmin=0, vmax=1, edgecolors='w', linewidths=4)
    for i in xrange(norm_avg_cm.shape[0]):
        for j in xrange(norm_avg_cm.shape[1]):
            print norm_avg_cm[i, j]
            if norm_avg_cm[i, j] >= 0.3:
                text(j + 0.5, i + 0.5, '%0.2f' %norm_avg_cm[i, j], color='white', ha='center', va='center', fontsize=10, fontweight='bold')
            else:
                text(j + 0.5, i + 0.5, '%0.2f' %norm_avg_cm[i, j], color='k', ha='center', va='center', fontsize=10, fontweight='bold')
    cb = colorbar(ticks=[0, 0.5, 1])
    cb.outline.set_edgecolor('white')
    cb.outline.set_linewidth(2)
    [tl.set_color('white') for tl in cb.ax.yaxis.get_ticklabels()]
    xticks(np.arange(3) + 0.5, ['0 Bikes', '1-2 Bikes', '2+ Bikes'], color='w')
    yticks(np.arange(3) + 0.5, ['0 Bikes', '1-2 Bikes', '2+ Bikes'], color='w')
    ylabel('Predicted', color='white')
    xlabel('Actual', color='white')
    tight_layout(rect=[0.05, 0, 1, 1])
    fix_axes(ax)
    savefig('cm_all.png', transparent=True, dpi=300)


# plot_average_cm()
plot_features()
show()