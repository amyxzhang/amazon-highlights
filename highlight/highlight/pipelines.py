import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request
from config import MYSQL_USER, MYSQL_HOST, MYSQL_PW, MYSQL_NAME

class HighlightMySQLPipeline(object):
    
    def __init__(self):
        self.conn = MySQLdb.connect(user=MYSQL_USER, passwd=MYSQL_PW, db=MYSQL_NAME, host=MYSQL_HOST, charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):    
        try:
            res = self.cursor.execute("select id from Book where book_link='%s' limit 1" % (item['book_link']))
            if res:
                b_id = self.cursor.fetchone()[0]
            else:
                self.cursor.execute("""insert into Book (title, book_link, highlight_link, author)
                                values (%s, %s, %s, %s)""", 
                               (item['title'].encode('utf-8'), 
                                item['book_link'].encode('utf-8'),
                                item['highlight_link'].encode('utf-8'),
                                item['author'].encode('utf-8'),
                                ))
                self.conn.commit()
                b_id = self.cursor.lastrowid

            unenc = item['text'].encode('ascii', 'ignore')
            hash_obj = hashlib.sha1(unenc.encode())
            text_hash = hash_obj.hexdigest()
            res = self.cursor.execute("select id, num_users from Highlight where text_hash='%s' limit 1" % (text_hash))
            if res:
                h_id, user_num = self.cursor.fetchone()
                if int(user_num) != int(item['num']):
                    self.cursor.execute("""update Highlight set num_users=%s where id=%s""", (user_num, h_id))
                    self.conn.commit()
            else:
                self.cursor.execute("""insert into Highlight (book_id, passage, text_hash, num_users)
                                values (%s, %s, %s, %s)""", 
                               (b_id, 
                                item['text'].encode('utf-8'),
                                hash,
                                item['num'],
                                ))
                self.conn.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            self.conn.rollback()
        return item