import ctypes

class NVMLError(Exception): pass

def load_nvml(libpath):
    return ctypes.cdll.LoadLibrary(libpath)

def check_error(code):
    if code != 0:
        raise NVMLError(f'NVML error code {code}')

def initialise(libnvml):
    check_error(libnvml.nvmlInit_v2())

def shutdown(libnvml):
    check_error(libnvml.nvmlShutdown())

def get_device_handle_by_index(libnvml, index):
    device = ctypes.c_void_p(0)
    pdev = ctypes.pointer(device)

    check_error(libnvml.nvmlDeviceGetHandleByIndex_v2(index, pdev))

    return device.value

def set_device_clock_offset(libnvml, handle, offset):
    check_error(libnvml.nvmlDeviceSetGpcClkVfOffset(ctypes.c_void_p(handle), ctypes.c_int(offset)))