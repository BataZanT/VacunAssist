import smtplib

from django.dispatch import receiver                                #La verdad ni idea que es esto pero el loco del video lo importa, asi que debe ser importante :D

EMAIL = 'vacunassist.contacto@gmail.com'
PASSW = 'xoejdavfzdfnoigf'
YO = 'agustinferrrr@gmail.com'


with smtplib.SMTP('smtp.gmail.com', 587) as smtp:                   #Esto prepara la conexion con gmail, utilizando el puerto 587, y lo llamamos smtp
    smtp.ehlo()                                                     #Nos identifica con gmail
    smtp.starttls()                                                 #Encripta algo que no se como se llama
    smtp.ehlo()                                                     #Nos identificamos de nuevo porque nos encriptamos    
    smtp.login(EMAIL, PASSW)                                        #Nos logeamos (xoejdavfzdfnoigf)
   
    subject = 'Confirmacion de cuenta'                              #Asunto del email
    body = 'Este es un mensage autogenerado por VacunAssist'        #Cuerpo del email

    msg = f'Subject: {subject}\n\n{body}'                           #Es necesario formatear el mensaje (f) para que lo tome gmail

    smtp.sendmail(EMAIL, YO, msg)                                   #Para enviarlo usamos sendmail con quien lo envia, a quien y el mensaje en cuestion

print ("Hola")