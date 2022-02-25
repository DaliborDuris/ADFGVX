from asyncio.windows_events import NULL
import sys
import re
import string
import random
import math
from itertools import cycle
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMessageBox
from numpy import mat

qtCreatorFile = "ADFGVXGUI.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

abeceda = string.ascii_uppercase
abecedaADFGVX = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def genAbeceda(moz, jaz):
	znaky = []
	counter = 0
	if moz == 5:
		x = len(abeceda)
		size = x
		abc = abeceda
	if moz == 6:
		y = len(abecedaADFGVX)
		size = y
		abc = abecedaADFGVX
	while counter < size:
		ch = random.choice(abc)
		if ch not in znaky:
			znaky.append(ch)
			counter+=1
	if moz == 5:
		removeFromAlp(znaky, jaz)

	matrixADF = matrixGen(znaky,moz)
	return matrixADF

# def test(vstupText):
# 	listToStr = ' '.join([str(elem) for elem in vstupText])
# 	return listToStr

def removeFromAlp(znaky, jazyk):
	if jazyk == 'en':
		znaky.remove('J')
	if jazyk == 'cz':
		znaky.remove('W')

def matrixGen(znaky, vyber):
	matica = [[0 for i in range(vyber)] for j in range(vyber)]
	k = 0
	for i in range(0, vyber):
		for j in range(0, vyber):
			matica[i][j] = znaky[k]
			k+=1
	return matica

def changeChar(vstupnyText, ch, moz, jaz):
	if moz == 5:
		if jaz == 'en':
			if ch=='J':
				ch='I'
		if jaz == 'cz':
			if ch=='W':
				ch=='V'
	index = list()
	for i, j in enumerate(vstupnyText):
		for k, l in enumerate(j):
			if ch==l:
				index.append(i)
				index.append(k)
	return index	

def diacRem(vstupText):	#diakritika
	text = vstupText.upper()
	text = text.replace("Ř","R")
	text = text.replace("Ě","E")
	text = text.replace("Š","S")
	text = text.replace("Ž","Z")
	text = text.replace("Ý","Y")
	text = text.replace("Á","A")
	text = text.replace("Č","C")
	text = text.replace("Í","I")
	text = text.replace("É","E")
	text = text.replace("Ť","T")
	text = text.replace("Ď","D")
	text = text.replace("Ň","N")
	text = text.replace("Ú","U")
	text = text.replace("Ů","U")
	text = text.replace("0","CDAT")
	text = text.replace("1","BGKL")
	text = text.replace("2","ASVF")
	text = text.replace("3","FCYO")   
	text = text.replace("4","TRLC")
	text = text.replace("5","JPWN")
	text = text.replace("6","KYZJ")
	text = text.replace("7","IDBP")
	text = text.replace("8","ZHLS")
	text = text.replace("9","NCTG")
	text = re.sub('[^A-Za-z0-9]+', '', text)
	return text

def numback(vstupText):	#cisla
	text = vstupText.upper()
	text = text.replace("CDAT","0")
	text = text.replace("BGKL","1")
	text = text.replace("ASVF","2")
	text = text.replace("FCYO","3")   
	text = text.replace("TRLC","4")
	text = text.replace("JPWN","5")
	text = text.replace("KYZJ","6")
	text = text.replace("IDBP","7")
	text = text.replace("ZHLS","8")
	text = text.replace("NCTG","9")

medzery = list()
def stackMedz(vstupText):
	for i in range(len(vstupText)):
		if vstupText[i] == ' ':
			medzery.append(i)

def tableForm(vstupnyTex, abeceda, moz, kluc, jazyk):
	if moz == 5:
		tabI = 'ADFGX'
	if moz == 6:
		tabI= 'ADFGVX'
	vstupnyTex = diacRem(vstupnyTex)
	form = list()
	i = 0
	tab = abeceda
	dlz = len(vstupnyTex)
	while i < dlz:
		idx = changeChar(tab, vstupnyTex[i], moz, jazyk)
		y = len(tabI)
		for k in range(y):	#riadky
			if idx[0] == k:
				form.append(tabI[k]) #priradenie do pola
		k = len(tabI)
		for k in range(k):	#stlpce
			if idx[1] == k:
				form.append(tabI[k]) #priradenie
		i+=1
	form = ''.join(map(str, form))	#join
	k = 0
	sizeRad = math.ceil(len(form)/len(kluc))

	x = [[0 for i in range(len(kluc))] 
		for j in range(sizeRad)]
	
	for i in range(0, sizeRad):
		for j in range(0, len(kluc)):
			if k == len(form):
				break
			x[i][j] = form[k]
			k+=1

	return x

def posun(vstupText, kluc):
	tab = {}

	for i in kluc:
		tab[i] = []
	counter = 0

	for i in cycle(kluc):
		tab[i].append('')
		counter += 1
		if counter == len(vstupText):
			break

	for i in sorted(tab.keys()):
		tab[i] = list(vstupText[:len(tab[i])])
		vstupText = vstupText[len(tab[i]):]

	return tab

def encrypt(vstupnyText, abeceda, kluc, moz, jazyk):
	medzery.clear()
	stackMedz(vstupnyText)

	tab = tableForm(vstupnyText, abeceda, moz, kluc, jazyk)

	x = [y for x in tab for y in x]

	form = ''.join(map(str, x))
	form = form.replace('0', '')

	sifra = {}
	counter = 0

	for i in cycle(kluc):
			if i not in sifra:
					sifra[i] = ''
			sifra[i] += ''.join(form)[counter]
			counter += 1
			if counter == len(''.join(form)):
					break
	return ''.join([sifra[i] 
	for i in sorted(sifra.keys())])

def desifra(vstupText, abeceda, kluc, moz):
	pos = posun(vstupText, kluc)
	x = ''
	cnt = 0
	for i in cycle(kluc):
		x += pos[i][0]
		del pos[i][0]
		cnt += 1
		if cnt == len(vstupText):
			break
	desif = ''
	if moz == 5:		#vyber medzi ADFGVX / ADFGX
		table = 'ADFGX'	
	if moz == 6:
		table= 'ADFGVX'
	for i in range(0, len(x), 2):
		riadok = table.index(x[i])
		stlpec = table.index(x[i+1])
		desif += abeceda[riadok][stlpec]
	k = 0
	for i in medzery:	#cyklus zaciatok
		if desif[i] == ' ':	#ak je medzera break
			break
		desif = desif[:i] + ' ' + desif[i:] #medzery pre vypis
	# text = numback(desif)
	# print(text)
	return desif
		
# def main():
# 	text = 'činčila sa pasie na chodníku'
# 	key = 'klucik'

# 	sifra = encrypt(text,matica,key,5,'cz')
# 	print(sifra)

# 	Desifra= decrypt(sifra,matica,key,5)
# 	print(Desifra)

# 	print('-------------')
# 	maticaEN = genRandAlpha(5,'en')
# 	print(maticaEN)

# 	sifra = encrypt(text,maticaEN,key,5,'en')
# 	print(sifra)

# 	Desifra= decrypt(sifra,maticaEN,key,5)
# 	print(Desifra)

# 	maticaADFGVX = genRandAlpha(6,'cz')
# 	print(maticaADFGVX)

# 	sifraAdfgvx = encrypt(text, maticaADFGVX,key,6,'cz')
# 	print(sifraAdfgvx)

# 	decr = decrypt(sifraAdfgvx,maticaADFGVX,key,6)
# 	print(decr) 

# 	maticaADFGVX = genRandAlpha(6,'en')
# 	print(maticaADFGVX)

# 	sifraAdfgvx = encrypt(text, maticaADFGVX,key,6,'en')
# 	print(sifraAdfgvx)

# 	decr = decrypt(sifraAdfgvx,maticaADFGVX,key,6)
# 	print(decr) 


# if __name__ == "__main__":
#     main()

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	
	def vysOkno(self, text):
		msg = QMessageBox()
		msg.setText(text)
		msg.exec_()

	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)
		self.setupUi(self)
		self.kluc.setText('Zadaj kluc')
		self.vstupText.setText('Zadaj text pre sifrovanie')
		self.pushButton_encrypt.clicked.connect(self.encrypt)


	def encrypt(self):		
		vstupText = self.vstupText.toPlainText()
	

		kluc = self.kluc.toPlainText()

		cz = self.ceska.isChecked()

		en = self.anglicka.isChecked()

		if cz == True:
			jazyk = 'cz'
		if en == True:
			jazyk = 'en'
		if (en==True and cz==True)or(en==False and cz==False):
			self.vysOkno('Vyber jazyk pre sifrovanie')			
			return

		if self.ADGVX.isChecked():
			moz = 5
		if self.ADFGVX.isChecked():
			moz = 6
		if (self.ADFGVX.isChecked()==True and self.ADGVX.isChecked()==True)or(self.ADFGVX.isChecked()==False and self.ADGVX.isChecked()==False):
			self.vysOkno('Vyber typ šifry pre sifrovanie')			
			return

		vygenAbeceda = genAbeceda(moz, jazyk)
		table = self.Mattica
		table.blockSignals(True)
		table.setRowCount(moz)
		table.setColumnCount(moz)
		s = len(vygenAbeceda)
		for i in range(s):
			x = len(vygenAbeceda[i])
			for j in range(len(vygenAbeceda[i])):

				index = QtWidgets.QTableWidgetItem(vygenAbeceda[i][j])

				index.setTextAlignment(QtCore.Qt.AlignCenter)

				table.setItem(i, j, index)

		table.resizeColumnsToContents()

		tableColumn = table.horizontalHeader()
		tableRow = table.verticalHeader()

		tableColumn.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		tableRow.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

		sifrovanyText = encrypt(vstupText, vygenAbeceda, kluc, moz, jazyk)
		up = sifrovanyText
		i = 5
		while i < len(up):
			up = up[:i] + ' ' + up[i:]
			i = i + 6

		self.sifrovanyText.setText(up)

		posun(sifrovanyText, kluc)

		desifrovanyText = desifra(sifrovanyText, vygenAbeceda, kluc, moz)
		self.desifra.setText(desifrovanyText)

		
app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
