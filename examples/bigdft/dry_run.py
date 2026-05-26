# SPDX-License-Identifier: GPL-3.0-or-later
#
# Optional extended example.
#
# This file is not required for any skill to function.
# If adapted from upstream material, add source and upstream license details.

from BigDFT import Calculators as C

calc = C.SystemCalculator()
log = calc.run(input=input_file, name="test", dry_run=True)
