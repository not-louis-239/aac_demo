# module to store UI elements
# because manually positioning UI elements using thinnicky arithmetic
# is a fat pain

# repo at: https://github.com/not-louis-239/sunrise-aac
# Copyright (C) 2026 Louis Masarei-Boulton <243234869+not-louis-239@users.noreply.github.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from . import boxes

from . import (
    boxes,
    spacer,
    input_boxes,
    labels
)

HBox = boxes.HBox
VBox = boxes.VBox
Spacer = spacer.Spacer
InputBox = input_boxes.InputBox
Label = labels.Label
