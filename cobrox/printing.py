from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, LongTable, TableStyle, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER,TA_RIGHT, TA_LEFT,TA_JUSTIFY
from reportlab.graphics.shapes import Drawing,Line
from reportlab.lib.units import inch,cm
from reportlab.lib import utils
from django.conf import settings
from .models import archivos_consulta_medica
from functools import partial
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import re
from urllib.request import urlopen
from io import BytesIO
from django.core.files import File


class MyPrint:

    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

    @staticmethod
    def _header_footer(canvas, doc,name_file_f,name_file,name_file_w):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()

        # Header
        if name_file is not None and name_file!='':
            img_url = settings.MEDIA_URL + name_file
            try:
                header = Image(img_url, width=500,height=90, hAlign='CENTER')
            except:
                header = Paragraph(Paragraph(" ", styles['BodyText']))
        #header = Paragraph('This is a multi-line header.  It goes on every page.   ' * 5, styles['Normal'])
        w, h = header.wrap(doc.width, doc.topMargin-100)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h+60)

        if name_file_w is not None and name_file_w!='':
            img_url = settings.MEDIA_URL + name_file_w
            try:
                canvas.drawImage(img_url,20,170,mask="auto")
            except:
                pass

        # Footer
        if name_file_f is not None and name_file_f!='':
            img_url = settings.MEDIA_URL + name_file_f
            try:
                footer = Image(img_url, width=500,height=90, hAlign='CENTER')
            except:
                footer = Paragraph(Paragraph(" ", styles['BodyText']))
        #footer = Paragraph('This is a multi-line footer.  It goes on every page.   ' * 5, styles['Normal'])
            w, h = footer.wrap(doc.width, doc.bottomMargin+100)
            footer.drawOn(canvas, doc.leftMargin, h-100)

        # Release the canvas
        canvas.restoreState()

    @staticmethod
    def get_image(path, width=1*cm):
        img = utils.ImageReader(path)
        iw,ih = img.getSize()
        aspect = ih / float(iw)
        return Image(path,width=width,height =(width*aspect),hAlign='CENTER')

    def print_cuadro(self, parrafo,name_file,name_file_f, consulta):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
                                rightMargin=72,
                                leftMargin=72,
                                topMargin=72,
                                bottomMargin=72,
                                pagesize=self.pagesize)

        # Our container for 'Flowable' objects
        elements = []

        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        d = Drawing(100, 1)

        if name_file is not None and name_file!='':
            img_url = settings.MEDIA_URL + name_file
            try:
                imagen = Image(img_url, width=500,height=90, hAlign='CENTER')
            except:
                imagen = Paragraph(Paragraph(" ", styles['BodyText']))
            elements.append(imagen)
        d.add(Line(0, 0, 460, 0))
        elements.append(d)

        for p in parrafo.split('**'):
            elements.append(Paragraph(p, styles['BodyText']))
            if p.find('textcolor') != -1:
                data = [['UT L:', str(consulta.consulta_ginecologica_ultra.ut_l)+' cm', ' ', 'UT W:', str(consulta.consulta_ginecologica_ultra.ut_w)+' cm'],
                        ['UT H:', str(consulta.consulta_ginecologica_ultra.ut_h)+' cm', ' ', 'Endo:', str(consulta.consulta_ginecologica_ultra.endo)+' mm'],
                        ['UT Vol:', str(consulta.consulta_ginecologica_ultra.ut_vol)+' cm3', ' ', 'Cuerpo Utero:', str(consulta.consulta_ginecologica_ultra.cuerpo_utero)+' cm'],
                        ['Ovario Derecho', ' ',' ', 'Ovario Izquierdo', ' '],
                        ['L Ovario:',str(consulta.consulta_ginecologica_ultra.r_ovario_l)+' cm', ' ', 'L Ovario:', str(consulta.consulta_ginecologica_ultra.l_ovario_l)+' cm'],
                        ['H Ovario:', str(consulta.consulta_ginecologica_ultra.r_ovario_h)+' cm', ' ', 'H Ovario:', str(consulta.consulta_ginecologica_ultra.l_ovario_h)+' cm'],
                        [str(consulta.consulta_ginecologica_ultra.r_ovario_desc),' ' , ' ', str(consulta.consulta_ginecologica_ultra.l_ovario_desc), ' ']]
                t = Table(data,5*[1*inch], 7*[.4*inch])
                elements.append(t)




        d = Drawing(200, 1)
        d.add(Line(0, 0, 460, 0))
        elements.append(d)
        if name_file_f is not None and name_file_f!='':
            img_url = settings.MEDIA_URL + name_file_f
            try:
                imagen = Image(img_url, width=500,height=90, hAlign='CENTER')
            except:
                imagen = Paragraph(Paragraph(" ", styles['BodyText']))
            elements.append(imagen)
        doc.build(elements)
        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(125 * mm, 0 * mm + (0.2 * inch),
                             "Página %d de %d" % (self._pageNumber, page_count))
