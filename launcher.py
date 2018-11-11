from lib import g910_gkey_mapper

DEVEL_WO_KEYBOARD = False
if __name__=="__main__":
    if DEVEL_WO_KEYBOARD:
        from lib import develop_wo_keyboard
        develop_wo_keyboard.main()
    else:
        g910_gkey_mapper.main()
