#!/usr/bin/env python3
#
# This file is part of Script of Scripts (sos), a workflow system
# for the execution of commands and scripts in different languages.
# Please visit https://github.com/bpeng2000/SOS
#
# Copyright (C) 2016 Bo Peng (bpeng@mdanderson.org)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import sys
import argparse

from io import StringIO

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook
from nbconvert.exporters import Exporter

from sos.utils import env
from sos.sos_syntax import SOS_SECTION_HEADER, SOS_CELL_LINE


#
# Converter from Notebook
#

def parse_convert_args(convert_args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--reorder', action='store_true')
    parser.add_argument('--reset-index', action='store_true')
    parser.add_argument('--add-header', action='store_true')
    parser.add_argument('--no-index', action='store_true')
    parser.add_argument('--remove-magic', action='store_true')
    parser.add_argument('--md-to-report', action='store_true')
    try:
        args = parser.parse_args(convert_args)
    except Exception as e:
        raise RuntimeError('Unrecognized style argument {}: {}'
            .format(' '.join(convert_args), e))
    return args


# This class cannot be defined in .kernel because it would cause some
# weird problem with unittesting not able to resolve __main__
class SoS_Exporter(Exporter):
    def __init__(self, config=None, reorder=False, reset_index=False, add_header=False,
            no_index=False, remove_magic=False, md_to_report=False,
            **kwargs):
        self.reorder = reorder
        self.reset_index = reset_index
        self.add_header = add_header
        self.no_index = no_index
        self.remove_magic = remove_magic
        self.md_to_report = md_to_report
        self.output_extension = '.sos'
        self.output_mimetype = 'text/x-sos'
        Exporter.__init__(self, config, **kwargs)

    def from_notebook_cell(self, cell, fh, idx = 0):
        if not hasattr(cell, 'execution_count') or cell.execution_count is None or self.no_index:
            fh.write('\n%cell {}\n'.format(cell.cell_type))
        else:
            idx += 1
            fh.write('\n%cell {} {}\n'.format(cell.cell_type,
                                              idx if self.reset_index else cell.execution_count))
        if cell.cell_type == 'code':
            if any(cell.source.startswith(x) for x in ('%run', '%restart', '%dict', '%use', '%with', '%set', '%paste')):
                if self.remove_magic:
                    cell.source = '\n'.join(cell.source.split('\n')[1:])
            if self.add_header and not any([SOS_SECTION_HEADER.match(x) for x in cell.source.split('\n')]):
                cell.source = '[{}]\n'.format(idx if self.reset_index else cell.execution_count) + cell.source
            fh.write(cell.source.strip() + '\n')
        elif cell.cell_type == "markdown":
            fh.write('\n'.join('#! ' + x for x in cell.source.split('\n') if x.strip()) + '\n')
        return idx

    def from_notebook_node(self, nb, resources, **kwargs):
        #
        if self.reorder:
            unnumbered_cells = {x: y for x, y in enumerate(nb.cells)
                              if not hasattr(y, 'execution_count') or y.execution_count is None}
            numbered_cells = [y for y in nb.cells
                              if hasattr(y, 'execution_count') and y.execution_count is not None]
            numbered_cells = sorted(numbered_cells, key = lambda x: x.execution_count)
            cells = []
            for idx in range(len(nb.cells)):
                if idx in unnumbered_cells:
                    cells.append(unnumbered_cells[idx])
                else:
                    cells.append(numbered_cells.pop(0))
        else:
            cells = nb.cells
        with StringIO() as fh:
            fh.write('#!/usr/bin/env sos-runner\n')
            fh.write('#fileformat=SOSNB1.0\n')
            idx = 0
            for cell in cells:
                idx = self.from_notebook_cell(cell, fh, idx)
            content = fh.getvalue()
        resources['output_extension'] = '.sos'
        return content, resources


def notebook_to_script(notebook_file, sos_file, convert_args=[]):
    '''
    Convert a ipython notebook to sos format. This converter accepts options
    --reorder to reorder cells according to executing order, --reset-index
    to reset executing counts, --add-header to add a SoS header, --no-index
    to ignore indexes, --remove-magic to remove ipynb-only magics, and 
    --md-to-report to convert markdown cells to sos report actions.
    '''
    sargs = parse_convert_args(convert_args)
    exporter = SoS_Exporter(reorder=sargs.reorder, reset_index=sargs.reset_index,
                            add_header=sargs.add_header, no_index=sargs.no_index,
                            remove_magic=sargs.remove_magic, md_to_report=sargs.md_to_report)
    notebook = nbformat.read(notebook_file, nbformat.NO_CONVERT)
    output, resource = exporter.from_notebook_node(notebook, {})
    if sos_file == '__STDOUT__':
        sys.stdout.write(output)
    else:
        with open(sos_file, 'w') as sos:
            sos.write(output)
        env.logger.info('SoS script saved to {}'.format(sos_file))

#
# Converter to Notebook
#
def add_cell(cells, content, cell_type, cell_count):
    # if a section consist of all report, report it as a markdown cell
    if not content:
        return
    if cell_type not in ('code', 'markdown'):
        env.logger.warning('Unrecognized cell type {}, code assumed.'.format(cell_type))
    if cell_type == 'markdown' and any(x.strip() and not x.startswith('#! ') for x in content):
        env.logger.warning('Markdown lines not starting with #!, code cell assumed.')
        cell_type = 'code'
    #
    if cell_type == 'markdown':
        cells.append(new_markdown_cell(source=''.join([x[3:] for x in content]),
            execution_count=cell_count))
    else:
        cells.append(
             new_code_cell(
                 source=''.join(content),
                 execution_count=cell_count)
        )

def script_to_notebook(script_file, notebook_file, *args):
    '''
    Convert a sos script to iPython notebook (.ipynb) so that it can be opened
    by Jupyter notebook.
    '''
    cells = []
    cell_count = 1
    cell_type = 'code'
    content = []

    with open(script_file) as script:
        first_block = True
        for line in script:
            if line.startswith('#') and first_block:
                if line.startswith('#!'):
                    continue
                if line.startswith('#fileformat='):
                    if not line[12:].startswith('SOS'):
                        raise RuntimeError('{} is not a SoS script according to #fileformat line.'.format(script_file))
                    continue

            first_block = False

            mo = SOS_CELL_LINE.match(line)
            if mo:
                # eat a new line before the CELL_LINE
                if content and content[-1] == '\n':
                    content = content[:-1]
                # get ride of empty content
                if not any(x.strip() for x in content):
                    continue
                add_cell(cells, content, cell_type, cell_count)
                cell_count += 1

                cell_type = mo.group(1)
                content = []
                continue
            else:
                content.append(line)
    #
    if content and any(x.strip() for x in content):
        add_cell(cells, content, cell_type, cell_count)
    #
    nb = new_notebook(cells = cells,
        metadata = {
            'kernelspec' : {
                "display_name": "SoS",
                "language": "sos",
                "name": "sos"
            },
            "language_info": {
                "file_extension": ".sos",
                "mimetype": "text/x-sos",
                "name": "sos",
                "pygments_lexer": "python"
            }
        }
    )
    if not notebook_file:
        nbformat.write(nb, sys.stdout, 4)
    else:
        with open(notebook_file, 'w') as notebook:
            nbformat.write(nb, notebook, 4)
        env.logger.info('SoS script saved to {}'.format(notebook_file))


