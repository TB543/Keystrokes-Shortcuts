from window import *


class DoneRecording(Window):
    """
    a class for the window when finished recording actions

    2 options:
        --> run recorded actions
        --> save shortcut
    """

    def __init__(self):
        """
        creates the window
        """

        # initializes super class and settings
        super().__init__(250)
        self.title('Done Recording')
        self.actions = None

        # creates window widgets and places them
        self.all_widgets.extend([[CTkFrame(self.all_widgets[-1][0]), 0, 5, LEFT, BOTH, True],
                                 [CTkFrame(self.all_widgets[-1][0]), 0, 5, RIGHT, BOTH, True]])
        self.all_widgets.extend([
            [CTkLabel(self.all_widgets[-2][0], text='Run:', text_font=('Roboto Medium', -16)), 10],
            [CTkLabel(self.all_widgets[-2][0], text='Repetitions:', text_font=('Roboto Medium', -16))],
            [CTkEntry(self.all_widgets[-2][0], placeholder_text='Enter An Integer')],
            [CTkCheckBox(self.all_widgets[-2][0], text='No Delay', onvalue=True, offvalue=False,
                         variable=BooleanVar(value=True)), 10],
            [CTkButton(self.all_widgets[-2][0], text='Run', command=lambda: self.run(
                self.actions, self.all_widgets[5][0].get(), self.all_widgets[6][0].get()))],
            [CTkLabel(self.all_widgets[-1][0], text='Save:', text_font=('Roboto Medium', -16)), 10],
            [CTkLabel(self.all_widgets[-1][0], text='Shortcut Name:', text_font=('Roboto Medium', -16))],
            [CTkEntry(self.all_widgets[-1][0], placeholder_text='Enter Name')],
            # [CTkCheckBox(self.all_widgets[-1][0], text='Require Password', onvalue=True, offvalue=False, #todo
            #              variable=BooleanVar(value=False)), 10],
            [CTkButton(self.all_widgets[-1][0], text='Save', command=self.save), 10]])  # todo remove pack 10
        self.place_widgets(self.all_widgets)

    def mainloop(self, actions: list):
        """
        a modified mainloop function set change the recorded actions and determine if it should run

        :param actions: a list of recorded actions that the user can run or save
        """

        # runs if actions exist
        if actions:
            self.actions = actions
            super().mainloop()

        # otherwise does nothing
        else:
            pass

    def set_appearance_mode(self, mode_string):
        """
        a modified set appearance mode method to hide the window after the new appearance mode has been set

        :param mode_string: the appearance mode to be set to, if None given nothing will happen
        """

        if mode_string:
            super().set_appearance_mode(mode_string)
            self.withdraw()

    def save(self):
        """
        saves the recorded actions to be played back later
        also configures data to be converted to automation if possible todo make error widgets and success widget
        """

        # makes sure a valid name is given
        name = self.all_widgets[10][0].get()
        if not name:
            raise NameError('enter a name')
        elif list(Window.shortcuts_loaded.keys()).count(name) > 0:
            raise NameError('name already exists')

        # saves the shortcut if there are no errors
        else:

            # asks user for password if checked todo
            # if self.all_widgets[11][0].get():
            #     password = CTkInputDialog(
            #         title='Enter Password', text='Enter A Password For This Shortcut:').get_input()

            # converts recorded action data to usable data type
            actions = []
            for event in self.actions:
                actions.append(vars(event))

            # saves the data and updates display widgets
            Window.shortcuts_unloaded[name] = {'actions': actions}
            self.write_to_file('saves/shortcuts.keystrokeshortcuts', Window.shortcuts_unloaded)
            Window.shortcuts_loaded[name] = {'actions': self.actions}
            self.update_widgets('shortcuts')
