"""Fun little helpers used by every lesson notebook.

Import with:  from helpers.kid_tools import celebrate, check_answer, quiz, badge
"""
import random

import ipywidgets as widgets
from IPython.display import HTML, display

CELEBRATIONS = [
    "Awesome job!",
    "You did it!",
    "Blast off, coder!",
    "Super work!",
    "You got it!",
    "Turtle-tastic!",
]

_CARD_STYLE = "font-size:20px; padding:14px; border-radius:12px; text-align:center; margin:8px 0;"


def celebrate(message=None):
    """Show a big green success card."""
    text = message or random.choice(CELEBRATIONS)
    display(HTML(
        f'<div style="{_CARD_STYLE} background:#e8f5e9; border:3px solid #4caf50;">'
        f'🎉 {text}</div>'
    ))


def try_again(hint=None):
    """Show an orange 'not quite yet' card, with an optional hint."""
    text = "Not quite — give it another try!"
    if hint:
        text += f'<br><span style="font-size:16px;">💡 Hint: {hint}</span>'
    display(HTML(
        f'<div style="{_CARD_STYLE} background:#fff3e0; border:3px solid #ff9800;">'
        f'🤔 {text}</div>'
    ))


def check_answer(user_answer, correct_answer, hint=None, case_sensitive=False):
    """Compare a kid's typed answer to the correct one and show a result card."""
    ua, ca = user_answer, correct_answer
    if isinstance(ua, str) and isinstance(ca, str) and not case_sensitive:
        ua, ca = ua.strip().lower(), ca.strip().lower()
    is_correct = ua == ca
    celebrate() if is_correct else try_again(hint)
    return is_correct


def quiz(question, choices, correct_index, hint=None):
    """A click-to-answer multiple choice quiz (no typing needed)."""
    output = widgets.Output()
    buttons = []

    def make_handler(choice_index, button):
        def handler(_):
            with output:
                output.clear_output()
                if choice_index == correct_index:
                    celebrate()
                    button.style.button_color = "#a5d6a7"
                else:
                    try_again(hint)
                    button.style.button_color = "#ffab91"
        return handler

    for i, choice_text in enumerate(choices):
        button = widgets.Button(description=choice_text, layout=widgets.Layout(width="auto"))
        button.on_click(make_handler(i, button))
        buttons.append(button)

    display(HTML(f"<h3>❓ {question}</h3>"))
    display(widgets.HBox(buttons))
    display(output)


def badge(name, emoji="🏅"):
    """Show a badge card at the end of a lesson."""
    display(HTML(
        '<div style="display:inline-block; font-size:20px; padding:10px 20px; '
        'border-radius:20px; background:#fff9c4; border:3px solid #fbc02d; margin:8px 0;">'
        f'{emoji} <b>Badge unlocked:</b> {name}</div>'
    ))
