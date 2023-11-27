import os
from utils import plotter
from scripts.nas import run as run_nas


def read_list_by_split(filepath: str, split_sym: str):
    return [float(x) for x in open(filepath).read().split(split_sym)]


model_labels = ['V', 'C', 'F', 'm', 'Z']
control_labels = ['\\psi', '\\psi_1', '\\psi_2', 'u']

a_subclinical = read_list_by_split('../coefficients/set_1/coeffs1.txt', '\n')
a_acute = read_list_by_split('../coefficients/set_1/coeffs2.txt', '\n')
a_chronic = read_list_by_split('../coefficients/set_1/coeffs3.txt', '\n')
a_lethal = read_list_by_split('../coefficients/set_1/coeffs4.txt', '\n')


images_paths = ['../images/test_nas/restricted/subclinical/png', '../images/test_nas/restricted/subclinical/svg',
                '../images/test_nas/restricted/acute/png', '../images/test_nas/restricted/acute/svg',
                '../images/test_nas/restricted/chronic/png', '../images/test_nas/restricted/chronic/svg',
                '../images/test_nas/restricted/lethal/png', '../images/test_nas/restricted/lethal/svg',

                '../images/test_nas/not_restricted/subclinical/png', '../images/test_nas/not_restricted/subclinical/svg',
                '../images/test_nas/not_restricted/acute/png', '../images/test_nas/not_restricted/acute/svg',
                '../images/test_nas/not_restricted/chronic/png', '../images/test_nas/not_restricted/chronic/svg',
                '../images/test_nas/not_restricted/lethal/png', '../images/test_nas/not_restricted/lethal/svg'
                ]

for path in images_paths:
    if not os.path.exists(path):
        os.makedirs(path)


t, t_aim_reach, x, control = run_nas(time=[0, 70, 0.26],
                                     model_params={
                                         'history': [1e-6, 1, 1, 0, 0],
                                         'a': a_acute,
                                         'm_threshold': 0.5
                                     },
                                     control_params={
                                         'x1_aim': 0,
                                         'l1': -0.9,
                                         'l2': -0.1,
                                         'b': -1,
                                         'c': 0.1,
                                         'mean': 0.0,
                                         'std': 0.5
                                     })

df_nas_acute = plotter.to_df(t, x, control, [model_labels, control_labels])

plotter.plot_x(df_nas_acute,'../images/test_nas/restricted/acute/')