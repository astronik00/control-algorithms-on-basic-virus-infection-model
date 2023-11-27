import os
from utils import plotter
from scripts.nas import run as run_nas
from scripts.nad import run as run_nad

model_labels = ['V', 'C', 'F', 'm']
model_labels_nad = ['V', 'C', 'F', 'm', 'Z']
control_labels = ['\psi', '\psi_1', 'u']
control_labels_nad = ['\psi', '\psi_1', '\psi_2', 'u']

a1 = [float(x) for x in open("../coefficients/set_1/coeffs1.txt").read().split("\n")]
a2 = [float(x) for x in open("../coefficients/set_1/coeffs2.txt").read().split("\n")]
a3 = [float(x) for x in open("../coefficients/set_1/coeffs3.txt").read().split("\n")]
a4 = [float(x) for x in open("../coefficients/set_1/coeffs4.txt").read().split("\n")]


images_paths = ['../images/nad_nas/subclinical/png', '../images/nad_nas/subclinical/svg',
                '../images/nad_nas/acute/png', '../images/nad_nas/acute/svg',
                '../images/nad_nas/chronic/png', '../images/nad_nas/chronic/svg',
                '../images/nad_nas/lethal/png', '../images/nad_nas/lethal/svg']

# create required paths if not exist
for path in images_paths:
    if not os.path.exists(path):
        os.makedirs(path)

# t, t_aim_reach, y, u, psi, psi1 = run_nas(time=[0, 20, 0.26],
#                                           m_threshold=0.5,
#                                           a=a1,
#                                           history=[1e-6, 1, 1, 0],
#                                           control=1,
#                                           u_params={
#                                               'x1_aim': 0,
#                                               'b': 5,
#                                               'c': 0.1,
#                                               'l1': -0.1,
#                                               'l2': -0.3,
#                                               'mean': 0.0,
#                                               'std': 0.5
#                                           })
#
# df = plotter.to_df(t, y, [psi, psi1, u], [model_labels, control_labels])
# plotter.plot_x(df, '../Results/new_nas/subclinical/')


t, t_aim_reach, x, control = run_nas(time=[0, 20, 0.26],
                                     model_params={
                                         'm_threshold': 0.5,
                                         'a': a2,
                                         'history': [1e-6, 1, 1, 0, 0],
                                         'control': 1,
                                     },
                                     control_params={
                                         'x1_aim': 0,
                                         'b': 5,
                                         'c': 0.1,
                                         'l1': -0.1,
                                         'l2': -0.3,
                                         'mean': 0.0,
                                         'std': 0.5
                                     })

df1 = plotter.to_df(t, x, control, [model_labels_nad, control_labels_nad])

# Nas, acute stage
# t, t_aim_reach, y, u, psi, psi1, psi2 = run_nas(time=[0, 70, 0.5],
#                                                 m_threshold=0.5,
#                                                 a=a3,
#                                                 history=[1e-6, 1, 1, 0],
#                                                 control=1,
#                                                 u_params={
#                                                     'x1_aim': 0,
#                                                     'b': 5,
#                                                     'c': 0.1,
#                                                     'l1': -0.2,
#                                                     'l2': -0.6,
#                                                     'mean': 0.0,
#                                                     'std': 0.5
#                                                 })
#
# df2 = plotter.to_df(t, y, [psi, psi1, psi2, u], [model_labels_nad, control_labels_nad])
# plotter.plot_x(df2, '../Results/new_nas/chronic/')


# t, t_aim_reach, y, u, psi, psi1 = run_nas(time=[0, 50, 2],
#                                           m_threshold=0.5,
#                                           a=a4,
#                                           history=[1e-6, 1, 1, 0],
#                                           control=1,
#                                           u_params={
#                                               'x1_aim': 0,
#                                               'b': 10,
#                                               'c': 0.1,
#                                               'l1': -0.9,
#                                               'l2': -0.6,
#                                               'mean': 0.0,
#                                               'std': 0.5
#                                           })
#
# df = plotter.to_df(t, y, [psi, psi1, u], [model_labels, control_labels])
# plotter.plot_x(df, '../Results/new_nas/lethal/')


# t, t_aim_reach, y, u, psi, psi1, psi2 = run_nad(time=[0, 20, 0.26],
#                                                 m_threshold=0.5,
#                                                 a=a1,
#                                                 history=[1e-6, 1, 1, 0, 0],
#                                                 control=1,
#                                                 u_params={
#                                                     'x1_aim': 0,
#                                                     'b': 5,
#                                                     'k': 0.1,
#                                                     'n': 0.1,
#                                                     'l1': -0.1,
#                                                     'l2': -0.9
#                                                 })
#
# df = plotter.to_df(t, y, [psi, psi1, psi2, u], [model_labels_nad, control_labels_nad])
# plotter.plot_x(df, '../Results/new_nad/subclinical/')


t, t_aim_reach, y, u, psi, psi1, psi2 = run_nad(time=[0, 20, 0.26],
                                                m_threshold=0.5,
                                                a=a2,
                                                history=[1e-6, 1, 1, 0, 0],
                                                control=1,
                                                u_params={
                                                    'x1_aim': 0,
                                                    'b': 5,
                                                    'k': 0.1,
                                                    'n': 0.1,
                                                    'l1': 0.1,
                                                    'l2': -0.9,
                                                    'disturbance': 0.1
                                                })

df3 = plotter.to_df(t, y, [psi, psi1, psi2, u], [model_labels_nad, control_labels_nad])

# t, t_aim_reach, y, u, psi, psi1, psi2 = run_nad(time=[0, 70, 0.5],
#                                                 m_threshold=0.5,
#                                                 a=a3,
#                                                 history=[1e-6, 1, 1, 0, 0],
#                                                 control=1,
#                                                 u_params={
#                                                     'x1_aim': 0,
#                                                     'b': 5,
#                                                     'k': 0.1,
#                                                     'n': 0.1,
#                                                     'l1': 0.7,
#                                                     'l2': -0.1
#                                                 })
#
# df4 = plotter.to_df(t, y, [psi, psi1, psi2, u], [model_labels_nad, control_labels_nad])
# plotter.plot_x(df4, '../Results/new_nad/chronic/')

# t, t_aim_reach, y, u, psi, psi1, psi2 = run_nad(
#     time=[0, 35, 2.5],
#     m_threshold=0.5,
#     a=a4,
#     history=[1e-6, 1, 1, 0, 0],
#     control=0,
#     u_params={
#         'x1_aim': 0,
#         'b': 5,
#         'k': 0.1,
#         'n': 0.1,
#         'l1': 0.1,
#         'l2': -0.9
#     })
#
# df = plotter.to_df(t, y, [psi, psi1, psi2, u], [model_labels_nad, control_labels_nad])
# plotter.plot_x(df, '../Results/new_nad/lethal/')

plotter.plot_two_one_axes(df1, df3, '../images/nad_nas/acute/')
# plotter.plot_two_one_axes(df2, df4, '../Results/nad_nas/chronic/')
