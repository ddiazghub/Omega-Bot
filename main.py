import nltk

nltk.download("omw-1.4")
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("names")
nltk.download("stopwords")
nltk.download("cess_esp")
nltk.download("conll2002")
nltk.download("words")
print("")

from bot import TelegramBot
from os import getenv
from sys import exit, stderr

if __name__ == "__main__":
  # Se obtiene el token generado en telegram de la variable de entorno "BOT_TOKEN". (Para que el programa funcione esta variable de entorno debe estar definida)
  BOT_TOKEN = getenv("BOT_TOKEN")

  # Si la variable de entorno no está definida, se muestra un mensaje de error y se termina el programa.
  if BOT_TOKEN is None:
    print("Error: Defina una variable de entorno llamada \"BOT_TOKEN\" y asígnele el token de su Bot", file=stderr)
    exit(1)

  # Se inicializa el bot, pasándole como parámetro el token. Si no se logra inicializar se muestra un mensaje de error y se termina el programa.
  try:
    bot = TelegramBot(BOT_TOKEN)
    bot.run()
  except:
    print("Error: No se pudo iniciar el bot, asegúrese de haber utilizado el token correcto", file=stderr)
    exit(1)