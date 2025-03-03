from os import linesep

from axelrod_evo.action import Action
from axelrod_evo.player import Player
from prompt_toolkit import prompt
from prompt_toolkit.validation import ValidationError, Validator

try:  # pragma: no cover
    from prompt_toolkit.styles import style_from_dict
    from prompt_toolkit.token import Token

    token_toolbar = Token.Toolbar
    bottom_toolbar_name = "get_bottom_toolbar_tokens"
    PROMPT2 = False

except ImportError:  # prompt_toolkit v2
    from prompt_toolkit.styles import Style

    style_from_dict = Style.from_dict
    token_toolbar = "pygments.toolbar"
    bottom_toolbar_name = "bottom_toolbar"
    PROMPT2 = True

C, D = Action.C, Action.D

toolbar_style = style_from_dict({token_toolbar: "#ffffff bg:#333333"})


class ActionValidator(Validator):
    """
    A class to validate input from prompt_toolkit.prompt
    Described at http://python-prompt-toolkit.readthedocs.io/en/latest/pages/building_prompts.html#input-validation
    """

    def validate(self, document) -> None:
        text = document.text

        if text and text.upper() not in ["C", "D"]:
            raise ValidationError(
                message="Action must be C or D", cursor_position=0
            )


class Human(Player):
    """
    A strategy that prompts for keyboard input rather than deriving its own
    action.

    This strategy is intended to be used interactively by a user playing
    against other strategies from within the rest of the library. Unlike
    other strategies, it is designed to be a teaching aid rather than a
    research tool.
    """

    name = "Human"
    classifier = {
        "memory_depth": float("inf"),
        "stochastic": True,
        "long_run_time": True,
        "inspects_source": True,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self, name="human", c_symbol="C", d_symbol="D"):
        """
        Parameters
        ----------
        name: string
            The name of the human player
        c_symbol: string
            A symbol to denote cooperation within the history toolbar
            and prompt
        d_symbol: string
            A symbol to denote defection within the history toolbar
            and prompt
        """
        super().__init__()
        self.human_name = name
        self.symbols = {C: c_symbol, D: d_symbol}

    def _history_toolbar(self):
        """
        A prompt-toolkit function to define the bottom toolbar.
        Described at http://python-prompt-toolkit.readthedocs.io/en/latest/pages/building_prompts.html#adding-a-bottom-toolbar
        """
        my_history = [self.symbols[action] for action in self.history]
        opponent_history = [
            self.symbols[action] for action in self.history.coplays
        ]
        history = list(zip(my_history, opponent_history))
        if self.history:
            content = "History ({}, opponent): {}".format(
                self.human_name, history
            )
        else:
            content = ""
        return content

    def _status_messages(self):
        """
        A method to define the messages printed to the console and
        displayed in the prompt-toolkit bottom toolbar.

        The bottom toolbar is defined only if a match is in progress.

        The console print statement is either the result of the previous
        turn or a message indicating that new match is starting.

        Returns
        -------
        dict
            mapping print or toolbar to the relevant string
        """
        if self.history:
            toolbar = (
                self._history_toolbar
                if PROMPT2
                else lambda cli: [(token_toolbar, self._history_toolbar())]
            )
            print_statement = (
                "{}Turn {}: {} played {}, opponent played {}".format(
                    linesep,
                    len(self.history),
                    self.human_name,
                    self.symbols[self.history[-1]],
                    self.symbols[self.history.coplays[-1]],
                )
            )
        else:
            toolbar = None
            print_statement = "{}Starting new match".format(linesep)

        return {"toolbar": toolbar, "print": print_statement}

    def _get_human_input(self) -> Action:  # pragma: no cover
        """
        A method to prompt the user for input, validate it and display
        the bottom toolbar.

        Returns
        -------
        string
            Uppercase C or D indicating the action to play
        """
        action = prompt(
            "Turn {} action [C or D] for {}: ".format(
                len(self.history) + 1, self.human_name
            ),
            validator=ActionValidator(),
            style=toolbar_style,
            **{bottom_toolbar_name: self.status_messages["toolbar"]},
        )

        return Action.from_char(action.upper())

    def strategy(self, opponent: Player, input_function=None):
        """
        Ordinarily, the strategy prompts for keyboard input rather than
        deriving its own action.

        However, it is also possible to pass a function which returns a valid
        action. This is mainly used for testing purposes in order to by-pass
        the need for human interaction.
        """

        self.status_messages = self._status_messages()
        self.status_messages = self._status_messages()
        print(self.status_messages["print"])

        if not input_function:  # pragma: no cover
            action = self._get_human_input()
        else:
            action = input_function()

        return action

    def __repr__(self):
        """
        Override the default __repr__ of the class
        """
        return "Human: {}".format(self.human_name)
