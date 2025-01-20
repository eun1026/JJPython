import mysql.connector
from datetime import datetime

class DBManager:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="3.36.231.115",
                user="jjeong",
                password="001125",
                database="board_db2"
            )
            self.cursor = self.connection.cursor(dictionary=True)
            
        except mysql.connector.Error as error:
            print(f"데이터베이스 연결 실패: {error}")

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            
    def get_all_posts(self):
        try:
            self.connect()
            sql = "SELECT * FROM posts"
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except mysql.connector.Error as error:
            print(f"게시글 조회 실패: {error}")
            return []
        finally:
            self.disconnect()
    
    def insert_post(self,title,content,filename):
        try:
            self.connect()
            sql = "INSERT INTO posts (title,content,filename,created_at) values (%s,%s,%s,%s)"
            values = (title,content,filename,datetime.now())            
            self.cursor.execute(sql, values)
            
            #values = [(name,email,department,salary,datetime.now().date()),(name,email,department,salary,datetime.now().date())]
            #self.cursor.executemany(sql, values)            
            
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"내용 추가 실패: {error}")
            return False
        finally:
            self.disconnect()
   
    def get_post_by_id(self, id):
        try:
            self.connect()
            sql = "SELECT * FROM posts WHERE id = %s"
            value = (id,) # 튜플 1개 일때
            self.cursor.execute(sql, value)
            return self.cursor.fetchone()
        except mysql.connector.Error as error:
            print(f"내용 조회 실패: {error}")
            return None
        finally:
            self.disconnect()
    
    def update_post(self,id,title,content,filename):
        try:
            self.connect()
            if filename:
                sql = """UPDATE posts 
                        SET title = %s, content = %s, filename = %s 
                        WHERE id = %s
                        """
                values = (title,content,filename,id)
            else:
                sql = """UPDATE posts 
                        SET title = %s, content = %s 
                        WHERE id = %s
                        """
                values = (title,content,id)
            self.cursor.execute(sql, values)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"게시글 수정 실패: {error}")
            return False
        finally:
            self.disconnect()
    
    def delete_post(self, id):
        try:
            self.connect()
            sql = "DELETE FROM posts WHERE id = %s"
            value = (id,) # 튜플 1개 일때
            self.cursor.execute(sql, value)
            self.connection.commit()
            return True
        except mysql.connector.Error as error:
            self.connection.rollback()
            print(f"게시판 삭제 실패: {error}")
            return False
        finally:
            self.disconnect()