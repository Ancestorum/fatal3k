censor.ccat = *, all, admin, censor 
censor.desc = Цензор. Позволяет задавать правила в конфереции, чтобы фильтровать нежелательные сообщения, ники, статусы.
censor.synt = %prefix%censor [[<regexp>|<word>[:<reason>]]|[-|-<number>]]
censor.exam = %prefix%censor
censor.exam = %prefix%censor [Зз]адница: Тут же дамы!
censor.exam = %prefix%censor [Зз]адница
censor.exam = %prefix%censor -3
censor.exam = %prefix%censor -

gcensor.ccat = *, all, superadmin, censor
gcensor.desc = Глобальный цензор. Позволяет глобально задавать правила для всех конференций, чтобы фильтровать нежелательные сообщения, ники, статусы.
gcensor.synt = %prefix%gcensor [[<regexp>|<word>[:<reason>]]|[-|-<number>]]
gcensor.exam = %prefix%gcensor
gcensor.exam = %prefix%gcensor [Зз]адница: Тут же дамы!
gcensor.exam = %prefix%gcensor [Зз]адница
gcensor.exam = %prefix%gcensor -3
gcensor.exam = %prefix%gcensor -

cresult.ccat = *, all, admin, censor
cresult.desc = Реакция цензора. Позволяет задавать реакцию цензора на нежелательные сообщения, ники, статусы.
cresult.synt = %prefix%cresult [kick|ban|visitor|warn|ignore]
cresult.exam = %prefix%cresult
cresult.exam = %prefix%cresult visitor
cresult.exam = %prefix%cresult ignore
