from xml.dom import minidom
import os

class XMLFileController:
	__GroupNodeList = [] #当前操作的结点
	__FileName = "" #当前操作的配置文件名
	__GroupDepth = 0 #__GroupNodeList的长度
	#打开文件
	def Open(self, filename):
		self.__FileName = filename
		self.__GroupNodeList = []
		if os.path.exists(filename) == True:
			self.__Document = minidom.parse(filename)
			rootNode = self.__Document.getElementsByTagName("root")
			if len(rootNode) <= 0:
				root = self.__Document.createElement("root")
				self.__Document.appendChild(root)
			else:
				self.__GroupNodeList.append(rootNode[0])
		else:
			self.__Document = minidom.Document()
			root = self.__Document.createElement("root")
			self.__Document.appendChild(root)
			self.__GroupNodeList.append(root)
		self.__GroupDepth = 1
	#设置当前操作的组
	def BeginParentNode(self, nodeName, index = 0):
		currentNode = self.__GroupNodeList[self.__GroupDepth - 1]
		childNode = currentNode.getElementsByTagName(nodeName)
		if len(childNode) <= 0:
			node = self.__Document.createElement(nodeName)
			currentNode.appendChild(node)
			self.__GroupNodeList.append(node)
		else:
			self.__GroupNodeList.append(childNode[index])
		self.__GroupDepth = self.__GroupDepth + 1
	#结束当前操作的组
	def EndParentNode(self):
		if self.__GroupDepth > 1:
			self.__GroupNodeList.pop()
			self.__GroupDepth = self.__GroupDepth - 1
	#设置结点的属性
	def SetParentId(self, value):
		currentNode = self.__GroupNodeList[self.__GroupDepth - 1]
		currentNode.setAttribute("id", value)
	#获取结点的属性
	def GetParentId(self):
		currentNode = self.__GroupNodeList[self.__GroupDepth - 1]
		return currentNode.getAttribute("id")
	#设置属性值
	def SetValue(self, key, value):
		currentNode = self.__GroupNodeList[self.__GroupDepth - 1]
		targetNode = currentNode.getElementsByTagName(key)
		if len(targetNode) == 0:
			finalNode = self.__Document.createElement(key)
			textNode = self.__Document.createTextNode(value)
			finalNode.appendChild(textNode)
			currentNode.appendChild(finalNode)
		else:
			for target in targetNode:
				if len(target.childNodes) == 0:
					textNode = self.__Document.createTextNode(value)
					target.appendChild(textNode)
				else:
					target.firstChild.data = value
	#添加属性值
	def AddValue(self, key, value):
		currentNode = self.__GroupNodeList[self.__GroupDepth - 1]
		finalNode = self.__Document.createElement(key)
		textNode = self.__Document.createTextNode(value)
		finalNode.appendChild(textNode)
		currentNode.appendChild(finalNode)
	#获取属性值
	def GetValue(self, key):
		currentNode = self.__GroupNodeList[self.__GroupDepth - 1]
		targetNode = currentNode.getElementsByTagName(key)
		try:
			if len(targetNode) == 0:
				return ""
			else:
				return targetNode[0].firstChild.data
		except Exception as e:
			return ""
	#获取当前结点下所有非文本结点的名称
	def GetChildParentNodeStringList(self):
		nodeList = []
		currentNode = self.__GroupNodeList[self.__GroupDepth - 1]
		childList = currentNode.childNodes
		if len(childList) > 0:
			for node in childList:
				if self.__isTextNode(node) == False:
					nodeList.append(node.nodeName)
		return nodeList
	#获取当前结点下所有文本结点
	def GetChildTextNodeName(self):
		stringList = []
		currentNode = self.__GroupNodeList[self.__GroupDepth - 1]
		childList = currentNode.childNodes
		for node in childList:
			if self.__isTextNode(node) == True:
				stringList.append(node.nodeName)
		return stringList
	#获取当前结点下所有文本结点的值
	def GetChildTextNodeValue(self):
		stringList = []
		currentNode = self.__GroupNodeList[self.__GroupDepth - 1]
		childList = currentNode.childNodes
		for node in childList:
			if self.__isTextNode(node) == True:
				stringList.append(node.firstChild.data)
		return stringList
	#移除结点
	def RemoveChildNode(self, nodeName):
		currentNode = self.__GroupNodeList[self.__GroupDepth - 1]
		targetNode = currentNode.getElementsByTagName(nodeName)
		for node in targetNode:
			currentNode.removeChild(node)
	#判断某个结点是否是文本结点
	def __isTextNode(self, node):
		if node.firstChild.nodeType == minidom.Node.TEXT_NODE:
			return True;
		else :
			return False;
	#关闭文件
	def Close(self):
		#读写文件的句柄  
		fileHandle = open(self.__FileName, "w")  
		#写入操作，第二个参数为缩进（加在每行结束后），第三个为增量缩进（加在每行开始前并增量）  
		self.__Document.writexml(fileHandle, addindent='  ', newl='\n', encoding='utf-8') 
		fileHandle.close()  
		self.__FileName = ""

#写入xml文件（重写函数）
def fixed_writexml(self, writer, indent="", addindent="", newl=""):  
	writer.write(indent + "<" + self.tagName)  
	attrs = self._get_attributes()  
	a_names = attrs.keys()  
	for a_name in a_names:  
		writer.write(" %s=\"" % a_name)  
		minidom._write_data(writer, attrs[a_name].value)  
		writer.write("\"")  
	if self.childNodes:  
		if len(self.childNodes) == 1 and self.childNodes[0].nodeType == minidom.Node.TEXT_NODE:  
			writer.write(">")  
			self.childNodes[0].writexml(writer, "", "", "")  
			writer.write("</%s>%s" % (self.tagName, newl))  
			return  
		writer.write(">%s"%(newl))  
		for node in self.childNodes:  
			if node.nodeType is not minidom.Node.TEXT_NODE:  
				node.writexml(writer,indent+addindent,addindent,newl)  
		writer.write("%s</%s>%s" % (indent,self.tagName,newl))  
	else:  
		writer.write("/>%s"%(newl))

minidom.Element.writexml = fixed_writexml 
