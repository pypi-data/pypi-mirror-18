from prompt_toolkit import prompt as pprompt
from prompt_toolkit.shortcuts import print_tokens
from prompt_toolkit.styles import style_from_dict
from pygments.token import Token

def prompt(message, options_values, default_index):

    if default_index is not False:
        default_value = options_values[default_index]
        default_print_message = " [default: " + str(default_value) + "] "
    else:
        default_value = False
        default_print_message = " "

    input_value = ""

    while input_value not in options_values:
        input_value = pprompt(
            message + str(options_values) + default_print_message)

        if default_value is not False and input_value == "":
            input_value = default_value

    return input_value


def notice_print(message):

    notice_style = style_from_dict({
        Token.Notice: '#44ff44 bold',
        Token.Message: '#000000 italic',
    })

    tokens = [
        (Token.Notice, 'Notice: '),
        (Token.Message, message),
        (Token, '\n'),
    ]
    print_tokens(tokens, style=notice_style)


def warning_print(message):

    warning_style = style_from_dict({
        Token.Warning: '#d3ac2b bold',
        Token.Message: '#000000 italic',
    })

    tokens = [
        (Token.Warning, 'Warning: '),
        (Token.Message, message),
        (Token, '\n'),
    ]
    print_tokens(tokens, style=warning_style)

def error_print(message):

    error_style = style_from_dict({
        Token.Error: '#ff0066 bold',
        Token.Message: '#000000 italic',
    })

    tokens = [
        (Token.Error, 'Error: '),
        (Token.Message, message),
        (Token, '\n'),
    ]
    print_tokens(tokens, style=error_style)
