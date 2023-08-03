import ctypes as ct

import sv_ttk


def setdark(root):
    """
    MORE INFO:
    https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmrootattribute
    """
    root.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_root_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(root.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_root_attribute(hwnd, rendering_policy, ct.byref(value),
                         ct.sizeof(value))

    sv_ttk.set_theme('dark')
