import random as rand


def get_ksi(m_threshold, x4):
    if x4 >= 1:
        raise Exception("patient has died, calculations stopped")
    elif x4 < 0:
        raise Exception("x4 is out of bound, expected: >=0, actual: " + str(x4))

    return 1 if 0 <= x4 < m_threshold else (x4 - 1) / (m_threshold - 1)


def get_psi(x1, x1_aim):
    return x1 - x1_aim


def get_fi(a, h, l2, x1_aim, x1):
    return a[0] / a[1] + (h * a[1] * x1) ** -1 * (1 + l2) * (get_psi(x1, x1_aim))


def get_psi1(x3, fi):
    return x3 - fi


def f1(a, x1, x3):
    return (a[0] - a[1] * x3) * x1


def f2(a, ksi, x2, x1_history, x3_history):
    return a[2] * ksi * x1_history * x3_history - a[4] * (x2 - 1)


def f3(a, x1, x2, x3):
    return a[3] * (x2 - x3) - a[7] * x1 * x3


def f4(a, x1, x4):
    return a[5] * x1 - a[6] * x4


def x1_next(a, h, x1, x3):
    return x1 + h * f1(a, x1, x3)


def x2_next(a, h, ksi, x2, x1_history, x3_history):
    return x2 + h * f2(a, ksi, x2, x1_history, x3_history)


def x3_next(a, h, u, disturbance1, disturbance2, x1, x2, x3):
    return x3 + h * (f3(a, x1, x2, x3) + u + disturbance1 + disturbance2)


def x4_next(a, h, x1, x4):
    return x4 + h * f4(a, x1, x4)


def get_u(a, h, x1_aim, l1, l2, c, x1, x2, x3, x1_prev, x3_prev):
    psi = get_psi(x1, x1_aim)
    fi = get_fi(a, h, l2, x1_aim, x1)
    psi1 = get_psi1(x3, fi)
    fi1 = get_fi(a, h, l2, x1_aim, x1_next(a, h, x1, x3))
    u = h ** -1 * (fi1 - l1 * psi1 - x3) - f3(a, x1, x2, x3) - c * h ** -1 * (
                psi1 + l1 * get_psi1(x3_prev, get_fi(a, h, l2, x1_aim, x1_prev)))
    return psi, psi1, u


def run(time, model_params, control_params=None):
    t_aim_reach = -1
    t0 = time[0]
    tn = time[1]
    h = time[2]

    a = model_params['a']
    history = model_params['history']
    m_threshold = model_params['m_threshold']
    
    t = [t0]
    u_nas = [0]
    x = [[history[0]], [history[1]], [history[2]], [history[3]], [0]]
    y = [[history[0]], [history[2]]]
    psi = [0]
    psi1 = [0]
    psi2 = [0]
    disturbances = [[0], [0]]

    for i in range(int((tn - t0) / h)):
        try:
            x1 = x[0][i]
            x2 = x[1][i]
            x3 = x[2][i]
            x4 = x[3][i]

            if x1 < 1e-16:
                t_aim_reach = t[i]

            ksi = get_ksi(m_threshold, x4)

            x1_history = y[0][i]
            x3_history = y[1][i]

            x1_aim, c, p, p1, p2, u, disturbance1, disturbance2 = 0, 0, 0, 0, 0, 0, 0, 0

            if control_params is not None:
                x1_aim = control_params['x1_aim']
                b = control_params['b']
                c = control_params['c']
                l1 = control_params['l1']
                l2 = control_params['l2']
                mean = control_params['mean']
                std = control_params['std']

                p, p1, u = get_u(a, h, x1_aim, l1, l2, c, x1, x2, x3, x1_history, x3_history)

                disturbance1 = rand.normalvariate(mean, std)
                disturbance2 = rand.normalvariate(mean, std)

                disturbances[0].append(disturbance1)
                disturbances[1].append(disturbance2)

                if b != -1:
                    if u > b:
                        u = b
                    elif u < 0:
                        u = 0

                    # if t_aim_reach != -1:
                    #     u = 0

            psi.append(p)
            psi1.append(p1)
            psi2.append(0)
            u_nas.append(u)

            x[0].append(x1_next(a, h, x1, x3))
            x[1].append(x2_next(a, h, ksi, x2, x1_history, x3_history))
            x[2].append(x3_next(a, h, u, disturbance1, disturbance2, x1, x2, x3))
            x[3].append(x4_next(a, h, x1, x4))
            x[4].append(0)
            y[0].append(x1)
            y[1].append(x3)
            t.append(t0 + (i + 1) * h)

        except Exception as exp:
            print(exp.args[0])
            break

    return t, t_aim_reach, x, [psi, psi1, psi2, u_nas], disturbances

# субклиническая
# c = 0.1 - 1, l1 = -0.9, l2 = -0.9, один запуск было
# c = 0.1 - 1, l1 = -0.5, l2 = -0.9, один запуск было
# острая
# c = 0.1 - 1, l1 = -0.9, l2 = -0.9
# хроническая
# c = 0.1 - 1, l1 = -0.9, l2 = -0.9
# летальная
