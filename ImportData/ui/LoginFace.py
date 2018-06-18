import wx
import sys
sys.path.append("../event")
from DatabaseController import DatabaseController
from FileController import XMLFileController

class LoginFace(wx.Dialog):
	__LoginMessageFileName = "login.xml"
	__Width = 300
	__Height = 200
	__BaseHeight = 25
	__BoundWidth = 9
	__TipStringWidth = 50
	__ButtonWidth = 60
	def __init__(self, parent, title):
		wx.Dialog.__init__(self, parent=parent, size=(self.__Width, self.__Height), title=title)
		self.__initUI()
		self.__param = self.ShowModal()
	#创建界面
	def __initUI(self):
		tempPosHeight = self.__BaseHeight + 5
		#用户名信息
		wx.StaticText(self, -1, "用户名：", 
			size=(self.__TipStringWidth +  self.__BoundWidth, self.__BaseHeight), 
			pos=(0, 5), 
			style=wx.ALIGN_RIGHT)
		#用户名输入框
		self.__UserInputString = wx.TextCtrl(self, -1, 
			size=(self.__Width - self.__TipStringWidth - 30, self.__BaseHeight), 
			pos=(self.__TipStringWidth +  self.__BoundWidth, 0))
		#密码信息
		wx.StaticText(self, -1, "密码：", 
			size=(self.__TipStringWidth +  self.__BoundWidth, self.__BaseHeight), 
			pos=(0, tempPosHeight + 5), 
			style=wx.ALIGN_RIGHT)
		#密码输入框
		self.__PasswordInputString = wx.TextCtrl(self, -1, 
			size=(self.__Width - self.__TipStringWidth - 30, self.__BaseHeight), 
			pos=(self.__TipStringWidth +  self.__BoundWidth, tempPosHeight),
			style=wx.TE_PASSWORD)
		#IP地址信息
		wx.StaticText(self, -1, "IP端口：", 
			size=(self.__TipStringWidth +  self.__BoundWidth, self.__BaseHeight), 
			pos=(0, 2 * tempPosHeight + 5), 
			style=wx.ALIGN_RIGHT)
		#IP地址输入框
		self.__IPInputString = wx.TextCtrl(self, -1, 
			size=(self.__Width - self.__TipStringWidth - 85, self.__BaseHeight), 
			pos=(self.__TipStringWidth +  self.__BoundWidth, 2 * tempPosHeight))
		#端口号输入框
		self.__PortInputString = wx.TextCtrl(self, -1, 
			size=(50, self.__BaseHeight), 
			pos=(self.__TipStringWidth + self.__BoundWidth + self.__Width - self.__TipStringWidth - 80, 2 * tempPosHeight))
		#数据库信息
		wx.StaticText(self, -1, "数据库：", 
			size=(self.__TipStringWidth +  self.__BoundWidth, self.__BaseHeight), 
			pos=(0, 3 * tempPosHeight + 5), 
			style=wx.ALIGN_RIGHT)
		#数据库输入框
		self.__DatabaseInputString = wx.TextCtrl(self, -1, 
			size=(self.__Width - self.__TipStringWidth - 30, self.__BaseHeight), 
			pos=(self.__TipStringWidth +  self.__BoundWidth, 3 * tempPosHeight))
		#登录按钮
		LoginButton = wx.Button(self, -1, "登录", 
			size=(self.__ButtonWidth, self.__BaseHeight),
			pos=(60, 4 * tempPosHeight))
		#退出按钮
		ExitButton = wx.Button(self, -1, "退出", 
			size=(self.__ButtonWidth, self.__BaseHeight),
			pos=(180, 4 * tempPosHeight))
		self.Bind(wx.EVT_CLOSE, self.__Exit_Event__)
		ExitButton.Bind(wx.EVT_BUTTON, self.__Exit_Event__)
		LoginButton.Bind(wx.EVT_BUTTON, self.__Login_Event__)
		self.__readLoginConfig()
	#读取登录记录
	def __readLoginConfig(self):
		configFile = XMLFileController()
		configFile.Open(self.__LoginMessageFileName)
		userid = configFile.GetValue("userid")
		password = configFile.GetValue("password")
		ip = configFile.GetValue("ipaddress")
		port = configFile.GetValue("portnumber")
		database = configFile.GetValue("database")
		self.__UserInputString.write(userid)
		self.__PasswordInputString.write(password)
		self.__IPInputString.write(ip)
		self.__PortInputString.write(port)
		self.__DatabaseInputString.write(database)
		configFile.Close()
	#保存登录记录
	def __saveLoginConfig(self):
		configFile = XMLFileController()
		configFile.Open(self.__LoginMessageFileName)
		configFile.SetValue("userid", self.__UserInputString.GetLineText(0))
		configFile.SetValue("password", self.__PasswordInputString.GetLineText(0))
		configFile.SetValue("ipaddress", self.__IPInputString.GetLineText(0))
		configFile.SetValue("portnumber", self.__PortInputString.GetLineText(0))
		configFile.SetValue("database", self.__DatabaseInputString.GetLineText(0))
		configFile.Close()
	#关闭事件
	def __Exit_Event__(self, event):
		sys.exit(0)
	#登录按钮事件
	def __Login_Event__(self, event):
		self.__saveLoginConfig()
		self.__DBController = DatabaseController()
		self.__DBController.setConnectArgue(
			self.__IPInputString.GetLineText(0),
			self.__PortInputString.GetLineText(0),
			self.__UserInputString.GetLineText(0),
			self.__PasswordInputString.GetLineText(0))
		if self.__DBController.open() == True:
			self.Show(False)
		else:
			fail = wx.MessageDialog(self, self.__DBController.getErrorMessage(), "登录失败", wx.ICON_ERROR)
			fail.ShowModal()
	#获取数据库对象
	def getDBController(self):
		return self.__DBController

