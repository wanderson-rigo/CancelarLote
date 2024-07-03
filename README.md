# Notas

Este software educacional experimental  foi desenvolvido pelo prof. Wanderson Rigo do IFC-Videira para se cancelar várias aulas no SIGAA de forma automatizada, poupando assim trabalho manual e repetitivo.

## Detalhes técnicos

Programado em Python.

As configurações a serem definidas no arquivo *config.json* são:

- "URL": "https://sig.ifc.edu.br/sigaa/verTelaLogin.do", do SIGAA
- "USERNAME": "fulano.sobrenome", nome de usuário do SIGAA
- "PASSWORD": "senha", a senha do SIGAA. Se não preencher aqui, uma caixa de diálogo vai pedir a senha.
- "SUBJECT": "Turma XYZ", nome da turma no SIGAA que precisa ter aulas canceladas.

Depois de definir as configurações, execute o arquivo *CancelarAulas.exe*

Se ocorrerem erros, eles serão descritos no arquivo *cancelar_aulas.log*