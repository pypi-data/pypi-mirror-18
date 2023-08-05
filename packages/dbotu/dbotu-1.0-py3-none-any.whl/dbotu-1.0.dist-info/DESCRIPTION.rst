Copyright (c) 2016 Scott W. Olesen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Description: Distribution-based OTU calling
        ==============================
        
        -  `source <https://github.com/swo/dbotu3>`__
        -  `academic <http://almlab.mit.edu/dbotu3.html>`__
        -  `PyPi <https://pypi.python.org/pypi/dbotu>`__
        
        *dbotu3* is a new implementation of Sarah Preheim's
        `dbOTU <http://aem.asm.org/content/79/21/6593.long>`__ algorithm. The
        scope is narrower, the numerical comparisons are faster, and the
        interface is more user-friendly.
        
        Read the `documentation <http://dbotu3.readthedocs.io/en/latest/>`__
        for:
        
        -  a guide to getting started,
        -  an explanation of the algorithm, and
        -  the API reference.
        
        You can also read our new
        `manuscript <http://dx.doi.org/10.1101/076927>`__ for more technical
        details about the algorithm.
        
        Requirements
        ------------
        
        -  **Python 3**
        -  Numpy, SciPy, `BioPython <http://biopython.org>`__,
           `Pandas <http://pandas.pydata.org>`__
        -  `Levenshtein <https://pypi.python.org/pypi/python-Levenshtein>`__
        
        To-do
        -----
        
        -  Better coverage for unit tests
        -  Expose key functionality so that the package can be imported and used
           in an existing python pipeline
        
        Authors
        -------
        
        -  **Scott Olesen** - *swo at alum.mit.edu*
        
Platform: any
