import sys
from cx_Freeze import setup, Executable

# Files to include
includefiles = [
    'icon.ico', 'bg.png', 'button.png', 'church logo.png', 'church_logo.ico',
    'hide_icon.png', 'log.png', 'login.png', 'loginbg.png', 'pass.png',
    'show_icon.png', 'user.png'
]

excludes = []  # modules to exclude
packages = []  # modules to include manually
base = None

# Main scripts
TARGET = 'login.py'  #

# If running on Windows, use GUI base (no terminal window)
if sys.platform == 'win32':
    base = 'Win32GUI'

# Create a shortcut for the desktop (this is for MSI installer)
shortcut_table = [
    ('DesktopShortcut', 'DesktopFolder', 'login', 'TARGETDIR', '[TARGETDIR]\\login.exe',
     None, None, None, None, None, None, 'TARGETDIR')
]

# Data for MSI installer
msi_data = {'Shortcut': shortcut_table}

# MSI build options
bdist_msi_options = {'data': msi_data}

# Setup cx_Freeze
setup(
    version='1.5.0',
    name='Welfare App',
    description='Vbci Welfare App',
    author='Kwabena Yeboah Isaac',
    Company_name='Deep Sight Engineering',
    license='MIT',
    options={
        'build_exe': {
            'packages': packages,
            'include_files': includefiles,
            'excludes': excludes
        },
        'bdist_msi': bdist_msi_options,
    },
    executables=[
        Executable(script="Login.py", base=base, icon="icon.ico"),   # 👈 OK
        Executable(script="App.py", base=base, icon="icon.ico")       # 👈 OK, but a caution
    ]
)
