# ############################################################################
# |W|I|D|E|I|O|L|T|D|W|I|D|E|I|O|L|T|D|W|I|D|E|I|O|L|T|D|W|I|D|E|I|O|L|T|D|
# Copyright (c) 2016 - WIDE IO LTD
# 
# Permission is hereby granted, free of charge, to any person 
# obtaining a copy of this software and associated documentation 
# files (the "Software"), to deal in the Software without 
# restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software 
# is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be 
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
# |D|O|N|O|T|R|E|M|O|V|E|!|D|O|N|O|T|R|E|M|O|V|E|!|D|O|N|O|T|R|E|M|O|V|E|!|
# ############################################################################

from . import autoimp2 as autoimp

from dfract.datasets.dfracthelper import DFractExposedDataset

class DFRACTBuilders:
    """
    This class is in charge for setting definition.
    """

    dataset_path = "dfract.:dfract.datasets."
    datastream_path = "dfract.:dfract.datastreams."
    aggregate_path = "dfract.:dfract.aggregates."
    index_path = "dfract.:dfract.indexes."

    def __init__(self):
        self.dbcontext={}
        self.dscontext={}
        self.dacontext={}
        self.dicontext={}

        for k in dir(__builtins__):
            self.dbcontext[k] = getattr(__builtins__, k)
            self.dscontext[k] = getattr(__builtins__, k)
            self.dacontext[k] = getattr(__builtins__, k)
            self.dicontext[k] = getattr(__builtins__, k)

        # add eventual functions to make language more powerful
        #add_context_basics(self.dbcontext)
        self.dbcontext["__all__"] = self.dbcontext.keys()
        self.dscontext["__all__"] = self.dscontext.keys()
        self.dacontext["__all__"] = self.dacontext.keys()
        self.dicontext["__all__"] = self.dicontext.keys()

        autoimp.import_all_as_context(self.dbcontext,
                                      ['']+self.dataset_path.split(':'),
                                      ['']
                                      )

        autoimp.import_all_as_context(self.dscontext,
                                      ['']+self.datastream_path.split(':'),
                                      ['']
                                      )

        autoimp.import_all_as_context(self.dacontext,
                                  [''] + self.dataset_path.split(':'),
                                  ['']
                                  )

        autoimp.import_all_as_context(self.dicontext,
                                  [''] + self.datastream_path.split(':'),
                                  ['']
                                  )

    def dataset_builder(self, expr, context_filter=lambda x: x, *supp_context):
        """
        This function evaluates an expression within a context that where the path for datasets are easily accessible.

        """
        context = context_filter(self.dbcontext)
        dataset = eval(expr, context, *supp_context)
        dataset._instantiating_expression = expr
        return DFractExposedDataset(dataset)

    def datastream_builder(self, expr, context_filter=lambda x: x, *supp_context):
        """
        This function evaluates an expression within a context that where the path for datastreams are easily accessible.

        """
        context = context_filter(self.dscontext)
        datastream =  eval(expr, context, *supp_context)
        datastream._instantiating_expression = expr
        return datastream


    def aggregate_builder(self, expr, context_filter=lambda x: x, *supp_context):
        """
        This function evaluates an expression within a context that where the path for aggregate are easily accessible.

        """
        context = context_filter(self.dacontext)
        datastream = eval(expr, context, *supp_context)
        datastream._instantiating_expression = expr
        return datastream


    def index_builder(self, expr, context_filter=lambda x: x, *supp_context):
        """
        This function evaluates an expression within a context that where the path for index are easily accessible.

        """
        context = context_filter(self.dicontext)
        datastream = eval(expr, context, *supp_context)
        datastream._instantiating_expression = expr
        return datastream


_dfract_builders = DFRACTBuilders()
dataset_builder = _dfract_builders.dataset_builder
datastream_builder = _dfract_builders.datastream_builder
aggregate_builder = _dfract_builders.aggregate_builder
index_builder = _dfract_builders.index_builder

def generic_builder(expr, *args):
   if expr.startswith("set:"):
     return dataset_builder(expr[4:])
   if expr.startswith("stream:"):
     return datastream_builder(expr[7:])
   if expr.startswith("index:"):
     return index_builder(expr[6:])
   if expr.startswith("aggregate:"):
     return aggregate_builder(expr[10:])

   if expr.startswith("dataset:"):
     return dataset_builder(expr[8:])
   if expr.startswith("datastream:"):
     return datastream_builder(expr[11:])

   raise ValueError("expression must start with set: or stream:")

