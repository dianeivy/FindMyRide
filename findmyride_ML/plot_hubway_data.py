from hubway_features import hubway_station_features
from pylab import *
from plot_figures import plot_data_parameters


## load data
station_number = 3
hubway_data = hubway_station_features(station_number)


plot_data_parameters(fs_offset=-6)
rcParams['axes.linewidth'] = 3
rcParams['axes.edgecolor'] = 'w'
rcParams['xtick.major.size'] = 0
rcParams['ytick.major.size'] = 0
rcParams['xtick.minor.size'] = 0
rcParams['ytick.minor.size'] = 0
rcParams['ytick.major.pad'] = '5'
rcParams['xtick.major.pad'] = '5'

# figure()
# subplot(1, 1, 1)
# plot(hubway_data['event_date'], hubway_data['num_bikes'], 'k.')
# ylabel('Number Bikes')
# show()

weekend_color = np.array([0, 221, 221]) / 255.
weekday_color = [0.65, 0.65, 0.65]
def fix_axes(ax):
    blue = 'white'
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_color(blue)
    ax.spines['bottom'].set_color(blue)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    [tl.set_color(blue) for tl in ax.get_yticklabels()]
    [tl.set_color(blue) for tl in ax.get_xticklabels()]
    ylabel('Number of Bikes', color=blue)
    ylim(0, 10)
    yticks([0, 10])
    xticks(np.arange(24), ['12am'] + [''] * 7 + ['8am'] + [''] * 9 + ['5pm'] + [''] * 6)
    xlim(0, 23)



figure(figsize=(4, 2))

hubway_wd = hubway_data[(hubway_data['day_of_week'] < 5)]
hubway_we = hubway_data[(hubway_data['day_of_week'] >= 5)]

ax = subplot(1, 1, 1)
hubway_dow = hubway_data[(hubway_data['month'] > 3)].groupby(['day_of_week', 'hour_of_day'])['num_bikes'].mean().reshape(7, 24)
plot([-99], [-99], color=weekday_color, lw=2, label='Weekday')
plot([-99], [-99], color=weekend_color, lw=2, label='Weekend')
plot(hubway_dow[:5, :].T, color=weekday_color, lw=1.25)
plot(hubway_dow[5:, :].T, color=weekend_color, lw=1.25)
l = legend(loc='best')
for text in l.get_texts():
    text.set_color('white')
fix_axes(ax)
suptitle('Commerical Station', color='white')
savefig('station_data_commercial.png', transparent=True, dpi=300)
show()

def average_morning_data():
    hubway_wd['event_date_day'] = hubway_wd['event_date'].apply(lambda x: x.date())
    all_event_dates = sort(list(set(hubway_wd['event_date_day'])))
    morning_bikes = []
    morning_temp = []
    morning_rain = []
    for tmp_date in all_event_dates:
        tmp_hubway_data = hubway_wd[(hubway_wd['event_date_day'] == tmp_date) & (hubway_wd['hour_of_day'] == 8)]
        morning_bikes.append(tmp_hubway_data['num_bikes'].mean())
        morning_temp.append(tmp_hubway_data['temp_avg'].mean())
        morning_rain.append(hubway_wd[(hubway_wd['event_date_day'] == tmp_date) & (hubway_wd['hour_of_day'] <= 8)]['precip'].mean())

    return all_event_dates, morning_bikes, morning_temp, morning_rain

morning_dates, morning_bikes, morning_temp, morning_rain = average_morning_data()

figure()
for i in xrange(len(morning_dates)):
    if morning_rain[i] > 0:
        plot(morning_dates[i], morning_bikes[i], 'bo')
    else:
        plot(morning_dates[i], morning_bikes[i], 'ko')
show()

# figure()
# subplot(3, 1, 1)
# plot(morning_dates, morning_bikes, 'k.')
# subplot(3, 1, 2)
# plot(morning_dates, morning_temp, 'k.')
# subplot(3, 1, 3)
# plot(morning_dates, morning_rain, 'k.')
# savefig('blah.pdf')
# show()
# figure()
# subplot(1, 1, 1)
# plot(hubway_data['event_date'], hubway_data['num_bikes'], 'k.')
# ylabel('Number Bikes')
# show()
#
# def calc_restock():
# figure()
#
# #
# #
# # ax = subplot(3, 1, 2)
# # hubway_wd_rain = hubway_wd[(hubway_wd['precip'] >= 0.005) & (hubway_data['month'] > 3)].groupby(['hour_of_day'])['num_bikes'].mean()
# # hubway_wd_norain = hubway_wd[(hubway_wd['precip'] < 0.005) & (hubway_data['month'] > 3)].groupby(['hour_of_day'])['num_bikes'].mean()
# # hubway_we_rain = hubway_we[(hubway_we['precip'] >= 0.005) & (hubway_data['month'] > 3)].groupby(['hour_of_day'])['num_bikes'].mean()
# # hubway_we_norain = hubway_we[(hubway_we['precip'] < 0.005) & (hubway_data['month'] > 3)].groupby(['hour_of_day'])['num_bikes'].mean()
# #
# #
# # plot(hubway_we_norain, color=weekend_color, lw=1.5, label='No Rain')
# # pl, = plot(hubway_we_rain, '--', color=weekend_color, lw=1.5, label='Rain')
# # pl.set_dashes([1, 1])
# # l = legend(loc='best')
# # for text in l.get_texts():
# #     text.set_color(weekday_color)
# # pl, = plot(hubway_wd_rain, '--', color=weekday_color, lw=1.5)
# # pl.set_dashes([1, 1])
# # plot(hubway_wd_norain, color=weekday_color, lw=1.5)
# # fix_axes(ax)
# #
# # fix_axes(ax)
# #
# # ax = subplot(3, 1, 3)
# # hubway_wd_cold = hubway_wd[(hubway_wd['temp_avg'] < 5) & (hubway_data['month'] > 3)].groupby(['hour_of_day'])['num_bikes'].mean()
# # hubway_wd_warm = hubway_wd[(hubway_wd['temp_avg'] >= 5) & (hubway_data['month'] > 3)].groupby(['hour_of_day'])['num_bikes'].mean()
# # hubway_we_cold = hubway_we[(hubway_we['temp_avg'] < 5) & (hubway_data['month'] > 3)].groupby(['hour_of_day'])['num_bikes'].mean()
# # hubway_we_warm = hubway_we[(hubway_we['temp_avg'] >= 5) & (hubway_data['month'] > 3)].groupby(['hour_of_day'])['num_bikes'].mean()
# #
# # plot(hubway_we_warm, color=weekend_color, lw=1.5, label='Warm')
# # plot(hubway_we_cold, '--', color=weekend_color, lw=1.5, label='Cold')
# # l = legend(loc='best')
# # for text in l.get_texts():
# #     text.set_color(weekday_color)
# # plot(hubway_wd_warm, color=weekday_color, lw=1.5)
# # plot(hubway_wd_cold, '--', color=weekday_color, lw=1.5)
# # # tight_layout(rect=(0, 0, 1, 0.97))
# # fix_axes(ax)
# # savefig('station_hour_%d.pdf' %station_number)
# # show()