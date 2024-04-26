
## FancyBus
FancyBus is a Python messaging system that allows handling of messages with optional middleware. It's ideal for applications that need to handle different types of messages with different handlers and middleware. Based on Symfony's messenger Message Bus.

Currently is WIP.

### Features
Register handlers for different types of messages.
Middleware to process messages before they are handled.
Wrapping of messages in envelopes to add additional information.
Installation
You could install FancyBus with pip:

```
pip install fancybus
```
### Usage
Here's how you can use FancyBus in your application:

```
from fancybus import FancyBus, Message, MessageHandler, Middleware

# Create a message handler
handler = MessageHandler()

# Create a bus
bus = FancyBus(handler)

# Register a handler for a type of message
bus.register_handler(Message, lambda message: print(message))

# Dispatch a message
bus.dispatch(Message("Hello, world!"))
```
###Contributing
Contributions are welcome! Please read the contributing guidelines to get started.

### License
FancyBus is licensed under the MIT license. See the LICENSE file for more details.

### Contact
If you have any questions or comments, please open an issue on GitHub.