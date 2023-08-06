from webgrid import Column, DateTimeColumn, YesNoColumn
from webgrid.blazeweb import Grid
from webgrid.filters import DateTimeFilter, TextFilter, YesNoFilter

from templatingbwc_ta.model import orm


class Make(Grid):
    Column('Label', orm.Make.label, TextFilter)
    Column('Active', orm.Make.active_flag, YesNoFilter)
    DateTimeColumn('Created', orm.Make.createdts, DateTimeFilter)
    DateTimeColumn('Last Updated', orm.Make.updatedts, DateTimeFilter)
