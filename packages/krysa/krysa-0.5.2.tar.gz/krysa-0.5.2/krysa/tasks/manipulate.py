from . import Task, SortLayout, AppendLayout, StandLayout
from kivy.uix.tabbedpanel import TabbedPanelItem
from functools import partial


class Manipulate(object):
    '''All :ref:`Task` s categorized as being able to `manipulate` data.
    A result after manipulation is a new data.

    .. versionadded:: 0.3.5
    '''

    def manip_sort(*args):
        '''Opens a :mod:`tasks.Task` with a :mod:`tasks.SortLayout` that gets
        from user the table which will be sorted and the type of sorting
        (`Ascending` or `Descending`). The function creates a new
        :mod:`main.Table`

        .. versionadded:: 0.3.5
        '''
        widget = SortLayout()
        task = Task(title='Sort', wdg=widget,
                    call=['Sort', Manipulate.manip_sort])
        task.tablecls = task.app.tablecls
        container = task.ids.container.children[0]
        task.run = partial(Manipulate._manip_sort,
                           task,
                           container.ids.sort_type)
        task.open()

    @staticmethod
    def _manip_sort(task, sort_type, *args):
        sort_type = 'Asc' not in sort_type.text
        from_address = task.from_address(task.tablenum, ':all', extended=True)
        values, cols, rows, labels = from_address

        # get separated cols to sort
        chunks = []
        for x in xrange(0, len(values), rows):
            chunks.append(values[x:x + rows])

        values = []
        for val in chunks:
            values.append(sorted(val, reverse=sort_type))

        # add Table
        table = task.ids.tablesel.text
        table += ' (desc)' if sort_type else ' (asc)'
        tabletab = TabbedPanelItem(text=table)
        task.app.root.ids.tabpanel.add_widget(tabletab)

        values = zip(*values)
        values = [v for vals in values for v in vals]
        task.app.root.tables.append((
            table, task.tablecls(max_cols=cols, max_rows=rows,
                                 pos=task.app.root.pos,
                                 size=task.app.root.size,
                                 values=values, labels=labels)
        ))
        tabletab.content = task.app.root.tables[-1][1]

    def manip_filter(*args):
        '''(Not yet implemented)
        '''

    def manip_append(*args):
        '''Opens a :mod:`tasks.Task` with a :mod:`tasks.AppendLayout` that gets
        from user :mod:`main.Table`, type of append and an amount of empty
        rows / cols to append.

        The function either returns a new, altered :mod:`main.Table` of
        selected one, or appends directly to the selected :class:`main.Table`.

        .. note:: Appending new columns doesn't work for now. When such
           an action is possible, this note will be removed.

        .. versionadded:: 0.3.6
        .. versionchanged:: 0.3.7
            Added overwriting of selected :mod:`main.Table`
        '''
        widget = AppendLayout()
        task = Task(title='Append', wdg=widget,
                    call=['Append', Manipulate.manip_append])
        task.tablecls = task.app.tablecls
        container = task.ids.container.children[0]
        task.run = partial(Manipulate._manip_append,
                           task,
                           container.ids.what,
                           container.ids.amount,
                           container.ids.overwrite)
        task.open()

    @staticmethod
    def _manip_append(task, append_type, amount, overwrite, *args):
        append_type = append_type.text
        overwrite = overwrite.active
        amount = int(amount.text) if amount.text else 0

        # Stop the task if no amount (or =0) is specified
        if not amount:
            return

        from_address = task.from_address(task.tablenum, ':all',
                                         extended=True)
        values, cols, rows, labels = from_address

        if append_type == 'Columns':
            cols += amount
            return
        elif append_type == 'Rows':
            # get columns
            chunks = []
            for x in xrange(0, len(values), rows):
                chunks.append(values[x:x + rows])

            # append to columns a zero value according
            # to their type int(amount)-times
            for r in range(amount):
                for chunk in chunks:
                    if isinstance(chunk[0], int):
                        chunk.append(0)
                    elif isinstance(chunk[0], float):
                        chunk.append(0.0)
                    else:
                        chunk.append(u'')

            # add Table
            tab_pos = 0
            table = task.ids.tablesel.text
            tabletab = TabbedPanelItem(text=table)
            if overwrite:
                tab_pos = task.tablenum + 1
                old_tab = task.app.root.ids.tabpanel.tab_list[tab_pos]
                task.app.root.ids.tabpanel.remove_widget(old_tab)
            else:
                table += ' (append {})'.format(str(amount))
            task.app.root.ids.tabpanel.add_widget(tabletab, tab_pos)

            # zip chunks to values, flatten values
            values = zip(*chunks)
            values = [v for vals in values for v in vals]

            # increase row count by new rows, make new table
            rows += amount
            new_table = (
                table, task.tablecls(max_cols=cols, max_rows=rows,
                                     pos=task.app.root.pos,
                                     size=task.app.root.size,
                                     values=values, labels=labels)
            )

            # place newly created table into tab's content
            if overwrite:
                task.app.root.tables[tab_pos - 1] = new_table
                tabletab.content = task.app.root.tables[tab_pos - 1][1]
            else:
                task.app.root.tables.append(new_table)
                tabletab.content = task.app.root.tables[-1][1]
        else:
            return

    def manip_split(*args):
        '''(Not yet implemented)
        '''

    def manip_merge(*args):
        '''(Not yet implemented)
        '''

    def manip_stand(*args):
        '''(Not yet implemented)
        Standardizing specified columns from data according to various
        types of standardiztion.
        '''
        widget = StandLayout()
        task = Task(title='Standardize', wdg=widget,
                    call=['Standardize', Manipulate.manip_stand])
        task.tablecls = task.app.tablecls
        container = task.ids.container.children[0]
        task.run = partial(Manipulate._manip_stand,
                           task)
        task.open()

    @staticmethod
    def _manip_stand(task, *args):
        pass

    names = (('Sort', manip_sort),
             ('_Filter', manip_filter),
             ('Append', manip_append),
             ('_Split', manip_split),   # split into two data(columns, rows)
             ('_Merge', manip_merge),
             ('_Standardize', manip_stand))
