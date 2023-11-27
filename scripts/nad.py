import math


def get_ksi(m_threshold, x4):
    if x4 >= 1:
        raise Exception("Patient has died, calculations stopped")
    elif x4 < 0:
        raise Exception("x4 is out of bound, expected: >=0, actual: " + str(x4))

    return 1 if 0 <= x4 < m_threshold else (x4 - 1) / (m_threshold - 1)


def get_psi(x1, x1_aim):
    return x1 - x1_aim


def get_psi1(x3, fi):
    return x3 - fi


def get_psi2(k, psi, x5):
    return psi + k * x5


def get_fi(a, h, k, n, l2, x1_aim, x1, x5):
    return a[0] / a[1] + (get_psi(x1, x1_aim) * (1 + l2 + k * n * h) + k * x5 * (1 + l2)) / h / a[1] / x1


def f1(a, x1, x3):
    return (a[0] - a[1] * x3) * x1


def f2(a, ksi, x2, x1_history, x3_history):
    return a[2] * ksi * x1_history * x3_history - a[4] * (x2 - 1)


def f3(a, x1, x2, x3):
    return a[3] * (x2 - x3) - a[7] * x1 * x3


def f4(a, x1, x4):
    return a[5] * x1 - a[6] * x4


def f5(n, x1_aim, x1):
    return n * get_psi(x1, x1_aim)


def x1_next(a, h, x1, x3):
    return x1 + h * f1(a, x1, x3)


def x2_next(a, h, ksi, x2, x1_history, x3_history):
    return x2 + h * f2(a, ksi, x2, x1_history, x3_history)


def x3_next(a, h, x1, x2, x3, u, noise):
    return x3 + h * (f3(a, x1, x2, x3) + u + noise)


def x4_next(a, h, x1, x4):
    return x4 + h * f4(a, x1, x4)


def x5_next(n, h, x1_aim, x1, x5):
    return x5 + h * f5(n, x1_aim, x1)


def get_u(a, h, k, n, l1, l2, x1_aim, x1, x2, x3, x5):
    psi = get_psi(x1, x1_aim)
    psi2 = get_psi2(k, psi, x5)
    fi = get_fi(a, h, k, n, l2, x1_aim, x1, x5)
    psi1 = get_psi1(x3, fi)
    fi1 = get_fi(a, h, k, n, l2, x1_aim, x1_next(a, h, x1, x3), x5_next(n, h, x1_aim, x1, x5))
    return psi, psi1, psi2, h ** -1 * (fi1 - l1 * psi1 - x3) - f3(a, x1, x2, x3) - x5


def run(time, m_threshold, a, history, control, u_params):
    t_aim_reach = -1
    t0 = time[0]
    tn = time[1]
    h = time[2]

    t = [t0]
    u_nad = [0]
    x = [[history[0]], [history[1]], [history[2]], [history[3]], [history[4]]]
    y = [[history[0]], [history[2]]]
    psi = [0]
    psi1 = [0]
    psi2 = [0]

    for i in range(int((tn - t0) / h)):
        try:
            x1 = x[0][i]
            x2 = x[1][i]
            x3 = x[2][i]
            x4 = x[3][i]
            x5 = x[4][i]

            ksi = get_ksi(m_threshold, x4)

            if x1 < 1e-16:
                t_aim_reach = t[i]

            x1_history = y[0][i]
            x3_history = y[1][i]

            if control == 0:
                x1_aim, n, p, p1, p2, u, disturbance = 0, 0, 0, 0, 0, 0, 0

            else:
                x1_aim = u_params['x1_aim']
                b = u_params['b']
                k = u_params['k']
                n = u_params['n']
                l1 = u_params['l1']
                l2 = u_params['l2']
                # disturbance = u_params['disturbance']
                # disturbance = u_params['disturbance']
                disturbance = math.sin(math.pi * t[-1] / 2)

                p, p1, p2, u = get_u(a, h, k, n, l1, l2, x1_aim, x1, x2, x3, x5)

                if b != -1:
                    if u > b:
                        u = b
                    elif u < 0:
                        u = 0

                    # if t_aim_reach != -1:
                    #     u = 0

                # print(u)

            u_nad.append(u)
            psi.append(p)
            psi1.append(p1)
            psi2.append(p2)

            # if t_aim_reach != -1:
            #     x[0].append(x1_aim)
            # else:
            x[0].append(x1_next(a, h, x1, x3))
            x[1].append(x2_next(a, h, ksi, x2, x1_history, x3_history))
            x[2].append(x3_next(a, h, x1, x2, x3, u, disturbance))
            x[3].append(x4_next(a, h, x1, x4))
            x[4].append(x5_next(n, h, x1_aim, x1, x5))
            y[0].append(x1)
            y[1].append(x3)
            t.append(t0 + (i + 1) * h)

        except Exception as exp:
            print(exp.args[0])
            break

    return t, t_aim_reach, x, u_nad, psi, psi1, psi2
