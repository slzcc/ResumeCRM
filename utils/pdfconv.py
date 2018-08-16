# -*- coding: utf-8 -*-

######################################################################################
# 
#    Copyright (C) 2017 Mathias Markl
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
#######################################################################################

import os
import io
import base64
import shutil
import urllib
import logging
import tempfile
import mimetypes
import subprocess

from contextlib import closing

logging.basicConfig(format= '%(asctime)s %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

WD_FORMAT_PDF = 17
PP_FORMAT_PDF = 32
EX_FORMAT_PDF = 57

def convert_binary2pdf(binary, mimetype=None, filename=None, format="binary"):
    """
    Converts a binary value to a PDF file.
    :param binary: The binary value
    :param mimetype: The mime tpye of the binary value
    :param filename: The filename of the binary value
    :param format: The output format (binary, file, base64 | default: binary)
    :return: returns output depending on the given format
    """
    if not mimetype and not filename:
        raise ValueError("Either a mime type or a filename has to be given as argument.")
    else:
        if not mimetype:
            mimetype = mimetypes.guess_type(urllib.request.pathname2url(filename))[0]
        if not filename:
            extension =  mimetypes.guess_extension(mimetype)
        else:
            extension = os.path.splitext(filename)[1]
        tmp_dir = tempfile.mkdtemp()
        try:
            tmp_wpath = os.path.join(tmp_dir, "tmpfile" + extension)
            tmp_ppath = os.path.join(tmp_dir, "tmpfile.pdf")
            if os.name == 'nt':
                tmp_wpath = tmp_wpath.replace("\\","/")
                tmp_ppath = tmp_ppath.replace("\\","/")
            with closing(open(tmp_wpath, 'wb')) as file:
                file.write(binary)
            __dispatch[mimetype](tmp_wpath, tmp_ppath)
            with closing(open(tmp_ppath, 'rb')) as file:
                if format == 'binary':
                    return file.read()
                elif format == 'file':
                    output = io.BytesIO()
                    output.write(file.read())
                    output.close()
                    return output
                elif format == 'base64':
                    return base64.b64encode(file.read())
                else:
                    raise ValueError("Unknown format type. Use one of these: path, binary, file, base64")
        finally:
            shutil.rmtree(tmp_dir)
        
def convert_document2pdf(input_path, output_path):
    """
    Converts a file to a PDF file.
    :param input_path: The input path
    :param output_path: The output path
    :return: returns nothing
    """
    if os.name == 'nt':
        try:
            _convert_word2pdf(input_path, output_path)
        except IOError as error:
            raise
        except (ImportError, OSError) as error:
            logger.info("Failed to use MS Office | %s | Fallback to unoconv" % error)
            _convert_unoconv2pdf(input_path, output_path)
    else:
        _convert_unoconv2pdf(input_path, output_path)

def convert_presentation2pdf(input_path, output_path):
    """
    Converts a file to a PDF file.
    :param input_path: The input path
    :param output_path: The output path
    :return: returns nothing
    """
    if os.name == 'nt':
        try:
            _convert_powerpoint2pdf(input_path, output_path)
        except IOError as error:
            raise
        except (ImportError, OSError) as error:
            logger.info("Failed to use MS Office | %s | Fallback to unoconv" % error)
            _convert_unoconv2pdf(input_path, output_path)
    else:
        _convert_unoconv2pdf(input_path, output_path)
                
def convert_spreadsheet2pdf(input_path, output_path):
    """
    Converts a file to a PDF file.
    :param input_path: The input path]
    :param output_path: The output path
    :return: returns nothing
    """
    if os.name == 'nt':
        try:
            _convert_excel2pdf(input_path, output_path)
        except IOError as error:
            raise
        except (ImportError, OSError) as error:
            logger.info("Failed to use MS Office | %s | Fallback to unoconv" % error)
            _convert_unoconv2pdf(input_path, output_path)
    else:
        _convert_unoconv2pdf(input_path, output_path)
            
def _convert_word2pdf(input_path, output_path):
    try:
        import comtypes
        import comtypes.client
    except ImportError:
        raise 
    else:
        word = doc = None
        try:
            comtypes.CoInitialize()
            word = comtypes.client.CreateObject('Word.Application')
            doc = word.Documents.Open(input_path)
            doc.SaveAs(output_path, FileFormat=WD_FORMAT_PDF)
        except WindowsError as error:
            raise OSError(error)
        except comtypes.COMError as error:
            raise IOError(error)
        finally:
            if doc:
                doc.Close()
            if word: 
                word.Quit()
            comtypes.CoUninitialize()
            
def _convert_powerpoint2pdf(input_path, output_path):
    try:
        import comtypes
        import comtypes.client
    except ImportError:
        raise 
    else:
        powerpoint = slides = None
        try:
            comtypes.CoInitialize()
            powerpoint = comtypes.client.CreateObject('Powerpoint.Application')
            slides = powerpoint.Presentations.Open(input_path)
            slides.SaveAs(output_path, FileFormat=PP_FORMAT_PDF)
        except WindowsError as error:
            raise OSError(error)
        except comtypes.COMError as error:
            raise IOError(error)
        finally:
            if slides:
                slides.Close()
            if powerpoint: 
                powerpoint.Quit()
            comtypes.CoUninitialize()
            
def _convert_excel2pdf(input_path, output_path):
    try:
        import comtypes
        import comtypes.client
    except ImportError:
        raise 
    else:
        excel = wb = None
        try:
            comtypes.CoInitialize()
            excel = comtypes.client.CreateObject('Excel.Application')
            wb = excel.Workbooks.Open(input_path)
            wb.SaveAs(output_path, FileFormat=EX_FORMAT_PDF)
        except WindowsError as error:
            raise OSError(error)
        except comtypes.COMError as error:
            raise IOError(error)
        finally:
            if wb:
                wb.Close()
            if excel: 
                excel.Quit()
            comtypes.CoUninitialize()

def _convert_unoconv2pdf(input_path, output_path):
    try:
        env = os.environ.copy()
        if 'PYTHONPATH' in env:
            del env['PYTHONPATH']
        # p = subprocess.Popen(['unoconv', '--format=pdf', '--output=%s' % output_path, input_path],stdout=subprocess.PIPE, env=env, shell=False)
        p = subprocess.Popen(['soffice', '--headless', '--invisible', '--convert-to', 'pdf', '{}'.format(input_path), '--outdir', '{}'.format(os.path.dirname(output_path))],stdout=subprocess.PIPE, env=env, shell=False)
        p.communicate()
        p.wait()
    except subprocess.CalledProcessError:
        raise
    except OSError:
        raise

__dispatch  = {
    'application/msword': convert_document2pdf,
    'application/ms-word': convert_document2pdf,
    'application/vnd.ms-word.document.macroEnabled.12': convert_document2pdf,
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': convert_document2pdf,
    'application/vnd.oasis.opendocument.text': convert_document2pdf,
    'application/vnd.mspowerpoint': convert_presentation2pdf,
    'application/vnd.ms-powerpoint': convert_presentation2pdf,
    'application/vnd.ms-powerpoint.addin.macroEnabled.12': convert_presentation2pdf,
    'application/vnd.openxmlformats-officedocument.presentationml.presentation': convert_presentation2pdf,
    'application/vnd.oasis.opendocument.presentation': convert_presentation2pdf,
    'application/vnd.msexcel': convert_spreadsheet2pdf,
    'application/vnd.ms-excel': convert_spreadsheet2pdf,
    'application/vnd.ms-excel.sheet.macroEnabled.12': convert_spreadsheet2pdf,
    'application/vnd.ms-excel.sheet.binary.macroEnabled.12': convert_spreadsheet2pdf,
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': convert_spreadsheet2pdf,
    'application/vnd.oasis.opendocument.spreadsheet': convert_spreadsheet2pdf,
}