acomm.ccat = *, all, admin, acomm
acomm.desc = Позволяет автоматически запускать команды если найдено совпадение с регулярным выражением в одной из следующих групп:\n\nbody - сообщения в общем чате. При указании параметров к команде допустимо использование с параметрами следующих строк замены: %body%, %groupchat%, %nick%, %jid%.\nstatus - статусное сообщение пользователей. При указании параметров к команде допустимо использование с параметрами следующих строк замены: %status%, %groupchat%, %nick%, %jid%.\nnick - ники пользователей. При указании параметров к команде допустимо использование с параметрами следующих строк замены: %groupchat%, %nick%, %jid%.\njid - джиды пользователей. При указании параметров к команде допустимо использование с параметрами следующих строк замены: %groupchat%, %nick%, %jid%.\ncvar - отслеживает изменение переменной или в выводе, который возвращает функция или вложенная команда, если изменения есть, выполняет команду.
acomm.synt = %prefix%acomm [[[<body>|]<status>|<nick>|<jid>|<cvar>]: <regexp>|<words>|<python>|<nested_command> := <command> [<parameters>] | -<number> | -]
acomm.exam = %prefix%acomm
acomm.exam = %prefix%acomm [Зз]дорово! := echo %nick%: И ты не болей!
acomm.exam = %prefix%acomm [Сс]ука := kick %nick%: Сам такой!
acomm.exam = %prefix%acomm jid: some@server\.tld := echo %nick%: Привееет!
acomm.exam = %prefix%acomm jid: some@server\.tld := member %jid%
acomm.exam = %prefix%acomm nick: guy := message admin@server.tld Юзер %nick% появился в конфе %groupchat%!
acomm.exam = %prefix%acomm body: [Гг][Гг] := echo %nick%: Гуси в другой конференции!
acomm.exam = %prefix%acomm cvar: get_revision() := say Вышла новая ревизия бота!
acomm.exam = %prefix%acomm cvar: #sh::git rev-list --count main# := say Вышла новая ревизия бота!
acomm.exam = %prefix%acomm -2
acomm.exam = %prefix%acomm -
