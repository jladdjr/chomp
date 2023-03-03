import pytest

from unittest.mock import patch, call

from chomp.commands import eat


class TestCommands:
    @patch("chomp.commands.add_food_diary_entry")
    @patch("chomp.commands.get_food")
    @patch("chomp.commands.print")
    def test_eat(self, mock_print, mock_get_food, mock_add_food_diary_entry):
        # given
        food_name = "everlasting gobstopper"
        food_data = {"calories": 42, "weight": 142}

        mock_get_food.return_value = food_data

        # when
        eat(food_name)

        # then
        expected_calls = [
            call(f"You ate {food_name}"),
            call(f"You ate {food_data['calories']} calories!"),
        ]
        assert mock_print.mock_calls == expected_calls

        mock_add_food_diary_entry.assert_called_with(food_name, food_data["calories"])
