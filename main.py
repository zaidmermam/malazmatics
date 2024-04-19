from telegram.ext import Updater, CommandHandler

def echo(update, context):
  """Responds to any message with a nerd emoji GIF"""
  nerd_gif_url = "https://media1.tenor.com/m/qhM54DikB7cAAAAC/nerd-emoji.gif"  # Replace with desired GIF URL if needed
  context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
  context.bot.send_animation(chat_id=update.effective_chat.id, animation_url=nerd_gif_url)

def main():
  """Starts the bot"""
  # Replace with your actual bot token (keep it private!)
  updater = Updater("6255596860:AAFVu3vCmRW9G7BjujcEnhJiMJCGyFj7joI")
  dispatcher = updater.dispatcher

  # Handle all messages with the echo function
  dispatcher.add_handler(CommandHandler("echo", echo))  # You can remove this line if you don't want a specific command

  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
  main()