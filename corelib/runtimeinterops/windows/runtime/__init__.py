from ctypes import Structure, wintypes, POINTER, byref, c_void_p, c_uint32, CFUNCTYPE, WinDLL, c_wchar_p
from ..com import IUnknownVtbl
from errors import WindowsRuntimeException

class IInspectableVtbl(IUnknownVtbl):
    _fields_ = [
        ("GetIids", CFUNCTYPE(wintypes.HRESULT, c_void_p, POINTER(wintypes.ULONG), POINTER(POINTER(c_void_p)))),
        ("GetRuntimeClassName", CFUNCTYPE(wintypes.HRESULT, c_void_p, POINTER(wintypes.ULONG), POINTER(c_void_p))),
        ("GetTrustLevel", CFUNCTYPE(wintypes.HRESULT, c_void_p, POINTER(c_uint32)))
    ]

class IInspectable(Structure):
    _fields_ = [
        ("lpVtbl", POINTER(IInspectableVtbl))
    ]

WINRT_DLL = WinDLL("api-ms-win-core-winrt-l1-1-0.dll")
COM_BASE = WinDLL("combase.dll")

HSTRING = c_void_p



COM_BASE.WindowsCreateString.argtypes = [
    c_wchar_p,
    wintypes.UINT,
    POINTER(HSTRING)
]

COM_BASE.WindowsCreateString.restype = wintypes.HRESULT

COM_BASE.WindowsDeleteString.argtypes = [
    HSTRING
]

COM_BASE.WindowsDeleteString.restype = wintypes.HRESULT

WINRT_DLL.RoGetActivationFactory.argtypes = [
    HSTRING,
    POINTER(c_void_p),
    POINTER(c_void_p)
]

WINRT_DLL.RoGetActivationFactory.restype = wintypes.HRESULT

def create_hstring(s: str) -> HSTRING:
    hstr = HSTRING()
    result = COM_BASE.WindowsCreateString(s, len(s), byref(hstr))
    if result != 0:
        raise WindowsRuntimeException(f"Call WindowsCreateString failed，HRESULT: {result}", result)
    return hstr
    
def delete_hstring(str: HSTRING):
    result = COM_BASE.WindowsDeleteString(str)
    if result != 0:
        raise WindowsRuntimeException(f"Call WindowsDeleteString failed, HRESULT: {result}", result)
    
