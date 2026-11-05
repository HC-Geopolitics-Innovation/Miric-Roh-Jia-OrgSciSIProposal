#!/usr/bin/env python3
"""
compile_latex.py
----------------
Compiles LaTeX documents into PDFs and immediately cleans up all intermediate
files (*.aux, *.log, *.out, *.toc, *.nav, *.snm, *.vrb, missfont.log, etc.).
"""
import glob
import os
import subprocess
import sys
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if os.path.basename(BASE_DIR).startswith("P1.2"):
    P_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
elif BASE_DIR.endswith("P - Paper, Writing and Output"):
    P_DIR = BASE_DIR
else:
    P_DIR = os.path.join(BASE_DIR, "P - Paper, Writing and Output")

P11_DIR = os.path.join(P_DIR, "P1.1 - PDFs for Submission")

def cleanup_intermediates(directory):
    for ext in ("*.aux", "*.log", "*.out", "*.toc", "*.nav", "*.snm", "*.vrb", "missfont.log"):
        for f in glob.glob(os.path.join(directory, ext)):
            try:
                os.remove(f)
            except OSError:
                pass

def compile_doc(tex_path, target_dir=None):
    tex_dir = os.path.dirname(os.path.abspath(tex_path))
    tex_name = os.path.basename(tex_path)
    print(f"Compiling {tex_name} in {tex_dir}...")
    for pass_num in (1, 2):
        cmd = ["/Library/TeX/texbin/pdflatex", "-interaction=nonstopmode", tex_name]
        res = subprocess.run(cmd, cwd=tex_dir, capture_output=True, text=True)
        if res.returncode != 0 and pass_num == 2:
            print(f"LaTeX Warning/Error on {tex_name}:\n{res.stdout[-600:]}", file=sys.stderr)

    cleanup_intermediates(tex_dir)
    pdf_name = tex_name.replace(".tex", ".pdf")
    pdf_path = os.path.join(tex_dir, pdf_name)
    if os.path.exists(pdf_path):
        print(f"Successfully generated {pdf_name} and cleaned up intermediate files.")
        if target_dir and os.path.abspath(tex_dir) != os.path.abspath(target_dir):
            shutil.copy2(pdf_path, os.path.join(target_dir, pdf_name))
            print(f"Copied {pdf_name} to {target_dir}")

def compile_all():
    # 1. Merged proposals in main P folder
    for doc in ["P2. Org Sci Proposal [Miric, Roh and Jia][PDF].tex", "P2. Org Sci Proposal [Anonymized][PDF].tex"]:
        p2_tex = os.path.join(P_DIR, doc)
        if os.path.exists(p2_tex):
            compile_doc(p2_tex)
    
    # Also provide [Annonymized] duplicate for safety
    anon_p2 = os.path.join(P_DIR, "P2. Org Sci Proposal [Anonymized][PDF].pdf")
    if os.path.exists(anon_p2):
        shutil.copy2(anon_p2, os.path.join(P_DIR, "P2. Org Sci Proposal [Annonymized][PDF].pdf"))
    
    # 2. Individual main and appendix files in P1.1 (separate files for submission)
    for doc in ["main.tex", "appendix.tex", "main [Anonymized].tex", "appendix [Anonymized].tex"]:
        doc_path = os.path.join(P11_DIR, doc)
        if os.path.exists(doc_path):
            compile_doc(doc_path)
            
    # Also provide [Annonymized] duplicates in P1.1
    for name in ["main", "appendix"]:
        src = os.path.join(P11_DIR, f"{name} [Anonymized].pdf")
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(P11_DIR, f"{name} [Annonymized].pdf"))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            compile_doc(arg)
    else:
        compile_all()
