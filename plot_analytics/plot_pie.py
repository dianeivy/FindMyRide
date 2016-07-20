from pylab import *
from plot_figures import plot_data_parameters



plot_data_parameters(fs_offset=-6)
rcParams['text.color'] = 'w'
rcParams['text.fontweight'] = 'bold'
rcParams['lines.linewidth'] = 2
figure(figsize=(4, 3))
pie_wedge_collection = pie([17, 7, 7], explode=(0, 0, 0.15), colors=[[0.6, 0.6, 0.6], np.array([0, 221, 221]) / 255., [1, 0, 0.5]],
    labels=['Training', 'Testing', 'Validation'], autopct='%0.1f%%', shadow=True, startangle=0)
for pie_wedge in pie_wedge_collection[0]:
    print(pie_wedge.__dict__.keys())
    pie_wedge.set_edgecolor('white')
    pie_wedge.set_linewidth(4)
axis('equal')
savefig('pie3.png', transparent=True, dpi=300)
show()