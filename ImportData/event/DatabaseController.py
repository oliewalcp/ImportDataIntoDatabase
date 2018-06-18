import pymssql

class DatabaseController:
	#私有成员
	__ipAddress = "127.0.0.1" #IP地址
	__portNumber = "1433"     #端口号
	__userid = "sa"           #用户名
	__password = "123456"     #密码
	__errorMessage = ""       #异常信息
	#设置连接对象
	def setConnectArgue(self, __ipAddress, __portNumber, __userid, __password):
		self.__ipAddress = __ipAddress
		self.__portNumber = __portNumber
		self.__userid = __userid
		self.__password = __password
	#打开数据库连接
	def open(self):
		try:
			self.__con = pymssql.connect(
				host = self.__ipAddress,
				port = self.__portNumber,
				user = self.__userid,
				password = self.__password)
			return True
		except Exception as e:
			self.__errorMessage = str(e)
			return False;
	#获取异常信息
	def getErrorMessage(self):
		return self.__errorMessage
	#关闭数据库连接
	def close(self):
		try:
			self.__con.close()
		except Exception as e:
			self.__errorMessage = e.message()
	#设置属性名
	def setProperties(self, properties):
		self.__properties = properties
		self.__propertiesString = self.__unpack(properties)
	#插入数据
	def inset(self, table, values):
		if len(self.__properties) != len(values):
			return False
		try:
			self.__con.cursor().executemany(
				"insert into %s(%s) values(%s)" % (
					table, 
					self.__propertiesString, 
					self.__unpack(values))
				)
			return True
		except Exception as e:
			self.__errorMessage = e.message()
			return False
	#元组解包
	def __unpack(self, arg):
		result = ""
		flag = False
		for a in arg:
			if flag == False:
				flag = True
			else:
				result += ","
			result += a
		return result
	#设置数据库
	def useDatabase(self, database):
		try:
			self.__con.cursor().executemany("use " + database)
			return True
		except Exception as e:
			self.__errorMessage = e.message()
			return False
	#查看表是否存在
	def existsTable(self, table):
		try:
			self.__con.cursor().executemany("select * from " + table + " limit 1")
			return True
		except Exception as e:
			self.__errorMessage = e.message()
			return False
	#删除一条数据
	def delete(self, table, key, value):
		try:
			self.__con.cursor().executemany("delete from %s where %s = \"%s\"" % (table, key, value))
			return True
		except Exception as e:
			self.__errorMessage = e.message()
			return False