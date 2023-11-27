import random as rand
from numerical_methods.euler import x1_next, x2_next, x3_next, x4_next
from models.basic_model import get_ksi, f3
from utils.adar_common_func import get_psi, get_psi1


def get_fi(a, h, l2, x1_aim, x1):
    return a[0] / a[1] + (h * a[1] * x1) ** -1 * (1 + l2) * (get_psi(x1_aim, x1))


def get_u(a, h, l1, l2, x1_aim, x):
    psi_temp = get_psi(x1_aim, x[0][-1])
    fi_temp = get_fi(a, h, l2, x1_aim, x[0][-1])
    psi1_temp = get_psi1(fi_temp, x[2][-1])
    psi2_temp = 0
    fi_next = get_fi(a, h, l2, x1_aim, x1_next(a, h, x))
    u = h**-1 * (fi_next - l1*psi1_temp - x[2][-1]) - f3(a, x[0][-1], x[1][-1], x[2][-1])
    return psi_temp, psi1_temp, psi2_temp, u


def run(time, model_params, control_params=None, disturbances=None):
    tstart = time[0]
    tend = time[1]
    h = time[2]

    a = model_params['a']
    history = model_params['history']
    m_threshold = model_params['m_threshold']

    points = int((tend - tstart) / h)
    t_aim_reach = -1

    x = [[history[0]], [history[1]], [history[2]], [history[3]], [0]]
    y = [[history[0]], [history[2]]]
    t = [tstart]

    control = [[0], [0], [0], [0]]  # psi, psi1, psi2, u

    for i in range(points):
        try:
            xi = get_ksi(m_threshold, x[3][-1])

            # x1_history = y[0][-1]
            # x3_history = y[1][-1]

            psi, psi1, psi2, u, disturbance1, disturbance2  = 0, 0, 0, 0, 0, 0

            if x[0][-1] < 1e-16:
                t_aim_reach = t[i]

            if control_params is not None:
                b = control_params['b']
                x1_aim = control_params['x1_aim']
                l1 = control_params['l1']
                l2 = control_params['l2']

                if disturbances is not None:
                    disturbance1 = disturbances[0][i]
                    disturbance2 = disturbances[1][i]
                    # mean = control_params['mean']
                    # std = control_params['std']
                    #
                    # disturbance1 = rand.normalvariate(mean, std)
                    # disturbance2 = rand.normalvariate(mean, std)

                psi, psi1, psi2, u = get_u(a, h, l1, l2, x1_aim, x)

                if u > b:
                    u = b
                elif u < 0:
                    u = 0

            control[0].append(psi)
            control[1].append(psi1)
            control[2].append(psi2)
            control[3].append(u)

            x[0].append(x1_next(a, h, x))
            x[1].append(x2_next(a, h, xi, x, y[0][-1], y[1][-1]))
            x[2].append(x3_next(a, h, u, x, disturbance1, disturbance2))
            x[3].append(x4_next(a, h, x))
            x[4].append(0)
            y[0].append(x[0][-1])
            y[1].append(x[2][-1])
            t.append(tstart + (i + 1) * h)

        except Exception as exp:
            print(exp.args[0])
            break

    return t, t_aim_reach, x, control
