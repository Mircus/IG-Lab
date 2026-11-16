"""Combine facsimile v0.1 and editable v0.2 research extension as a PDF.
Requires: pypdf; run from repository root: python book/build_compilation.py.
"""
from pathlib import Path
from pypdf import PdfReader,PdfWriter
HERE=Path(__file__).resolve().parent
parts=[HERE/'research_compilation_cover.pdf',HERE/'Information_Geometry_v0.1_original.pdf',HERE/'Information_Geometry_v0.2_mathematical_extension.pdf']
out=HERE/'Information_Geometry_for_the_Impatient_v0.2_RESEARCH.pdf'
writer=PdfWriter();total=0
for path in parts:
    r=PdfReader(path)
    writer.append(r)
    print(path.name,len(r.pages))
writer.add_outline_item('Edition note / cover',0)
writer.add_outline_item('Part I — original v0.1 foundation',1)
writer.add_outline_item('Part II — mathematical core v0.2',28)
writer.add_metadata({'/Title':'Information Geometry for the Impatient — v0.2 research compilation',
                     '/Author':'Mirco A. Mannucci','/Subject':'Fisher–Rao, Chentsov uniqueness, information projections, geometric learning'})
with out.open('wb') as f:writer.write(f)
print('Wrote',out,'with',len(writer.pages),'pages')
