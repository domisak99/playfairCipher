import sys
import math
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, uic
 
qtCreatorFile = "playfair.ui"
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class PlayFair(QMainWindow, Ui_MainWindow):

    #Vytvoreni klice jako pole 5x5
    def Create_table(self):
        abc = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'
        key_array = [[0] * 5 for x in range(5)]
        key=self.klicvstup.toPlainText()
        key = key.upper();
        key = key.replace('W', 'V')
        key = key.replace('J', 'I')
        for x in range(5):
            for y in range(5):
                if len(key):
                    key_array[x][y] = key[0]
                    abc = abc.replace(key[0], '')
                    key = key.replace(key[0], '', -1)
                else:
                    key_array[x][y] = abc[0]
                    abc = abc[1:]

        self.vypis_tabulky.setColumnCount(5)
        self.vypis_tabulky.setRowCount(5)
        for i in range(5):
            for j in range(5):
                self.vypis_tabulky.setItem(i, j, QTableWidgetItem((key_array[i][j])))

        return key_array

    #Funkce pro zasifrovani sifry
    def encrypt(self):
        key_array=self.Create_table()
        message=self.vstup.toPlainText()
        message=message.upper()                     #Vysoke pismena
        message=message.replace(" ", "")            #Odstraneni mezer
        message=message.replace("J", "I")            #Zmena znaku J na I
        message=message.replace("W", "V")            #Zmena dvojteho W na V


        for i in range(0,len(message)):
            if message[i]=='j':
                message = message[:i] + 'i' + message[i+1:]
                
        for i in range(1,len(message),2):           #Vytvori dvojice a zjisti jestli jsou pismena stejne, pokud jsou vlozi mezi ne pismeno X
            if message[i-1]==message[i]:
                message = message[:i] + 'X' + message[i:]

        if(len(message)%2 != 0):                    #Pokud je delka zpravy licha prida se nakonec taktez x
            length=len(message)
            message = message[:length]+'X'

    
        chunks = [None] * math.ceil(len(message)/2)
        encrypted_message=[None] * len(message)
        
        n = 2
        index = 0

        #Rozdeleni textu po 2 pismenech
        for i in range(0, len(message), n):
            chunks[index]=message[i:i+n]
            index=index+1

        index = 0
        index1 =0
        index2 = 0
    
        
        for chunk in chunks:
            first_index = 0
            second_index = 0
            first_element = 0
            #Vlozi do promennych prvni a druhe pismeno
            first_letter=chunk[0]
            second_letter=chunk[1]
            #Pomoci funkce flatten jsem pole pretransformoval pro lepsi manipulaci (vyhovovalo mi to lepe)
            key_array = self.flatten(key_array)
            index1=key_array.index(first_letter)
            index2=key_array.index(second_letter)


            for i in range(0,21,5):
                if abs(index1-i) in range(0,5):
                    first_element=i
                    break

            #Pro pismena ve stejnem sloupci
            if abs(index1-index2)%5 == 0:
                first_index=(index1 +5)%25
                second_index=(index2 +5)%25
                encrypted_message[index] = key_array[first_index]
                index = index+1
                encrypted_message[index] = key_array[second_index]
                index=index+1
                
            #Pro pismena ve stejnem radku
            elif index2 in range(first_element,first_element + 5):
                first_index=(index1 +1)%5
                second_index=(index2 +1)%5
                encrypted_message[index] = key_array[first_index]
                index = index+1
                encrypted_message[index] = key_array[second_index]
                index=index+1
                
            #Pro pismena ktera nejsou ve stejnem sloupci/radku
            else:
                for i in range(first_element,first_element + 5):
                    if abs(index2-i)%5 ==0:
                        first_index=i
                        break
                difference=abs(first_index - index1)
                if index1 > first_index:
                    second_index=index2 + difference
                else:
                    second_index=index2 - difference

                encrypted_message[index] = key_array[first_index]
                index = index+1
                encrypted_message[index] = key_array[second_index]
                index=index+1

        str1=""
        self.vystup.setText(str1.join(encrypted_message))
    def decrypt(self):
        key_array=self.Create_table()
        message=self.vstup.toPlainText()
        message=message.upper()                         
        message=message.replace(" ", "")            

        chunks = [None] * math.ceil(len(message)/2)
        decrypted_message=[None] * len(message)
        n = 2
        index = 0

        for i in range(0, len(message), n):
            chunks[index]=message[i:i+n]
            index=index+1

        index = 0
        index1 = 0
        index2 = 0

        for chunk in chunks:
            first_index = 0
            second_index = 0
            first_element = 0

            first_letter=chunk[0]
            second_letter=chunk[1]

            key_array = self.flatten(key_array)
            index1=key_array.index(first_letter)
            index2=key_array.index(second_letter)

            for i in range(0,21,5):
                if abs(index1-i) in range(0,5):
                    first_element=i
                    break

            if abs(index1-index2)%5 == 0:
                first_index=(index1 -5)%25
                second_index=(index2 -5)%25
                decrypted_message[index] = key_array[first_index]
                index = index+1
                decrypted_message[index] = key_array[second_index]
                index=index+1

    
            elif index2 in range(first_element,first_element + 5):
                first_index=(index1 -1)%5
                second_index=(index2 -1)%5
                decrypted_message[index] = key_array[first_index]
                index = index+1
                decrypted_message[index] = key_array[second_index]
                index=index+1


            else:
                for i in range(first_element,first_element + 5):
                    if abs(index2-i)%5 ==0:
                        first_index=i
                        break
                difference=abs(first_index - index1)
                if index1 > first_index:
                    second_index=index2 + difference
                else:
                    second_index=index2 - difference

                decrypted_message[index] = key_array[first_index]
                index = index+1
                decrypted_message[index] = key_array[second_index]
                index=index+1

  
        str1=""
        self.vystup.setText(str1.join(decrypted_message))
        
    def flatten(self, input):
        new_list = []
        for i in input:
            for j in i:
                new_list.append(j)
        return new_list

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.T_sifrovat.clicked.connect(self.encrypt)
        self.T_desifrovat.clicked.connect(self.decrypt)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlayFair()
    window.show()
    sys.exit(app.exec_()) 
