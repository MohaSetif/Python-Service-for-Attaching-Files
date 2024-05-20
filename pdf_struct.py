import os
import PyPDF2
from PyPDF2.generic import DictionaryObject, DecodedStreamObject, NameObject

def resolve_indirect(obj):
    """ Helper function to resolve indirect objects in PyPDF2. """
    while isinstance(obj, PyPDF2.generic.IndirectObject):
        obj = obj.get_object()
    return obj

def attach_files_to_pdf(input_pdf, output_pdf, files):
    """
    Attaches files to a PDF.

    Args:
        input_pdf (str): Path to the input PDF file.
        output_pdf (str): Path to the output PDF file with attachments.
        files (list): List of file paths to be attached.

    Returns:
        None
    """
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(len(reader.pages)):
            pdf_writer.add_page(reader.pages[page_num])

        for file_path in files:
            with open(file_path, 'rb') as attachment:
                pdf_writer.add_attachment(os.path.basename(file_path), attachment.read())

        with open(output_pdf, 'wb') as file:
            pdf_writer.write(file)

def extract_attachments_from_pdf(input_pdf, output_dir):
    """
    Extracts attachments from a PDF and saves them to a directory.

    Args:
        input_pdf (str): Path to the input PDF file.
        output_dir (str): Path to the output directory for extracted files.

    Returns:
        None
    """
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        print("Document Trailer:")
        print(reader.trailer)
        
        root = resolve_indirect(reader.trailer['/Root'])
        print("Root Object:")
        print(root)
        
        root = resolve_indirect(reader.trailer['/Root'])
        if '/Names' not in root:
            print('No attachments found in the PDF.')
            return

        names = resolve_indirect(root['/Names'])
        if '/EmbeddedFiles' not in names:
            print('No attachments found in the PDF.')
            return
        
        embedded_files = resolve_indirect(names['/EmbeddedFiles'])
        attachments = embedded_files['/Names']
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        for i in range(0, len(attachments), 2):
            attachment_name = attachments[i].get_object()
            attachment_file = attachments[i+1].get_object()
            
            file_spec = resolve_indirect(attachment_file)
            file_data = resolve_indirect(file_spec['/EF']['/F']).get_data()

            output_path = os.path.join(output_dir, attachment_name)
            with open(output_path, 'wb') as output_file:
                output_file.write(file_data)

            print(f"Extracted: {attachment_name}")


# Example usage
input_pdf = 'Micro-1.pdf'
output_pdf = 'output2.pdf'
files_to_attach = ['Micro.pdf']
attach_files_to_pdf(input_pdf, output_pdf, files_to_attach)

input_pdf = 'output.pdf'  # Ensure this matches the output PDF from the attachment process
output_dir = 'extracted_attachments'
extract_attachments_from_pdf(input_pdf, output_dir)
