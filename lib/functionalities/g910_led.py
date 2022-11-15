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


def change_profile(profile: str):
    if is_installed():
        n = profile[1]
        if n == 'r':
            subprocess.run(['g910-led', '-mn', '0'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(['g910-led', '-mr', '1'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif n == '1' or n == '2':
            subprocess.run(['g910-led', '-mr', '0'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(['g910-led', '-mn', n], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.run(['g910-led', '-mr', '0'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(['g910-led', '-mn', '4'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
