join.ccat = *, all, muc, admin 
join.desc = Зайти в определенную конференцию. Если она под паролем то нужно писать пароль сразу после ее названия или после ника, если он уазан. Если бот зарегистрирован на том же сервере на котором находится конференция, то @conference.jabber.aq указывать не обязательно.
join.synt = %prefix%join <конференция> [<ник_бота>[:<пароль>]]
join.exam = %prefix%join conf
join.exam = %prefix%join conf@conference.jabber.aq
join.exam = %prefix%join conf@conference.jabber.aq somebot
join.exam = %prefix%join conf@conference.jabber.aq somebot:secret

leave.ccat = *, all, muc, admin
leave.desc = Заставляет бота выйти из текущей или определенной конференции.
leave.synt = %prefix%leave [<конференция>] [причина]
leave.exam = %prefix%leave
leave.exam = %prefix%leave Good bye!
leave.exam = %prefix%leave conf@conference.jabber.aq
leave.exam = %prefix%leave conf@conference.jabber.aq Good bye!

message.ccat = *, all, muc, admin
message.desc = Отправляет сообщение от имени бота на определённый JID.
message.synt = %prefix%message <jid> <сообщение>
message.exam = %prefix%message guy@jabber.aq Здорово!
message.exam = %prefix%message guy@jabber.aq Здорово! Зайди
message.exam = сам знаешь куда.

say.ccat = *, all, muc, admin
say.desc = Говорить через бота в конференции.
say.synt = %prefix%say <сообщение>
say.exam = %prefix%say Всем привет!

echo.ccat = *, all, muc, admin
echo.desc = Возвращает тот же самый текст, который был послан боту.
echo.synt = %prefix%echo <текст>
echo.exam = %prefix%echo Yo!
echo.exam = %prefix%echo Проверка!!!

restart.ccat = *, all, muc, admin
restart.desc = Позволяет перезапустить бота, указав если необходимо причину.
restart.synt = %prefix%restart [причина]
restart.exam = %prefix%restart
restart.exam = %prefix%restart Обновление бота!

halt.ccat =  *, all, superadmin, admin
halt.desc = Остановка и полный выход бота.
halt.synt = %prefix%halt [причина]
halt.exam = %prefix%halt
halt.exam = %prefix%halt Профилактические работы на сервере!

globmsg.ccat = *, all, muc, superadmin, admin
globmsg.desc = Разослать сообщение по всем конференциям, в которых сидит бот.
globmsg.synt = %prefix%globmsg [сообщение]
globmsg.exam = %prefix%globmsg C Новым Годом!!!

set_status.ccat = *, all, muc, admin
set_status.desc = Меняет статус бота на указанный из списка:\naway - отсутствую;\nxa - давно отсутствую;\ndnd - не беспокоить;\nchat - хочу чатиться, а также статусное сообщение (если оно указывается). Если указать только статусное сообщение, изменится только оно.
set_status.synt = %prefix%set_status [статус] [сообщение]
set_status.exam = %prefix%set_status chat
set_status.exam = %prefix%set_status dnd Лежу где-то рядом!
set_status.exam = %prefix%set_status Думаю...

set_nick.ccat = *, all, muc, admin
set_nick.desc = Меняет ник бота в текущей конференции.
set_nick.synt = %prefix%set_nick <nick>
set_nick.exam = %prefix%set_nick somebot

remote.ccat = *, all, muc, superadmin, admin
remote.desc = Позволяет удаленно выполнять команды и алиасы в других конференциях от имени бота и получать результат. Без параметров выводит список конференций с номерами, вместо полного названия конференции можно использовать номер из списка.
remote.synt = %prefix%remote <конференция|номер_из_списка> <команда> [<параметры>]
remote.exam = %prefix%remote
remote.exam = %prefix%remote room@conference.jabber.aq ping guy
remote.exam = %prefix%remote 2 time guy

redirect.ccat = *, all, muc, admin
redirect.desc = Перенаправляет результат команды или алиаса указанному пользователю в приват. Если алиас или команда не указаны и вместо них текст, или указанны неверно, то отправляет пользователю сообщение.
redirect.synt = %prefix%redirect <ник>:<команда> [<параметры>]|<сообщение>
redirect.exam = %prefix%redirect some guy: ping guy

rejoin.ccat = *, all, muc, superadmin, admin
rejoin.desc = Позволяет выполнить перезаход бота в конференции.
rejoin.synt = %prefix%rejoin
rejoin.exam = %prefix%rejoin

cmd_name.ccat = *, all, superadmin, admin
cmd_name.desc = Позволяет изменить имя используемой команды. Без параметра <новое_имя> выводит реальное имя команды. Без параметров выводит список измененных имен. При указании отрицательного числа удаляет измененное имя из списка с этим номером. При указании "-" очищает весь список и восстанавливает имена команд по-умолчанию.
cmd_name.synt = %prefix%cmd_name [<команда> [<новое_имя>]]|-[<номер из списка>]
cmd_name.exam = %prefix%cmd_name
cmd_name.exam = %prefix%cmd_name ping
cmd_name.exam = %prefix%cmd_name help помощь
cmd_name.exam = %prefix%cmd_name -3
cmd_name.exam = %prefix%cmd_name -

gblock.ccat = *, all, superadmin, admin
gblock.desc = Позволяет глобально заблокировать бота. Бот не будет отвечать ни на чьи команды и сообщения, пока админ бота не снимет блокировку. Админам бота доступны все функции во время блокировки.
gblock.synt = %prefix%gblock [1|0]
gblock.exam = %prefix%gblock
gblock.exam = %prefix%gblock 1
gblock.exam = %prefix%gblock 0

cblock.ccat = *, all, superadmin, admin
cblock.desc = Позволяет локально (в определенной конференции) заблокировать бота. Бот не будет отвечать ни на чьи команды и сообщения, пока админ бота не снимет блокировку. Админам бота доступны все функции во время блокировки.
cblock.synt = %prefix%cblock [1|0]
cblock.exam = %prefix%cblock
cblock.exam = %prefix%cblock 1
cblock.exam = %prefix%cblock 0

bot_lang.ccat = *, all, locale, superadmin, admin
bot_lang.desc = Позволяет вручную задать язык сообщений, которые выводит бот. Язык определяется автоматически при первой загрузке бота, в зависимости от текущей системной локали. По-умолчанию "en".
bot_lang.synt = %prefix%bot_lang [<код_языка>]
bot_lang.exam = %prefix%bot_lang
bot_lang.exam = %prefix%bot_lang ru

prefix.ccat = *, all, muc, admin
prefix.desc = Позволяет сменить префикс команд в конференции, если вызывается в конференции и в ростере, если вызывается в ростере.
prefix.synt = %prefix%prefix [<prefix>]
prefix.exam = %prefix%prefix
prefix.exam = %prefix%prefix !

connect.ccat = *, all, accounts, superadmin, admin
connect.desc = Позволяет подключить любое количество дополнительных аккаунтов с сохранением джидов и паролей в конфиге.
connect.synt = %prefix%connect <jid>:<password>[:<resource>]
connect.exam = %prefix%connect user@server.tld: secret
connect.exam = %prefix%connect user@server.tld: secret: fatal-rsrc

disconnect.ccat = *, all, accounts, superadmin, admin
disconnect.desc = Позволяет отключить любое количество подключенных аккаунтов, кроме того, через который производится отключение. Удаляет джиды и пароли отключаемых аккаунтов из конфига. Без параметров выводит список подключенных аккаунтов.
disconnect.synt = %prefix%disconnect [<number>|<jid>]
disconnect.exam = %prefix%disconnect
disconnect.exam = %prefix%disconnect 3
disconnect.exam = %prefix%disconnect user@server.tld

syslog.ccat = *, all, info, superadmin, admin
syslog.desc = Позволяет просматривать и очищать системные логи бота из директории syslogs.
syslog.synt = %prefix%syslog [[<number>|<logname>] [<lines>]|-]
syslog.exam = %prefix%syslog
syslog.exam = %prefix%syslog 3
syslog.exam = %prefix%syslog 3 17
syslog.exam = %prefix%syslog error
syslog.exam = %prefix%syslog error 26
syslog.exam = %prefix%syslog 4 -
syslog.exam = %prefix%syslog output -

config.ccat = *, all, config, superadmin, admin
config.desc = Позволяет смотреть и редактировать параметры: конфига бота (группа bot) fatal.conf, базу глобальных параметров (группа glob) и базы параметров конференций (группа room) соответственно. Группы room или glob определяются автоматически, в зависимости от того, где вы находитесь: в конференции или в ростере бота. К тому же группы bot и glob доступны и в конференции при явном указании, в то время как группа room не доступна в ростере бота, так как нет возможности определить для какой конференции запрашиваются конфигурации.\n\nПредупреждение: Эта команда только для опытных пользователей, ибо неправильное ее использование может привести к неработоспособности бота! Так как параметры редактируются напрямую и правильность устанавливаемых значений не проверяется.
config.synt = %prefix%config [bot|[glob|room]] <param> [<value>]
config.exam = %prefix%config bot auto_subscribe 
config.exam = %prefix%config bot auto_subscribe 1
config.exam = %prefix%config room muc_filter
config.exam = %prefix%config muc_filter 1
config.exam = %prefix%config glob prefix
config.exam = %prefix%config glob prefix *

