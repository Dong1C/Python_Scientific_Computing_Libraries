class A:
    def __init__(self, name, timeout=100):
        self.timeout = timeout
        self.name = name

    def __str__(self) -> str:
        return f"{{name: {self.name}, timeout: {self.timeout}}}"

    def __repr__(self) -> str:
        return f"{{name: {self.name}, timeout: {self.timeout}}}"