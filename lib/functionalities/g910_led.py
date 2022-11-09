import subprocess

installed = None

def is_installed():
    global installed
    if installed is None:
        which_led_process = subprocess.run(['which', 'g910-led'], capture_output=True)
        if len(which_led_process.stdout) > 0:
            installed = True
        else:
            installed = False

    return installed