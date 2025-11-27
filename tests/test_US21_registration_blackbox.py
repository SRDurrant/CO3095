"""
White-box testing for US21 - User Registration

These tests simulate the user interactions with the system by fake input functions and
capture printed output via a fake print function.
"""

from app.auth import register_user
from app.data_store import USERS, add_user


def run_reg_with_inputs(inputs):
    """
    This function simulates a registration flow for US21

    Inputs:
        inputs (list[str]): list of user inputs: [username, password, confirm_password]

    Returns:
        tuple:
            - Success (bool): True if successful, False otherwise
            - Result (dict | str): New user dict on success, Error message on failure
            - Outputs (list[str]): List of printed messages from registration
    """

    inputs_iter = iter(inputs)

    def fake_input(prompt: str) -> str:
        try:
            return next(inputs_iter)
        except StopIteration:
            return ""

    outputs = []

    def fake_print(message: str) -> None:
        outputs.append(message)

    # Resets the user before each simulation
    USERS.clear()

    success, result = register_user(input_func=fake_input, print_func=fake_print)
    return success, result, outputs