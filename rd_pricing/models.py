from otree.api import *
import numpy as np
import itertools
import math
import random


# ============================================================
# HELPER
# ============================================================

def bounds_from_durations(durations):
    last = list(itertools.accumulate(durations))
    first = [1] + [x + 1 for x in last[:-1]]
    return last, first, last[-1]


# ============================================================
# CONSTANTS
# ============================================================

class Constants(BaseConstants):

    name_in_url = 'rd_pricing'
    players_per_group = 2

    # ========================================================
    # EXPERIMENT PARAMETERS
    # ========================================================

    delta = 0.8
    num_supergames = 2

    investment_cost = 247

    # State-dependent price grids
    price_choices_11 = [
        63, 64, 65, 66,
        68, 70, 71, 72,
    ]

    price_choices_asym = [
        81, 84, 87, 90,
        92, 94, 96, 97,
    ]

    price_choices_00 = [
        108, 108.5, 109, 109.5,
        110, 110.5, 111, 112,
    ]

    # ========================================================
    # OTHER TASK PARAMETERS
    # ========================================================

    BOMB_NUMBER_OF_BOXES = 100
    BOMB_DOLLARS_PER_SAFE_BOX = 0.05
    BOMB_COLLECTION_INTERVAL_MS = 500

    SVO_DOLLARS_PER_POINT = 0.05
    PRICING_POINTS_PER_DOLLAR = 1500
    QUIZ_DOLLARS_PER_CORRECT = 0.50
    SHOW_UP_FEE_USD = 5.00

    # ========================================================
    # SUPERGAME LENGTHS
    # ========================================================


    match_duration = [2, 2]

    last_rounds, first_rounds, last_round = bounds_from_durations(
        match_duration
    )

    num_rounds = last_round

    # ========================================================
    # PAYOFF TABLES
    # ========================================================

    # --------------------------------------------------------
    # Both invest: (1,1)
    # m_i = 0
    # R&D cost F = 247 is deducted
    # --------------------------------------------------------

    PAYOFF_11 = {
        63: {
            63: 216.91,
            64: 218.55,
            65: 220.18,
            66: 221.82,
            68: 225.09,
            70: 228.36,
            71: 230.00,
            72: 231.64,
        },
        64: {
            63: 216.79,
            64: 218.45,
            65: 220.12,
            66: 221.78,
            68: 225.10,
            70: 228.43,
            71: 230.09,
            72: 231.75,
        },
        65: {
            63: 216.44,
            64: 218.13,
            65: 219.82,
            66: 221.51,
            68: 224.88,
            70: 228.26,
            71: 229.95,
            72: 231.64,
        },
        66: {
            63: 215.86,
            64: 217.57,
            65: 219.29,
            66: 221.00,
            68: 224.43,
            70: 227.86,
            71: 229.57,
            72: 231.29,
        },
        68: {
            63: 213.99,
            64: 215.75,
            65: 217.52,
            66: 219.29,
            68: 222.82,
            70: 226.35,
            71: 228.12,
            72: 229.88,
        },
        70: {
            63: 211.18,
            64: 213.00,
            65: 214.82,
            66: 216.64,
            68: 220.27,
            70: 223.91,
            71: 225.73,
            72: 227.55,
        },
        71: {
            63: 209.43,
            64: 211.27,
            65: 213.12,
            66: 214.96,
            68: 218.65,
            70: 222.34,
            71: 224.18,
            72: 226.03,
        },
        72: {
            63: 207.44,
            64: 209.31,
            65: 211.18,
            66: 213.05,
            68: 216.79,
            70: 220.53,
            71: 222.40,
            72: 224.27,
        },
    }

    # --------------------------------------------------------
    # Neither invests: (0,0)
    # m_i = 80
    # No R&D cost
    # --------------------------------------------------------

    PAYOFF_00 = {
        108: {
            108: 91.64,
            108.5: 92.00,
            109: 92.36,
            109.5: 92.73,
            110: 93.09,
            110.5: 93.45,
            111: 93.82,
            112: 94.55,
        },
        108.5: {
            108: 91.61,
            108.5: 91.98,
            109: 92.35,
            109.5: 92.72,
            110: 93.09,
            110.5: 93.46,
            111: 93.83,
            112: 94.57,
        },
        109: {
            108: 91.52,
            108.5: 91.90,
            109: 92.27,
            109.5: 92.65,
            110: 93.03,
            110.5: 93.40,
            111: 93.78,
            112: 94.53,
        },
        109.5: {
            108: 91.37,
            108.5: 91.76,
            109: 92.14,
            109.5: 92.52,
            110: 92.91,
            110.5: 93.29,
            111: 93.67,
            112: 94.44,
        },
        110: {
            108: 91.17,
            108.5: 91.56,
            109: 91.95,
            109.5: 92.34,
            110: 92.73,
            110.5: 93.12,
            111: 93.51,
            112: 94.29,
        },
        110.5: {
            108: 90.91,
            108.5: 91.30,
            109: 91.70,
            109.5: 92.09,
            110: 92.49,
            110.5: 92.89,
            111: 93.28,
            112: 94.07,
        },
        111: {
            108: 90.58,
            108.5: 90.99,
            109: 91.39,
            109.5: 91.79,
            110: 92.19,
            110.5: 92.60,
            111: 93.00,
            112: 93.81,
        },
        112: {
            108: 89.77,
            108.5: 90.18,
            109: 90.60,
            109.5: 91.01,
            110: 91.43,
            110.5: 91.84,
            111: 92.26,
            112: 93.09,
        },
    }

    # --------------------------------------------------------
    # You invest, counterpart does not: (1,0)
    # m_i = 30
    # R&D cost F = 247 is deducted
    # --------------------------------------------------------

    PAYOFF_10 = {
        81: {
            81: 45.09,
            84: 49.06,
            87: 53.04,
            90: 57.01,
            92: 59.66,
            94: 62.31,
            96: 64.96,
            97: 66.29,
        },
        84: {
            81: 43.34,
            84: 47.55,
            87: 51.75,
            90: 55.96,
            92: 58.77,
            94: 61.57,
            96: 64.38,
            97: 65.78,
        },
        87: {
            81: 39.48,
            84: 43.92,
            87: 48.36,
            90: 52.81,
            92: 55.77,
            94: 58.73,
            96: 61.69,
            97: 63.17,
        },
        90: {
            81: 33.52,
            84: 38.19,
            87: 42.87,
            90: 47.55,
            92: 50.66,
            94: 53.78,
            96: 56.90,
            97: 58.45,
        },
        92: {
            81: 28.38,
            84: 33.21,
            87: 38.04,
            90: 42.87,
            92: 46.09,
            94: 49.31,
            96: 52.53,
            97: 54.14,
        },
        94: {
            81: 22.30,
            84: 27.29,
            87: 32.27,
            90: 37.26,
            92: 40.58,
            94: 43.91,
            96: 47.23,
            97: 48.90,
        },
        96: {
            81: 15.29,
            84: 20.43,
            87: 25.57,
            90: 30.71,
            92: 34.14,
            94: 37.57,
            96: 41.00,
            97: 42.71,
        },
        97: {
            81: 11.43,
            84: 16.65,
            87: 21.87,
            90: 27.09,
            92: 30.57,
            94: 34.05,
            96: 37.53,
            97: 39.27,
        },
    }

    # --------------------------------------------------------
    # You do not invest, counterpart invests: (0,1)
    # m_i = 50
    # No R&D cost
    # --------------------------------------------------------

    PAYOFF_01 = {
        81: {
            81: 177.55,
            84: 179.96,
            87: 182.38,
            90: 184.79,
            92: 186.40,
            94: 188.01,
            96: 189.62,
            97: 190.43,
        },
        84: {
            81: 182.81,
            84: 185.45,
            87: 188.10,
            90: 190.75,
            92: 192.52,
            94: 194.29,
            96: 196.05,
            97: 196.94,
        },
        87: {
            81: 185.96,
            84: 188.84,
            87: 191.73,
            90: 194.61,
            92: 196.53,
            94: 198.45,
            96: 200.38,
            97: 201.34,
        },
        90: {
            81: 187.01,
            84: 190.13,
            87: 193.25,
            90: 196.36,
            92: 198.44,
            94: 200.52,
            96: 202.60,
            97: 203.64,
        },
        92: {
            81: 186.55,
            84: 189.82,
            87: 193.09,
            90: 196.36,
            92: 198.55,
            94: 200.73,
            96: 202.91,
            97: 204.00,
        },
        94: {
            81: 185.14,
            84: 188.57,
            87: 192.00,
            90: 195.43,
            92: 197.71,
            94: 200.00,
            96: 202.29,
            97: 203.43,
        },
        96: {
            81: 182.81,
            84: 186.39,
            87: 189.97,
            90: 193.56,
            92: 195.95,
            94: 198.34,
            96: 200.73,
            97: 201.92,
        },
        97: {
            81: 181.29,
            84: 184.95,
            87: 188.61,
            90: 192.27,
            92: 194.71,
            94: 197.16,
            96: 199.60,
            97: 200.82,
        },
    }

    # ========================================================
    # PAYOFF TABLE LOOKUP
    # ========================================================

    PAYOFF_TABLES = {
        (1, 1): PAYOFF_11,
        (0, 0): PAYOFF_00,
        (1, 0): PAYOFF_10,
        (0, 1): PAYOFF_01,
    }

    # ========================================================
    # SVO TASKS
    # ========================================================

    SVO_TASKS = [
        dict(
            you=[85, 85, 85, 85, 85, 85, 85, 85, 85],
            other=[85, 76, 68, 59, 50, 41, 33, 24, 15],
        ),
        dict(
            you=[85, 87, 89, 91, 93, 94, 96, 98, 100],
            other=[15, 19, 24, 28, 33, 37, 41, 46, 50],
        ),
        dict(
            you=[50, 54, 59, 63, 68, 72, 76, 81, 85],
            other=[100, 98, 96, 94, 93, 91, 89, 87, 85],
        ),
        dict(
            you=[50, 54, 59, 63, 68, 72, 76, 81, 85],
            other=[100, 89, 79, 68, 58, 47, 36, 26, 15],
        ),
        dict(
            you=[100, 94, 88, 81, 75, 69, 63, 56, 50],
            other=[50, 56, 63, 69, 75, 81, 88, 94, 100],
        ),
        dict(
            you=[100, 98, 96, 94, 93, 91, 89, 87, 85],
            other=[50, 54, 59, 63, 68, 72, 76, 81, 85],
        ),
    ]


# ============================================================
# SUBSESSION
# ============================================================

class Subsession(BaseSubsession):

    supergame_number = models.IntegerField()
    round_in_supergame = models.IntegerField()

    def creating_session(self):

        for k, last_round in enumerate(
            Constants.last_rounds
        ):
            if self.round_number <= int(last_round):
                self.supergame_number = int(k + 1)
                break

        first = Constants.first_rounds[
            self.supergame_number - 1
        ]

        self.round_in_supergame = int(
            self.round_number
            - int(first)
            + 1
        )

        if self.round_number in Constants.first_rounds:
            self.group_randomly()

        else:
            self.group_like_round(
                self.round_number - 1
            )


# ============================================================
# GROUP
# ============================================================

class Group(BaseGroup):

    def determine_svo_payment(self):

        players = self.get_players()

        if len(players) != 2:
            raise ValueError(
                "The SVO payment procedure requires exactly 2 players."
            )

        selected_question = random.randint(
            1,
            len(Constants.SVO_TASKS)
        )

        sender = random.choice(players)

        receiver = next(
            player
            for player in players
            if player.id_in_group != sender.id_in_group
        )

        response_field = (
            f'svo_q{selected_question}'
        )

        selected_option = getattr(
            sender,
            response_field
        )

        option_index = selected_option - 1

        task = Constants.SVO_TASKS[
            selected_question - 1
        ]

        sender_points = task['you'][
            option_index
        ]

        receiver_points = task['other'][
            option_index
        ]

        sender_payment = (
            sender_points
            * Constants.SVO_DOLLARS_PER_POINT
        )

        receiver_payment = (
            receiver_points
            * Constants.SVO_DOLLARS_PER_POINT
        )

        for player in players:

            player.svo_selected_question = (
                selected_question
            )

            player.svo_selected_option = (
                selected_option
            )

            player.svo_sender_id = (
                sender.id_in_group
            )

            player.svo_receiver_id = (
                receiver.id_in_group
            )

            player.svo_sender_points = (
                sender_points
            )

            player.svo_receiver_points = (
                receiver_points
            )

        sender.svo_role = 'Sender'
        sender.svo_points = sender_points
        sender.svo_payment_usd = sender_payment

        receiver.svo_role = 'Receiver'
        receiver.svo_points = receiver_points
        receiver.svo_payment_usd = receiver_payment

        sender.participant.vars.update(
            dict(
                svo_selected_question=selected_question,
                svo_selected_option=selected_option,
                svo_role='Sender',
                svo_points=sender_points,
                svo_payment_usd=sender_payment,
                svo_sender_points=sender_points,
                svo_receiver_points=receiver_points,
            )
        )

        receiver.participant.vars.update(
            dict(
                svo_selected_question=selected_question,
                svo_selected_option=selected_option,
                svo_role='Receiver',
                svo_points=receiver_points,
                svo_payment_usd=receiver_payment,
                svo_sender_points=sender_points,
                svo_receiver_points=receiver_points,
            )
        )


# ============================================================
# PLAYER
# ============================================================

class Player(BasePlayer):

    # ========================================================
    # INVESTMENT AND PRICING
    # ========================================================

    invest = models.BooleanField(
        label="Do you want to invest?",
        choices=[
            (
                True,
                "Yes, I want to invest.",
            ),
            (
                False,
                "No, I do not want to invest.",
            ),
        ],
        widget=widgets.RadioSelect,
    )

    price = models.FloatField(
        label="Please choose your price:",
        widget=widgets.RadioSelect,
    )

    profit = models.FloatField()

    # ========================================================
    # INVESTMENT STATE
    # ========================================================

    def get_persistent_investment_decision(self):

        first_round = Constants.first_rounds[
            self.subsession.supergame_number - 1
        ]

        first_round_player = self.in_round(
            first_round
        )

        return bool(
            first_round_player.invest
        )

    # ========================================================
    # OTHER PLAYER
    # ========================================================

    def other(self):
        return self.get_others_in_group()[0]

    # ========================================================
    # DYNAMIC PRICE CHOICES
    # ========================================================

    def price_choices(self):

        my_invest = int(
            self.get_persistent_investment_decision()
        )

        other_invest = int(
            self.other()
            .get_persistent_investment_decision()
        )

        if (my_invest, other_invest) == (1, 1):
            return Constants.price_choices_11

        elif (my_invest, other_invest) == (0, 0):
            return Constants.price_choices_00

        else:
            return Constants.price_choices_asym

    # ========================================================
    # PRICING PAYOFF
    # ========================================================

    def set_payoff(self):

        other = self.other()

        my_invest = int(
            self.get_persistent_investment_decision()
        )

        other_invest = int(
            other.get_persistent_investment_decision()
        )

        payoff = Constants.PAYOFF_TABLES[
            (my_invest, other_invest)
        ][self.price][other.price]

        self.profit = payoff
        self.payoff = payoff

    # ========================================================
    # COMPREHENSION QUIZ
    # ========================================================

    quiz_q1 = models.IntegerField(
        label=(
            "After each pricing round, what is the probability "
            "that the current match continues for another "
            "pricing round?"
        ),
        choices=[
            (1, "20%"),
            (2, "50%"),
            (3, "80%"),
            (4, "100%"),
        ],
        widget=widgets.RadioSelect,
    )

    quiz_q2 = models.IntegerField(
        label=(
            "When do you learn your counterpart's "
            "investment decision?"
        ),
        choices=[
            (
                1,
                "Before I make my own investment decision.",
            ),
            (
                2,
                "After both producers have made their "
                "investment decisions.",
            ),
            (
                3,
                "After the first pricing round.",
            ),
            (
                4,
                "I never learn my counterpart's "
                "investment decision.",
            ),
        ],
        widget=widgets.RadioSelect,
    )

    quiz_q3 = models.IntegerField(
        label=(
            "Suppose both producers invest. "
            "You choose Price Choice 6 and your counterpart "
            "chooses Price Choice 8. "
            "How many points do you earn?"
        ),
        choices=[
            (1, "216.91 points"),
            (2, "224.27 points"),
            (3, "227.55 points"),
            (4, "231.75 points"),
        ],
        widget=widgets.RadioSelect,
    )

    quiz_q4 = models.IntegerField(
        label=(
            "Suppose the match continues after a pricing round. "
            "What happens to the investment decisions?"
        ),
        choices=[
            (
                1,
                "You and your counterpart make new "
                "investment decisions.",
            ),
            (
                2,
                "The investment decisions made at the beginning "
                "of the match remain unchanged.",
            ),
            (
                3,
                "Only the producer with the higher price "
                "makes a new investment decision.",
            ),
            (
                4,
                "The computer randomly chooses new "
                "investment decisions.",
            ),
        ],
        widget=widgets.RadioSelect,
    )

    quiz_q1_correct = models.BooleanField(
        initial=False
    )

    quiz_q2_correct = models.BooleanField(
        initial=False
    )

    quiz_q3_correct = models.BooleanField(
        initial=False
    )

    quiz_q4_correct = models.BooleanField(
        initial=False
    )

    quiz_score = models.IntegerField(
        initial=0
    )

    quiz_bonus_usd = models.FloatField(
        initial=0
    )

    # ========================================================
    # SVO FIELDS
    # ========================================================

    svo_q1 = models.IntegerField(
        choices=[
            (i, f"Option {i}")
            for i in range(1, 10)
        ]
    )

    svo_q2 = models.IntegerField(
        choices=[
            (i, f"Option {i}")
            for i in range(1, 10)
        ]
    )

    svo_q3 = models.IntegerField(
        choices=[
            (i, f"Option {i}")
            for i in range(1, 10)
        ]
    )

    svo_q4 = models.IntegerField(
        choices=[
            (i, f"Option {i}")
            for i in range(1, 10)
        ]
    )

    svo_q5 = models.IntegerField(
        choices=[
            (i, f"Option {i}")
            for i in range(1, 10)
        ]
    )

    svo_q6 = models.IntegerField(
        choices=[
            (i, f"Option {i}")
            for i in range(1, 10)
        ]
    )

    svo_mean_self = models.FloatField(
        blank=True
    )

    svo_mean_other = models.FloatField(
        blank=True
    )

    svo_angle = models.FloatField(
        blank=True
    )

    svo_category = models.StringField(
        blank=True
    )

    svo_self_1 = models.IntegerField(blank=True)
    svo_self_2 = models.IntegerField(blank=True)
    svo_self_3 = models.IntegerField(blank=True)
    svo_self_4 = models.IntegerField(blank=True)
    svo_self_5 = models.IntegerField(blank=True)
    svo_self_6 = models.IntegerField(blank=True)

    svo_other_1 = models.IntegerField(blank=True)
    svo_other_2 = models.IntegerField(blank=True)
    svo_other_3 = models.IntegerField(blank=True)
    svo_other_4 = models.IntegerField(blank=True)
    svo_other_5 = models.IntegerField(blank=True)
    svo_other_6 = models.IntegerField(blank=True)

    # ========================================================
    # SVO PAYMENT
    # ========================================================

    svo_selected_question = models.IntegerField(
        blank=True
    )

    svo_selected_option = models.IntegerField(
        blank=True
    )

    svo_role = models.StringField(
        blank=True
    )

    svo_sender_id = models.IntegerField(
        blank=True
    )

    svo_receiver_id = models.IntegerField(
        blank=True
    )

    svo_points = models.IntegerField(
        blank=True
    )

    svo_payment_usd = models.FloatField(
        blank=True
    )

    svo_sender_points = models.IntegerField(
        blank=True
    )

    svo_receiver_points = models.IntegerField(
        blank=True
    )

    # ========================================================
    # BOMB RISK TASK
    # ========================================================

    bomb_location = models.IntegerField(
        blank=True
    )

    bomb_boxes_collected = models.IntegerField(
        blank=True
    )

    bomb_exploded = models.BooleanField(
        blank=True
    )

    bomb_safe_boxes = models.IntegerField(
        blank=True
    )

    bomb_payment_usd = models.FloatField(
        blank=True
    )

    # ========================================================
    # DEMOGRAPHICS
    # ========================================================

    age_group = models.StringField(
        label="What is your age?",
        choices=[
            ("18-24", "18-24"),
            ("25-29", "25-29"),
            ("30-34", "30-34"),
            ("35-39", "35-39"),
            ("40-44", "40-44"),
            ("45-49", "45-49"),
            ("50-54", "50-54"),
            ("55-59", "55-59"),
            ("60-64", "60-64"),
            (
                "65 or older",
                "65 or older",
            ),
            (
                "Prefer not to answer",
                "Prefer not to answer",
            ),
        ],
        widget=widgets.RadioSelect,
    )

    gender = models.StringField(
        label="What is your gender?",
        choices=[
            (
                "Woman",
                "Woman",
            ),
            (
                "Man",
                "Man",
            ),
            (
                "Non-binary",
                "Non-binary",
            ),
            (
                "Self-describe",
                "Prefer to self-describe",
            ),
            (
                "Prefer not to answer",
                "Prefer not to answer",
            ),
        ],
        widget=widgets.RadioSelect,
    )

    gender_self_description = models.StringField(
        label="Please describe your gender:",
        blank=True,
    )

    education = models.StringField(
        label=(
            "What is the highest level of education "
            "you have completed?"
        ),
        choices=[
            (
                "Less than high school",
                "Less than high school",
            ),
            (
                "High school",
                "High school diploma or equivalent",
            ),
            (
                "Some college",
                "Some college, but no degree",
            ),
            (
                "Associate degree",
                "Associate degree",
            ),
            (
                "Bachelor degree",
                "Bachelor's degree",
            ),
            (
                "Graduate degree",
                "Graduate or professional degree",
            ),
            (
                "Prefer not to answer",
                "Prefer not to answer",
            ),
        ],
        widget=widgets.RadioSelect,
    )

    student_status = models.StringField(
        label="Are you currently a student?",
        choices=[
            (
                "Undergraduate",
                "Yes, undergraduate student",
            ),
            (
                "Graduate",
                "Yes, graduate or professional student",
            ),
            (
                "Not a student",
                "No",
            ),
            (
                "Prefer not to answer",
                "Prefer not to answer",
            ),
        ],
        widget=widgets.RadioSelect,
    )

    field_of_study = models.StringField(
        label="What is your primary field of study?",
        blank=True,
    )

    race_ethnicity = models.StringField(
        label=(
            "Which racial or ethnic group best describes you?"
        ),
        choices=[
            (
                "American Indian or Alaska Native",
                "American Indian or Alaska Native",
            ),
            (
                "Asian",
                "Asian",
            ),
            (
                "Black or African American",
                "Black or African American",
            ),
            (
                "Hispanic or Latino",
                "Hispanic or Latino",
            ),
            (
                "Middle Eastern or North African",
                "Middle Eastern or North African",
            ),
            (
                "Native Hawaiian or Pacific Islander",
                "Native Hawaiian or Other Pacific Islander",
            ),
            (
                "White",
                "White",
            ),
            (
                "Another identity",
                "Another identity",
            ),
            (
                "Prefer not to answer",
                "Prefer not to answer",
            ),
        ],
        widget=widgets.RadioSelect,
    )

    race_ethnicity_other = models.StringField(
        label=(
            "Please describe your racial or ethnic identity:"
        ),
        blank=True,
    )

    economics_courses = models.StringField(
        label=(
            "How many economics courses have you completed, "
            "including courses you are currently taking?"
        ),
        choices=[
            ("0", "0"),
            ("1", "1"),
            ("2", "2"),
            (
                "3 or more",
                "3 or more",
            ),
        ],
        widget=widgets.RadioSelect,
    )

    previous_experiment = models.BooleanField(
        label=(
            "Before today, have you participated in an economics "
            "or decision-making experiment?"
        ),
        choices=[
            (
                True,
                "Yes",
            ),
            (
                False,
                "No",
            ),
        ],
        widget=widgets.RadioSelect,
    )

    # ========================================================
    # FINAL PAYMENT
    # ========================================================

    pricing_total_points = models.FloatField(
        blank=True
    )

    pricing_payment_usd = models.FloatField(
        blank=True
    )

    final_quiz_payment_usd = models.FloatField(
        blank=True
    )

    final_svo_payment_usd = models.FloatField(
        blank=True
    )

    final_bomb_payment_usd = models.FloatField(
        blank=True
    )

    final_show_up_fee_usd = models.FloatField(
        blank=True
    )

    final_payment_usd = models.FloatField(
        blank=True
    )

    # ========================================================
    # SVO CALCULATION
    # ========================================================

    def calculate_svo(self):

        responses = [
            self.svo_q1,
            self.svo_q2,
            self.svo_q3,
            self.svo_q4,
            self.svo_q5,
            self.svo_q6,
        ]

        self_allocations = []
        other_allocations = []

        for item_index, selected_option in enumerate(
            responses
        ):

            option_index = (
                selected_option - 1
            )

            task = Constants.SVO_TASKS[
                item_index
            ]

            self_points = task["you"][
                option_index
            ]

            other_points = task["other"][
                option_index
            ]

            self_allocations.append(
                self_points
            )

            other_allocations.append(
                other_points
            )

            setattr(
                self,
                f"svo_self_{item_index + 1}",
                self_points,
            )

            setattr(
                self,
                f"svo_other_{item_index + 1}",
                other_points,
            )

        self.svo_mean_self = (
            sum(self_allocations)
            / len(self_allocations)
        )

        self.svo_mean_other = (
            sum(other_allocations)
            / len(other_allocations)
        )

        shifted_self = (
            self.svo_mean_self - 50
        )

        shifted_other = (
            self.svo_mean_other - 50
        )

        self.svo_angle = math.degrees(
            math.atan2(
                shifted_other,
                shifted_self,
            )
        )

        if self.svo_angle >= 57.15:
            self.svo_category = "Altruistic"

        elif self.svo_angle >= 22.45:
            self.svo_category = "Prosocial"

        elif self.svo_angle >= -12.04:
            self.svo_category = "Individualistic"

        else:
            self.svo_category = "Competitive"

    # ========================================================
    # BOMB RISK
    # ========================================================

    def initialize_bomb_task(self):

        if self.field_maybe_none(
            "bomb_location"
        ) is None:

            self.bomb_location = random.randint(
                1,
                Constants.BOMB_NUMBER_OF_BOXES,
            )

    def calculate_bomb_payment(self):

        boxes_collected = (
            self.field_maybe_none(
                "bomb_boxes_collected"
            )
        )

        if boxes_collected is None:
            boxes_collected = 0

        boxes_collected = max(
            0,
            min(
                boxes_collected,
                Constants.BOMB_NUMBER_OF_BOXES,
            ),
        )

        self.bomb_boxes_collected = (
            boxes_collected
        )

        self.bomb_exploded = (
            self.bomb_location
            <= boxes_collected
        )

        if self.bomb_exploded:

            self.bomb_safe_boxes = 0
            self.bomb_payment_usd = 0.0

        else:

            self.bomb_safe_boxes = (
                boxes_collected
            )

            self.bomb_payment_usd = (
                boxes_collected
                * Constants.BOMB_DOLLARS_PER_SAFE_BOX
            )

        self.participant.vars.update(
            dict(
                bomb_location=(
                    self.bomb_location
                ),
                bomb_boxes_collected=(
                    self.bomb_boxes_collected
                ),
                bomb_exploded=(
                    self.bomb_exploded
                ),
                bomb_safe_boxes=(
                    self.bomb_safe_boxes
                ),
                bomb_payment_usd=(
                    self.bomb_payment_usd
                ),
            )
        )

    # ========================================================
    # FINAL PAYMENT
    # ========================================================

    def calculate_final_payment(self):

        pricing_points = sum(
            round_player.profit
            for round_player in self.in_all_rounds()
            if round_player.field_maybe_none(
                "profit"
            ) is not None
        )

        pricing_payment_usd = (
            pricing_points
            / Constants.PRICING_POINTS_PER_DOLLAR
        )

        quiz_payment_usd = (
            self.participant.vars.get(
                "quiz_bonus_usd",
                0.0,
            )
        )

        svo_payment_usd = (
            self.participant.vars.get(
                "svo_payment_usd",
                0.0,
            )
        )

        bomb_payment_usd = (
            self.participant.vars.get(
                "bomb_payment_usd",
                0.0,
            )
        )

        show_up_fee_usd = (
            Constants.SHOW_UP_FEE_USD
        )

        total_payment_usd = (
            pricing_payment_usd
            + quiz_payment_usd
            + svo_payment_usd
            + bomb_payment_usd
            + show_up_fee_usd
        )

        self.pricing_total_points = (
            pricing_points
        )

        self.pricing_payment_usd = (
            pricing_payment_usd
        )

        self.final_quiz_payment_usd = (
            quiz_payment_usd
        )

        self.final_svo_payment_usd = (
            svo_payment_usd
        )

        self.final_bomb_payment_usd = (
            bomb_payment_usd
        )

        self.final_show_up_fee_usd = (
            show_up_fee_usd
        )

        self.final_payment_usd = (
            total_payment_usd
        )

        self.participant.vars.update(
            dict(
                pricing_total_points=(
                    pricing_points
                ),
                pricing_payment_usd=(
                    pricing_payment_usd
                ),
                quiz_payment_usd=(
                    quiz_payment_usd
                ),
                svo_payment_usd=(
                    svo_payment_usd
                ),
                bomb_payment_usd=(
                    bomb_payment_usd
                ),
                show_up_fee_usd=(
                    show_up_fee_usd
                ),
                final_payment_usd=(
                    total_payment_usd
                ),
            )
        )
