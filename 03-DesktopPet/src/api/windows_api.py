"""
Windows API 封装
获取窗口位置、任务栏位置等信息
需要: pip install pywin32
"""
import win32gui
import win32con
import win32api


def get_target_window():
    """
    获取当前最顶层的普通窗口（排除全屏、桌面、任务栏）
    返回 (hwnd, left, top, right, bottom) 或 None
    """
    result = []

    def callback(hwnd, _):
        # 只处理可见窗口
        if not win32gui.IsWindowVisible(hwnd):
            return
        # 排除没有标题的窗口
        if not win32gui.GetWindowText(hwnd):
            return

        style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
        # 必须有标题栏
        if not (style & win32con.WS_CAPTION):
            return

        rect = win32gui.GetWindowRect(hwnd)
        left, top, right, bottom = rect
        w = right - left
        h = bottom - top

        # 排除过小的窗口
        if w < 100 or h < 100:
            return

        # 排除全屏窗口
        sw = win32api.GetSystemMetrics(0)
        sh = win32api.GetSystemMetrics(1)
        if w >= sw and h >= sh:
            return

        result.append((hwnd, left, top, right, bottom))

    win32gui.EnumWindows(callback, None)

    # EnumWindows 返回的第一个就是 Z 序最顶层
    if result:
        return result[0]
    return None


def get_taskbar_rect():
    """
    获取任务栏的位置
    返回 (left, top, right, bottom) 或 None
    """
    hwnd = win32gui.FindWindow("Shell_TrayWnd", None)
    if hwnd:
        return win32gui.GetWindowRect(hwnd)
    return None


def get_screen_size():
    """返回 (width, height)"""
    w = win32api.GetSystemMetrics(0)
    h = win32api.GetSystemMetrics(1)
    return w, h