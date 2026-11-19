from ctypes import windll, Structure, wintypes, POINTER, byref, c_void_p, c_uint32, c_wchar_p, CFUNCTYPE

class IUnknownVtbl(Structure):
    _fields_ = [
        ("QueryInterface", CFUNCTYPE(wintypes.HRESULT, c_void_p, POINTER(c_void_p), POINTER(c_void_p))),
        ("AddRef", CFUNCTYPE(wintypes.ULONG, c_void_p))
        ("Release", CFUNCTYPE(wintypes.ULONG, c_void_p))
    ]

class IUnknown(Structure):
    _fields_ = [
        ("lpVtbl", POINTER(IUnknownVtbl))
    ]
