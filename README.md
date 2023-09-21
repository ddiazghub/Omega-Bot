# Omega Bot

Telegram bot which can encrypt and decrypt text messages using a modified version of Caesar encryption that includes some unicode characters.
The decryption is done without receiving the key as a parameter. When decrypting a message, the bot uses various language corpora to spell check each respective decrypted message for all the different possible keys. Each decrypted message is then given a score based on how "correct" it is. The message with the highest score is chosen as the decrypted message, which essentially brute forces the decryption.
