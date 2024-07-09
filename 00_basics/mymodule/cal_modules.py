from .main_class import A


def A_add(a: A, b: A) -> A:
    return A(f"{a.name} + {b.name}", a.timeout + b.timeout)


def A_sub(a: A, b: A) -> A:
    return A(f"{a.name} - {b.name}", a.timeout - b.timeout)
