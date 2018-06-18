import sys
import wx
import xlrd
import datetime
sys.path.append("../event")
from DatabaseController import DatabaseController
from FileController import XMLFileController
from LoginFace import LoginFace

class MainWindow(wx.Frame):
	__LoginMessageFileName = "login.xml"
	__ImportMessageFileName = "data.xml"
	__WindowWidth = 500  #窗口宽度
	__WindowHeight = 250 #窗口高度
	__BoundWidth = 9  #边沿宽度
	__BaseHeight = 25 #控件的基本高度
	__TipStringWidth = 50 #“数据库：”文本框宽度
	__SelectButtonWidth = 60 #选择文件按钮宽度
	__FileNameSelectedWidth = __WindowWidth - __SelectButtonWidth - __TipStringWidth - 4 * __BoundWidth #文件名称文本框的宽度
	__SheetDropDownWidth = 300 #Sheet列表宽度
	#构造函数
	def __init__(self):
		wx.Frame.__init__(self, parent=None, size=(self.__WindowWidth, self.__WindowHeight))
		self.SetTitle("数据导入工具")
		self.SetMaxSize((self.__WindowWidth, self.__WindowHeight))
		self.SetMinSize((self.__WindowWidth, self.__WindowHeight))
		self.__initUI()
		self.__DBController = LoginFace(self, "登录界面").getDBController()
		self.Bind(wx.EVT_CLOSE, self.__Exit_Event__)
	#初始化界面
	def __initUI(self):
		self.__createDatabaseString()
		self.__createFileMessage()
		self.__createWithdrawMessage()
		self.__createProgressMessage()
		self.__readFileMessage()
	#读取文件信息到界面
	def __readFileMessage(self):
		#读取数据库和表信息
		configFile = XMLFileController()
		configFile.Open(self.__LoginMessageFileName)
		database = configFile.GetValue("database")
		table = configFile.GetValue("table")
		self.__TableInputString.write(table)
		self.__DatabaseInputString.write(database)
		configFile.Close()
		self.__refleshTimeList()
	#更新撤回的时间列表
	def __refleshTimeList(self):
		self.__TimeList.Clear()
		configFile = XMLFileController()
		configFile.Open(self.__ImportMessageFileName)
		time = configFile.GetChildParentNodeStringList()
		for t in time:
			configFile.BeginParentNode(t)
			tempTime = configFile.GetParentId()
			self.__TimeList.Insert(tempTime, self.__TimeList.GetCount())
	#创建数据库栏目
	def __createDatabaseString(self):
		wx.StaticText(self, -1, "数据库：", 
			size=(self.__TipStringWidth +  self.__BoundWidth, self.__BaseHeight), 
			pos=(0, 5), 
			style=wx.ALIGN_RIGHT)
		#数据库名称输入框
		self.__DatabaseInputString = wx.TextCtrl(self, -1, 
			size=(self.__WindowWidth - self.__TipStringWidth - 30, self.__BaseHeight), 
			pos=(self.__TipStringWidth +  self.__BoundWidth, 0))
		wx.StaticText(self, -1, "表名：", 
			size=(self.__TipStringWidth +  self.__BoundWidth, self.__BaseHeight), 
			pos=(0, self.__BaseHeight + 10), 
			style=wx.ALIGN_RIGHT)
		#表名输入框
		self.__TableInputString = wx.TextCtrl(self, -1, 
			size=(self.__WindowWidth - self.__TipStringWidth - 30, self.__BaseHeight), 
			pos=(self.__TipStringWidth +  self.__BoundWidth, self.__BaseHeight + 5))
	#创建文件信息栏目
	def __createFileMessage(self):
		tempPosHeight = 2 * self.__BaseHeight + 15
		tempPosHeight2 = 3 * self.__BaseHeight + 20
		wx.StaticText(self, -1, "文件名：", 
			size=(self.__TipStringWidth +  self.__BoundWidth, self.__BaseHeight), 
			pos=(0, tempPosHeight), 
			style=wx.ALIGN_RIGHT)
		#显示所选文件的文件名的文本框
		self.__SelectFileName = wx.StaticText(self, -1,
			size=(self.__FileNameSelectedWidth - 3, self.__BaseHeight), 
			pos=(self.__TipStringWidth +  self.__BoundWidth, tempPosHeight))
		#选择文件按钮
		SelectFileButton = wx.Button(self, -1, "选择文件", 
			size=(self.__SelectButtonWidth, self.__BaseHeight),
			pos=(self.__TipStringWidth +  self.__BoundWidth + self.__FileNameSelectedWidth - 3, tempPosHeight - 5))
		SelectFileButton.Bind(wx.EVT_BUTTON, self.__SelectFileButton_Event__)
		#选择Sheet
		wx.StaticText(self, -1, "请选择工作空间：", style=wx.ALIGN_RIGHT,
			size=(self.__TipStringWidth * 2, self.__BaseHeight),
			pos=(0, tempPosHeight2 + 5))
		#Sheet列表
		self.__SheetList = wx.ComboBox(self, -1, style=wx.CB_DROPDOWN | wx.CB_READONLY,
			pos=(self.__TipStringWidth * 2, tempPosHeight2),
			size=(self.__SheetDropDownWidth, self.__BaseHeight))
		#导入按钮
		ImportButton = wx.Button(self, -1, "导入数据", 
			size=(self.__SelectButtonWidth, self.__BaseHeight),
			pos=(self.__TipStringWidth * 2 + self.__SheetDropDownWidth + 10, tempPosHeight2))
		ImportButton.Bind(wx.EVT_BUTTON, self.__ImportDataButton_Event__)
	#选择文件按钮事件
	def __SelectFileButton_Event__(self, event):
		tempSelect = wx.FileDialog(self, message="选择Excel文件", wildcard="Excel (.xlsx)|*.xlsx|Excel (.xls)|*.xls|Excel (.xlsb)|*.xlsb") 
		if tempSelect.ShowModal() == wx.ID_OK:
			self.__SheetList.Clear()
			fileSelected = tempSelect.GetPath()
			self.__SelectFileName.SetLabel(fileSelected) #设置文本框文本
			#获取Sheet列表，并插入到下拉列表控件中
			__SheetList = xlrd.open_workbook(fileSelected).sheet_names()
			for item in __SheetList:
				self.__SheetList.Insert(item, self.__SheetList.GetCount())
		tempSelect.Destroy()
	#导入数据按钮事件
	def __ImportDataButton_Event__(self, event):
		if self.__DBController.useDatabase(self.__DatabaseInputString.GetLineText(0)) == False:
			self.__messagePopup(self.__DBController.getErrorMessage(), "无法连接数据库")
			return
		if self.__DBController.existsTable(self.__TableInputString.GetLineText(0)) == False:
			self.__messagePopup(self.__DBController.getErrorMessage(), "表不存在")
			return
		currentTable = self.__TableInputString.GetLineText(0)
		currentDatabase = self.__DatabaseInputString.GetLineText(0)
		currentTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		noNeedColumn = {} #记录字段名为空的列数
		configFile = XMLFileController()
		configFile.Open(self.__LoginMessageFileName)
		memoryNumber = int(configFile.GetValue("num"))
		configFile.Close()
		configFile.Open(self.__ImportMessageFileName)
		configFile.BeginParentNode(currentTime)
		try:
			#获取Sheet中的表格
			sheetName = self.__SheetList.GetStringSelection()
			file = xlrd.open_workbook(self.__SelectFileName.GetLabel())
			table = file.sheet_by_name(sheetName)
			totalRow = table.nrows
			totalCol = table.ncols
			#获取属性名
			properties = []
			for i in range(totalCol):
				temp = table.cell(0, i).value.encode("utf-8")
				if temp.strip() != "":
					if i == 0:
						configFile.SetValue("key", temp)
					properties.append(temp)
				else:
					noNeedColumn[i] = i
			self.__DBController.setProperties(properties)
			#设置本次数据的信息
			configFile.SetValue("table", currentTable)
			configFile.SetValue("database", currentDatabase)
			#读取Sheet数据并插入到数据库
			configFile.BeginParentNode("data")
			try:
				self.__ProgressBar.SetValue(0)
				for i in range(1, totalRow):
					currentData = [table.cell(i, 0).value.encode("utf-8")]
					configFile.AddValue("value", currentData)
					for j in range(1, totalCol):
						if not noNeedColumn.has_key(j):#如果不是空字段的列
							currentData.append(table.cell(i, j).value.encode("utf-8"))
					self.__DBController.inset(currentTable, currentData)
					self.__ProgressBar.SetValue(i / totalRow)
				self.__ProgressBar.SetValue(100)
				self.__messagePopup("插入数据完成", "任务完成", wx.OK)
			except Exception as e:
				self.__messagePopup(self.__DBController.getErrorMessage(), "插入数据异常")
				raise Exception()
			finally:
				configFile.EndParentNode()
		except Exception as e:
			return
		finally:
			configFile.EndParentNode()
			timeList = configFile.GetChildParentNodeStringList()
			timeList.sort()
			while len(timeList) > memoryNumber:
				removedArgue = timeList.pop(0)
				configFile.RemoveChildNode(removedArgue)
			configFile.Close()
			self.__TimeList.Insert(currentTime, self.__TimeList.GetCount())

	#弹出警告窗
	def __messagePopup(self, message, title, style=wx.ICON_ERROR):
		window = wx.MessageDialog(self, message, title, style=style)
		window.ShowModal()
	#撤回选择信息栏
	def __createWithdrawMessage(self):
		tempPosHeight = 5 * self.__BaseHeight
		self.__TimeList = wx.ComboBox(self, -1, style=wx.CB_DROPDOWN | wx.CB_READONLY,
			pos=(self.__BoundWidth, tempPosHeight),
			size=(self.__SheetDropDownWidth, self.__BaseHeight))
		#撤回按钮
		WithdrawButton = wx.Button(self, -1, "撤回该时间点导入的数据", 
			size=(150, self.__BaseHeight),
			pos=(self.__SheetDropDownWidth + 20, tempPosHeight))
		WithdrawButton.Bind(wx.EVT_BUTTON, self.__WithdrawButton_Event__)
	#撤回按钮事件
	def __WithdrawButton_Event__(self, event):
		self.__ProgressBar.SetValue(0)
		selectTime = self.__TimeList.GetStringSelection()
		configFile = XMLFileController()
		configFile.Open(self.__ImportMessageFileName)
		configFile.BeginParentNode(selectTime)
		try:
			if self.__DBController.useDatabase(configFile.GetValue("database")):
				table = configFile.GetValue("table")
				key = configFile.GetValue("key")
				configFile.BeginParentNode("data")
				dataValue = configFile.GetChildTextNodeValue()
				currentTotalDataNumber = len(dataValue)
				try:
					i = 0
					for value in dataValue:
						self.__DBController.delete(table, key, value)
						i += 1
						self.__ProgressBar.SetValue(i / currentTotalDataNumber)
					self.__ProgressBar.SetValue(100)
					configFile.EndParentNode()
					configFile.EndParentNode()
					configFile.RemoveChildNode(selectTime)
					configFile.Close()
				except Exception as e:
					configFile.EndParentNode()
					raise Exception()
		except Exception as e:
			self.__messagePopup(self.__DBController.getErrorMessage(), "撤回数据失败")
		finally:
			configFile.EndParentNode()
	#进度信息栏
	def __createProgressMessage(self):
		tempPosHeight = 6 * self.__BaseHeight + 10
		#进度条
		self.__ProgressBar = wx.Gauge(self, -1, 
			pos=(self.__BoundWidth, tempPosHeight),
			size=(self.__WindowWidth - 4 * self.__BoundWidth, self.__BaseHeight))
	#窗口关闭事件
	def __Exit_Event(self):
		self.__DBController.close()

if __name__ == '__main__':
	ex = wx.App()
	MainWindow().Show(show=True)
	ex.MainLoop()