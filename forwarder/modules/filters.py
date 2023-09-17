import os
from pyrogram.types import Message

FILES_FILTERS = "video document"
DEFAULT_FILTERS = "video document photo audio text gif forwarded poll sticker"
FORWARD_FILTERS = list(set(x for x in os.environ.get("FORWARD_FILTERS", FILES_FILTERS).split()))    

async def FilterMessage(message: Message):
    if (message.forward_from or message.forward_from_chat) and ("forwarded" not in FORWARD_FILTERS):
        return 400
    if (len(FORWARD_FILTERS) == 9) or ((message.video and ("video" in FORWARD_FILTERS)) or (message.document and ("document" in FORWARD_FILTERS)) or (message.photo and ("photo" in FORWARD_FILTERS)) or (message.audio and ("audio" in FORWARD_FILTERS)) or (message.text and ("text" in FORWARD_FILTERS)) or (message.animation and ("gif" in FORWARD_FILTERS)) or (message.poll and ("poll" in FORWARD_FILTERS)) or (message.sticker and ("sticker" in FORWARD_FILTERS))):
        return 200
    else:
        return 400
