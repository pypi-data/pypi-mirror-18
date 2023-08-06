from nbodykit.core import Algorithm, DataSource
import numpy


class Describe(Algorithm):
    """
    A simple example Algorithm that loads a specific column
    from a DataSource and prints the min/max of the column
    """
    plugin_name = "Describe"

    def __init__(self, datasource, column='Position'):
        
        self.datasource = datasource
        self.column     = column

    @classmethod
    def fill_schema(cls):
        s = cls.schema
        s.description = "describe a specific column of the input DataSource"
        s.add_argument("datasource", type=DataSource.from_config, 
            help='the DataSource to describe; run `nbkit.py --list-datasources` for all options')
        s.add_argument("column", type=str, 
            help='the column in the DataSource to describe')
     
    def run(self):
        """
        Run the algorithm, which does nothing
        """
        left = []
        right = []
        with self.datasource.open() as stream:
            for [col] in stream.read([self.column]):
                left.append(numpy.min(col, axis=0))
                right.append(numpy.max(col, axis=0))
            left = numpy.min(left, axis=0)
            right = numpy.max(right, axis=0)
            left = numpy.min(self.comm.allgather(left), axis=0)
            right = numpy.max(self.comm.allgather(right), axis=0)
        return left, right

    def save(self, output, data):
        left, right = data
        if self.comm.rank == 0:
            template = "DataSource %s Column %s : min = %s max = %s\n"
            if output == '-' or output is None:
                import sys
                output = sys.stdout
            else:
                output = open(output, 'w')
            args = (self.datasource.plugin_name, self.column, str(left), str(right))
            output.write(template %args)

