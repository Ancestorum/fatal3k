watcher.ccat = superadmin, all, *
watcher.desc = Позволяет удаленно в реальном времени наблюдать за другими конференциями в которых бот, т.е. устанавливает наблюдателя. Без параметров выводит список конференций в которых установлен наблюдатель. При указании отрицательного числа удаляет конференцию с этим номером из списка и снимает наблюдение.
watcher.synt = %prefix%watcher [<конференция>]|[-|-<номер из списка>]
watcher.exam = %prefix%watcher
watcher.exam = %prefix%watcher conf@conference.jabber.aq
watcher.exam = %prefix%watcher -2
watcher.exam = %prefix%watcher -
