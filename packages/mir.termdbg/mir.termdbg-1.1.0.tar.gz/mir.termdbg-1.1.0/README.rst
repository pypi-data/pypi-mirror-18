mir.termdbg
=============

.. image:: https://circleci.com/gh/project-mir/mir.termdbg.svg?style=shield
   :target: https://circleci.com/gh/project-mir/mir.termdbg
   :alt: CircleCI
.. image:: https://codecov.io/gh/project-mir/mir.termdbg/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/project-mir/mir.termdbg
   :alt: Codecov
.. image:: https://badge.fury.io/py/mir.termdbg.svg
   :target: https://badge.fury.io/py/mir.termdbg
   :alt: PyPi Release

Simple terminal key press debugger.

termdbg echoes the bytes received directly from the terminal for debugging
exactly what bytes or escape sequences a particular terminal is sending.  The
terminal is set to raw mode if possible.

termdbg's output is intended for human consumption; the output format is not
guaranteed and should not be parsed.

To exit, send the byte value 3.  This is the ASCII encoding for ``^C``
(End Of Text), which is sent by pressing CTRL-C for most terminals.
If you are unable to exit, you can send SIGINT from a separate
terminal.

Example usage::

  $ termdbg
  27, o33, 0x1B  # F1 pressed, terminal emits three bytes
  79, o117, 0x4F
  80, o120, 0x50
  27, o33, 0x1B  # F2 pressed, terminal emits three bytes
  79, o117, 0x4F
  81, o121, 0x51
  3, o3, 0x3  # Ctrl-C pressed, terminal emits ^C and termdbg quits
  $
