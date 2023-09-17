from typing import Union, Optional
#from forwarder.modules.filters import FilterMessage
from telegram import Update, Message, MessageId
from telegram.error import ChatMigrated
from telegram.ext import MessageHandler, filters, ContextTypes

from forwarder import bot, REMOVE_TAG, LOGGER
from forwarder.utils import get_source, get_destenation, parse_topic

async def send_message(
    message: Message, chat_id: int, thread_id: Optional[int] = None
) -> Union[MessageId, Message]:
    if REMOVE_TAG:
        return await message.copy(chat_id, message_thread_id=thread_id)  # type: ignore
    return await message.forward(chat_id, message_thread_id=thread_id)  # type: ignore

async def forwarder(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    source = update.effective_chat
#    filter_forward = FilterMessage(message)
#    if filter_forward == 400:
#        return 400
    if not message or not source:
        return

    for chat in get_destenation(source.id):
        try:
            await send_message(message, chat["chat_id"], thread_id=chat["thread_id"])
        except ChatMigrated as err:
            await send_message(message, err.new_chat_id)
            LOGGER.warning(
                f"Chat {chat} has been migrated to {err.new_chat_id}!! Edit the config file!!"
            )
        except Exception as err:
            LOGGER.warning(f"Failed to forward message from {source.id} to {chat} due to {err}")


FORWARD_HANDLER = MessageHandler(
    filters.Chat([source["chat_id"] for source in get_source()])
    & ~filters.COMMAND
    & ~filters.StatusUpdate.ALL,
    forwarder,
    filters.Document,
    filters.VIDEO,
)
bot.add_handler(FORWARD_HANDLER)

# document

# Message Filters
# filters.ALL             All Messages will Forward 
# filters.VIDEO           Filter Videos
# filters.Document        Filter Documents 
# filters.ANIMATION       Filter Animations
# filters.FORWARDED       Filter Forwarded Messages 
# filters.AUDIO           Filter Audios
# filters.POLL            Filter Polls (Quiz Message)
# filters.TEXT            Filter Text Messages
# filters.Document.ALL    Filter All Documents
# filters.Document.AUDIO  Filter Document Audios 
# filters.Document.VIDEO  Filter Document Videos
# filters.Sticker.ALL     Filter Stickers
# filters.Document.IMAGE  Filter Document Image
# filters.Document.PDF    Filter Document PDF
# filters.PHOTO           Filter Photo
