from onderwijsscrapers.codebooks import load_codebook, Codebook
import csv

"""
    Usage:
    python codebook_test.py <codebook path> <table file> <filter> <# head rows>
"""

if __name__ == '__main__':
    import sys, StringIO
    import pprint
    pp = pprint.PrettyPrinter()

    def print_schema(sch, n=0):
        print ' '*n, sch.name, '(%s)' % type(sch.typ).__name__
        for s in sch:
            if type(sch.typ).__name__ in ['Mapping', 'Sequence']:
                print_schema(s, n+1)

    if len(sys.argv)>1:
        cb = load_codebook(sys.argv[1])

        pp.pprint(cb)
        print_schema(cb.schema(root=True))
        from onderwijsscrapers.tabular_utilities import get_tables, next_n_extended
        from os.path import splitext
        root, ext = splitext(sys.argv[2])
        argv = dict(enumerate(sys.argv))
        filt = argv.get(3, None)
        head_rows = int(argv.get(4, 1))

        for table in get_tables(open(sys.argv[2]), ext, filt=filt):
            rows = table.rows()
            # head = next(rows)
            head = [';'.join(f) for f in next_n_extended(rows, head_rows)]
            key, val = next(cb.parse(head, rows))
            print key
            print cb.schema(root=False).deserialize(val)
    else:

        book = """field;keyed;source;type;description
board_id;0;BEVOEGD GEZAG NUMMER;int;
vavo;;AANTAL LEERLINGEN;int;
"""
        table = """BEVOEGD GEZAG NUMMER;AANTAL LEERLINGEN
1;10
2;20
"""

        cb = Codebook(csv.DictReader(StringIO.StringIO(book), delimiter=';'))
        pp.pprint(cb)
        print_schema(cb.schema(root=True))
        t = csv.reader(StringIO.StringIO(table), delimiter=';')
        for l in cb.parse(next(t), t):
            print l

        # artificial
        book = """field;keyed;source;type;description
board_id;0;BEVOEGD GEZAG NUMMER;int;
reference_year;0;JAAR;int;
student_year;1;LEERJAAR;int;
vavo;;AANTAL LEERLINGEN;int;
non_vavo;;NIET VAVO;int;
"""
        table = """BEVOEGD GEZAG NUMMER;JAAR;LEERJAAR;AANTAL LEERLINGEN;NIET VAVO
1;2014;1;10;40
2;2014;1;20;70
2;2014;2;4;34
"""
        cb = Codebook(csv.DictReader(StringIO.StringIO(book), delimiter=';'))
        pp.pprint(cb)
        print_schema(cb.schema(root=True))
        t = csv.reader(StringIO.StringIO(table), delimiter=';')
        for l in cb.parse(next(t), t):
            print l

        
