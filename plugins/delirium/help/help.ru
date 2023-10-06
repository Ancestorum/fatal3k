poke.ccat = *, all, fun, poke, delirium
poke.desc = Тыкает юзера. Заставляет его обратить внимание на вас/на чат, специально для слоупоков (slow poke). Без парметров покажет список ников, которые тыкали последними.
poke.synt = %prefix%poke [<nick>]
poke.exam = %prefix%poke
poke.exam = %prefix%poke qwerty

poke_add.ccat = *, all, fun, poke, delirium
poke_add.desc = Позволяет добавить пользовательскую фразу. Строка замены %nick% во фразе обозначает место для вставки ника (обязательный параметр). Фраза должна быть написана от третьего лица, т.к. будет использоваться в виде "/me ваша фраза".
poke_add.synt = %prefix%poke_add <фраза>
poke_add.exam = %prefix%poke_add Поцеловал %nick% в щечку!

poke_del.ccat = *, all, fun, poke, delirium
poke_del.desc = Позволяет удалить пользовательскую фразу по номеру из списка.
poke_del.synt = %prefix%poke_del <номер>
poke_del.exam = %prefix%poke_del 5

poke_show.ccat = *, all, fun, poke, delirium
poke_show.desc = Показывает пронумерованный список всех пользовательских фраз.
poke_show.synt = %prefix%poke_show
poke_show.exam = %prefix%poke_show

test.ccat = *, all, fun, poke, delirium
test.desc = Тупо отвечает: Пройден успешно!
test.synt = %prefix%test
test.exam = %prefix%test

clean.ccat = *, all, fun, muc, delirium
clean.desc = Очищает конференцию (втихую).
clean.synt = %prefix%clean
clean.exam = %prefix%clean
