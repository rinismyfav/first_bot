import pymysql


class Base:
    def __init__(self):
        self.con = pymysql.connect(host='172.16.5.35',
                                    user='ITCube',
                                    password='ITCube',
                                    database='superbotesenii',
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def execute(self, command):
        self.cur.execute(command)
        self.con.commit()
        return [x for x in self.cur.fetchall()]


if __name__ == '__main__':
    pass

#print(Base().execute('select * from users;'))
#Base().execute('insert into users(name) values("Oleg");')


