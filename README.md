# Notas

Este software educacional experimental  foi desenvolvido pelo prof. Wanderson Rigo do IFC-Videira para se cancelar várias aulas no SIGAA de forma automatizada, poupando assim trabalho manual e repetitivo.

As aulas podem ser canceladas por INTERVALO ou REPETIÇÃO.
- a) INTERVALO, insira a data inicial e a data final e clique no botão 'Cancelar Aulas'.
- b) REPETIÇÃO, insira a data inicial, a quantidade de dias entre as aulas e o número de repetições e clique no botão 'Cancelar Aulas'.


## Detalhes técnicos

Programado em Python no Inverno de 2024.

As configurações a serem definidas no arquivo *config.json* são:

- "URL": "https://sig.ifc.edu.br/sigaa/verTelaLogin.do", do SIGAA
- "USERNAME": "fulano.sobrenome", nome de usuário do SIGAA
- "PASSWORD": "senha", a senha do SIGAA. Se não preencher aqui, uma caixa de diálogo vai pedir a senha.
- "SUBJECT": "Turma XYZ", nome da turma no SIGAA que precisa ter aulas canceladas.

Depois de definir as configurações, execute o arquivo *CancelarAulas.exe*

Se ocorrerem erros, eles serão descritos no arquivo *cancelar_aulas.log*