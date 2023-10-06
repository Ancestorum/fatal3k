paste.ccat = *, all, net, paste, pastebin
paste.desc = Позволяет сделать пост на ресурсе быстрого обмена и хранения фрагментов текста - www.pastebin.com. Без параметров выводит список форматов (языков программирования).
paste.synt = %prefix%paste [[<формат>:]<текст>]
paste.exam = %prefix%paste
paste.exam = %prefix%paste if True: pass
paste.exam = %prefix%paste python: if True: pass

pstopt.ccat = *, all, net, paste, pastebin
pstopt.desc = Позволяет задавать некоторые опции постинга фрагментов текста на www.pastebin.com. Без параметров выводит список опций.
pstopt.synt = %prefix%pstopt [paste_private [0|1]|paste_expire_date [N|10M|1H|1D|1M]|paste_format [<формат>]]
pstopt.exam = %prefix%pstopt
pstopt.exam = %prefix%pstopt paste_private
pstopt.exam = %prefix%pstopt paste_private 0
pstopt.exam = %prefix%pstopt paste_private 1
pstopt.exam = %prefix%pstopt paste_expire_date
pstopt.exam = %prefix%pstopt paste_expire_date N
pstopt.exam = %prefix%pstopt paste_expire_date 10M
pstopt.exam = %prefix%pstopt paste_expire_date 1H
pstopt.exam = %prefix%pstopt paste_expire_date 1D
pstopt.exam = %prefix%pstopt paste_expire_date 1M
pstopt.exam = %prefix%pstopt paste_format
pstopt.exam = %prefix%pstopt paste_format python

pstget.ccat = *, all, net, paste, pastebin
pstget.desc = Позволяет загружать и смотреть посты с pastebin.com по URL или по Id.
pstget.synt = %prefix%pstget <url>|<paste_id>
pstget.exam = %prefix%pstget tHnQ343z
pstget.exam = %prefix%pstget http://pastebin.com/tHnQ343z
