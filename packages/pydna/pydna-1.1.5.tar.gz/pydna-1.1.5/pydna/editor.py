#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''This module provides a class for opening a sequence using an editor
that accepts a file as a command line argument.

ApE - A plasmid Editor [#]_ is and excellent editor for this purpose.

References
----------

.. [#] http://biologylabs.utah.edu/jorgensen/wayned/ape/

'''

import time
import tempfile
import os
import subprocess
import itertools
import operator
from Bio.SeqRecord import SeqRecord
from .dseqrecord import Dseqrecord


class Editor:
    '''
    The Editor class needs to be instantiated before use.

    Parameters
    ----------

    shell_command_for_editor : str
        String containing the path to the editor
    tmpdir : str, optional
        String containing path to the temprary directory where sequence
        files are stored before opening.

    Examples
    --------

    >>> import pydna
    >>> #ape = pydna.Editor("tclsh8.6 /home/bjorn/.ApE/apeextractor/ApE.vfs/lib/app-AppMain/AppMain.tcl")
    >>> #ape.open("aaa") # This command opens the sequence in the ApE editor

    '''
    def __init__(self, shell_command_for_editor, tmpdir=None):
        path    = (shell_command_for_editor,
                   shell_command_for_editor.split().pop(),)

#        if True in [os.path.isfile(p) for p in path]:
#            self.path_to_editor = shell_command_for_editor
#        else:
#            print()
#            print(shell_command_for_editor)
#            print("is not a valid path to ApE")
#            raise ValueError

        self.tmpdir = tmpdir or os.path.join(tempfile.gettempdir(),"ApE")
        try:
            os.makedirs(self. tmpdir)
        except OSError:
            pass

    def open(self,*args,**kwargs):
        '''Open a sequence for editing in an external (DNA) editor.

        Parameters
        ----------
        args : sequence or iterable of sequences


       '''

        args=list(args)
        for i, arg in enumerate(args):
            if not hasattr(arg, "__iter__") or isinstance(arg, SeqRecord):
                args[i] = (arg,)
        seqs = []
        names = []
        for arg in itertools.chain.from_iterable(args):
            seq=Dseqrecord(arg)
            for feature in seq.features:
                qf = feature.qualifiers
                if not "label" in qf:
                    try:
                        qf["label"] = qf["note"]
                    except KeyError:
                        qf["label"] = "feat{}".format(len(feature))
                if not "ApEinfo_fwdcolor" in qf:
                    qf["ApEinfo_fwdcolor"]="cyan"
                if not "ApEinfo_revcolor" in qf:
                    qf["ApEinfo_revcolor"]="red"
            seq.features.sort(key = operator.attrgetter("location.start"))
            seqs.append(seq)
            name=seq.description.strip(".").replace(" ","_")
            n=1
            while True:
                if name in names:
                    newname=name+"_"+str(n)
                    if newname in names:
                        n+=1
                        continue
                    else:
                        names.append(newname)
                        break
                else:
                    names.append(name)
                    break
        pathstofiles = []
        path = tempfile.mkdtemp(dir=self.tmpdir)

        for name, seq in zip(names, seqs):
            whole_path = os.path.join(path, name)+".gb"
            seq.write(whole_path)
            pathstofiles.append('"{}"'.format(whole_path))

        p = subprocess.Popen("{} {}".format(self.path_to_editor," ".join(pathstofiles)),
                             shell=True,
                             stdout = tempfile.TemporaryFile(),
                             stderr = tempfile.TemporaryFile()).pid
        time.sleep(0.5)
        #shutil.rmtree(path)
        #for name in names:
        #    print os.path.join(path, name)+".gb"

apeloader = Editor( os.getenv("pydna_ape") )

def ape(*args,**kwargs):
    return apeloader.open(*args,**kwargs)


if __name__=="__main__":
    import os
    cache = os.getenv("pydna_cache")
    os.environ["pydna_cache"]="nocache"
    import doctest
    doctest.testmod()
    os.environ["pydna_cache"]=cache
