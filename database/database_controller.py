import json

import pymysql


class DatabaseController:
    def __init__(self):
        self.use_prod_db = True

    def get_mysql_connection(self):
        if self.use_prod_db:
            conn = pymysql.connect(
                host='influens-mysql.mysql.database.azure.com',
                user='eric_admin',
                password="influens1!",
                db='influence',
                port=3306,
                ssl_disabled=False,
                ssl_ca='cert/DigiCertGlobalRootG2.crt.pem'
            )
        else:
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password="123456",
                db='influence',
            )

        conn.autocommit(True)

        return conn

    def get_script_generators(self, user_id):
        # To connect MySQL database
        conn = self.get_mysql_connection()

        query = f"select script_generator_id, name, created_timestamp, name_concat from script_generators where user_id = {user_id}  order by created_timestamp desc;"
        cur = conn.cursor()

        # Select query
        cur.execute(query)
        script_generators_rows = cur.fetchall()

        for i in script_generators_rows:
            print(i)

        script_generators = [
            {"script_generator_id": row[0], "name": row[1], "created_timestamp": row[2].strftime("%H:%M:%S, %B %d, %Y"),
             "name_concat": row[3]} for row in
            script_generators_rows]
        response_json = {"script_generators": script_generators}
        response = json.dumps(response_json)

        # To close the connection
        conn.close()

        return response

    def get_recent_scripts(self, script_generator_id):
        # To connect MySQL database
        conn = self.get_mysql_connection()

        query = f"select rc.recent_script_id, rc.product_name, " \
                " rc.status, rc.created_timestamp, rc.last_updated_timestamp, rc.script_generator_id " \
                "from recent_scripts rc " \
                "where rc.script_generator_id = " + str(script_generator_id) + " and rc.status <> \"DELETED\" " \
                                                                               "order by created_timestamp desc;"

        cur = conn.cursor()

        # Select query
        cur.execute(query)
        recent_scripts_rows = cur.fetchall()

        for i in recent_scripts_rows:
            print(i)

        recent_scripts = [
            {"recent_script_id": row[0], "product_name": row[1],
             "status": row[2], "created_timestamp": row[3].strftime("%H:%M:%S, %B %d, %Y"),
             "last_updated_timestamp": row[4].strftime("%H:%M:%S, %B %d, %Y"), "script_generator_id": row[5]} for row in
            recent_scripts_rows]
        response_json = {"recent_scripts": recent_scripts}
        response = json.dumps(response_json)

        # To close the connection
        conn.close()

        return response

    def get_recent_scripts_by_name(self, script_generator_name_concat):
        # To connect MySQL database
        conn = self.get_mysql_connection()

        query = f"select rc.recent_script_id, rc.product_name, " \
                " rc.status, rc.created_timestamp, rc.last_updated_timestamp, rc.script_generator_id, sg.name_concat, sg.name " \
                "from script_generators sg, recent_scripts rc " \
                "where sg.script_generator_id= rc.script_generator_id " \
                "and sg.name_concat = \"" + script_generator_name_concat + "\" and rc.status <> \"DELETED\" " \
                                                                           "order by created_timestamp desc;"

        cur = conn.cursor()

        # Select query
        cur.execute(query)
        recent_scripts_rows = cur.fetchall()

        for i in recent_scripts_rows:
            print(i)

        recent_scripts = [
            {"recent_script_id": row[0], "product_name": row[1],
             "status": row[2], "created_timestamp": row[3].strftime("%H:%M:%S, %B %d, %Y"),
             "last_updated_timestamp": row[4].strftime("%H:%M:%S, %B %d, %Y"), "script_generator_id": row[5],
             "script_generator_name_concat": row[6], "script_generator_name": row[7]} for row in
            recent_scripts_rows]
        response_json = {"recent_scripts": recent_scripts}
        response = json.dumps(response_json)

        # To close the connection
        conn.close()

        return response

    def get_recent_script(self, recent_script_id):
        # To connect MySQL database
        conn = self.get_mysql_connection()

        query = f"select recent_script_id, product_name, keywords_desc, script, status, created_timestamp, last_updated_timestamp from recent_scripts  where recent_script_id = {recent_script_id};"
        cur = conn.cursor()

        # Select query
        cur.execute(query)
        recent_scripts_rows = cur.fetchall()

        for i in recent_scripts_rows:
            print(i)

        if not recent_scripts_rows or len(recent_scripts_rows) == 0:
            recent_script = {}
        else:
            row = recent_scripts_rows[0]
            recent_script = {"recent_script_id": row[0], "product_name": row[1], "keywords_desc": row[2],
                             "script": row[3], "status": row[4],
                             "created_timestamp": row[5].strftime("%H:%M:%S, %B %d, %Y"),
                             "last_updated_timestamp": row[6].strftime("%H:%M:%S, %B %d, %Y")}

        response = json.dumps(recent_script)

        # To close the connection
        conn.close()

        return response

    def add_new_script(self,
                       script_generator_id,
                       product_name,
                       keywords_desc,
                       script,
                       status,
                       created_timestamp,
                       last_updated_timestamp):

        # To connect MySQL database
        conn = self.get_mysql_connection()

        cur = conn.cursor()
        cur.execute(
            f"insert into recent_scripts (product_name,keywords_desc,script,status,created_timestamp,last_updated_timestamp,script_generator_id) values ( \"{product_name}\", \"{keywords_desc}\",\"{script}\",\"{status}\",\"{created_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\",\"{last_updated_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\",{script_generator_id});")
        new_recent_script_id = cur.lastrowid
        cur.close()
        conn.commit()

        # To close the connection
        conn.close()

        response_json = {"new_recent_script_id": new_recent_script_id}
        response = json.dumps(response_json)
        return response

    def get_recent_completed_scripts(self, script_generator_id: int, count: int = 5):
        # To connect MySQL database
        conn = self.get_mysql_connection()

        query = f"select rc.recent_script_id, rc.product_name, rc.keywords_desc, rc.script," \
                " rc.status, rc.created_timestamp, rc.last_updated_timestamp, rc.script_generator_id " \
                "from recent_scripts rc " \
                "where rc.script_generator_id = " + str(script_generator_id) + " and rc.status = \"COMPLETED\" " \
                                                                               "order by created_timestamp desc limit " + str(
            count) + ";"

        cur = conn.cursor()

        # Select query
        cur.execute(query)
        recent_scripts_rows = cur.fetchall()

        for i in recent_scripts_rows:
            print(i)

        recent_scripts = [
            {"recent_script_id": row[0], "product_name": row[1], "keywords_desc": row[2], "script": row[3],
             "status": row[4], "created_timestamp": row[5].strftime("%H:%M:%S, %B %d, %Y"),
             "last_updated_timestamp": row[6].strftime("%H:%M:%S, %B %d, %Y"), "script_generator_id": row[7]} for row in
            recent_scripts_rows]

        # To close the connection
        conn.close()

        return recent_scripts

    def update_recent_script(self,
                             recent_script_id,
                             product_name,
                             keywords_desc,
                             script,
                             status,
                             last_updated_timestamp):

        # To connect MySQL database
        conn = self.get_mysql_connection()

        cur = conn.cursor()
        cur.execute(
            f"update recent_scripts set product_name = \"{product_name}\" ,keywords_desc= \"{keywords_desc}\",script=\"{script}\",status=\"{status}\",last_updated_timestamp = \"{last_updated_timestamp.strftime('%Y-%m-%d %H:%M:%S')}\" where recent_script_id = \"{recent_script_id}\";")
        new_recent_script_id = cur.lastrowid
        cur.close()
        conn.commit()

        # To close the connection
        conn.close()

        response_json = {"updated_recent_script_id": new_recent_script_id}
        response = json.dumps(response_json)
        return response

    def get_all_script_generator_id_recent_script_id(self, user_id):
        # To connect MySQL database
        conn = self.get_mysql_connection()

        query = "select sg.script_generator_id, rc.recent_script_id " \
                "from script_generators sg, recent_scripts rc " \
                "where sg.script_generator_id=rc.script_generator_id " \
                "and sg.user_id = " + str(user_id) + " and (rc.status= \"INPROGRESS\" or  rc.status=\"COMPLETED\");"

        cur = conn.cursor()

        # Select query
        cur.execute(query)
        all_script_generator_id_recent_script_id_rows = cur.fetchall()

        for i in all_script_generator_id_recent_script_id_rows:
            print(i)

        all_script_generator_id_recent_script_id = [{"script_generator_id": row[0], "recent_script_id": row[1]} for row
                                                    in all_script_generator_id_recent_script_id_rows]

        # To close the connection
        conn.close()

        return all_script_generator_id_recent_script_id

    def get_all_script_generator_id(self, user_id):
        # To connect MySQL database
        conn = self.get_mysql_connection()

        query = f"select script_generator_id from script_generators where user_id={user_id};"

        cur = conn.cursor()

        # Select query
        cur.execute(query)
        all_script_generator_id_recent_rows = cur.fetchall()

        for i in all_script_generator_id_recent_rows:
            print(i)

        all_script_generator_id = [{"script_generator_id": row[0]} for row
                                   in all_script_generator_id_recent_rows]

        # To close the connection
        conn.close()

        return all_script_generator_id

    def get_script_generator_name(self, script_generator_id):
        # To connect MySQL database
        conn = self.get_mysql_connection()

        query = f"select name from script_generators where script_generator_id={script_generator_id};"

        cur = conn.cursor()

        # Select query
        cur.execute(query)
        script_generator_name_rows = cur.fetchall()

        for i in script_generator_name_rows:
            print(i)

        if not script_generator_name_rows or len(script_generator_name_rows) == 0:
            script_generator_name = {"script_generator_name": ""}
        else:
            script_generator_name = {"script_generator_name": script_generator_name_rows[0][0]}

        # To close the connection
        conn.close()

        return script_generator_name

    def get_user_for_email(self, email):
        # To connect MySQL database
        conn = self.get_mysql_connection()

        query = f"select user_id, full_name, email, password_hash from users where email = \"{email.lower()}\" and status = \"ACTIVE\";"

        cur = conn.cursor()

        # Select query
        cur.execute(query)
        user_rows = cur.fetchall()

        for i in user_rows:
            print(i)

        if not user_rows or len(user_rows) == 0:
            user = None
            password_hash = None
        else:
            user = {"user_id": user_rows[0][0], "full_name": user_rows[0][1], "email": user_rows[0][2]}
            password_hash = user_rows[0][3]

        # To close the connection
        conn.close()

        return user, password_hash
