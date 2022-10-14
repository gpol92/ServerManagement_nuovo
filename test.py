from cgitb import html


fileHTML = open('test.html', "a")
nome = input("Inserisci nome")
htmlContent = '''<p>{}</p>'''.format(nome)
fileHTML.write(htmlContent)