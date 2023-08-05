from notify import *
from button_matcher import Click


class EventReceiver(object):
    def __init__(self, button_matcher):
        self.button_matcher = button_matcher

    def receive_mouse_event(self, event):
        Notify.show_notification(
            "MouseEvent: x = %s, y = %s, screenshot = %s" % (event.click_x, event.click_y, event.screenshot))
        self._save_event_screenshot(event)
        button = self.button_matcher.find_button_on_clicked_position(Click(event.click_x, event.click_y), event.screenshot)
        if button is not None:
            print("You clicked on button")

    def receive_keyboard_state_change_event(self, event):
        Notify.show_notification("Keys pressed : %s" % event.pressed_keys)

    def _save_event_screenshot(self, event):
        event.screenshot.save("screenshot_x_" + str(event.click_x) + "_y_" + str(event.click_y) + ".png", "PNG")
