eval.ccat = superadmin, all, *
eval.desc = Расчитывает и показывает заданное выражение питона.
eval.synt = %prefix%eval <выражение>
eval.exam = %prefix%eval 1+1

exec.ccat = superadmin, all, *
exec.desc = Выполняет выражение питона.
exec.synt = %prefix%exec <выражение>
exec.exam = %prefix%exec pass

sh.ccat = superadmin, all, *
sh.desc = Выполняет шелл команду.
sh.synt = %prefix%sh <команда>
sh.exam = %prefix%sh ls
sh.exam = %prefix%sh dir

ssh.ccat = superadmin, all, *
ssh.desc = Выполняет шелл команду, экранируя специальные символы, такие как: >, & и пр.
ssh.synt = %prefix%ssh <команда>
ssh.exam = %prefix%ssh ls
ssh.exam = %prefix%ssh dir

calc.ccat = *, all, info
calc.desc = Калькулятор.
calc.synt = %prefix%calc <выражение>
calc.exam = %prefix%calc 2+2*2
