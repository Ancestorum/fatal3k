commands.ccat = help, info, all, *
commands.desc = Показывает список всех категорий команд. При запросе категории показывает список команд находящихся в ней.
commands.synt = %prefix%commands [категория]
commands.exam = %prefix%commands
commands.exam = %prefix%commands *

help.ccat = help, info, all, *
help.desc = Дает основную справку или показывает информацию по использованию определенной команды.
help.synt = %prefix%help [команда]
help.exam = %prefix%help
help.exam = %prefix%help ping

help_cat.ccat = help, info, all, *
help_cat.desc = Показывает список всех доступных категорий команд. При указании команды показывает список категорий к которым она принадлежит. При указании после команды с двоеточием категорий через пробел, добавляет новые категории к команде. При указании после команды отрицательного числа, удаляет категорию с этим номером в списке.
help_cat.synt = %prefix%help_cat [<команда> [-[<номер_из_списка>]]][:<категории>]
help_cat.exam = %prefix%help_cat
help_cat.exam = %prefix%help_cat test
help_cat.exam = %prefix%help_cat test -3
help_cat.exam = %prefix%help_cat test: fun others
help_cat.exam = %prefix%help_cat test -

help_ex.ccat = help, info, all, *
help_ex.desc = Показывает список всех доступных примеров команды. При указании после команды с двоеточием примера использования, добавляет новые примеры использования к команде. При указании после команды отрицательного числа, удаляет пример использования с этим номером в списке. Допустимо использование в примерах строки замены %рrеfiх%, которая заменится на текущий префикс команд.
help_ex.synt = %prefix%help_ex [команда [-номер_из_списка]][:пример]
help_ex.exam = %prefix%help_ex test
help_ex.exam = %prefix%help_ex test -3
help_ex.exam = %prefix%help_ex test: %рrеfiх%test
help_ex.exam = %prefix%help_ex test -

help_syn.ccat = help, info, all, *
help_syn.desc = Позволяет посмотреть или установить общий вид использования команды.
help_syn.synt = %prefix%help_syn [команда][:синтаксис]
help_syn.exam = %prefix%help_syn test
help_syn.exam = %prefix%help_syn test: %рrеfiх%test

help_desc.ccat = help, info, all, *
help_desc.desc = Позволяет посмотреть или установить описание на использование команды.
help_desc.synt = %prefix%help_desc [команда][:описание]
help_desc.exam = %prefix%help_desc test
help_desc.exam = %prefix%help_desc test: Тупо отвечает: Пройден успешно!

help_del.ccat = *, all, help, info
help_del.desc = Позволяет удалить пользовательскую помощь по команде.
help_del.synt = %prefix%help_del <команда>
help_del.exam = %prefix%help_del ping
