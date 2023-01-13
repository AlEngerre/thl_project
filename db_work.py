import sqlite3


def db_search_task(task_n, user_id):
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()

    taskj = cursor.execute(
        "SELECT id, addition_path, text_condition FROM tasks WHERE task_number = ? and id NOT in(SELECT cur_task FROM users WHERE user_id = ?)",
        (task_n, user_id)).fetchone()

    if not taskj:
        return "no act"
    cursor.execute('''INSERT INTO users(user_id, cur_task, solved) VALUES (?,?,?)''', (user_id, taskj[0], 0))
    connection.commit()
    return [taskj[0], taskj[1], taskj[2]]


def answer_cor(user_id, answer):
    print(user_id)
    print(answer)
    resp = []
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    answ = cursor.execute(
        '''SELECT answer, answer_comment FROM tasks WHERE id in(SELECT cur_task FROM users WHERE user_id = ? AND solved = ?)''',
        (user_id, False)).fetchone()
    print(answ)
    cursor.execute('''UPDATE users SET solved = ? WHERE user_id = ?''', (True, user_id))
    connection.commit()
    if not answ:
        return "no_act"
    if str(answ[0]) == str(answer):
        resp = [True, answ[1]]
    else:
        resp = [False, answ[0], answ[1]]
    return resp


def is_solving(user_id):
    temp = []
    try:
        connection = sqlite3.connect("main.db")
        cursor = connection.cursor()
        answ = cursor.execute(
            '''SELECT user_id FROM users WHERE solved = ?''', (False,)).fetchall()
        for i in answ:
            temp.append(i[0])

        print(user_id)
        print(answ)
        return user_id in temp
    except IndexError:
        return False


def del_by_id(user_id):
    connection = sqlite3.connect("main.db")
    cursor = connection.cursor()
    cursor.execute('''DELETE from users WHERE user_id = ? and solved = ?''', (user_id,False))
    connection.commit()
