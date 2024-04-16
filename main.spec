# -*- mode: python ; coding: utf-8 -*-
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--one", action="store_true")
options = parser.parse_args()

a = Analysis(
    ['main.py', 'launcher.py', 'masterController.py'],
    pathex=[],
    binaries=[],
    datas=[('./dwrg.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure, a.zipped_data)

if options.one:
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        icon='D:\\Workspace\\CodeSpace\\idv-Tproxy\\dwrg.ico',
        name='idv登录助手',
        debug=False,
        exclude_binaries=False,
        bootloader_ignore_signals=False,
        strip=True,
        upx=True,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        uac_admin=True,
    )
else:
    exe = EXE(
        pyz,
        a.scripts,
        [],
        icon='D:\\Workspace\\CodeSpace\\idv-Tproxy\\dwrg.ico',
        exclude_binaries=True,
        name='idv登录助手',
        debug=False,
        bootloader_ignore_signals=False,
        strip=True,
        upx=True,
        console=False,
        disable_windowed_traceback=False,
        argv_emulation=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        uac_admin=True,
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=True,
        upx=True,
        upx_exclude=[],
        name='idv_helper',
    )
