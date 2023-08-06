"""The serve command."""

from .base import *

class Serve(Base):
  """Serve Julia code"""

  def run(self):
    call('escher --serve --dir app/controllers', shell=True)
