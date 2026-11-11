"""Опросы и голосования — самостоятельный первый сценарий."""
HELP = '/poll вопрос | вариант 1 | вариант 2 — опрос (админ)\n/list — опросы\n/vote ID | 1/2 — голос\n/results ID — результаты\n/close ID — закрыть (админ)'

def handle(s, u, cmd, arg, admin):
    from core import require_admin, parts, positive, add, item, listing

    if cmd == '/poll':
        require_admin(admin)
        title, a, b = parts(arg, 3)
        if a == b: raise ValueError('Варианты должны различаться.')
        return 'Создано #' + add(s, title=title, options=[a,b], votes={}, status='open')
    if cmd == '/list': return listing(s)
    if cmd == '/vote':
        key, choice = parts(arg, 2)
        row = item(s, key)
        if row['status'] != 'open': raise ValueError('Опрос закрыт.')
        if choice not in ('1','2'): raise ValueError('Выберите 1 или 2.')
        row['votes'][u] = int(choice)-1
        return 'Голос сохранён.'
    if cmd == '/results':
        row = item(s, arg)
        return '\n'.join(f"{name}: {list(row['votes'].values()).count(i)}" for i,name in enumerate(row['options']))
    if cmd == '/close':
        require_admin(admin)
        item(s, arg)['status'] = 'closed'
        return 'Опрос закрыт.'
