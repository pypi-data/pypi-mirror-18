# Tapioca Rocket.Chat

## Installation

```
pip install tapioca-rocketchat
```

## Documentation

``` python
from tapioca_rocketchat import Rocketchat

api = Rocketchat(host='your-host', token='your-token', user_id='your-user-id')
# or api = Rocketchat(host='your-host', username='your-username', password='your-password')

api.version().get()
api.rooms().get()
api.messages(room='room-id').get()
api.join(room='room-id').post()
api.send(room='room-id').post(data={'msg': 'your-message'})
api.leave(room='room-id').post()
api.logoff().post()
```