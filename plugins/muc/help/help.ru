kick.ccat = admin, all, *, muc
kick.desc = Кикнуть дебошира!
kick.synt = %prefix%kick <nick>[:<reason>]
kick.exam = %prefix%kick guy
kick.exam = %prefix%kick guy: Первый пошел!!!

ban.ccat = admin, all, *, muc
ban.desc = Забанить дебошира по нику (nick) или джиду (jid)! Также позволяет банить jabber-сервер целиком, указав его джид.
ban.synt = %prefix%ban <nick>|<jid> [:<reason>]
ban.exam = %prefix%ban guy
ban.exam = %prefix%ban guy: Тебе тут не место!
ban.exam = %prefix%ban spam@jabber.aq
ban.exam = %prefix%ban spam@jabber.aq: Пшел!
ban.exam = %prefix%ban jabber.aq

visitor.ccat = admin, all, *, muc
visitor.desc = Забрать у дебошира право говорить!
visitor.synt = %prefix%visitor <nick>
visitor.exam = %prefix%visitor guy
visitor.exam = %prefix%avisitor
visitor.exam = %prefix%avisitor guy
visitor.exam = %prefix%avisitor .*@jabber\.aq

participant.ccat = admin, all, *, muc
participant.desc = Возвращает положение занимаемое участником в первоначально состояние, т.е. участник (participant).
participant.synt = %prefix%participant <nick>
participant.exam = %prefix%participant guy

unban.ccat = admin, all, *, muc
unban.desc = Достать засранца из бани! Также позволяет разбанить jabber-сервер целиком, указав его джид.
unban.synt = %prefix%unban <jid>
unban.exam = %prefix%unban guy@jabber.aq
unban.exam = %prefix%unban jabber.aq

none.ccat = admin, all, *, muc
none.desc = Понизить положение участника до самого низкого, т.е. никто(none).
none.synt = %prefix%none <nick>|<jid>
none.exam = %prefix%none guy
none.exam = %prefix%none pinguin@jabber.ru

member.ccat = admin, all, *, muc
member.desc = Повысить ранг участника с none до ранга member, т.е. сделать постоянным участником!
member.synt = %prefix%member <nick>|<jid>[:<reason>]
member.exam = %prefix%member guy
member.exam = %prefix%member guy: Радуйся, теперь ты мембер!
member.exam = %prefix%member pinguin@jabber.aq
member.exam = %prefix%member pinguin@jabber.aq: Так надо!

moderator.ccat = admin, all, *, muc
moderator.desc = Повысить положение занимаемое участником с participant до положения moderator, т.е. сделать временным модератором, до выхода из конференции.
moderator.synt = %prefix%moderator <nick>
moderator.exam = %prefix%moderator guy

admin.ccat = superadmin, all, *, muc
admin.desc = Повысить ранг участника с none или member до ранга admin, т.е. сделать админом конференции и постоянным модератором.
admin.synt = %prefix%admin <nick>|<jid>[:<reason>]
admin.exam = %prefix%admin guy
admin.exam = %prefix%admin guy: Радуйся, теперь ты админ!
admin.exam = %prefix%admin pinguin@jabber.aq
admin.exam = %prefix%admin pinguin@jabber.aq: Одмин суров и бородат!

owner.ccat = superadmin, all, *, muc
owner.desc = Повысить ранг участника до высшего - owner, т.е. сделать хозяином конференции.
owner.synt = %prefix%owner <nick>|<jid>[:<reason>]
owner.exam = %prefix%owner guy
owner.exam = %prefix%owner guy: Нащяльника!
owner.exam = %prefix%owner pinguin@jabber.aq
owner.exam = %prefix%owner pinguin@jabber.aq: Главный!

subject.ccat = admin, all, *, muc, info
subject.desc = Устанавливает тему (топик) в конференции. Без параметров выводит текущую тему конференции.
subject.synt = %prefix%subject [<subject>]
subject.exam = %prefix%subject
subject.exam = %prefix%subject Пустая тема.

akick.ccat = admin, all, *, muc
akick.desc = Добавляет правило в список автокиков, может быть как любым словом, так и регулярным выражением. Без параметров выводит список правил. При указании отрицательного числа удаляет правило с номером после "-" из списка правил. При указании "-" без числа очищает список правил.
akick.synt = %prefix%akick [<word>|<regexp>[:reason]]
akick.exam = %prefix%akick
akick.exam = %prefix%akick guy
akick.exam = %prefix%akick guy: Тебя тут не ждут!
akick.exam = %prefix%akick .*@jabber\.ru
akick.exam = %prefix%akick .*@jabber\.aq: Opa-opa!
akick.exam = %prefix%akick -3
akick.exam = %prefix%akick -

amoderator.ccat = admin, all, *, muc
amoderator.desc = Добавляет правило в список автомодераторов, может быть как любым словом, так и регулярным выражением. Без параметров выводит список правил. При указании отрицательного числа удаляет правило с номером после "-" из списка правил. При указании "-" без числа очищает список правил.
amoderator.synt = %prefix%amoderator [<word>|<regexp>]
amoderator.exam = %prefix%amoderator
amoderator.exam = %prefix%amoderator .*@jabber\.aq
amoderator.exam = %prefix%amoderator guy
amoderator.exam = %prefix%amoderator -3
amoderator.exam = %prefix%amoderator -

avisitor.ccat = admin, all, *, muc
avisitor.desc = Добавляет правило в список автовизитеров, может быть как любым словом, так и регулярным выражением. Без параметров выводит список правил. При указании "-" без числа очищает список правил. При указании отрицательного числа удаляет правило с номером после "-" из списка правил.
avisitor.synt = %prefix%avisitor [<word>|<regexp>]
avisitor.exam = %prefix%avisitor
avisitor.exam = %prefix%avisitor .*@jabber\.aq
avisitor.exam = %prefix%avisitor guy
avisitor.exam = %prefix%avisitor -3
avisitor.exam = %prefix%avisitor -

aban.ccat = admin, all, *, muc
aban.desc = Добавляет правило в список автобанов, может быть как любым словом, так и регулярным выражением. Без параметров выводит список правил. При указании отрицательного числа удаляет правило с номером после "-" из списка правил. При указании "-" без числа очищает список правил.
aban.synt = %prefix%aban [<word>|<regexp>[:<reason>]]
aban.exam = %prefix%aban
aban.exam = %prefix%aban guy
aban.exam = %prefix%aban guy: Хоп-хоп!
aban.exam = %prefix%aban .*@jabber\.aq
aban.exam = %prefix%aban .*@jabber\.aq: Таким как ты вход заказан!

avoice.ccat = admin, all, *, muc
avoice.desc = Позволяет включить или выключить функцию автоголоса. По-умолчанию отключена. Без параметров выводит текущее состояние. Описание: Если в конференцию входят пользователи с ролью visitor, то они получают возможность посылать сообщения в общий чат через время в диапазоне от 3 до 300 секунд. Время ожидания по-умолчанию 15 секунд.
avoice.synt = %prefix%avoice [1|0]
avoice.exam = %prefix%avoice
avoice.exam = %prefix%avoice 1
avoice.exam = %prefix%avoice 0

avtime.ccat = admin, all, *, muc
avtime.desc = Позволяет установить время ожидания для функции автоголоса в диапазоне от 3 до 300 секунд, по-умолчанию равно 15-ти секундам. Без параметров выводит текущее время ожидания.
avtime.synt = %prefix%avtime [3-300]
avtime.exam = %prefix%avtime
avtime.exam = %prefix%avtime 10
avtime.exam = %prefix%avtime 80

regvoice.ccat = admin, all, *, muc
regvoice.desc = Позволяет включить или выключить функцию регистрации голоса. По-умолчанию отключена. Без параметров выводит текущее состояние. Описание: Если в конференцию входят пользователи с ролью visitor, то им в ростер автоматически отсылается вопрос, при правильном ответе они получают возможность посылать сообщения в общий чат.
regvoice.synt = %prefix%regvoice [1|0]
regvoice.exam = %prefix%regvoice
regvoice.exam = %prefix%regvoice 1
regvoice.exam = %prefix%regvoice 0

rvquest.ccat = admin, all, *, muc
rvquest.desc = Позволяет установить вопрос для функции регистрации голоса. По-умолчанию: 2+2*2 = ?. Без параметров выводит текущий установленный вопрос.
rvquest.synt = %prefix%rvquest [<text>]
rvquest.exam = %prefix%rvquest
rvquest.exam = %prefix%rvquest Сколько на небе звезд?

rvansw.ccat = admin, all, *, muc
rvansw.desc = Позволяет установить ответ на вопрос для функции регистрации голоса. По-умолчанию: 6. Без параметров выводит текущий установленный ответ.
rvansw.synt = %prefix%rvansw [<text>]
rvansw.exam = %prefix%rvansw
rvansw.exam = %prefix%rvansw уйма

rvmess.ccat = admin, all, *, muc
rvmess.desc = Позволяет установить сообщение-запрос в который будет вставлен вопрос для функции регистрации голоса. Без параметров выводит текущее установленное сообщение. Допустимо использовать строки замены, которые будут заменены на реальные значения: %nick% - заменится на ник пользователя которому предназначен запрос, %conf% - заменится на жид текущей конференции, %tries% - заменится на количество попыток. Эти строки могут отсутствовать, впрочем как и сообщение-запрос.
rvmess.synt = %prefix%rvmess [<text>]
rvmess.exam = %prefix%rvmess
rvmess.exam = %prefix%rvmess Привет, %nick%, ты вошел в %conf%, ответь на вопрос и общайся, у тебя %tries% попытки!

rvtries.ccat = admin, all, *, muc
rvtries.desc = Позволяет установить число попыток ответа на вопрос для функции регистрации голоса. По-умолчанию: 3. Без параметров выводит текущее установленное число. При значении равном 0, число попыток бесконечно.
rvtries.synt = %prefix%rvtries [<число>]
rvtries.exam = %prefix%rvtries
rvtries.exam = %prefix%rvtries 8
