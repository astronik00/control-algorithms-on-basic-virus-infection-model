import os
from utils import plotter
from scripts.nas import run as run_nas
from scripts.dadar import run as run_dadar


def read_list_by_split(filepath: str, split_sym: str):
    return [float(x) for x in open(filepath).read().split(split_sym)]


model_labels = ['V', 'C', 'F', 'm', 'Z']
control_labels = ['\\psi', '\\psi_1', '\\psi_2', 'u']
measure_labels = ['', 'particle/ml', 'cell/ml', 'particle/ml', '', '', '', '', '', 'particle/ml']

a_subclinical = read_list_by_split('../coefficients/set_1/coeffs1.txt', '\n')
a_acute = read_list_by_split('../coefficients/set_1/coeffs2.txt', '\n')
a_chronic = read_list_by_split('../coefficients/set_1/coeffs3.txt', '\n')
a_lethal = read_list_by_split('../coefficients/set_1/coeffs4.txt', '\n')

images_paths = ['../images/nas+dadar/subclinical/png', '../images/nas+dadar/subclinical/svg',
                '../images/nas+dadar/acute/png', '../images/nas+dadar/acute/svg',
                '../images/nas+dadar/chronic/png', '../images/nas+dadar/chronic/svg',
                '../images/nas+dadar/lethal/png', '../images/nas+dadar/lethal/svg']

# create required paths if not exist
for path in images_paths:
    if not os.path.exists(path):
        os.makedirs(path)

# ACUTE STAGE
# t, t_aim_reach, x, control, disturbances = run_nas(time=[0, 20, 0.26],
#                                                    model_params={
#                                                        'history': [1e-6, 1, 1, 0, 0],
#                                                        'a': a_acute,
#                                                        'm_threshold': 0.5
#                                                    },
#                                                    control_params={
#                                                        'x1_aim': 0,
#                                                        'l1': -0.1,
#                                                        'l2': -0.3,
#                                                        'b': 5,
#                                                        'c': 0.1,
#                                                        'mean': 0.0,
#                                                        'std': 0.5
#                                                    })
#
# df_nas_acute = plotter.to_df(t, x, control, [model_labels, control_labels])
#
# t, t_aim_reach, x, control = run_dadar(time=[0, 20, 0.26],
#                                        disturbances=disturbances,
#                                        model_params={
#                                            'history': [1e-6, 1, 1, 0, 0],
#                                            'a': a_acute,
#                                            'm_threshold': 0.5
#                                        },
#                                        control_params={
#                                            'x1_aim': 0,
#                                            'l1': -0.9,
#                                            'l2': -0.9,
#                                            'b': 5
#                                        })
#
# df_dadar_acute = plotter.to_df(t, x, control, [model_labels, control_labels])
#
# plotter.plot_two_one_axes(df_dadar_acute, df_nas_acute, '../images/nas+dadar/acute/', measure_labels)

# CHRONIC STAGE

t, t_aim_reach, x, control, disturbances = run_nas(time=[0, 20, 0.5],
                                                   model_params={
                                                       'history': [1e-6, 1, 1, 0, 0],
                                                       'a': a_chronic,
                                                       'm_threshold': 0.5
                                                   },
                                                   control_params={
                                                       'x1_aim': 0,
                                                       'b': 5,
                                                       'c': 0.1,
                                                       'mean': 0.0,
                                                       'std': 0.5,
                                                       'l1': -0.2,
                                                       'l2': -0.6
                                                   })
df_nas_chronic = plotter.to_df(t, x, control, [model_labels, control_labels])

t, t_aim_reach, x, control = run_dadar(time=[0, 20, 0.5],
                                       disturbances=disturbances,
                                       model_params={
                                           'history': [1e-6, 1, 1, 0, 0],
                                           'a': a_chronic,
                                           'm_threshold': 0.5
                                       },
                                       control_params={
                                           'x1_aim': 0,
                                           'l1': -0.2,
                                           'l2': -0.3,
                                           'b': 5
                                       })

df_dadar_chronic = plotter.to_df(t, x, control, [model_labels, control_labels])

plotter.plot_two_one_axes(df_dadar_chronic, df_nas_chronic, '../images/nas+dadar/chronic/')
