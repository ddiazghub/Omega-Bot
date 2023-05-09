from typing import Tuple, Callable, List
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, Defaults
from pytz import timezone
from caesar import caesarEncrypt, caesarDecrypt
"""
Clase principal para el Bot

Parámetros:
token - Token generado por telegram para identificar al Bot.
"""


class TelegramBot(Updater):
    """
  Descripción del Bot
  """
    BOT_DESCRIPTION = """
<b>Omega Bot</b>
  
Bienvenido, mi nombre es Omega Bot. Los comandos que te permito utilizar son: 
  
$ <i>/ayuda</i> ---> Si utilizas este comando te mostraré esta descripción.

$ <i>/cifrar {mensaje} {clave}</i> ---> Con este comando debes darme un mensaje y un valor numérico. Voy a encriptar el mensaje mediante cifrado César, haciendo uso del segundo parámetro como clave o número de desplazamientos.

$ <i>/descifrar {mensaje}</i> ---> Con este comando debes darme un mensaje encriptado por mí en cifrado César. Lo que haré será descifrar el texto y responderte con el mensaje en texto plano.
"""
    """
Lista de comandos del Bot, cada comando es una tupla donde el primer parámetro es el nombre del comando y el segundo es la función a ejecutar para dar respuesta al comando
"""
    commands: List[Tuple[str, Callable]]
    """
Crea un nuevo Bot de Telegram
"""
    def __init__(self, token: str) -> None:
        # Se inicializa el Bot y se configuran valores predeterminados.
        super().__init__(token,
                         defaults=Defaults(parse_mode=ParseMode.HTML,
                                           tzinfo=timezone("America/Bogota")))

        # Se definen los comandos del Bot
        self.commands = [("start", self.help), ("ayuda", self.help),
                         ("help", self.help), ("cifrar", self.cipher),
                         ("descifrar", self.decipher)]

    """
  Se inicializa el Bot
  """

    def run(self) -> None:
        # Se lee y registra cada comando
        for command in self.commands:
            self.dispatcher.add_handler(CommandHandler(command[0], command[1]))

        # Se inicia el Bot
        self.start_polling()
        print("Bot iniciado")
        self.idle()

    """
Comando de ayuda, responde con la descripción del Bot
"""

    def help(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_html(TelegramBot.BOT_DESCRIPTION)

    """
Comando cifrar, encripta un mensaje usando cifrado césar con un determinado desplazamiento
"""

    def cipher(self, update: Update, context: CallbackContext) -> None:
        # Se valida que se suministren todos los parámetros.
        if len(context.args) < 2:
            update.message.reply_html(
                "No estás utilizando el comando correctamente. Recuerda que debes usarlo de la siguiente forma: /cifrar <i>{mensaje} {clave}</i>"
            )

            return

        # Se valida que la clave es un valor numérico entero positivo.
        if not context.args[-1].isdigit():
            update.message.reply_html(
                "No me estás dando la clave de desplazamiento. Recuerda que el comando se usa de la siguiente forma: <i>/cifrar {mensaje} {clave}</i>"
            )

            return

        # Se unen todas las palabras que hacen parte del mensaje para extraer este y se extrae la clave.
        message = ' '.join(context.args[:-1])
        key = int(context.args[-1])

        # Se responde con el mensaje cifrado.
        update.message.reply_text(f"""Mensaje cifrado:

{caesarEncrypt(message, key)}""")

    """
Comando descifrar, descifra un mensaje en cifrado césar.
"""

    def decipher(self, update: Update, context: CallbackContext) -> None:
        # Se valida que se suministró el mensaje
        if len(context.args) == 0:
            update.message.reply_html(
                "No me estás dando el mensaje a descifrar. Recuerda que el comando se usa de la siguiente forma: <i>/descifrar {mensaje}</i>"
            )

        # Se juntan las palabras que forman parte del mensaje con espacios.
        cipherText = ' '.join(context.args)

        # Se responde con el mensaje descifrado. Si ocurre algún error al descifrar el mensaje, se le notifica al usuario.
        try:
            decrypted = caesarDecrypt(cipherText)
            update.message.reply_text(f"""Mensaje descifrado:

{decrypted[1]}

Clave: {decrypted[0]}""")
        except BaseException as e:
            print(e)
            update.message.reply_html(
                f"El mensaje no es correcto, no puedo determinar la cantidad de desplazamientos para descifrarlo"
            )
