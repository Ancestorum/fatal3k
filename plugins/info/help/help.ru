realjid.ccat = *, all, admin, muc, info
realjid.desc = Показывает реальный жид указанного ника. Работает только если бот модератор!
realjid.synt = %prefix%realjid <nick>
realjid.exam = %prefix%realjid guy

users.ccat = *, all, muc, info
users.desc = Показывает количество и ники пользователей находящихся в конференции.
users.synt = %prefix%users
users.exam = %prefix%users

botup.ccat = *, all, admin, info
botup.desc = Показывает сколько времени бот работает без реконнектов и рестартов.
botup.synt = %prefix%botup
botup.exam = %prefix%botup

sestime.ccat = *, all, admin, info
sestime.desc = Позволяет посмотреть сколько времени бот находится в сети, без реконнектов. Не одно и то же, что и время работы.
sestime.synt = %prefix%sestime
sestime.exam = %prefix%sestime

chatrooms.ccat = *, all, admin, info
chatrooms.desc = Показать в каких конференциях находится бот!
chatrooms.synt = %prefix%chatrooms
chatrooms.exam = %prefix%chatrooms

nicks.ccat = *, all, admin, info
nicks.desc = Показать сколько всего пользователей, и какие, были в текущей конференции за последние 3 дня! При указании ника или джида, выводит полный список ников, которые использовал в текущей конференции указанный пользователь.
nicks.synt = %prefix%nicks [<nick>|<jid>]
nicks.exam = %prefix%nicks
nicks.exam = %prefix%nicks guy
nicks.exam = %prefix%nicks guy@jabber.aq

here.ccat = *, all, muc, info
here.desc = Показывает сколько времени провел пользователь в текущей конференции.
here.synt = %prefix%here [<nick>]
here.exam = %prefix%here
here.exam = %prefix%here guy

seen.ccat = *, all, muc, info
seen.desc = Показывает когда как давно пользователь был в текущей конференции и сколько времени в ней находился.
seen.synt = %prefix%seen <nick>|<jid>
seen.exam = %prefix%seen guy
seen.exam = %prefix%seen pinguin@jabber.aq

members.ccat = *, all, muc, info
members.desc = Выводит список джидов (jids) постоянных учаcтников текущей конференции.
members.synt = %prefix%members
members.exam = %prefix%members

admins.ccat = *, all, muc, info
admins.desc = Выводит список джидов (jids) админов текущей конференции.
admins.synt = %prefix%admins
admins.exam = %prefix%admins

owners.ccat = *, all, muc, info
owners.desc = Выводит список джидов (jids) овнеров конференции.
owners.synt = %prefix%owners
owners.exam = %prefix%owners

banned.ccat = *, all, muc, info
banned.desc = Выводит список джидов (jids) изгоев конференции, т.е. тех кто в бане.
banned.synt = %prefix%banned
banned.exam = %prefix%banned

remind.ccat = *, all, muc, info
remind.desc = Выводит в приват сообщение-напоминание, заданное пользователем, через определенный промежуток времени, или в указанное время. Время задается в минутах (если указывается целое число), тогда задается интервал времени через который нужно вывести напоминание, например 2 - напомнить через две минуты, или в формате: <hh:mm:ss|hh:mm|:mm>, тогда задается точное время, когда выводить напоминание, например 22:30 - напомнить в 22:30, :30 - напомнить в 30 минут текущего часа. Чтобы удалить какое-либо напоминание нужно указать номер напоминания со знаком "-" перед номером, чтобы очистить список напоминаний, т.е. удалить все имеющиеся напоминания нужно указать знак "-". Без параметров выводит список назначенных напоминаний. Если дать команду в общем чате, напоминание будет создано для чата - групповое напоминание. 
remind.synt = %prefix%remind [<minutes>|<hh:mm:ss>|<hh:mm>|[:]<mm>|-<номер>|-] [<message>|<command>]
remind.exam = %prefix%remind
remind.exam = %prefix%remind -
remind.exam = %prefix%remind -2
remind.exam = %prefix%remind :20 Уже готово?
remind.exam = %prefix%remind 23:30 Так, 23:30, ты хотел посмотреть интересную передачку по телеку!
remind.exam = %prefix%remind 22:30:10 Самое время для чая ^^
remind.exam = %prefix%remind 10 Хватит ждать, пора!
remind.exam = %prefix%remind 5 ping
remind.exam = %prefix%remind 30 unban some@jabber.aq

ctask.ccat = *, all, muc, info 
ctask.desc = Выводит в приват результат выполнения команды или сообщение, каждые n минут. Время задается в минутах, тогда задается интервал времени через который нужно вывести результат выполнения, например 2. Чтобы удалить какую-либо циклическую задачу нужно указать номер со знаком "-" перед номером, чтобы очистить список циклических задач, т.е. удалить все имеющиеся циклические задачи нужно указать знак "-". Без параметров выводит список циклических задач. Если дать команду в общем чате, циклическая задача будет создана для чата - групповая циклическая задача. При использовании модификатора "q" или "Q" задача выполняется без вывода. Когда в качестве модификатора используется число, задача выполняется заданое этим числом раз.
ctask.synt = %prefix%ctask [<minutes>[:q|Q|0|<num>]|-<номер>|-] [<message>|<command>]
ctask.exam = %prefix%ctask
ctask.exam = %prefix%ctask -
ctask.exam = %prefix%ctask -2
ctask.exam = %prefix%ctask 5 borg
ctask.exam = %prefix%ctask 10 ping
ctask.exam = %prefix%ctask 35:q sh rm -f *.log
ctask.exam = %prefix%ctask 5:15 test

dmess.ccat = *, all, muc, info 
dmess.desc = Включает или отключает автоматическую систему отложенных сообщений.
dmess.synt = %prefix%dmess [1|0]
dmess.exam = %prefix%dmess
dmess.exam = %prefix%dmess 1
dmess.exam = %prefix%dmess 0

tell.ccat = *, all, muc, info 
tell.desc = Позволяет оставить пользователю не находящемуся в конференции сообщение, которое он получит при следующем входе.
tell.synt = %prefix%tell <nick>:|,<message>
tell.exam = %prefix%tell guy: Как получишь это сообщение стучи в ростер.
tell.exam = %prefix%tell guy, Нам надо встретиться, срочно!

thr_show.ccat = *, all, superadmin, info
thr_show.desc = Позволяет посмотреть список активных потоков бота.
thr_show.synt = %prefix%thr_show
thr_show.exam = %prefix%thr_show

thr_dump.ccat = *, all, superadmin, info
thr_dump.desc = Позволяет сохранить список активных потоков бота в файл. Необходимо, когда потоков много.
thr_dump.synt = %prefix%thr_dump
thr_dump.exam = %prefix%thr_dump

http.ccat = *, all, http, info
http.desc = Позволяет послать get-запрос на URL и получить содержимое страницы из сети. С параметром headers|hdrs выводит заголовки get-запроса.
http.synt = %prefix%http [headers:entity|hdrs:entity] <URL>
http.exam = %prefix%http http://fatal-dev.ru
http.exam = %prefix%http headers http://fatal-dev.ru
http.exam = %prefix%http headers:content-length http://fatal-dev.ru
http.exam = %prefix%http hdrs:content-type http://fatal-dev.ru