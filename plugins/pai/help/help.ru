pai.ccat = fun, muc, all, *, pai
pai.desc = Включает и выключает функцию болтливости бота, который выдает случайные фразы на сообщения пользователей. Без параметров показывает текущее значение.
pai.synt = %prefix%pai [1|0]
pai.exam = %prefix%pai
pai.exam = %prefix%pai 1
pai.exam = %prefix%pai 0

pai_learn.ccat = fun, muc, all, *, pai
pai_learn.desc = Включает и выключает обучение болтливости бота, т.е. сохраняет в базе сообщения пользователей, на которые реагирует. Без параметров показывает текущее значение.
pai_learn.synt = %prefix%pai_learn [1|0]
pai_learn.exam = %prefix%pai_learn
pai_learn.exam = %prefix%pai_learn 1
pai_learn.exam = %prefix%pai_learn 0

pai_occ.ccat = fun, muc, all, *, pai
pai_occ.desc = Устанавливает уровень болтливости бота в процентах от 0% до 100%, т.е. чем выше значение этого параметра, тем больше бот будет болтать. Без параметров показывает текущее значение.
pai_occ.synt = %prefix%pai_occ [0-100]
pai_occ.exam = %prefix%pai_occ
pai_occ.exam = %prefix%pai_occ 10
pai_occ.exam = %prefix%pai_occ 80

pai_think.ccat = fun, muc, all, *, pai
pai_think.desc = Устанавливает время на обдумывание фраз пользователей от 4 до 100 сек, т.е. минимальное время на обдумывание - 4 секунды.  Без параметров показывает текущее значение.
pai_think.synt = %prefix%pai_think [4-100]
pai_think.exam = %prefix%pai_think
pai_think.exam = %prefix%pai_think 8
pai_think.exam = %prefix%pai_think 35

pai_ron.ccat = fun, muc, all, *, pai
pai_ron.desc = Добавляет в список слова на которые реагирует бот, т.е. это интерес бота к той или иной теме. Добавляемые слова должны быть разделены пробелом! Без параметров выводит этот список.
pai_ron.synt = %prefix%pai_ron [<слово 1> <слово 2> .. <словоN>]
pai_ron.exam = %prefix%pai_ron
pai_ron.exam = %prefix%pai_ron хозяин
pai_ron.exam = %prefix%pai_ron боты жизнь конфа

pai_roff.ccat = fun, muc, all, *, pai
pai_roff.desc = Добавляет в список слова которые игнорирует бот, т.е. темы, которые не интересуют бота. Если добавить ник, то будет игнорировать сообщения пользователя с этим ником. Добавляемые слова должны быть разделены пробелом! Без параметров выводит этот список.
pai_roff.synt = %prefix%pai_roff [<слово 1> <слово 2> .. <словоN>]
pai_roff.exam = %prefix%pai_roff
pai_roff.exam = %prefix%pai_roff хозяин
pai_roff.exam = %prefix%pai_roff боты жизнь конфа

pai_rond.ccat = fun, muc, all, *, pai
pai_rond.desc = Удаляет слово из списка слов на которые реагирует бот, т.е. бота больше не итересует та или иная тема. Без параметров очищает список.
pai_rond.synt = %prefix%pai_rond [<слово>]
pai_rond.exam = %prefix%pai_rond
pai_rond.exam = %prefix%pai_rond конфа

pai_roffd.ccat = fun, muc, all, *, pai
pai_roffd.desc = Удаляет слово из списка слов которые игнорирует бот, т.е. бота больше не игнорирует сообщения с этим словом. Без параметров очищает список.
pai_roffd.synt = %prefix%pai_roffd [<слово>]
pai_roffd.exam = %prefix%pai_roffd
pai_roffd.exam = %prefix%pai_roffd хозяин

pai_add.ccat = fun, muc, all, *, pai
pai_add.desc = Добавляет фразу а базу, т.е. фразу которой бот будет отвечать на сообщения пользователей.
pai_add.synt = %prefix%pai_add <фраза>
pai_add.exam = %prefix%pai_add Такова жизнь!
pai_add.exam = %prefix%pai_add Эхехехе...

pai_del.ccat = fun, muc, all, *, pai
pai_del.desc = Удаляет фразу из базы по ее номеру, ключевому слову или фразе. Без параметров удаляет последнюю фразу, которой бот отвечал на сообщение пользователя в текущей конференции.
pai_del.synt = %prefix%pai_del [<номер>|<слово>|<фраза>]
pai_del.exam = %prefix%pai_del
pai_del.exam = %prefix%pai_del 1654
pai_del.exam = %prefix%pai_del хрен
pai_del.exam = %prefix%pai_del ты дурак

pai_count.ccat = fun, muc, all, *, pai
pai_count.desc = Показывает количество фраз в базе.
pai_count.synt = %prefix%pai_count
pai_count.exam = %prefix%pai_count

pai_chpm.ccat = fun, muc, all, *, pai
pai_chpm.desc = Позволяет установить псевдо-скорость с которой бот набирает ответ на фразу пользователя, измеряется в знаках в минуту. Без параметров показывает это значение. По-умолчанию 350 знаков в минуту. Минимально возможная скорость 120 зн/мин, максимальная 600 зн/мин.
pai_chpm.synt = %prefix%pai_chpm [<зн/мин>]
pai_chpm.exam = %prefix%pai_chpm
pai_chpm.exam = %prefix%pai_chpm 260
pai_chpm.exam = %prefix%pai_chpm 420

pai_show.ccat = *, all, fun, muc, pai
pai_show.desc = Позволяет просматривать фразы в базе. Без параметров выводит первые 10 фраз, если их больше 10, или все если их меньше 10 и 10 если их всего 10. При указании номера выводит фразу с этим номером. При указании диапазона в формате <начало>-<конец>, выводит фразы начиная с номера заданного границей <начало> и до номера заданного границей <конец>. При указании текста, пытается найти в базе фразы в которых есть совпадения с текстом, выводит первые 10 найденных фраз.
pai_show.synt = %prefix%pai_show [<номер>|<начало>-<конец>|<текст>]
pai_show.exam = %prefix%pai_show
pai_show.exam = %prefix%pai_show 4
pai_show.exam = %prefix%pai_show 3-8
pai_show.exam = %prefix%pai_show что-то
