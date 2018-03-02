class ButtonSystem:
    def __init__(self, buttons):
        self.buttons = buttons

    def poll(self):
        for button in self.buttons:
            if button.poll():
                return button.name

        return None
