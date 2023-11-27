def get_psi(x1_aim, x1):
    return x1 - x1_aim


def get_psi1(fi, x3):
    return x3 - fi


def get_psi2(k, x1_aim, x1, x5):
    return get_psi(x1_aim, x1) + k * x5
