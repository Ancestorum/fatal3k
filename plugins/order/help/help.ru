filt.ccat = *, all, admin, muc, order
filt.desc = Включает или отключает определенные фильтры для конференции.\ntime — временной фильтр;\nlen — количественный фильтр;\npresence — фильтр презенсов;\nlike — фильтр одинаковых сообщений;\ncaps — фильтр капса (ЗАГЛАВНЫХ букв);\nprsstlen — фильтр длинных статусных сообщений;\nprscaps — фильтр пустых капсов в презенсах;\nobscene — фильтр матов;\nfly — фильтр полётов (частых входов/выходов в конмату), имеет два режима ban и kick, таймер от 0 до 120 секунд;\nkicks — автобан после N киков, параметр cnt - количество киков от 1 до 10;\nidle — кик за молчание в общем чате после N секунд, параметр time - кол-во секунд для срабатывания;\nnick — фильтр ограничения на длину ника, имеет три режима ban, kick и visitor, параметр len позволяет задать ограничение в символах.\nspace — фильтр ограничения на пробелы по краям ника, имеет два режима kick и ban.\nstrict — режим строгой фильтрации, при которой фильтры применяются и к постоянным участникам, т.е. к пользователям с рангом member.
filt.synt = %prefix%filt [<фильтр> [<режим> [<состояние>]]]
filt.exam = %prefix%filt len 0
filt.exam = %prefix%filt fly mode ban
