'''
--------------------------------------------------------------------------
Copyright (C) 2016 Lukasz Laba <lukaszlab@o2.pl>

File version 0.6 date 2016-12-15

This file is part of SeePy.
SeePy is a python script visualisation tool.
http://seepy.org/

SeePy is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

SeePy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
'''

import os
import sys
import re
import copy
import tempfile

from PyQt4 import QtGui
import mistune
try:
    import svgwrite
except ImportError:
    pass
try:
    import matplotlib.pyplot as plt
except ImportError:
    pass

class Shell():
    def __init__(self):
        self.report_markdown = ''
        self.report_html = ''
        #---
        self.savedir = os.path.dirname(__file__)
        #---
        self.Code = None
        #----
        self.float_display_precison = 4
        #----
        self.tmpdir = self.__get_tempdir()
        
        
    def assign_code(self, CodeObiect):
        self.Code = CodeObiect
        
    def run_oryginal(self):
        exec self.Code.code_oryginal in globals(), locals()
        
    def run_parsed(self):
        self.report_markdown = ''
        self.report_html = ''
        self._id = 1
        #-----------------------------------------------------------------
        # Here are functions needed in namespace where parsed code is run
        #-----------------------------------------------------------------
        def r_comment(object):
            self.report_markdown += str(object) + '\n\n'
            
        def r_seepywarning(warning):
            r_comment('>>*!!! SeePyWarning - %s !!!*'%warning)
        
        def r_mathcomment(object):
            comment_string = str(object)
            comment_string_formated = codeformat(comment_string)
            r_comment(comment_string_formated)
                    
        def r_adj(text = 'text', link = 'link', comment = 'somecomment', mode = 1, code = ''):
            islist = re.search(r'(\w+)\s*=\s*(\w+)\s*[[](\d+)[]]\s*', code)
            setvalues = None
            index = None
            #---changing True False display on report
            if text == 'True':
                text = '\xe2\x98\x91'
            if text == 'False':
                text = '\xe2\x98\x90'
            #---
            if islist:
                variable = islist.group(2)
                index = int(islist.group(3))
                setvalues = ('%(' + str(variable) + ')s') % vars_formated()
            if mode == 1:
                href='[{0}]({1};{3};{4}) {2}'.format(text, link, comment, setvalues, index)
            if mode == 2:
                href='{2} [{0}]({1};{3};{4})'.format(text, link, comment, setvalues, index)
            self.report_markdown += href +'\n\n'
            
        def r_img(imagename):
            image_path = os.path.dirname(self.Code.script_path) + '/' + imagename
            self.report_markdown += '![Alt text](%s)\n\n' % image_path

        def r_plt(pltObject):
            try:
                name = 'tmp_seepy_' + str(self._id) + '.png'
                image_path = os.path.join(self.tmpdir, name)
                pltObject.savefig(image_path, dpi=(60))
                self.report_markdown += '![Alt text](%s)\n\n' % image_path
                self._id += 1
            except Exception as e :
                r_seepywarning('Matplotlib plt image save failure - %s' %str(e))
                
        def r_pil(PilImageObject):
            try:
                name = 'tmp_seepy_' + str(self._id) + '.png'
                image_path = os.path.join(self.tmpdir, name)
                PilImageObject.save(image_path)
                self.report_markdown += '![Alt text](%s)\n\n' % image_path
                self._id += 1
            except Exception as e :
                r_seepywarning('Pillow image save failure - %s' %str(e))
                
        def r_tex(string):
            plt.figure(frameon=False)
            plt.axes(frameon=0)
            if string[0] != '$' and string[-1] != '$':
                string = '$' + string + '$'
            plt.text(0.0, 0.0, string, fontsize=600)
            plt.xticks(())
            plt.yticks(())
            plt.tight_layout()
            name = 'tmp_seepy_' + str(self._id) + '.png'
            image_path = os.path.join(self.tmpdir, name)
            plt.savefig(image_path, bbox_inches='tight', dpi=(2))
            plt.close()
            self.report_markdown += '![Alt text](%s)\n\n' % image_path
            self._id += 1

        def r_codetex(string):
            r_tex(codeformat(string))
        
        def codeformat(string):
            #changing 3**3 to 3^2
            string = string.replace('**', '^')
            #changing math.sin(1) to sin(1)
            string = string.replace('math.', '')
            #changing 3 * u.mm to 3[mm] - usable when Unum SI units system used in script
            string = re.sub(    r'\s*\*\s*u.(\w+)',
                                r'[\1]',
                                string  )
            #changing (3*u.mm + 3*u.m).asUnit(u.mm) to 3*u.mm + 3*u.m - usable when Unum SI units system used in script
            string = re.sub(    r'\((.+)\).asUnit\((.+)\)',
                                r'\1',
                                string  )            
            return string
        
        def r_svg(svgObject):
            name = 'tmp_seepy_' + str(self._id) + '.svg'
            image_path = os.path.join(self.tmpdir, name)
            if type(svgObject) is str:
                svg_file = open(image_path, "w")
                svg_file.write(svgObject)
                self.report_markdown += '![Alt text](%s)\n\n' % image_path
                svg_file.close()
                self._id += 1
            elif type(svgObject) is svgwrite.drawing.Drawing:
                svg_file = open(image_path, "w")
                svg_file.write(svgObject.tostring())
                self.report_markdown += '![Alt text](%s)\n\n' % image_path
                svg_file.close()
                self._id += 1
            else:
                r_seepywarning('Unknown SVG format given')


        def vars_formated(variables = vars()):
            out = copy.copy(variables)
            for key in out:
                if type(out[key]) is float:
                    out[key] = round(out[key], self.float_display_precison)
            return out
        #---Adding current script dir to python PATH list
        #---(user will be able to import modules from dir where his seepy script is stored)
        script_dir = os.path.dirname(self.Code.script_path)
        sys.path.append(script_dir) 
        #-----------------------------------------------------------------
        #---------- Here the code_parsed is finally executed -------------
        #-----------------------------------------------------------------
        exec self.Code.code_parsed in locals(), locals() #----------------
        #-----------------------------------------------------------------
        #-----------------------------------------------------------------
        #---so the report_markdown has been created-----------------------
        #---and mistune is used to get report_html from report_markdown
        self.report_html = mistune.markdown(self.report_markdown)
        #-----------------------------------------------------------------
        self._id = 0
        #---Deleting current script dir from python PATH list
        sys.path = list(set(sys.path)) # first deleting duplicates
        sys.path.remove(script_dir) # and finaly deleting script dir 
        
    def show_report_markdown(self):
        print self.report_markdown
        
    def show_report_html(self):
        print self.report_html

    def save_report_markdown(self, savedir = os.path.dirname(__file__), initfilename = 'new.md'):
        #---asking for file path
        filename = QtGui.QFileDialog.getSaveFileName(caption = 'Save as Markdown document',
                                                directory = self.savedir + '/' + initfilename,
                                                filter = "Markdown document (*.md)")
        filename = str(filename)
        #---
        if not filename == '':
            self.savedir = os.path.dirname(filename)
            md_file = open(filename, "w")
            md_file.write(self.report_markdown)
            md_file.close()
            
    def __get_tempdir(self):
        dirpath = tempfile.mkdtemp()
        dirname = os.path.basename(dirpath)
        new_dirname = 'seepy_' + dirname
        new_dirpath = dirpath.replace(dirname, new_dirname)
        os.rename(dirpath, new_dirpath)
        return new_dirpath
            
    def delete_tmpfile(self, deleteall=False):
        if deleteall:
            for content in os.listdir(self.tmpdir):
                os.remove(self.tmpdir + '/' + content)
        else:
            for content in os.listdir(self.tmpdir):
                if 'tmp_seepy' in content :
                    os.remove(self.tmpdir + '/' + content)
    
    def close_shell (self):
        self.delete_tmpfile(deleteall=True)
        os.removedirs(self.tmpdir)
    
    def __del__ (self):
        self.close_shell()

# Test if main
if __name__ == '__main__':
    Environment = Shell()
    from Code import Code
    ScriptCode = Code()
    Environment.assign_code(ScriptCode)
    #---
    ScriptCode.openFile()
    #Environment.run_parsed()
    #Environment.run_oryginal()
    #----
    #Environment.show_report_markdown()
    #Environment.show_report_html()