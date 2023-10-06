login.ccat = *, all, admin, access 
login.desc = Залогиниться как админиcтратор бота. Использовать только в привате!
login.synt = %prefix%login <пароль>
login.exam = %prefix%login jay63xNer

logout.ccat = *, all, admin, access 
logout.desc = Разлогиниться.
logout.synt = %prefix%logout
logout.exam = %prefix%logout

access.ccat = *, all, admin, access 
access.desc = Показывает уровень доступа определенного ника.\n-100 — полное игнорирование, все сообщения от пользователя с таким доступом будут пропускатся на уровне ядра.\n-1 — не сможет сделать ничего.\n0 — очень ограниченное кол-во команд, автоматически присваивается посетителям (visitor).\n10 — стандартный набор команд, автоматически присваивается участникам (participant).\n11 — расширенный набор команд (например доступ к wtf), автоматически присваивается членам (member).\n15 (16) — модераторский набор команд, автоматически присваивается модераторам (moderator).\n20 — админский набор команд, автоматически присваивается админам (admin).\n30 — овнерский набор команд, автоматически присваиватся овнерам (owner).\n40 — позволяет пользователю с этим доступом заводить и выводить бота из конференций.\n100 — администратор бота, может все.
access.synt = %prefix%access [nick]
access.exam = %prefix%access
access.exam = %prefix%access guy

access_set.ccat = *, all, admin, access 
access_set.desc = Устанавливает или снимает локальный (если ник писать без уровня) уровень доступа для определенного ника на определенный уровень.\n-100 — полное игнорирование, все сообщения от пользователя с таким доступом будут пропускатся на уровне ядра.\n-1 — не сможет сделать ничего.\n0 — очень ограниченное кол-во команд, автоматически присваивается посетителям (visitor).\n10 — стандартный набор команд, автоматически присваивается участникам (participant).\n11 — расширенный набор команд (например доступ к wtf), автоматически присваивается членам (member).\n15 (16) — модераторский набор команд, автоматически присваивается модераторам (moderator).\n20 — админский набор команд, автоматически присваивается админам (admin).\n30 — овнерский набор команд, автоматически присваиватся овнерам (owner).\n40 — позволяет пользователю с этим доступом заводить и выводить бота из конференций.\n100 — администратор бота, может все.
access_set.synt = %prefix%access_set <nick>[:<level>]
access_set.exam = %prefix%access_set guy
access_set.exam = %prefix%access_set guy: 20

gaccess_set.ccat = *, all, superadmin, access 
gaccess_set.desc = Устанавливает или снимает (если ник писать без уровня) глобальный уровень доступа для определенного ника на определенный уровень.
gaccess_set.synt = %prefix%gaccess_set <nick>[:<level>]
gaccess_set.exam = %prefix%gaccess_set guy
gaccess_set.exam = %prefix%gaccess_set guy: 15

cmd_access.ccat = *, all, superadmin, access
cmd_access.desc = Устанавливает или показывает уровень доступа к определенной команде. Без параметров выводит весь список команд с доступами.
cmd_access.synt = %prefix%cmd_access [<cmd>[<level>]]
cmd_access.exam = %prefix%cmd_access
cmd_access.exam = %prefix%cmd_access test
cmd_access.exam = %prefix%cmd_access echo 30
    