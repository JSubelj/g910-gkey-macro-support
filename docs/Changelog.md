# Current:
**RELEASE-0.2.5:**
  - Four profiles (Mkeys to switch profiles, up to 28 GKey bindings)
  - New hotkey_type python (execute simple one-line python code on a Gkey press)
  - New argument -c PATH or --set-config PATH to load a different config on startup
  - Remove uinput device on exit consequently (reworked exit strategy)
  - Detecting JSONDecodeError helps on syntax problems in config.json with better error messages
  - Added uninstall script and improved install script
  - Keyboard layouts:
    - Fixed 'w' char in fr
    - Added '?' character in en

# Older:

**RELEASE-0.2.4:**
  - Changed logger levet to INFO
  - g910-gkeys.service is now platform independant (no more /usr/local/bin vs /usr/bin)
  - Updated Troubleshooting wiki
  - Bugfix:
    - Changed 'is' keyword with '==' with string literals

**RELEASE-0.2.3:**
  - Updated readme and wiki
  - When running now prints PID
  - Bugfix:
    - Fixed a bug causing the driver not shutting down

**RELEASE-0.2.2:**
  - Versioning fix
  - Added -v and --version flags to display version
  - Flags -v, --version and --help can now be executed as normal user
  - Project is now consistently named g910-gkeys (GitHub repo name stays the same)

**RELEASE-0.2.1:**
  - Hotfix: The driver could not find the keyboard on boot.

**RELEASE-0.2.0:**
  - New features: 
    - GKeys can now be used as modifiers
    - Disabling the GKey to FKey mapping is now done in the driver (g810-leds controller is no longer needed)
    - G910 Spark is now supported without any modification
    - New types of keys supported
  - Bugfixes:
    - Minor bugfixes