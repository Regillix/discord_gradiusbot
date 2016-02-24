import asyncio
from datetime import datetime
import traceback
import elasticsearch

es = elasticsearch.Elasticsearch()

print("[Public Plugin] <log_messages.py>: Log messages to ElasticSearch.")


def setup_index():
    elastic = elasticsearch.Elasticsearch()
    try:
        mapping = {
            "chat_message": {
                "properties": {
                    "server": {"type": "string"},
                    "author": {"type": "string", "index": "not_analyzed"},
                    "channel": {"type": "string", "index": "not_analyzed"},
                    "content": {"type": "string"},
                    "timestamp": {"type": "date"},
                    "author_id": {"type": "string"},
                }
            }
        }

        elastic.indices.create("discord_chat")
        elastic.indices.put_mapping(index="discord_chat", doc_type="chat_message", body=mapping)

    except:
        traceback.print_exc()


@asyncio.coroutine
def action(message, client, config):
    try:
        author = str(message.author)
        content = message.clean_content
        server = str(message.server)
        channel = str(message.channel)
        timestamp = datetime.utcnow()
        author_id = str(message.author.id)

        body = {"author_id": author_id, "server": server, "author": author, "channel": channel, "content": content,
                "timestamp": timestamp}

        es.index(index='discord_chat', doc_type='chat_message', body=body)

    except:
        traceback.print_exc()
