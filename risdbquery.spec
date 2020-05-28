# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['risdbquery.py'],
             pathex=['C:\\Users\\1879\\PycharmProjects\\risdbquery'],
             binaries=[],
             datas=[('../python-ucmapi/build/lib/ucmapi', 'ucmapi')],
             hiddenimports=['pkg_resources.py2_warn', 'uuid', 'requests', 'six', 'zeep', 'attr', 'pkg_resources'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='risdbquery',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
