import random

from e2c.comp.signal import Signal

from loki.comp.contracts.token import FToken


# ======================================================= #
# PLAYER OBJECT
# ======================================================= #

class Player(object):
    """ Represents the object for each player in comp.engine.
    """

    unknow_messages = [
        'Wie bitte?',
        'Was soll das sein?',
        'Sowas kenne ich nicht!',
        'Machst du Witze?',
        'Das kenne ich nicht!',
        'Keine Ahnung was das sein soll!',
        'Wie? Was? Verstehe ich nicht!',
        'So ein Unsinn!',
    ]

    output = Signal(lambda text, token: ...)
    """ The event to send message. """

    flush = Signal(lambda text: ...)
    """ The flush signal. """

    truncate_text = Signal(lambda msg: ...)
    """ Truncates the text. """

    parse = Signal(lambda player, text: ...)
    """ The event to parse the input. """

    def __init__(self):
        self.avatar = None
        self.buffer = []
        self.tasks = []

    def command(self, command: str = ''):
        """ Do the player action.
        """
        self.parse.emit(self, command or '')

    def command_unknow(self):
        """ Sends the unknow command message.
        """
        # Verstehe ich nicht.
        system_random = random.SystemRandom()
        self.send(system_random.choice(self.unknow_messages) + '<br>', FToken.text)

    def send(self, msg: str, token: FToken, commit:bool=False):
        """ Sends the given message to the player.
        """
        msg = self.truncate_text.emit(msg)
        self.buffer.append(self.output.emit(msg, token))
        if commit:
            self.commit()

    def commit(self):
        """ Commits the buffer. 
        """
        if self.buffer:
            self.flush.emit("".join(self.buffer))
        self.buffer.clear()
