#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
# librerías de google cloud
from google.cloud import dialogflow_v2beta1 as dialogflow
from google.api_core.exceptions import InvalidArgument
# reproducir los vídeos
import cv2
# poner el texto en color
import colorama
from colorama import Fore


# In[2]:


# conecto con el chatbot de Dialogflow
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'DialogdlowKey.json'

DIALOGFLOW_PROJECT_ID = 'traductorbot-whkt'
DIALOGFLOW_LANGUAGE_CODE = '[en]'
SESSION_ID = 'me'


# In[3]:


print('Antes de comenzar, asegúrese de que el texto que desea traducir a Lenguaje de Signos en Español sea en castellano')
print('Intentaremos proporcionar la mejor traducción de su texto')
print('')
print('¿Qué texto desea traducir?')
frase = input()


# In[4]:


frase=frase.lower()
frase


# In[5]:


# función para eliminar las tildes y diéresis
def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("ä", "a"),
        ("ë", "e"),
        ("ï", "i"),
        ("ö", "o"),
        ("ü", "u"),     
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s


# In[6]:


frase=normalize(frase)
frase


# In[7]:


length = len(frase.split())
length


# In[8]:


frase=frase.split()
frase


# In[16]:


for i in range(0, length):   
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=frase[i], language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    # Imprimo la palabra que se va a traducir
    print(Fore.RED + '\033[1m' + "Palabra a traducir:", response.query_result.query_text + '\033[0m')
    # Imprimo la apalbra/frase de donde el chatbot extrae el vídeo
    # Elimino los primeros 28 caracteres ya que las primeras 28 letras de los intents son
    # Knowledge.Database.Palabras.
    print(Fore.BLUE + '\033[1m' + "Palabra o frase detectada:", response.query_result.intent.display_name[28:] + '\033[0m')
    # Imprimo la confianza de que la palabra sea la correcta o similar
    print(Fore.GREEN + '\033[1m' + "Porcentaje de confianza:", response.query_result.intent_detection_confidence*100,'%' + '\033[0m')
    # Imprimo el identificador del vídeo
    print(Fore.YELLOW + '\033[1m' + "Identificador del vídeo:", response.query_result.fulfillment_text + '\033[0m')
    print()
    
    # Código para reproducir los vídeos
    capture = cv2.VideoCapture('./Videos/'+response.query_result.fulfillment_text+'.mp4')

    while (capture.isOpened()):
        ret, frame = capture.read()
        if (ret == True):
            cv2.imshow(response.query_result.intent.display_name, frame)
            if (cv2.waitKey(30) == ord('s')):
                break
        else:
            break

    capture.release()
    cv2.destroyAllWindows()

