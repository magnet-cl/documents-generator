""" Pandoc operations handler. """

from sh import pandoc


def md_to_latex(md_file='.tmp.md', latex_file='.tmp.tex'):
    """ Converts from Markdown to LaTeX. """
    pandoc(md_file, '-o', latex_file)


def latex_to_pdf(latex_file='.tmp.tex', pdf_file='output.pdf'):
    """ Converts from LaTeX to PDF. """
    pandoc(latex_file, '-o', pdf_file)


def md_to_pdf(md_file='.tmp.md', pdf_file='output.pdf'):
    """ Converts from Markdown to PDF. """
    pandoc(md_file, '-o', pdf_file)


def md_to_pdf_with_template(md_file, pdf_file, template):
    """ Converts from Markdown to PDF using a template. """
    pandoc(md_file, '-o', pdf_file, '--template={}'.format(template))
