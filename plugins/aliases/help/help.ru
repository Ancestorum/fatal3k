alias_add.ccat = *, all, admin, alias, aliases
alias_add.desc = Позволяет добавить локальный алиас, т.е. алиас, который будет работать только в данной конкретной конференции.
alias_add.synt = %prefix%alias_add <имя_алиаса>[:<доступ>] = <тело_алиаса> [$<N>|$*]
alias_add.exam = %prefix%alias_add p = ping $*
alias_add.exam = %prefix%alias_add think = say /me задумался...
alias_add.exam = %prefix%alias_add tsys:30 = sh echo "Passed!"
alias_add.exam = %prefix%alias_add ver = version $1

galias_add.ccat = *, all, superadmin, alias, aliases
galias_add.desc = Позволяет добавить глобальный алиас, т.е. алиас, который будет работать во всех конференциях и в ростере бота.
galias_add.synt = %prefix%galias_add <имя_алиаса>[:<доступ>] = <тело_алиаса> [$<N>|$*]
galias_add.exam = %prefix%galias_add p = ping $*
galias_add.exam = %prefix%galias_add think = say /me задумался...
galias_add.exam = %prefix%galias_add tsys:30 = sh echo "Passed!"
galias_add.exam = %prefix%galias_add ver = version $1

alias_del.ccat = *, all, admin, alias, aliases
alias_del.desc = Позволяет удалить локальный алиас.
alias_del.synt = %prefix%alias_del <имя_алиаса>
alias_del.exam = %prefix%alias_del tsys

galias_del.ccat = *, all, superadmin, alias, aliases
galias_del.desc = Позволяет удалить глобальный алиас.
galias_del.synt = %prefix%galias_del <имя_алиаса>
galias_del.exam = %prefix%galias_del tsys

alias_exp.ccat = *, all, admin, info, alias, aliases
alias_exp.desc = Позволяет развернуть локальный алиас, т.е. посмотреть на готовый алиас в сыром виде.
alias_exp.synt = %prefix%alias_exp <имя_алиаса> [<параметры>]
alias_exp.exam = %prefix%alias_exp tsys
alias_exp.exam = %prefix%alias_exp print Hello!

galias_exp.ccat = *, all, superadmin, info, alias, aliases
galias_exp.desc = Позволяет развернуть глобальный алиас, т.е. посмотреть на него в сыром виде.
galias_exp.synt = %prefix%galias_exp <имя_алиаса> [<параметры>]
galias_exp.exam = %prefix%galias_exp tsys
galias_exp.exam = %prefix%galias_exp print Hello!

alias_show.ccat = *, all, admin, info, alias, aliases
alias_show.desc = Показывает содержимое локального алиаса. Без параметров показывает содержимое всех локальных алиасов.
alias_show.synt = %prefix%alias_show [<имя_алиаса>]
alias_show.exam = %prefix%alias_show
alias_show.exam = %prefix%alias_show tsys

galias_show.ccat = *, all, superadmin, info, alias, aliases
galias_show.desc = Показывает содержимое глобального алиаса. Без параметров показывает содержимое всех глобальных алиасов.
galias_show.synt = %prefix%galias_show [<имя_алиаса>]
galias_show.exam = %prefix%galias_show
galias_show.exam = %prefix%galias_show tsys

alias_list.ccat = *, all, info, alias, aliases
alias_list.desc = Позволяет вывести список всех алиасов, как локальных, так и глобальных.
alias_list.synt = %prefix%alias_list
alias_list.exam = %prefix%alias_list

alias_acc.ccat = *, all, admin, alias, aliases
alias_acc.desc = Позволяет изменить или посмотреть уровень доступа к определенному локальному алиасу.
alias_acc.synt = %prefix%alias_acc <алиас> [<доступ>]
alias_acc.exam = %prefix%alias_acc tsys
alias_acc.exam = %prefix%alias_acc tsys 10

galias_acc.ccat = *, all, superadmin, alias, aliases
galias_acc.desc = Позволяет изменить или посмотреть уровень доступа к определенному глобальному алиасу.
galias_acc.synt = %prefix%galias_acc <алиас> [<доступ>]
galias_acc.exam = %prefix%galias_acc tsys
galias_acc.exam = %prefix%galias_acc tsys 10
