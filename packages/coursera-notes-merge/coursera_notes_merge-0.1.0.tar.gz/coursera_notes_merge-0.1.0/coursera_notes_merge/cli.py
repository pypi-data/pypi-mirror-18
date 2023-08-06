import click
import os
import sys
import fnmatch
from PyPDF2 import PdfFileMerger

merger = PdfFileMerger()

def traverse_dir(directory):
  count = 0
  for root, subdir, files in os.walk(directory):
    for item in fnmatch.filter(files, "*.pdf"):
      input_path = os.path.join(root, item)
      try:
        input = open(input_path, "rb")
        merger.append(input)
        click.echo('File {0} added'.format(item))
        input.close()
        count += 1
      except:
        click.echo('File {0} skipped.'.format(input_path))

  return count

@click.command()
@click.option('--output', '-o', help='Name of output file.')
@click.argument('path', default='', required=False)
def main(path, output):
  """Merges course notes downloaded from coursera-dl"""
  cwd = os.getcwd()

  if path != '':
    cwd = os.path.join(cwd, path)

  if not os.path.isdir(cwd):
    click.echo('Given path must be a direcory.')
    sys.exit()

  if output is not None and not output.endswith('.pdf'):
    click.echo('Given output name should end in \".pdf\"')
    sys.exit()

  if output == None:
    (base, tail) = os.path.split(cwd)
    output = tail + '-notes.pdf'
    
  output_path = os.path.join(cwd, output)

  if os.path.exists(output_path):
    click.echo('Deleting output file that already exists.')
    os.remove(output_path)

  count = traverse_dir(cwd)

  of = open(output_path, "wb")

  if count != 0:
    merger.write(of)
    click.echo('Notes merged into {0}'.format(output_path))
  else:
    click.echo('No notes found.')

  of.close()
