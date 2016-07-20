from pylab import *
from plot_figures import plot_data_parameters
from my_colormaps import *
import pickle
import glob


model_features = ['minute_of_day', 'month', 'day_of_week', 'holidays', 'temp_avg', 'precip']
model_feature_labels = ['minute', 'month', 'day', 'holidays', 'temp', 'precip']


## load data
def load_model(station_file):
    with open(station_file, 'rb') as f:
        rf_classifier = pickle.load(f)
    return rf_classifier


def load_cm(station_file):
    with open(station_file, 'rb') as f:
        rf_cm = pickle.load(f)
    return rf_cm


def get_cm():
    cm_files = sort(glob.glob('../findmyride_models/rfc_all_cm_*.pkl'))
    all_cms = []
    for cm_file in cm_files:
        print(cm_file)
        tmp_cm =load_cm(cm_file)
        print(tmp_cm.shape)
        if len(tmp_cm) > 15:
            all_cms.append(tmp_cm[:16, :16])
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
rcParams['axes.linewidth'] = 1.5
rcParams['axes.edgecolor'] = 'w'
rcParams['ytick.major.pad'] = '5'
rcParams['xtick.major.pad'] = '5'


def plot_average_cm():
    rf_cms = get_cm()
    print(ma.array(rf_cms).shape)
    figure(figsize=(5, 4))
    ax = subplot(111)
    avg_cm = ma.mean(ma.array(rf_cms), axis=0)
    norm_avg_cm = avg_cm.astype('float') / avg_cm.sum(axis=1)[:, None]
    pcolor(norm_avg_cm, cmap=get_cmap('plasma_r'), vmin=0, vmax=1, edgecolors='w', linewidths=4)
    # for i in xrange(norm_avg_cm.shape[0]):
    #     for j in xrange(norm_avg_cm.shape[1]):
    #         print norm_avg_cm[i, j]
    #         if norm_avg_cm[i, j] >= 0.3:
    #             text(j + 0.5, i + 0.5, '%0.2f' %norm_avg_cm[i, j], color='white', ha='center', va='center', fontsize=10, fontweight='bold')
    #         else:
    #             text(j + 0.5, i + 0.5, '%0.2f' %norm_avg_cm[i, j], color='grey', ha='center', va='center', fontsize=10, fontweight='bold')

    cb = colorbar(ticks=[0, 0.5, 1])
    cb.outline.set_edgecolor('white')
    cb.outline.set_linewidth(2)
    [tl.set_color('white') for tl in cb.ax.yaxis.get_ticklabels()]
    xticks(np.arange(16) + 0.5, np.arange(16), color='w')
    yticks(np.arange(16) + 0.5, np.arange(16), color='w')
    # xticks(np.arange(3) + 0.5, ['0 Bikes', '1-2 Bikes', '2+ Bikes'], color='w')
    # yticks(np.arange(3) + 0.5, ['0 Bikes', '1-2 Bikes', '2+ Bikes'], color='w')
    ylabel('Predicted', color='white')
    xlabel('Actual', color='white')
    tight_layout(rect=[0.05, 0, 1, 1])
    fix_axes(ax)
    savefig('cm_all_16.png', transparent=True, dpi=300)

plot_data_parameters(fs_offset=-6)
plot_average_cm()
show()
