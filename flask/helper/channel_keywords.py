from helper import send_message
import logging
import json
from models import Channel

logger = logging.getLogger(__name__)


def get_channel_keywords_info_db(channel_name):
    pass


def get_all_channel_info():

    channel_data = json.loads(Channel.objects().to_json())
    return {"status": "success", "data": channel_data}


def get_channel_info(channel_id):

    channel_data = Channel.objects(channel_id=channel_id).first().to_json()
    if channel_data is not None:
        return {"status": "success", "data": channel_data}
    else:
        return {{"status": "failure", "data": "channel not found"}}


def return_channel_name(channel_id):
    from slack_sdk import WebClient
    import os

    client = WebClient(token=os.environ.get("BOT_TOKEN"))

    channel_name = client.conversations_info(channel=channel_id).data["channel"]["name"]
    return channel_name


def update_channel_info(request_data):
    try:
        channel_id = request_data["channel_id"]
        keywords = request_data["keywords"]
    except Exception as e:
        logger.error(e)
        return {"status": "failure", "message": "incorrect request"}

    try:
        channel = Channel.objects(channel_id=channel_id).first()
        if channel is None:
            channel_name = return_channel_name(channel_id)
            channel_obj = Channel(
                channel_id=channel_id,
                channel_name=channel_name,
                keywords=keywords,
                subreddits=[],
            )
            channel_obj.save()
            return {"status": "success", "data": json.loads(channel_obj.to_json())}

        else:
            channel.update(keywords=keywords)
            return {"status": "success", "data": channel.to_json()}
    except Exception as e:
        logger.error(e)
        return {"status": "failure", "data": "keyword not updated"}
