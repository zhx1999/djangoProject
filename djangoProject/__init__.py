import pymysql
pymysql.version_info = (1, 4, 13, "final", 0) #不加报错则加
pymysql.install_as_MySQLdb()