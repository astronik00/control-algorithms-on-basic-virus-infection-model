from utils.adar_common_func import get_psi


def get_ksi(m_threshold, x4):
    if x4 >= 1:
        raise Exception("patient has died, calculations stopped")
    elif x4 < 0:
        raise Exception("x4 is out of bound, expected: >=0, actual: " + str(x4))

    return 1 if 0 <= x4 < m_threshold else (x4 - 1) / (m_threshold - 1)


def f1(a, x1, x3):
    return (a[0] - a[1] * x3) * x1


def f2(a, ksi, x2, x1_history, x3_history):
    return a[2] * ksi * x1_history * x3_history - a[4] * (x2 - 1)


def f3(a, x1, x2, x3):
    return a[3] * (x2 - x3) - a[7] * x1 * x3


def f4(a, x1, x4):
    return a[5] * x1 - a[6] * x4


def f5(n, x1_aim, x1):
    return n * get_psi(x1_aim, x1)
