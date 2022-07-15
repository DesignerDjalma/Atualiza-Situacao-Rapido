import arcpy

import sys 
reload(sys) # ignore
sys.setdefaultencoding("utf-8")


def texto(txt):
    """Recebe uma string e formata ao padrão utf-8"""
    return txt.encode('cp1252')


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Atualizador de Mapa de Situação"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [AtualizaSituacao]


class Argumentos:
    pString = {
    "datatype":"GPString",
    "parameterType":"Required",
    "direction":"Input",
    }


class AtualizaSituacao(object):
    def func_atualiza_situacao(self, mxd, lista):
        """Atualiza o mapa de situacao de acordo com as 
        entradas fornecidas (1 ou mais): EX.:
        att_situacao('BELÉM','ACARÁ',...)"""

        UNICODES_LOWERCASE = ['\xc3\xa1',
            '\xc3\xa9','\xc3\xad',
            '\xc3\xb3','\xc3\xba',
            '\xc3\xa3','\xc3\xb5',
            '\xc3\xa2','\xc3\xaa',
            '\xc3\xae','\xc3\xb4',
            '\xc3\xbb','\xc3\xa7',
            ]

        UNICODES_UPPERCASE = ['\xc3\x81',
            '\xc3\x89','\xc3\x8d',
            '\xc3\x93','\xc3\x9a',
            '\xc3\x83','\xc3\x95',
            '\xc3\x82','\xc3\x8a',
            '\xc3\x8e','\xc3\x94',
            '\xc3\x9b','\xc3\x87',
            ]

        DEFINITION_QUERY_SITUACAO = {
            1:"{}nmSede = \'{}\'",
            2:"{}nmMun <> \'{}\'",
            3:"{}nmMun = \'{}\'",
            }

        P = DEFINITION_QUERY_SITUACAO
        UNI = UNICODES_UPPERCASE
        uni = UNICODES_LOWERCASE
        #municipio = tuple([municipios]) + args
        municipio = tuple(lista)
        EXP = ['1', '2', '3']
        fz = 1.084556648631034
        df = False
        
        cmds = arcpy.mapping.ListLayers(mxd)
        cdi = [cmd for exp in EXP for cmd in cmds if cmd.description[:1] == exp]
        
        if municipio[0] == 'nenhum':
            e1 = e2 = e3 = ""
            for i, (c, exp) in enumerate(zip(cdi, [e1, e2, e3])):
                c.definitionQuery = exp
            arcpy.RefreshActiveView()
            return

        if not df:
            df = arcpy.mapping.ListDataFrames(mxd)[-1]

        if municipio and isinstance(municipio, tuple):
            lm = []
            for m in municipio:
                m.replace(" ", "")
                m = m.upper()
                for u, U in zip(uni, UNI):
                    m = m.replace(u,U)

                lm.append(m)
            for i, v in enumerate(lm):

                if i == 0:
                    e1 = P[1].format("", v)
                    e2 = P[2].format("", v)
                    e3 = P[3].format("", v)
                    continue

                e1 += P[1].format(" OR ", v)
                e2 += P[2].format(" AND ",v)
                e3 += P[3].format(" OR ", v)

        if municipio and isinstance(municipio, str):
            municipio = municipio.upper()
            for u, U in zip(uni, UNI):
                municipio = municipio.replace(u,U)
                m = municipio

            e1 = P[1].format("",m)
            e2 = P[2].format("",m)
            e3 = P[3].format("",m)
        
        for i, (c, exp) in enumerate(zip(cdi, [e1, e2, e3])):
            c.definitionQuery = exp
            if i == 2:
                z = c.getSelectedExtent()

        df.extent = z
        df.scale *= fz

        arcpy.RefreshActiveView()
    
    def __init__(self):
        self.label = texto("Atualizador de Mapa de Situação")
        self.description = texto("Essa feramenta faz a atualização do definitions querys muito rápido.")
        self.canRunInBackground = False

    def getParameterInfo(self):
        municipio = arcpy.Parameter(displayName=texto('Município'),name='municipio',**Argumentos.pString)
        params = [municipio]
        return params

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        mxd, true_list = atualizaMapaDeSitucao(parameters[0].valueAsText, messages)
        self.func_atualiza_situacao(mxd, true_list)
        return



def atualizaMapaDeSitucao(parametro, mensagem):
    mxd = arcpy.mapping.MapDocument("Current")
    municipios = texto(parametro)
    lista = municipios.split(',')
    true_list = []
    for i in lista:
        if i[0] == " ":
            true_list.append(i[1:])
        else:
            true_list.append(i)
    mensagem.addMessage('municipios {}'.format(municipios))
    mensagem.addMessage('lista {}'.format(true_list))
    return mxd, true_list




# comentario inutil



