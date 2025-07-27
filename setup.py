from cx_Freeze import setup, Executable
import os
import sys

include_files = [
    ('resource', 'resource'),
    ('icon.png', 'icon.png'),
    ('.venv/Lib/site-packages/pymupdf/_mupdf.pyd', 'pymupdf/_mupdf.pyd'),
    ('.venv/Lib/site-packages/pymupdf/mupdf.py', 'pymupdf/mupdf.py')
]

base = None
if sys.platform == "win32":
    base = "Console"  # Use "Win32GUI" for Tkinter/PyQt GUI apps

executables = [
    Executable(
        script='main.py',
        base=base,
        target_name='pdfwordsearch.exe',
        icon='icon.png'  # Optional
    )
]

setup(
    name="PDFWordSearch",
    version="1.0",
    description="A PDF word search tool using NLTK",
    options={
        "build_exe": {
            "packages": ["nltk", "fitz", "tkinter"],
            "include_files": include_files,
            "zip_include_packages": ["*"],      # ensure it bundles installed packages
            "zip_exclude_packages": ["ttkbootstrap"],  # <-- force ttkbootstrap to load dynamically
        }
    },
    executables=executables
)