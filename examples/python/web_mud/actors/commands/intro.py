from typing import Callable


def run(cmd: str,
        out: Callable[[str], None],
        new: Callable[[str], None],
        load: Callable[[str], None]):
    if not cmd:
        text = (
            'Du verlierst die Besinnung...<br>'
            '<br>'
            'Du tauchst in einen Strudel bunter Farben ein.<br>'
            'Ein kleiner grüner Steinbeisser erscheint.<br>'
            '<br>'
            'Der Steinbeisser sagt:<br>'
            '  ''Willkommen im Mud.''<br>'
            '<br>'
            'Der Steinbeisser warnt dich:<br>'
            '  ''Wehe, Du machst hier etwas kaputt.<br>'''
            '<br>'
            'Der Steinbeisser verschwindet wieder, und Du wachst in einer anderen Welt wieder auf.<br>'
            'Wie heisst Du denn ("neu" für neuen Avatar)?<br>')
        out(text)
    elif cmd == 'neu':
        new('')
    else:
        load(cmd)
