from models.basic_model import f1, f2, f3, f4, f5


def x1_next(a, h, x):
    return x[0][-1] + h * f1(a, x[0][-1], x[2][-1])


def x2_next(a, h, xi, x, x1_history, x3_history):
    return x[1][-1] + h * f2(a, xi, x[1][-1], x1_history, x3_history)


def x3_next(a, h, u, x, disturbance1=None, disturbance2=None):
    if disturbance1 and disturbance2 is None:
        return x[2][-1] + h * (f3(a, x[0][-1], x[1][-1], x[2][-1]) + u)
    elif disturbance1 and disturbance2 is not None:
        return x[2][-1] + h * (f3(a, x[0][-1], x[1][-1], x[2][-1]) + u + disturbance1 + disturbance2)
    else:
        return x[2][-1] + h * (f3(a, x[0][-1], x[1][-1], x[2][-1]) + u + disturbance1)


def x4_next(a, h, x):
    return x[3][-1] + h * f4(a, x[0][-1], x[3][-1])


def x5_next(n, h, x1_aim, x):
    return x[4][-1] + h * f5(n, x1_aim, x[0][-1])