subscribe.ccat = roster, superadmin, all, *
subscribe.desc = Позволяет добавить контакт в ростер бота и посылает этому контакту запрос на авторизацию.
subscribe.synt = %prefix%subscribe <jid> [<name>][:<access>]
subscribe.exam = %prefix%subscribe guy@jabber.aq
subscribe.exam = %prefix%subscribe guy@jabber.aq: 20
subscribe.exam = %prefix%subscribe guy@jabber.aq Friend
subscribe.exam = %prefix%subscribe guy@jabber.aq Friend: 80

usubscribe.ccat = roster, superadmin, all, *
usubscribe.desc = Позволяет удалить контакт и подписку из ростера бота.
usubscribe.synt = %prefix%usubscribe <jid>
usubscribe.exam = %prefix%usubscribe guy@jabber.aq

roster.ccat = roster, superadmin, all, *
roster.desc = Позволяет посмотреть ростер бота.
roster.synt = %prefix%roster [<jid>]
roster.exam = %prefix%roster
roster.exam = %prefix%roster guy@jabber.aq
