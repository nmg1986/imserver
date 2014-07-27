from distutils.core import setup

import py2exe


setup(
    options = {
        'py2exe':{
            'includes':['zope', 'zope.interface', 'zope.interface.adapter','twisted.web.resource'],
            'dll_excludes':['OLEAUT32.dll','USER32.dll','SHELL32.dll','ole32.dll',
                            'COMDLG32.dll','COMCTL32.dll','ADVAPI32.dll','NETAPI32.dll',
                            'msvcrt.dll','WS2_32.dll','GDI32.dll','VERSION.dll','KERNEL32.dll',
                            'ntdll.dll','RPCRT4.dll','mswsock.dll', 'powrprof.dll'],
            'bundle_files': 1,
            "compressed": 1,
            }
        },
    zipfile=None,
    data_files=['hbimserver.ini'],
    windows = ["hbimserver.py"],
    service = ["winserver"],
)


