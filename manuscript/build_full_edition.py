"""Assemble a clean reading edition from the preserved v0.1 chapter PDF and the editable v0.2 mathematical core.

Requires reportlab, pypdf, and Pillow. Re-run pdflatex twice on Information_Geometry_v0.2_integrated_part_II.tex
before running this script if you change the mathematical core.
"""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from pypdf import PdfReader, PdfWriter

base=Path(__file__).parent
repo=base.parent
original=base/'Information_Geometry_v0.1_original.pdf'
math=base/'Information_Geometry_v0.2_integrated_part_II.pdf'
out=repo/'book'/'Information_Geometry_for_the_Impatient_v0.2_COMPLETE.pdf'
front=base/'full_edition_frontmatter.pdf'
navy=HexColor('#0A315B'); blue=HexColor('#145788'); gold=HexColor('#CE9C33'); pale=HexColor('#E8F5F4'); muted=HexColor('#627381')
W,H=487.559,688.819
# Prefer the original typefaces when available; use standard PDF fonts elsewhere.
for name, path, fallback in [
    ('Lato','/usr/share/fonts/truetype/lato/Lato-Regular.ttf','Helvetica'),
    ('Lato-Bold','/usr/share/fonts/truetype/lato/Lato-Bold.ttf','Helvetica-Bold'),
    ('Lato-Italic','/usr/share/fonts/truetype/lato/Lato-Italic.ttf','Helvetica-Oblique'),
    ('Serif','/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf','Times-Roman'),
    ('Serif-Bold','/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf','Times-Bold'),
]:
    if Path(path).is_file():
        pdfmetrics.registerFont(TTFont(name,path))
    else:
        pdfmetrics.registerFont(pdfmetrics.Font(name,fallback,'WinAnsiEncoding'))

def heading(c,title,kicker=None):
    c.setFillColor(navy)
    if kicker:
        c.setFont('Lato-Bold',9);c.drawString(49,H-52,kicker.upper())
    c.setFont('Serif-Bold',20);c.drawString(49,H-91,title)
    c.setStrokeColor(gold);c.setLineWidth(1.8);c.line(49,H-105,W-49,H-105)

def wrap(c, txt, x,y,width,font='Lato',size=10.2,leading=16):
    c.setFont(font,size);c.setFillColor(HexColor('#263D51'))
    for para in txt.split('\n'):
        if para.strip()=='': y-=8;continue
        words=para.split(); line=''
        for word in words:
            trial=(line+' '+word).strip()
            if pdfmetrics.stringWidth(trial,font,size)>width and line:
                c.drawString(x,y,line);y-=leading;line=word
            else: line=trial
        if line: c.drawString(x,y,line);y-=leading
        y-=5
    return y

c=canvas.Canvas(str(front),pagesize=(W,H),pageCompression=1)
# Cover
c.setFillColor(navy);c.rect(0,H-17,W,17,stroke=0,fill=1)
c.setFillColor(navy);c.setFont('Lato-Bold',10.5);c.drawCentredString(W/2,H-65,'HIGHER MATH FOR THE IMPATIENT')
c.setFillColor(gold);c.rect(W/2-38,H-79,76,2,stroke=0,fill=1)
c.setFillColor(navy);c.setFont('Serif-Bold',36);c.drawCentredString(W/2,H-141,'INFORMATION')
c.drawCentredString(W/2,H-185,'GEOMETRY')
c.setFont('Serif',15);c.setFillColor(blue);c.drawCentredString(W/2,H-221,'When Probability Becomes Geometry')
# simplex visual
c.drawImage(ImageReader(str(base/'simplex_emblem.png')),95,193,width=W-190,height=248,preserveAspectRatio=True,mask='auto')
c.setStrokeColor(gold);c.setLineWidth(1);c.line(108,181,W-108,181)
c.setFont('Serif',15);c.setFillColor(navy);c.drawCentredString(W/2,153,'Mirco A. Mannucci')
c.setFont('Lato',10);c.setFillColor(muted);c.drawCentredString(W/2,132,'HoloMathics, LLC')
c.setFont('Lato-Bold',9);c.setFillColor(blue);c.drawCentredString(W/2,98,'INTEGRATED WORKING EDITION 0.2   •   NOVEMBER 2026')
c.setFont('Lato',8.5);c.setFillColor(muted);c.drawCentredString(W/2,75,'Proofs  •  Statistical invariance  •  Dual geometry  •  Geometric learning')
c.showPage()
# Preface; original author's Wager inserted by assembler after cover
heading(c,'About the integrated edition','Preface to edition 0.2')
y=H-137
for paragraph in [
    'The first part asks a question with a surprising answer: why should a family of probability laws possess a geometry at all? Gaussian distributions are hyperbolic; categorical laws are spherical after taking square roots; exponential families have two natural but distinct notions of straightness.',
    'The second part takes the claim of naturalness seriously. It asks what must remain invariant when statistical experiments are refined, relabelled, or degraded by a stochastic channel. The answer is not coordinate invariance alone. Across compatible finite simplexes, sufficient stochastic embeddings force the Fisher metric up to an overall scale.',
    'With this principle in place, information divergences generate a metric and dual affine connections; KL projections satisfy a precise Pythagorean identity; and natural-gradient learning becomes a geometric dynamical system. Proofs, careful hypotheses, counterexamples, and exercises form the spine of the exposition.',
    'This is an integrated reading edition rather than a typeset facsimile followed by an unrelated supplement. Chapters 1–5 preserve the original mathematical typesetting, while Chapters 6–11 come from editable LaTeX. The original source of Chapters 1–5 remains to be recovered or faithfully retyped before a completely source-unified edition can be claimed.',
    'The companion IG-Lab repository supplies symbolic calculations, numerical examples, and regression tests. These experiments illuminate the theorems; they do not replace their proofs.'
]:y=wrap(c,paragraph,49,y,W-98,leading=16.6)
c.setStrokeColor(gold);c.line(49,94,W-49,94)
c.setFont('Lato-Italic',9);c.setFillColor(muted);c.drawString(49,76,'Mirco A. Mannucci  |  HoloMathics, LLC  |  November 2026')
c.setFont('Serif',8);c.drawCentredString(W/2,36,'ii')
c.showPage()
# Contents
heading(c,'Contents','A single mathematical narrative')
chapters=[
('1','The Gaussian surprise: uncertainty is hyperbolic','1'),
('2','Why probability carries a metric','5'),
('3','Two straightnesses on one curved space','9'),
('4','Natural gradient: learning without coordinate illusions','13'),
('5','A mathematical laboratory: work it out','17'),
('6','Why Fisher geometry is forced','20'),
('7','Data processing is geometry','23'),
('8','A divergence creates more than a metric','25'),
('9','Projection, orthogonality and Pythagoras','27'),
('10','Learning as a geometric dynamical system','29'),
('11','Proof problems and computational checks','31'),
]
y=H-142
c.setFont('Lato-Bold',9);c.setFillColor(blue);c.drawString(49,y,'PART I — GEOMETRY THROUGH EXAMPLES');y-=20
for idx,(n,title,page) in enumerate(chapters):
    if idx==5:
        y-=17;c.setFont('Lato-Bold',9);c.setFillColor(blue);c.drawString(49,y,'PART II — GEOMETRY, INVARIANCE AND PROOFS');y-=24
    c.setFillColor(navy);c.setFont('Lato-Bold',11);c.drawString(52,y,n)
    c.setFont('Lato',10.2);c.drawString(81,y,title)
    c.setFillColor(blue);c.setFont('Lato-Bold',10);c.drawRightString(W-52,y,page)
    y-=31
c.setFont('Lato',10);c.setFillColor(muted);c.drawString(81,y-6,'Sources and further directions');c.drawRightString(W-52,y-6,'33')
c.setStrokeColor(gold);c.line(49,76,W-49,76)
c.setFont('Lato-Italic',9);c.setFillColor(muted);c.drawString(49,60,'Part I gives the examples; Part II derives the constraints that make them work.')
c.setFont('Serif',8);c.drawCentredString(W/2,36,'iii')
c.showPage()
c.save()

# Assemble: cover, original wager, new preface and TOC, original chapters1-5, new chapters6-11.
fr=PdfReader(str(front)); orig=PdfReader(str(original)); ext=PdfReader(str(math))
w=PdfWriter();w.add_page(fr.pages[0]);w.add_page(orig.pages[1]);w.add_page(fr.pages[1]);w.add_page(fr.pages[2]);
for page in orig.pages[5:24]:w.add_page(page)
for page in ext.pages:w.add_page(page)
w.add_metadata({'/Title':'Information Geometry for the Impatient — Complete Integrated Working Edition v0.2','/Author':'Mirco A. Mannucci','/Subject':'Fisher–Rao geometry, Cencov uniqueness, Markov contraction, dual connections, KL projection, natural gradient'})
# Global PDF page index: 0 cover,1 wager,2 preface,3 toc,4 chapter1,8 ch2,12 ch3,16 ch4,20 ch5,23 ch6,26 ch7,28 ch8,30 ch9,32 ch10,34 ch11,36 refs.
w.add_outline_item('The Wager',1)
w.add_outline_item('Preface to Edition 0.2',2)
w.add_outline_item('Contents',3)
for title,index in [
('1. Gaussian Surprise',4),('2. Why Probability Carries a Metric',8),('3. Two Straightnesses',12),('4. Natural Gradient',16),('5. Mathematical Laboratory',20),('6. Why Fisher Geometry is Forced',23),('7. Data Processing is Geometry',26),('8. Divergence and Dual Connections',28),('9. Projection and Pythagoras',30),('10. Geometric Learning',32),('11. Proof Problems and Computational Checks',34),('References and Scope',36)]:w.add_outline_item(title,index)
with out.open('wb') as fd:w.write(fd)
print('WROTE',out,'PAGES',len(w.pages),'BYTES',out.stat().st_size)
