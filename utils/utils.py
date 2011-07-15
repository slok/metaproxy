#Copyright (C) 2011 Iraide Diaz (sharem)
#Copyright (C) 2011 Xabier Larrakoetxea (slok)
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.

import urllib2

#####################################################################################
def download_file(url, destination):
    """Gets a file from an URL and stores in a destination
    Keyword arguments:
    url -- The url of the file to download
    destination -- The path to store the downloaded file
    """
    #get the file from Internet
    tempFile = urllib2.urlopen(url)
    parts = []
    #split the URL(we want to get the last part(file name))
    for part in url.split('/'):
        parts.append(part)
    #if the URL isn't pointing to a file, raise exception
    if parts[len(parts)-1] == '' :
        raise Exception, "The URL has to point to a concrete file"
    else:
        #add to the destination the last part of the splitted url (length -1)
        destination += parts[len(parts)-1]
        #open the destination file (with wb flags) and writes the "buffer"
        output = open(destination, 'wb')
        output.write(tempFile.read())
        
        #close the opened file
        output.close()

#####################################################################################
def find_in_list(list, key):
    i = 0
    for k, v in list:
        i += 1
        if k == key:
            break
    return i-1
#####################################################################################
def debug_print(x):
    print '##################################################################'
    print x
    print '##################################################################'

