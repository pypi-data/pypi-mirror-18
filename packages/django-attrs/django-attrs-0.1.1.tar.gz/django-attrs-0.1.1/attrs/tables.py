from tables3.accessors import A
from tables3.columns import LinkColumn
from tables3.tables import Table


class AttrTable(Table):
    name = LinkColumn(viewname='attr_detail', kwargs={'pk': A('pk')})
