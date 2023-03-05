from sqlalchemy.orm import Session

from database.chat import ChatRecord
from schema.chat import Chat


def get_last_two_chats(session: Session, af_chat: Chat):
    limit = 2
    chat_records = (
        session.query(ChatRecord)
        .filter(ChatRecord.user_id == af_chat.user_id)
        .order_by(ChatRecord.created_at.desc())
        .limit(limit)
    )

    return chat_records


def get_chat_context(session: Session, user_chat: Chat):
    depth = 5
    chat_records = (
        session.query(ChatRecord)
        .filter(ChatRecord.user_id == user_chat.user_id)
        .order_by(ChatRecord.created_at.asc())
        .limit(depth)
    )
    chat_context = [
        {"role": "system", "content": user_chat.behaviour},
    ]
    for chat_record in chat_records:
        chat = Chat.from_orm(chat_record)
        if chat.is_prompt:
            chat_context.append(
                {"role": "user", "content": chat.text},
            )
        else:
            chat_context.append(
                {"role": "assistant", "content": chat.text},
            )

    chat_context.append(
        {"role": "user", "content": user_chat.text},
    )
    return chat_context
