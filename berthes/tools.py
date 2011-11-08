# JunkBackup
# Copyright (C) 2011 Kantist
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#     
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#     GNU General Public License for more details.
#     
#     You should have received a copy of the GNU General Public License
#     along with this program.
#     If not, see http://www.gnu.org/licenses/gpl-3.0.html

import re

# trims or adds substring at each end of the string
def trim(text, tr, right=-1, left=-1, left_least=-1, right_least=-1, left_most=-1, right_most=-1):
    if left >= 0:
        text = re.sub("^(%s)*" % tr, tr * left, text)
    elif left_least >= 0:
        text = re.sub("^(%s){,%i}(?!=(%s))" % (tr, left_least, tr), tr * left_least, text)
    elif left_most >= 0:
        text = re.sub("^(%s){%i,}" % (tr, left_most), tr * left_most, text)
    if right >= 0:
        text = re.sub("(%s)*$" % tr, tr * right, text)
    elif right_least >= 0:
        text = re.sub("(?!<=(%s))(%s){,%i}$" % (tr, tr, right_least), tr * right_least, text)
    elif right_most >= 0:
        text = re.sub("(%s){%i,}$" % (tr, right_most), tr * right_most, text)
    return text
