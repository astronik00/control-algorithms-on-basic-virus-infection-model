import os

import matplotlib.pyplot as plt
import numpy as np
from utils import plotter
from scripts.nad import run as run_nad


def read_list_by_split(filepath: str, split_sym: str):
    return [float(x) for x in open(filepath).read().split(split_sym)]


model_labels = ['V', 'C', 'F', 'm', 'Z']
control_labels = ['\\psi', '\\psi_1', '\\psi_2', 'u']

measure_labels = ['days', 'particle/ml', 'cell/ml', 'particle/ml', '', '', '', '', '', 'particle/ml']

a_subclinical = read_list_by_split('../coefficients/set_1/coeffs1.txt', '\n')
a_acute = read_list_by_split('../coefficients/set_1/coeffs2.txt', '\n')
a_chronic = read_list_by_split('../coefficients/set_1/coeffs3.txt', '\n')
a_lethal = read_list_by_split('../coefficients/set_1/coeffs4.txt', '\n')

images_paths = ['../images/test_nad/restricted/subclinical/png', '../images/test_nad/restricted/subclinical/svg',
                '../images/test_nad/restricted/acute/png', '../images/test_nad/restricted/acute/svg',
                '../images/test_nad/restricted/chronic/png', '../images/test_nad/restricted/chronic/svg',
                '../images/test_nad/restricted/lethal/png', '../images/test_nad/restricted/lethal/svg',

                '../images/test_nad/not_restricted/subclinical/png',
                '../images/test_nad/not_restricted/subclinical/svg',
                '../images/test_nad/not_restricted/acute/png', '../images/test_nad/not_restricted/acute/svg',
                '../images/test_nad/not_restricted/chronic/png', '../images/test_nad/not_restricted/chronic/svg',
                '../images/test_nad/not_restricted/lethal/png', '../images/test_nad/not_restricted/lethal/svg'
                ]

for path in images_paths:
    if not os.path.exists(path):
        os.makedirs(path)

# restricted k = 0.1, n = 0.1, l1=-0.9, l2=-0.2
# t, t_aim_reach, y, u, psi, psi1, psi2 = run_nad(time=[0, 20, 0.26],
#                                                 m_threshold=0.5,
#                                                 a=a_acute,
#                                                 history=[1e-6, 1, 1, 0, 0],
#                                                 control=1,
#                                                 u_params={
#                                                     'x1_aim': 0,
#                                                     'b': 5,
#                                                     'k': 0.1,
#                                                     'n': 0.1,
#                                                     'l1': -0.9,
#                                                     'l2': -0.2,
#                                                     'disturbance': 0.1
#                                                 })



# df_nad_restricted_acute = plotter.to_df(t, y,
#                                         [psi, psi1, psi2, u],
#                                         [model_labels, control_labels])
#
# plotter.plot_x(df_nad_restricted_acute, '../images/test_nad/restricted/acute/')
#
# t, t_aim_reach, y, u, psi, psi1, psi2 = run_nad(time=[0, 35, 0.5],
#                                                 m_threshold=0.5,
#                                                 a=a_chronic,
#                                                 history=[1e-6, 1, 1, 0, 0],
#                                                 control=1,
#                                                 u_params={
#                                                     'x1_aim': 0,
#                                                     'b': 5,
#                                                     'k': 0.1,
#                                                     'n': 0.1,
#                                                     'l1': -0.9,
#                                                     'l2': -0.9,
#                                                     'disturbance': 0.1
#                                                 })



#
# df_nad_restricted_chronic = plotter.to_df(t, y,
#                                           [psi, psi1, psi2, u],
#                                           [model_labels, control_labels])
#
# plotter.plot_x(df_nad_restricted_chronic, '../images/test_nad/restricted/chronic/')

# not restricted: k = 0.1, n = 0.1, l1 = -0.1, l2 = -0.9
# restricted: k = 0.1, n = 0.1, l1 = -0.3, l2 = -0.9

t, t_aim_reach, y, u, psi, psi1, psi2 = run_nad(time=[0, 40, 2.5],
                                                m_threshold=0.5,
                                                a=a_lethal,
                                                history=[1e-6, 1, 1, 0, 0],
                                                control=1,
                                                u_params={
                                                    'x1_aim': 0,
                                                    'b': -1,
                                                    'k': 0.1,
                                                    'n': 0.01,
                                                    'l1': -0.1,
                                                    'l2': -0.9,
                                                    'disturbance': 0.1
                                                })

fig, ax = plt.subplots()
ax.plot(t, y[0], color='black')
ax.plot(t, np.zeros(len(y[0])), linewidth=3.0, color="red", alpha=0.5)
ax.set_ylim(min(y[0]), max(y[0]) * 1.2)
ax.text(.01, .97, "$V_f(t)$", ha='left', va='top', transform=ax.transAxes)
ax.set_xlabel("$t$, days", loc="right")
# ax.set_ylabel('particle/ml')
fig.tight_layout()
plt.show()


#
print(y[0][-1])
print(u[-1])
df_nad_not_restricted_lethal = plotter.to_df(t, y,
                                             [psi, psi1, psi2, u],
                                             [model_labels, control_labels])

plotter.plot_x(df_nad_not_restricted_lethal, '../images/test_nad/restricted/lethal/')
