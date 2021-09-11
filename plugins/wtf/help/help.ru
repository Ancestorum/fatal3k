wtf.ccat = info, wtf, all, *
wtf.desc = Выводит статью из базы. Целиком, если статья небольшая или первую страницу, если статья большая. Также позволяет получать и остальные страницы и задавать размер страницы в символах.
wtf.synt = %prefix%wtf [<номер_страницы>[<размер_страницы>[k]]] <название_статьи>
wtf.exam = %prefix%wtf статья
wtf.exam = %prefix%wtf 5 статья
wtf.exam = %prefix%wtf 7 3000 статья
wtf.exam = %prefix%wtf 7 3k статья

wtfp.ccat = info, wtf, all, *
wtfp.desc = Выводит статью из базы в приват. Целиком, если статья небольшая или первую страницу, если статья большая. Также позволяет получать и остальные страницы и задавать размер страницы в символах.
wtfp.synt = %prefix%wtfp [<номер_страницы>[<размер_страницы>[k]]] <название_статьи>
wtfp.exam = %prefix%wtfp статья
wtfp.exam = %prefix%wtfp 10 статья
wtfp.exam = %prefix%wtfp 17 1000 статья
wtfp.exam = %prefix%wtfp 17 10k статья

next.ccat = info, wtf, all, *
next.desc = Позволяет получить следующие страницы статьи. Без параметров выводит следующую страницу статьи из базы, после вывода командой %prefix%wtf, если размер страницы меньше размера статьи и не указан шаг. При указании шага выводит страницу с номером равным номеру текущей страницы + шаг. При указании названия статьи, она становится текущей, т.е. при следующем вызове команды %prefix%next будет выведена следующая страница данной статьи.
next.synt = %prefix%next [<название_статьи>]|[<шаг>]
next.exam = %prefix%next
next.exam = %prefix%next статья
next.exam = %prefix%next 4

prev.ccat = info, wtf, all, *
prev.desc = Позволяет получить предыдущие страницы статьи. Без параметров выводит предыдущую страницу статьи из базы, после вывода командой %prefix%wtf, если размер страницы меньше размера статьи и не указан шаг. При указании шага выводит страницу с номером равным номеру текущей страницы - шаг. При указании названия статьи, она становится текущей, т.е. при следующем вызове команды %prefix%prev будет выведена предыдущая страница данной статьи.
prev.synt = %prefix%prev [<название_статьи>]|[<шаг>]
prev.exam = %prefix%prev
prev.exam = %prefix%prev статья
prev.exam = %prefix%prev 3

list.ccat = info, wtf, all, *
list.desc = Позволяет получить список статей, целиком или по частям. Без параметров выводит весь список статей если статей меньше 50, или часть списка размером 50 названий, если статей больше 50.
list.synt = %prefix%list [[<страница>]<размер>]
list.exam = %prefix%list
list.exam = %prefix%list 3
list.exam = %prefix%list 2 20

books.ccat = info, wtf, all, *
books.desc = Позволяет получить список книг, целиком или по частям. Без параметров выводит весь список книг если книг меньше 50, или часть списка размером 50 названий, если книг больше 50.
books.synt = %prefix%books [[<страница>]<размер>]
books.exam = %prefix%books
books.exam = %prefix%books 2
books.exam = %prefix%books 2 10

stat.ccat = info, wtf, all, *
stat.desc = Позволяет получить статистику по открытым книгам. При указании отрицательного целого числа закрывает книгу с этим номером.
stat.synt = %prefix%stat [-<номер>]
stat.exam = %prefix%stat
stat.exam = %prefix%stat -3

dfn.ccat = info, wtf, all, *
dfn.desc = Добавляет новую, или обновляет уже существующую статью. При указании вместо текста статьи, пути до текстового файла со статьей, добавляет статью из текстового файла.
dfn.synt = %prefix%dfn <название>=<тело_статьи>|<путь_до_текстового_файла>
dfn.exam = %prefix%dfn первая статья=Интересная статья.
dfn.exam = %prefix%dfn книга=/home/user/books/book.txt

del.ccat = info, wtf, all, *
del.desc = Удаляет статью с указанным именем из словаря.
del.synt = %prefix%del <название>
del.exam = %prefix%del первая статья

rnd.ccat = info, wtf, all, *
rnd.desc = Выводит случайную статью из словаря.
rnd.synt = %prefix%rnd
rnd.exam = %prefix%rnd

find.ccat = info, wtf, all, *
find.desc = Ищет слова или фразы в названиях и тексте статей. После поиска выводит список статей, в которых были найдены совпадения.
find.synt = %prefix%find <слово>|<фраза>
find.exam = %prefix%find жизнь
find.exam = %prefix%find что-то интересное

search.ccat = info, wtf, all, *
search.desc = Ищет слова или фразы в тексте указанной статьи и выводит страницу на которой найдено искомое слово или фраза. Помечает слова или фразы на найденной странице прописными буквами.
search.synt = %prefix%search <статья>:<слово>|<фраза>
search.exam = %prefix%search книга: загадка

count.ccat = info, wtf, all, *
count.desc = Выводит количество статей в словаре.
count.synt = %prefix%count
count.exam = %prefix%count

get_wtf.ccat = info, wtf, all, *
get_wtf.desc = Посылает статью из словаря через джаббер файлом.
get_wtf.synt = %prefix%get_wtf <название_статьи>
get_wtf.exam = %prefix%get_wtf статья
