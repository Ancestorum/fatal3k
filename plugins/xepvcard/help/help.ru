novc_mess.ccat = muc, info, all, *
novc_mess.desc = Устанавливает или показывает сообщение при реакции бота на пустой вкард.
novc_mess.synt = %prefix%novc_mess [<сообщение>]
novc_mess.exam = %prefix%novc_mess
novc_mess.exam = %prefix%novc_mess Заполни вкард, потом поговорим!

novc_res.ccat = muc, info, all, *
novc_res.desc = Устанавливает или показывает реакцию бота на пустой вкард: ignore, warn, kick, ban, visitor.
novc_res.synt = %prefix%novc_res [ignore|warn|kick|ban|visitor]
novc_res.exam = %prefix%novc_res
novc_res.exam = %prefix%novc_res warn
novc_res.exam = %prefix%novc_res kick
novc_res.exam = %prefix%novc_res ignore

vcard.ccat = muc, info, all, *
vcard.desc = Показывает vCard указанного пользователя. Без параметров показывает vCard запросившего пользователя.
vcard.synt = %prefix%vcard [<nick>]
vcard.exam = %prefix%vcard
vcard.exam = %prefix%vcard guy
