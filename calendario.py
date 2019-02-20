#coding: utf-8
#author Henrique Lucas Gomes Rezende
import sqlite3
import kivy
kivy.require("1.9.1")
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.lang import Builder

Window.clearcolor=[1,1,1,1]
conn=sqlite3.connect(r"C:\dev\calendario_db\calendario.db")

vol=None
d=None
nv=None
class Visualizar(StackLayout):
    def editar(self):
        global ed
        ed = Editar()
        ed.visul(nx,no)
    def visual(self,x,o):
        tela.root_window.remove_widget(t)  # root_window acessa o topo da hierarquia
        tela.root_window.remove_widget(vol)
        tela.root_window.remove_widget(nv)
        global v
        global no
        global nx
        nx=x
        no=o
        v = Visualizar()
        v.text(x,o)
        tela.root_window.add_widget(v)

    def text(self,x,o):
        di = {"01": "janeiro", "02": "fevereiro", "03": "março", "04": "abril", "05": "maio", "06": "junho",
              "07": "julho", "08": "agosto", "09": "setembro", "10": "outubro", "11": "novembro", "12": "dezembro"}
        mes=di.pop(o)
        cursor = conn.execute("select "+mes+" from Calendário_2018 where dia="+str(x.text))
        rows = cursor.fetchall()
        dia=int(x.text)
        if(dia>=1 and dia<=9):
            dia = str("0" + str(x.text))
        self.ids.data.text=str(dia)+"/"+str(o)+"/2018"
        global r
        for f in rows:
            r=f[0]
        self.ids.assunto.text=str(r)
    def voltar(self):
        tela.root_window.remove_widget(v)  # root_window acessa o topo da hierarquia
        global vol
        vol= Calendario()
        vol.ver()
        tela.root_window.add_widget(vol)

nv=None


class Editar(StackLayout):
    def visul(self, x, o):
        tela.root_window.remove_widget(v)  # root_window acessa o topo da hierarquia
        tela.root_window.remove_widget(nv)
        tela.root_window.remove_widget(d)
        global e
        e = Editar()
        e.text(x, o)
        tela.root_window.add_widget(e)

    def text(self, x, o):
        di = {"01": "janeiro", "02": "fevereiro", "03": "março", "04": "abril", "05": "maio", "06": "junho",
              "07": "julho", "08": "agosto", "09": "setembro", "10": "outubro", "11": "novembro", "12": "dezembro"}
        global mes
        mes = di.pop(o)
        cursor = conn.execute("select " + mes + " from Calendário_2018 where dia=" + str(x.text))
        rows = cursor.fetchall()
        dia = int(x.text)
        if (dia >= 1 and dia <= 9):
            dia = str("0" + str(x.text))
        self.ids.data.text = str(dia) + "/" + str(o) + "/2018"
        global r
        for f in rows:
            r = f[0]
        self.ids.assunto.text = str(r)

    def cancelar(self):
        tela.root_window.remove_widget(e)  # root_window acessa o topo da hierarquia
        global nv
        nv = Calendario()
        nv.ver()
        tela.root_window.add_widget(nv)
    def salvar(self):
        assunto=self.ids.assunto.text
        dia=nx.text
        conn.execute(
        "update Calendário_2018 set " + mes + "='" + assunto + "' where dia=" + str(dia))
        conn.commit()
        tela.root_window.remove_widget(e)
        global d
        d=Visualizar()
        d.visual(nx,no)


class Calendario(StackLayout):
    def dia(self,x,o):
       i=Visualizar()
       i.visual(x,o)
    def ver(self):
        tela.root_window.remove_widget(tela.root)  # root_window acessa o topo da hierarquia
        global t
        t = Calendario()
        tela.root_window.add_widget(t)


class Tela(FloatLayout):
    def botao1(self):
       i=Calendario()
       i.ver()

    def botao2(self):
        try:
            a = 10 / 0
        except ZeroDivisionError:
            pass


class CalApp(App):
    pass

tela=CalApp()
tela.title="Calendário"
tela.run()
conn.close()

#print("Bem Vindo ao Calendário Anula de 2018!\nOpções:\n1-Ver meu Calendário\n2-Editar meu Calendário\n3-Sair")
#  def botao1(self):
#        cursor = conn.execute("select * from Calendário_2018")
#        rows = cursor.fetchall()
#        for row in rows:
#            print(row)
#
# def botao1(self):
#    return Calendario()
#def botao2(self):
#    assunto = input("Qual o assunto do dia?\n")
#   mes = input("Qual mes refe
# rente?\n")
#    dia = input("Qual dia referente?\n")
#    conn.execute(
#        "update Calendário_2018 set " + mes + "='" + assunto + "' where dia=" + str(dia))  # maique gambiarra buníta so
#    conn.commit()


