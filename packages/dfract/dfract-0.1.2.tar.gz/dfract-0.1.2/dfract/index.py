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
class Index:
    """
    In DFRACT,
    Indexes are object that return efficiently and accurayely keys according to values or expressions based on values.
    
    They can be associated to datasets and datastreams to allow to find keys that match some criteria based on values.

    There are so many possible type of static that we can't really provide a precise language that will
    support all the types of static that can be imagined
    We recommend using expressions based on documents to create queries (similar to mongo queries). 
    
    
    Indexers may not this convention However respecting it  for query could hopefully favor 
    interoperability between different index systems.
    
    # ...
    {"$value": an expression describing single value to be matched }
    {"x": {"$in": { "$type": "ball", "$center": {}, "$radius":5 } }
    
    
    Each index has different feature.

    Example of indexes include:
        - hash tables based on strings
        - geospatial queries from point, or region
        - graph queries
        - ...


    The fact that an index is associated to a dataset should be persistable across versions of the datasets.
    It would be memorise in the metadata associated with the dataset. Initiating the creation of updated datasets
    should probably be the responsibility of the dfract server. While this class should focus on basic logic for versionning.

    """
    _incremental_index = False  # set to true if the index can be built as an incrementl index and can improve an existing index
                               # incremental index are not yet implemented they will ideally imply some kind of reference counting
    # they should rely on dfract versionning and or datastreams API

    def __getitem__(self, query):
        return self.get_single_exact(query)

    def build_index(self):
        assert False

    def on_new_dataset_version(self, *args):
        if self._incremental_index:
            self.create_diff_index()

    ##  Additional syntaxic sugar optional
    def get_single_exact(self,query):
        """
        Returns a single element solving query.
        """
        return self.get_exact(query, 1)[0]

    
    def get_exact(self,query, n):
        """
        Returns multiple elements approximatively solving query.
        Also returns the distances of the elements.
        """
        pass            
    
    
    
    def get_single_approximate(self,query):
        """
        Returns a single element approximatively solving query.
        Also returns its distance
        """
        return self.get_approximate(query, 1)[0]
    
    def get_approximate(self,query, n):
        """
        Returns multiple elements approximatively solving query.
        Also returns the distances of the elements.
        """
        pass            
    
    
    def get_single_near(self,query, maxdist):
        """
        Returns a single element approximatively solving query 
        and at most distant of maxdist from the query.
        Also returns its distance
        """
        return self.get_near(query, maxdist, 1)[0]
    
    def get_near(self,query, maxdist, n):
        """
        Returns multiple elements approximatively solving query 
        and at most distant of maxdist from the query.
        
        Also returns the distances of the elements.
        """
        pass                
    