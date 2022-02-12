from flask import Flask, render_template
from flask_restful import Api, Resource
from S37U.views import channel

app = Flask(__name__)

# two decorators, same function
api = Api(app)

api.add_resource(channel.UpsertChannel, "/api/v1/channel/")
api.add_resource(channel.GetChannelKeyword, "/api/v1/channel/<string:channel_id>")


if __name__ == "__main__":
    app.run(host="0.0.0.0")