import sys
from mouse_events import FullscreenMouseEventCreator, MouseEventListener, MouseClickEventListener, \
    FixedSizeScreenshotEventCreator
from events import EventReceiver
from screen import ScreenshotTaker, ScreenManager
from keyboard_events import KeyboardEventListener, KeyboardListener, KeyboardStateManager
from repository import ButtonRepository, ShortcutRepository, ShortcutStatRepository, ButtonStatRepository
from button_matcher import ButtonMatcher
from template_matcher import CCOEFFNORMEDTemplateMatcher
from database import *
from program_identifier import *
from time import sleep
from statistic import StatisticCollector
import signal


def exit_program(signal, frame):
    print('Keycat terminated!')
    sys.exit(0)


def main():
    session = get_database_scoped_session()
    button_repository = ButtonRepository(session)
    shortcut_repository = ShortcutRepository(session)
    shortcut_stat_repository = ShortcutStatRepository(session)
    button_stat_repository = ButtonStatRepository(session)
    statistic_collector = StatisticCollector(shortcut_stat_repository, button_stat_repository)
    if len(button_repository.find_all_buttons()) == 0:
        load_data_to_database(button_repository)

    program_identifier = ProgramIdentifier()
    button_matcher = ButtonMatcher(CCOEFFNORMEDTemplateMatcher(), button_repository)

    event_receiver = EventReceiver(button_matcher, shortcut_repository, statistic_collector)

    keyboard_event_listener = KeyboardEventListener(KeyboardListener(
        KeyboardStateManager(event_receiver, program_identifier)))
    keyboard_event_listener.daemon = True
    keyboard_event_listener.start()

    mouse_event_creator = FixedSizeScreenshotEventCreator(ScreenshotTaker(), ScreenManager(), program_identifier,
                                                          700, 100)

    mouse_click_listener = MouseClickEventListener(
        MouseEventListener(mouse_event_creator, event_receiver))
    mouse_click_listener.daemon = True
    mouse_click_listener.start()

    while 1:
        signal.signal(signal.SIGINT, exit_program)
        sleep(1)


if __name__ == '__main__':
    sys.exit(main())
