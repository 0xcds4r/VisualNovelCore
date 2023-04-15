# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['Animation.py', 'Audio.py', 'DelayNotification.py', 'ButtonRender.py', 'FileManager.py', 'FontHelper.py', 'ImageRender.py', 'RenderData.py', 'SpritesRender.py', 'TextRender.py', 'Game.py', 'main.py', 'Events.py', 'Log.py', 'LuaWrapper.py', 'MenuSystem.py', 'RectWrapper.py', 'Render.py', 'Scenes.py', 'ScriptLoader.py', 'VNCore.py'],
    pathex=[],
    binaries=[],
    datas=[
    ('assets/arial.ttf', 'assets'), 
    ('assets/icon256.png', 'assets'), 
    ('assets/bg/*', 'assets/bg'), 
    ('assets/characters/*', 'assets/characters'), 
    ('assets/items/*', 'assets/items'), 
    ('assets/sound/*', 'assets/sound'), 
    ('data/*', 'data'),  
    ('scripts/main.lua', 'scripts'), 
    ('scripts/utils/*', 'scripts/utils')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VNCore_Game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VNCore_Game',
)
