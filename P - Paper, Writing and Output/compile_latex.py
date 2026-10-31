#!/usr/bin/env python3
"""
compile_latex.py
----------------
Compiles main.tex and appendix.tex into main.pdf and appendix.pdf using pdflatex,
and automatically deletes all intermediate files (*.aux, *.log, *.out, missfont.log)
after every compilation run.
"""
import glob
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def cleanup_intermediates():
    for ext in ("*.aux", "*.log", "*.out", "*.toc", "*.nav", "*.snm", "*.vrb", "missfont.log"):
        for f in glob.glob(os.path.join(BASE_DIR, ext)):
            try:
                os.remove(f)
            except OSError:
                pass

def compile_doc(tex_filename):
    print(f"Compiling {tex_filename}...")
    for pass_num in (1, 2):
        cmd = ["/Library/TeX/texbin/pdflatex", "-interaction=nonstopmode", tex_filename]
        res = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
        if res.returncode != 0 and pass_num == 2:
            print(f"LaTeX Warning/Error on {tex_filename}:\n{res.stdout[-400:]}", file=sys.stderr)

    cleanup_intermediates()
    pdf_name = tex_filename.replace(".tex", ".pdf")
    print(f"Successfully created {pdf_name} and cleaned up all intermediate files.")

if __name__ == "__main__":
    compile_doc("main.tex")
    compile_doc("appendix.tex")
