#coding: utf-8
#author Henrique Lucas Gomes Rezende
import sqlite3
import kivy
kivy.require("1.9.1")
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout

Window.clearcolor=[1,1,1,1]#define o fundo padrão como brnaco
#conn=sqlite3.connect(r"C:\dev\calendario_db\calendario.db")#Conexão com o BD no windows
conn=sqlite3.connect(r"/home/henrique/projetos/Calendario/Calendario-Kivy/calendario.db")#Conexão com o BD no linux


def text(self, x, o):#exibe as informações sobre o dia
    di = {"01": "janeiro", "02": "fevereiro", "03": "março", "04": "abril", "05": "maio", "06": "junho",
          "07": "julho", "08": "agosto", "09": "setembro", "10": "outubro", "11": "novembro", "12": "dezembro"}#dicionário que informa os meses por número
    global mes
    mes = di.pop(o)#pega o mes em palavra de acordo com o seu número
    cursor = conn.execute("select " + mes + " from Calendário_2018 where dia=" + str(x.text))#busca no BD as informações
    rows = cursor.fetchall()
    dia = int(x.text)#pega o texto do dia (no caso o numero dele)
    if (dia >= 1 and dia <= 9):
        dia = str("0" + str(x.text))
    self.ids.data.text = str(dia) + "/" + str(o) + "/2018"#define qual a data deve aparecer nas informações
    global r
    for f in rows:
        r = f[0]
    self.ids.assunto.text = str(r)#informação sobre o dia

class Visualizar(StackLayout):
    def editar(self):#leva para a classe de edição
        global ed
        ed = Editar()
        ed.visul(nx,no)
    def visual(self,x,o):#visualiza as informações do dia
        tela.root_window.remove_widget(c)
        tela.root_window.remove_widget(vol)
        tela.root_window.remove_widget(nv)
        global v
        global no
        global nx
        nx=x
        no=o
        v = Visualizar()
        text(v,x,o)
        tela.root_window.add_widget(v)

    def voltar(self):#volta para o calendario
        tela.root_window.remove_widget(v)
        global vol
        vol= Calendario()
        vol.ver()
        tela.root_window.add_widget(vol)



class Editar(StackLayout):#ativa a edição das informações do dia
    def visul(self, x, o):#tela de edição
        tela.root_window.remove_widget(v)
        tela.root_window.remove_widget(nv)
        tela.root_window.remove_widget(d)
        global e
        e = Editar()
        text(e,x, o)
        tela.root_window.add_widget(e)

    def cancelar(self):#cancela as alterações
        tela.root_window.remove_widget(e)
        global nv
        nv = Calendario()
        nv.ver()
        tela.root_window.add_widget(nv)
    def salvar(self):#salva as alterações
        assunto=self.ids.assunto.text#pega o que foi registrado
        dia=nx.text
        conn.execute(
        "update Calendário_2018 set " + mes + "='" + assunto + "' where dia=" + str(dia))#registra as alterações no BD
        conn.commit()#salva o registro
        tela.root_window.remove_widget(e)#remove um widget
        global d
        d=Visualizar()
        d.visual(nx,no)


class Calendario(StackLayout):
    def dia(self,x,o):#ativa ao clicar em qualquer dia
       v=Visualizar()
       v.visual(x,o)
    def ver(self):#volta a tela do calendário
        tela.root_window.remove_widget(tela.root)  # root_window acessa o topo da hierarquia, remove o topo da hierarquia
        global c
        c = Calendario()
        tela.root_window.add_widget(c)#adiciona um novo widget


class Tela(FloatLayout):#primeira tela
    def ver(self):#botão Ver Calendario
       c=Calendario()
       c.ver()#Chama a tela do calendario


class CalApp(App):#classe princiapl que imorta o arquivo kivy
    #inicialização das variaveis
    global vol
    global d
    global nv
    global c
    c=None
    vol = None
    d = None
    nv = None

tela=CalApp()
tela.title="Calendário"
tela.run()
conn.close()
