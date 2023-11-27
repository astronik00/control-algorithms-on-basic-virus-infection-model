import os
from utils import plotter
from scripts.nas import run as run_nas
from scripts.dadar import run as run_dadar


def read_list_by_split(filepath: str, split_sym: str):
    return [float(x) for x in open(filepath).read().split(split_sym)]


model_labels = ['V', 'C', 'F', 'm', 'Z']
control_labels = ['\\psi', '\\psi_1', '\\psi_2', 'u']

a_subclinical = read_list_by_split('../coefficients/set_1/coeffs1.txt', '\n')
a_acute = read_list_by_split('../coefficients/set_1/coeffs2.txt', '\n')
a_chronic = read_list_by_split('../coefficients/set_1/coeffs3.txt', '\n')
a_lethal = read_list_by_split('../coefficients/set_1/coeffs4.txt', '\n')


images_paths = ['../images/test_nas/subclinical/png', '../images/test_nas/subclinical/svg',
                '../images/test_nas/acute/png', '../images/test_nas/acute/svg',
                '../images/test_nas/chronic/png', '../images/test_nas/chronic/svg',
                '../images/test_nas/lethal/png', '../images/test_nas/lethal/svg']

for path in images_paths:
    if not os.path.exists(path):
        os.makedirs(path)

t, t_aim_reach, x, control = run_nas(time=[0, 120, 0.5],
                                     model_params={
                                         'history': [1e-6, 1, 1, 0, 0],
                                         'a': a_chronic,
                                         'm_threshold': 0.1})
                                     # },
                                     # control_params={
                                     #     'x1_aim': 0,
                                     #     'l1': -0.1,
                                     #     'l2': -0.3,
                                     #     'b': 5,
                                     #     'c': 0.1,
                                     #     'mean': 0.0,
                                     #     'std': 0.5
                                     # })

df_nas_acute = plotter.to_df(t, x, control, [model_labels, control_labels])
plotter.plot_x(df_nas_acute, '../images/test_nas/chronic/')


t, t_aim_reach, x, control = run_nas(time=[0, 40, 2.5],
                                     model_params={
                                         'history': [1e-6, 1, 1, 0, 0],
                                         'a': a_lethal,
                                         'm_threshold': 0.1})
                                     # },
                                     # control_params={
                                     #     'x1_aim': 0,
                                     #     'l1': -0.1,
                                     #     'l2': -0.3,
                                     #     'b': 5,
                                     #     'c': 0.1,
                                     #     'mean': 0.0,
                                     #     'std': 0.5
                                     # })

df_nas_lethal = plotter.to_df(t, x, control, [model_labels, control_labels])
plotter.plot_x(df_nas_lethal, '../images/test_nas/lethal/')

