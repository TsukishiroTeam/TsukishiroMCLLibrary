class WindowsRuntimeException(Exception):
    def __init__(self, message: str, hresult:int):
        super.__init__()
        self.hresult = hresult