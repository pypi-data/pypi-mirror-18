
from .lib import *
from .util import *
from future.builtins import object

def make_post_request(url, data, auth):
    response = None
    try:
        response = requests.post(url,
                                 data=data,
                                 headers=HEADERS,
                                 auth=auth,
                                 timeout=30)
    except Exception as error:
        print(error)
        traceback.print_exc(file=sys.stdout)
    finally:
        return response

def rowgen(buffer):
    for row in buffer:
        yield row

class Column(object):
    def __init__(self, table, id):
        self.table = table
        self.id = id

    def __init__(self, table, data):
        self.table = table
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.type = data['type']
        self.field = data['sqlname']

    def __str__(self):
        return "%s-%s (%s)" % (self.type, self.field, self.name)

    def __repr__(self):
        return "<quilt.Column %s.%s>" % (self.table.sqlname, self.field)


class Table(object):
    _schema = None
    _quilts = None
    _chr = None
    _start = None
    _end = None
    branch = None
    index = None

    def __init__(self, con, data, branch=None, index=None):
        self.connection = con
        self.id = data.get('id')
        self.name = data.get('name')
        self.sqlname = data.get('sqlname')
        self.description = data.get('description')
        self.owner = data.get('owner')
        self.is_public = data.get('is_public')
        self._reset_iteration()
        self.branch = branch

        if 'columns' in data:
            self._schema = [Column(self, cdata) for cdata in data.get('columns')]

        if 'quilts' in data:
            self._quilts = data.get('quilts')

        if index:
            for col in self.columns:
                if col.field == index:
                    self.index = col
                    break
            if not self.index:
                print("Warning: index column %s not found" % index)

    def __str__(self):
        return "[%04d] %s" % (self.id, self.name)

    def __repr__(self):
        return "<quilt.Table %d.%s>" % (self.id, self.sqlname)

    def __eq__(self, table):
        return self.id == table.id

    def _guess_bed_columns(self):
        for c in self.columns:
            name = c.name.lower()
            if 'chromosome' in name:
                self._chr = c
            elif not self._chr and 'chr' in name:
                self._chr = c

            if 'start' in name and not self._start:
                self._start = c
            elif 'end' in name and not self._end:
                self._end = c
            elif not self._end and 'stop' in name:
                self._end = c

    def delete(self):
        response = requests.delete("%s/tables/%s/" % (self.connection.url, self.id),
                                   headers=HEADERS,
                                   auth=self.connection.auth)
        if response.status_code == requests.codes.no_content:
            self.id = None
            self.name = None
            self.description = None
            self.owner = None
            self.sqlname = None
            self._schema = None
            self._quilts = None
        else:
            print("Oops, something went wrong.")
            print(response.text)

    @property
    def columns(self):
        if not self._schema:
            response = requests.get("%s/tables/%s/" % (self.connection.url, self.id),
                                    headers=HEADERS,
                                    auth=self.connection.auth)
            data = response.json()
            if 'columns' in data:
                self._schema = [Column(self, cdata) for cdata in data.get('columns')]

        for c in self._schema:
            setattr(self, c.field, c)

        return self._schema

    def add_column(self, name, type, field=None, description=None):
        data = { 'name' : name,
                 'type' : type}
        if field:
            data['sqlname'] = field

        if description:
            data['description'] = description

        response = requests.post("%s/tables/%s/columns/" % (self.connection.url, self.id),
                                 headers=HEADERS,
                                 data=json.dumps(data),
                                 auth=self.connection.auth)
        if response.status_code == requests.codes.ok:
            newcol = response.json()
            self._schema = None
            return newcol
        else:
            print("Oops, something went wrong")
            print(response.text)
            return None

    def delete_column(self, column):
        response = requests.delete("%s/tables/%s/columns/%s/" % (self.connection.url, self.id, column.id),
                                   headers=HEADERS,
                                   auth=self.connection.auth)
        if response.status_code == requests.codes.no_content:
            self._schema = None
            return None
        else:
            print("Oops, something went wrong")
            print(response.text)
            return None

    @property
    def quilts(self):
        if not self._quilts is None:
            response = requests.get("%s/tables/%s/" % (self.connection.url, self.id),
                                    headers=HEADERS,
                                    auth=self.connection.auth)
            data = response.json()
            if 'quilts' in data:
                self._quilts = [Quilt(self, d) for d in data.get('quilts')]
            else:
                self._quilts = []
        return self._quilts

    def df(self):
        if not PANDAS:
            print("Install pandas to use DataFrames: http://pandas.pydata.org/")
            return None

        df = None
        if self.connection._sqlengine and self._search is None:
            type_map = {
                'String' : sa.String,
                'Number' : sa.Float,
                'Float' : sa.Float,
                'Integer' : sa.Integer,
                'Unsigned' : sa.Integer,
                'Bool' : sa.Boolean,
                'Text' : sa.Text,
                'Date' : sa.Date,
                'DateTime' : sa.DateTime,
                'Image' : sa.String }

            columns = [sa.Column('qrid', sa.Integer)]
            columns += [sa.Column(c.field, type_map[c.type]) for c in self.columns]
            viewname = "%s_%s" % (self.sqlname, self.branch) if self.branch else self.sqlname
            table = sa.Table(viewname, sa.MetaData(),*columns)

            stmt = sa.select([table])
            if self._ordering_fields:
                ordering_clause = []
                for f in self._ordering_fields:
                    if f.startswith("-"):
                        fname = f.lstrip("-")
                        ordering_clause.append(getattr(table.c, fname).desc())
                    else:
                        ordering_clause.append(getattr(table.c, f).asc())
                stmt = stmt.order_by(*ordering_clause)

            if self._limit is not None:
                stmt = stmt.limit(self._limit)

            idx = self.index.field if self.index else 'qrid'
            try:
                df = pd.read_sql(stmt, self.connection._sqlengine, index_col=idx)
            except:
                pass

        if df is None:
            data = []
            index = []
            columns = [c.field for c in self.columns]
            for i, row in enumerate(self):
                index.append(row['qrid'])
                data.append(row)
            df = pd.DataFrame(data, columns=columns, index=index)

        return df

    def __getitem__(self, iloc):
        if self.index:            
            response = requests.get("%s/data/%s/rows/?%s=%s" % (self.connection.url,
                                                                self.id,
                                                                self.index.field,
                                                                iloc),
                                    headers=HEADERS,
                                    auth=self.connection.auth)            
        else:
            response = requests.get("%s/data/%s/rows/%s/" % (self.connection.url, self.id, iloc),
                                    headers=HEADERS,
                                    auth=self.connection.auth)
        if response.status_code == requests.codes.ok:
            data = response.json()
            if 'results' in data:
                return data['results']
            else:
                return data
        else:
            print("Oops, something went wrong.")
            return response

    def __setitem__(self, iloc, newvalues):
        data=json.dumps(newvalues)
        if self.index:
            qrid = None
            response = requests.get("%s/data/%s/rows/?%s=%s" % (self.connection.url,
                                                                self.id,
                                                                self.index.field,
                                                                iloc),
                                    headers=HEADERS,
                                    auth=self.connection.auth)
            if response.status_code == requests.codes.ok:
                searchdata = response.json()
                matches = searchdata['results']
                if len(matches) == 1:
                    qrid = matches[0]['qrid']
                else:
                    print("%s=%s does not specify a unique row!")
                    return
            else:
                print("Oops, something went wrong getting qrid.")
                return response
        else:
            qrid = iloc

        response = requests.patch("%s/data/%s/rows/%s/" % (self.connection.url, self.id, qrid),
                                  data=data,
                                  headers=HEADERS,
                                  auth=self.connection.auth)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            print("Oops, something went wrong in patch.")
            self.error = response
            return response

    def __delitem__(self, qrid):
        response = requests.delete("%s/data/%s/rows/%s/" % (self.connection.url, self.id, qrid),
                                   headers=HEADERS,
                                   auth=self.connection.auth)
        return response.status_code

    def __iter__(self):
        self._buffer = []
        self._generator = rowgen(self._buffer)
        if self.branch:
            self.nextlink = "%s/data/%s/branches/%s/rows/" % (self.connection.url, self.id, self.branch)
        else:
            self.nextlink = "%s/data/%s/rows/" % (self.connection.url, self.id)
        return self

    def _genemath(self, b, operator):
        a_chr, a_start, a_end = self.get_bed_cols()
        if not (a_chr and a_start and a_end):
            print("Chromosome, start, stop columns not found.")
            return

        b_chr, b_start, b_end = b.get_bed_cols()
        if not (b_chr and b_start and b_end):
            print("Chromosome, start, stop columns not found in table %s." % b.name)
            return

        data = { 'left_chr' : a_chr.id,
                 'left_start' : a_start.id,
                 'left_end' : a_end.id,
                 'right_chr' : b_chr.id,
                 'right_start' : b_start.id,
                 'right_end' : b_end.id,
                 'operator' : operator }
        response = requests.post("%s/genemath/" % self.connection.url,
                                 data = json.dumps(data),
                                 headers=HEADERS,
                                 auth=self.connection.auth)
        if response.status_code == requests.codes.ok:
            data = response.json()
            result_table_id = data.get('table')
            result = self.connection.get_table(result_table_id)
            return result
        else:
            print("Oops, something went wrong")
            return response

    def export(self):
        response = requests.get("%s/data/%s/rows/export" % (self.connection.url, self.id),
                                headers=HEADERS,
                                auth=self.connection.auth)
        return File(self.connection, response.json())

    def order_by(self, fields):
        if not fields:
            self._ordering_fields = []
        elif isinstance(fields, list):
            self._ordering_fields = fields
        else:
            self._ordering_fields = [fields]
        return self.__iter__()

    def search(self, term):
        self._search = term
        return self.__iter__()

    def limit(self, limit):
        self._limit = limit
        return self

    @property
    def commits(self):
        branch = self.branch if self.branch else 'master'
        response = requests.get("%s/data/%s/branches/%s/commits/" % (self.connection.url,
                                                                     self.id,
                                                                     branch),
                                headers=HEADERS,
                                auth=self.connection.auth)
        if response.status_code == requests.codes.ok:
            # We'll need to handle paging for large commit histories
            return response.json()['results']
        else:
            print("Oops, something went wrong.")
            return response

    def commit(self, message):
        branch = self.branch if self.branch else 'master'
        data = {'message' : message}
        response = requests.post("%s/data/%s/branches/%s/commits/" % (self.connection.url,
                                                                      self.id,
                                                                      branch),
                                 data = json.dumps(data),
                                 headers=HEADERS,
                                 auth=self.connection.auth)

    def create_branch(self, name, parent=None):
        data = {'table_id' : self.id,
                'name' : name}
        if parent:
            data['parent'] = parent

        response = requests.post("%s/data/%s/branches/" % (self.connection.url, self.id),
                                 data = json.dumps(data),
                                 headers=HEADERS,
                                 auth=self.connection.auth)
        if response.status_code == requests.codes.ok:
            self.__iter__()
            branch = Branch(self, response.json())
            self.branch = branch.name
        else:
            print("Oops, something went wrong.")

        return response

    def get_branch(self, name):
        response = requests.get("%s/data/%s/branches/%s" % (self.connection.url, self.id, name),
                                headers=HEADERS,
                                auth=self.connection.auth)
        if response.status_code == requests.codes.ok:
            return Branch(self, response.json())
        else:
            print("Oops, something went wrong.")
            return response

    def checkout(self, commit):
        branch = self.branch if self.branch else 'master'
        data = {}
        response = requests.post("%s/data/%s/branches/%s/commits/%s/checkout/" % (self.connection.url,
                                                                                  self.id,
                                                                                  branch,
                                                                                  commit),
                                 data = json.dumps(data),
                                 headers=HEADERS,
                                 auth=self.connection.auth)
        if response.status_code == requests.codes.ok:
            self.__iter__()
        else:
            print("Oops, something went wrong.")
            return response

    def _reset_iteration(self):
        self._buffer = []
        self._limit = None
        self._count = 0
        self._search = None
        self._ordering_fields = []

    def __at_limit(self):
        return (self._limit is not None and self._count >= self._limit)

    def __nextrow(self):
        row = next(self._generator)
        self._count += 1
        return row

    def __next__(self):
        if self.__at_limit():
            self._reset_iteration()
            raise StopIteration()

        try:
            return self.__nextrow()
        except StopIteration:
            if self.nextlink:
                assert not self.__at_limit(), "Already checked for limit"
                params = {}
                if self._ordering_fields:
                    params['ordering'] = [f for f in self._ordering_fields]

                if self._search:
                    params['search'] = self._search

                response = requests.get(self.nextlink,
                                        headers=HEADERS,
                                        params=params,
                                        auth=self.connection.auth)
                data = response.json()
                self.nextlink = data['next']
                self._buffer = []
                for row in data['results']:
                    self._buffer.append(row)
                self._generator = rowgen(self._buffer)
                return self.__nextrow()
            else:
                self._reset_iteration()
                raise StopIteration()

    def create(self, data):
        if self.branch:
            response = requests.post("%s/data/%s/branches/%s/rows/" % (self.connection.url,
                                                                       self.id,
                                                                       self.branch),
                                     data = json.dumps(data),
                                     headers=HEADERS,
                                     auth=self.connection.auth)
        else:
            response = requests.post("%s/data/%s/rows/" % (self.connection.url, self.id),
                                     data = json.dumps(data),
                                     headers=HEADERS,
                                     auth=self.connection.auth)

        return response

    def create_json(self, jsondata):
        response = requests.post("%s/data/%s/rows/" % (self.connection.url, self.id),
                                 data = jsondata,
                                 headers=HEADERS,
                                 auth=self.connection.auth)

        return response


    def create_async(self, data, callback=None):
        """
        Use an asynchronous POST request with the process pool.
        """
        url = "%s/data/%s/rows/" % (self.connection.url, self.id)
        res = self.connection.get_thread_pool().apply_async(make_post_request,
                                                            args=(url, json.dumps(data), self.connection.auth),
                                                            callback=callback)
        return res

    def create_json_async(self, jsondata, callback=None):
        """
        Use an asynchronous POST request with the process pool.
        """
        url = "%s/data/%s/rows/" % (self.connection.url, self.id)
        res = self.connection.get_thread_pool().apply_async(make_post_request,
                                                            args=(url, jsondata, self.connection.auth),
                                                            callback=callback)
        return res

    def quilt(self, left_column, right_column):
        data = {}
        data['left_table'] = self.id
        data['left_column'] = left_column.id
        data['right_column'] = right_column.id

        response = requests.post("%s/quilts/" % self.connection.url,
                                 data = json.dumps(data),
                                 headers=HEADERS,
                                 auth=self.connection.auth)
        if response.status_code == requests.codes.ok:
            i = self.__iter__() # reset iterator
            data=response.json()
            q = Quilt(self, data)
            if self.quilts is not None:
                self.quilts.append(q)
            return q
        else:
            print("Oops, something went wrong.")
            print("response=%s" % response.status_code)
            return None

    def set_bed_cols(self, chr, start, end):
        self._chr = chr.id
        self._start = start.id
        self._end = end.id

    def get_bed_cols(self):
        if not (self._chr and self._start and self._end):
            self._guess_bed_columns()
        return self._chr, self._start, self._end

    def intersect(self, b):
        return self._genemath(b, 'Intersect')

    def subtract(self, b):
        return self._genemath(b, 'Subtract')

    def intersect_wao(self, b):
        return self._genemath(b, 'Intersect_WAO')
