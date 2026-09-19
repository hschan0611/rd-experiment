from otree.api import Page, WaitPage
from .models import Constants


# ============================================================
# QUIZ ANSWERS
# ============================================================

QUIZ_ANSWERS = {
    'quiz_q1': 3,   # 80%
    'quiz_q2': 2,   # Learn counterpart's investment after both decide
    'quiz_q3': 3,   # 120.00 points
    'quiz_q4': 2,   # Investment decisions remain unchanged
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def matrix_to_rows(matrix, prices):

    rows = []

    for display_choice, actual_price in enumerate(
        prices,
        start=1,
    ):

        row = [
            matrix[actual_price][other_price]
            for other_price in prices
        ]

        rows.append(
            (
                display_choice,
                row,
            )
        )

    return rows

def matrix_for_profile(my_invest, other_invest):
    return Constants.PAYOFF_TABLES[
        (my_invest, other_invest)
    ]


def prices_for_profile(my_invest, other_invest):

    if (my_invest, other_invest) == (1, 1):
        return Constants.price_choices_11

    if (my_invest, other_invest) == (0, 0):
        return Constants.price_choices_00

    return Constants.price_choices_asym


def all_payoff_tables_for_template():

    p11_prices = Constants.price_choices_11
    p00_prices = Constants.price_choices_00
    pasym_prices = Constants.price_choices_asym

    return dict(

        p11_prices=p11_prices,
        p00_prices=p00_prices,
        pasym_prices=pasym_prices,

        p11_rows=matrix_to_rows(
            Constants.PAYOFF_11,
            p11_prices,
        ),

        p00_rows=matrix_to_rows(
            Constants.PAYOFF_00,
            p00_prices,
        ),

        p10_rows=matrix_to_rows(
            Constants.PAYOFF_10,
            pasym_prices,
        ),

        p01_rows=matrix_to_rows(
            Constants.PAYOFF_01,
            pasym_prices,
        ),
    )


def update_quiz_totals(player):

    score = sum(
        player.field_maybe_none(field_name)
        == correct_answer
        for field_name, correct_answer
        in QUIZ_ANSWERS.items()
    )

    bonus_usd = (
        score
        * Constants.QUIZ_DOLLARS_PER_CORRECT
    )

    player.quiz_score = score
    player.quiz_bonus_usd = bonus_usd

    player.participant.vars[
        'quiz_score'
    ] = score

    player.participant.vars[
        'quiz_bonus_usd'
    ] = bonus_usd


# ============================================================
# INSTRUCTIONS
# ============================================================

class Instructions1(Page):

    def is_displayed(self):
        return self.round_number == 1


class Instructions2(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return all_payoff_tables_for_template()


class Instructions3(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):

        p11_prices = Constants.price_choices_11
        p00_prices = Constants.price_choices_00
        pasym_prices = Constants.price_choices_asym

        return dict(

            p11_rows=matrix_to_rows(
                Constants.PAYOFF_11,
                p11_prices,
            ),

            p00_rows=matrix_to_rows(
                Constants.PAYOFF_00,
                p00_prices,
            ),

            p10_rows=matrix_to_rows(
                Constants.PAYOFF_10,
                pasym_prices,
            ),

            p01_rows=matrix_to_rows(
                Constants.PAYOFF_01,
                pasym_prices,
            ),
        )



class Intro(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):
        return all_payoff_tables_for_template()


# ============================================================
# QUIZ 1
# ============================================================

class Quiz1(Page):

    form_model = 'player'
    form_fields = ['quiz_q1']

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):

        self.player.quiz_q1_correct = (
            self.player.quiz_q1
            == QUIZ_ANSWERS['quiz_q1']
        )

        update_quiz_totals(
            self.player
        )


class Quiz1Answer(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):

        return dict(

            question=(
                "After each pricing round, what is the probability that "
                "the current match continues for another pricing round?"
            ),

            selected_answer=(
                self.player.get_quiz_q1_display()
            ),

            is_correct=(
                self.player.quiz_q1_correct
            ),

            correct_answer="80%",

            explanation=(
                "After each pricing round, the match continues with a "
                "80% probability and ends with a 20% probability."
            ),

            quiz_score=(
                self.player.quiz_score
            ),

            quiz_bonus=(
                self.player.quiz_bonus_usd
            ),
        )


# ============================================================
# QUIZ 2
# ============================================================
class Quiz2(Page):

    form_model = 'player'
    form_fields = ['quiz_q2']

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):

        self.player.quiz_q2_correct = (
            self.player.quiz_q2
            == QUIZ_ANSWERS['quiz_q2']
        )

        update_quiz_totals(
            self.player
        )


class Quiz2Answer(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):

        option1 = (
            "Before I make my own investment decision."
        )

        option2 = (
            "After both producers have made their "
            "investment decisions."
        )

        option3 = (
            "After the first pricing round."
        )

        option4 = (
            "I never learn my counterpart's "
            "investment decision."
        )

        return dict(

            question=(
                "When do you learn your counterpart's "
                "investment decision?"
            ),

            selected_answer=(
                self.player.get_quiz_q2_display()
            ),

            is_correct=(
                self.player.quiz_q2_correct
            ),

            correct_answer=option2,

            explanation=(
                "You and your counterpart make your investment "
                "decisions simultaneously. After both investment "
                "decisions have been made, you learn your "
                "counterpart's investment decision."
            ),

            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,

            quiz_score=(
                self.player.quiz_score
            ),

            quiz_bonus=(
                self.player.quiz_bonus_usd
            ),
        )


# ============================================================
# QUIZ 3
# ============================================================

class Quiz3(Page):

    form_model = 'player'
    form_fields = ['quiz_q3']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):

        prices = Constants.price_choices_11

        return dict(

            # matrix_to_rows converts the underlying
            # economic prices into displayed choices 1-8.
            p11_rows=matrix_to_rows(
                Constants.PAYOFF_11,
                prices,
            ),
        )

    def before_next_page(self):

        self.player.quiz_q3_correct = (
            self.player.quiz_q3
            == QUIZ_ANSWERS['quiz_q3']
        )

        update_quiz_totals(
            self.player
        )


class Quiz3Answer(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):

        prices = Constants.price_choices_11

        option1 = "216.91 points"
        option2 = "224.27 points"
        option3 = "227.55 points"
        option4 = "231.75 points"

        return dict(

            question=(
                "Suppose both producers invest. "
                "You choose Price Choice 6 and your counterpart "
                "chooses Price Choice 8. "
                "How many points do you earn?"
            ),

            selected_answer=(
                self.player.get_quiz_q3_display()
            ),

            is_correct=(
                self.player.quiz_q3_correct
            ),

            correct_answer=option3,

            explanation=(
                "Your Price 6 selects row 6, and your "
                "counterpart's Price 8 selects column 8. "
                "The entry at the intersection of row 6 and "
                "column 8 is 227.55 points."
            ),

            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,

            p11_rows=matrix_to_rows(
                Constants.PAYOFF_11,
                prices,
            ),

            quiz_score=(
                self.player.quiz_score
            ),

            quiz_bonus=(
                self.player.quiz_bonus_usd
            ),
        )


# ============================================================
# QUIZ 4
# ============================================================

class Quiz4(Page):

    form_model = 'player'
    form_fields = ['quiz_q4']

    def is_displayed(self):
        return self.round_number == 1

    def before_next_page(self):

        self.player.quiz_q4_correct = (
            self.player.quiz_q4
            == QUIZ_ANSWERS['quiz_q4']
        )

        update_quiz_totals(
            self.player
        )


class Quiz4Answer(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):

        option1 = (
            "You and your counterpart make new "
            "investment decisions."
        )

        option2 = (
            "The investment decisions made at the beginning "
            "of the match remain unchanged."
        )

        option3 = (
            "Only the producer with the higher price "
            "makes a new investment decision."
        )

        option4 = (
            "The computer randomly chooses new "
            "investment decisions."
        )

        return dict(

            question=(
                "Suppose the match continues after a pricing round. "
                "What happens to the investment decisions?"
            ),

            selected_answer=(
                self.player.get_quiz_q4_display()
            ),

            is_correct=(
                self.player.quiz_q4_correct
            ),

            correct_answer=option2,

            explanation=(
                "When the match continues, the investment decisions "
                "made at the beginning of the match continue to apply, "
                "and the same earnings table remains in effect. "
                "New investment decisions are made only when "
                "a new match begins."
            ),

            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,

            quiz_score=(
                self.player.quiz_score
            ),

            quiz_bonus=(
                self.player.quiz_bonus_usd
            ),
        )

class QuizEnd(Page):

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self):

        return dict(

            quiz_score=(
                self.player.quiz_score
            ),

            quiz_bonus=(
                self.player.quiz_bonus_usd
            ),
        )


# ============================================================
# INVESTMENT STAGE
# ============================================================

class Investment(Page):

    form_model = 'player'
    form_fields = ['invest']

    def is_displayed(self):

        return (
            self.round_number
            in Constants.first_rounds
        )

    def vars_for_template(self):

        return all_payoff_tables_for_template()


class InvestmentWait(WaitPage):

    def is_displayed(self):

        return (
            self.round_number
            in Constants.first_rounds
        )


# ============================================================
# INVESTMENT RESULT
# ============================================================

class InvestmentResult(Page):

    def is_displayed(self):

        return (
            self.round_number
            in Constants.first_rounds
        )

    def vars_for_template(self):

        player = self.player
        other = player.other()

        my_invest = int(
            player.get_persistent_investment_decision()
        )

        other_invest = int(
            other.get_persistent_investment_decision()
        )

        matrix = matrix_for_profile(
            my_invest,
            other_invest,
        )

        prices = prices_for_profile(
            my_invest,
            other_invest,
        )

        return dict(

            my_decision=bool(
                my_invest
            ),

            other_decision=bool(
                other_invest
            ),

            my_invest=my_invest,

            other_invest=other_invest,

            prices=prices,

            matrix_rows=matrix_to_rows(
                matrix,
                prices,
            ),
        )


# ============================================================
# PRICING
# ============================================================

class Pricing(Page):

    form_model = 'player'
    form_fields = ['price']

    def get_form(self, *args, **kwargs):

        form = super().get_form(
            *args,
            **kwargs
        )

        player = self.player
        other = player.other()

        my_invest = int(
            player.get_persistent_investment_decision()
        )

        other_invest = int(
            other.get_persistent_investment_decision()
        )

        prices = prices_for_profile(
            my_invest,
            other_invest,
        )

        # Store the actual economic price internally,
        # but display choices 1 through 8 to subjects.
        form.price.choices = [
            (
                actual_price,
                str(display_choice),
            )
            for display_choice, actual_price
            in enumerate(
                prices,
                start=1,
            )
        ]

        return form

    def vars_for_template(self):

        player = self.player
        other = player.other()

        my_invest = int(
            player.get_persistent_investment_decision()
        )

        other_invest = int(
            other.get_persistent_investment_decision()
        )

        matrix = matrix_for_profile(
            my_invest,
            other_invest,
        )

        prices = prices_for_profile(
            my_invest,
            other_invest,
        )

        return dict(

            # matrix_to_rows should display row labels 1-8
            matrix_rows=matrix_to_rows(
                matrix,
                prices,
            ),

            # Actual prices are retained internally if needed.
            prices=prices,

            # Subjects see these as column labels.
            display_choices=list(
                range(1, 9)
            ),

            my_invest=my_invest,

            other_invest=other_invest,
        )


# ============================================================
# PRICING RESULTS
# ============================================================

class ResultsWait(WaitPage):

    def after_all_players_arrive(self):

        for player in self.group.get_players():
            player.set_payoff()


class Results(Page):

    def vars_for_template(self):

        player = self.player
        other = player.other()

        my_invest = int(
            player.get_persistent_investment_decision()
        )

        other_invest = int(
            other.get_persistent_investment_decision()
        )

        matrix = matrix_for_profile(
            my_invest,
            other_invest,
        )

        prices = prices_for_profile(
            my_invest,
            other_invest,
        )

        # ----------------------------------------------------
        # Convert actual prices into displayed choices 1-8
        # ----------------------------------------------------

        my_price_index = prices.index(
            player.price
        )

        other_price_index = prices.index(
            other.price
        )

        my_display_price = (
            my_price_index + 1
        )

        other_display_price = (
            other_price_index + 1
        )

        # ----------------------------------------------------
        # History
        # ----------------------------------------------------

        first_round = Constants.first_rounds[
            self.subsession.supergame_number - 1
        ]

        history_rows = []

        for round_number in range(
            self.round_number,
            first_round - 1,
            -1,
        ):

            me_in_round = player.in_round(
                round_number
            )

            other_in_round = (
                me_in_round.other()
            )

            round_my_invest = int(
                me_in_round
                .get_persistent_investment_decision()
            )

            round_other_invest = int(
                other_in_round
                .get_persistent_investment_decision()
            )

            round_prices = prices_for_profile(
                round_my_invest,
                round_other_invest,
            )

            # Convert stored actual prices to
            # displayed choices 1-8.
            round_my_display_price = (
                round_prices.index(
                    me_in_round.price
                )
                + 1
            )

            round_other_display_price = (
                round_prices.index(
                    other_in_round.price
                )
                + 1
            )

            history_rows.append(
                dict(

                    round_in_supergame=(
                        round_number
                        - first_round
                        + 1
                    ),

                    my_invest=(
                        round_my_invest
                    ),

                    other_invest=(
                        round_other_invest
                    ),

                    # Subjects see 1-8
                    my_price=(
                        round_my_display_price
                    ),

                    other_price=(
                        round_other_display_price
                    ),

                    profit=(
                        me_in_round.profit
                    ),
                )
            )

        return dict(

            # Subjects see choices 1-8
            my_price=(
                my_display_price
            ),

            other_price=(
                other_display_price
            ),

            profit=player.profit,

            matrix_rows=matrix_to_rows(
                matrix,
                prices,
            ),

            # Actual prices retained internally
            prices=prices,

            # Displayed table headings
            display_choices=list(
                range(1, 9)
            ),

            history_rows=history_rows,

            # Zero-based index is still useful
            # for highlighting the selected column.
            other_price_index=(
                other_price_index
            ),

            # Displayed row choice for highlighting
            my_price_index=(
                my_price_index
            ),

            my_invest=my_invest,

            other_invest=other_invest,
        )
# ============================================================
# MATCH STATUS
# ============================================================

class MatchStatus(Page):

    def vars_for_template(self):

        current_round = self.round_number

        match_ends = (
            current_round
            in Constants.last_rounds
        )

        match_continues = not match_ends

        part_ends = (
            current_round
            == Constants.num_rounds
        )

        new_match_next = (
            match_ends
            and not part_ends
        )

        return dict(

            match_continues=match_continues,

            match_ends=match_ends,

            new_match_next=new_match_next,

            part_ends=part_ends,

            current_match=(
                self.subsession.supergame_number
            ),

            current_round_in_match=(
                self.subsession.round_in_supergame
            ),
        )


# ============================================================
# END OF PRICING PART
# ============================================================

class Part1End(Page):

    def is_displayed(self):

        return (
            self.round_number
            == Constants.num_rounds
        )


# ============================================================
# SVO
# ============================================================

class SVO(Page):

    form_model = 'player'

    form_fields = [
        'svo_q1',
        'svo_q2',
        'svo_q3',
        'svo_q4',
        'svo_q5',
        'svo_q6',
    ]

    def is_displayed(self):

        return (
            self.round_number
            == Constants.num_rounds
        )

    def vars_for_template(self):

        questions = []

        for question_number, task in enumerate(
            Constants.SVO_TASKS,
            start=1,
        ):

            columns = []

            for option_index in range(9):

                columns.append(
                    dict(
                        value=(
                            option_index + 1
                        ),

                        you=(
                            task['you'][option_index]
                        ),

                        other=(
                            task['other'][option_index]
                        ),
                    )
                )

            questions.append(
                dict(
                    number=question_number,

                    field_name=(
                        f'svo_q{question_number}'
                    ),

                    columns=columns,
                )
            )

        return dict(

            questions=questions,

            dollars_per_point=(
                Constants.SVO_DOLLARS_PER_POINT
            ),
        )

    def before_next_page(self):

        self.player.calculate_svo()


class SVOWait(WaitPage):

    wait_for_all_groups = False

    def is_displayed(self):

        return (
            self.round_number
            == Constants.num_rounds
        )

    def after_all_players_arrive(self):

        self.group.determine_svo_payment()


class SVOEnd(Page):

    def is_displayed(self):

        return (
            self.round_number
            == Constants.num_rounds
        )


# ============================================================
# BOMB RISK TASK
# ============================================================

class BombIntro(Page):

    def is_displayed(self):

        return (
            self.round_number
            == Constants.num_rounds
        )

    def vars_for_template(self):

        return dict(

            number_of_boxes=(
                Constants.BOMB_NUMBER_OF_BOXES
            ),

            dollars_per_box=(
                Constants.BOMB_DOLLARS_PER_SAFE_BOX
            ),
        )


class BombStart(Page):

    def is_displayed(self):

        return (
            self.round_number
            == Constants.num_rounds
        )

    def before_next_page(self):

        self.player.initialize_bomb_task()


class BombStop(Page):

    form_model = 'player'

    form_fields = [
        'bomb_boxes_collected'
    ]

    def is_displayed(self):

        return (
            self.round_number
            == Constants.num_rounds
        )

    def vars_for_template(self):

        return dict(

            number_of_boxes=(
                Constants.BOMB_NUMBER_OF_BOXES
            ),

            dollars_per_box=(
                Constants.BOMB_DOLLARS_PER_SAFE_BOX
            ),

            collection_interval_ms=(
                Constants.BOMB_COLLECTION_INTERVAL_MS
            ),
        )

    def error_message(self, values):

        boxes_collected = values.get(
            'bomb_boxes_collected'
        )

        if boxes_collected is None:

            return (
                'Please complete the task by pressing STOP.'
            )

        if not (
            0
            <= boxes_collected
            <= Constants.BOMB_NUMBER_OF_BOXES
        ):

            return (
                'The number of collected boxes must be between '
                f'0 and {Constants.BOMB_NUMBER_OF_BOXES}.'
            )

    def before_next_page(self):

        self.player.calculate_bomb_payment()


class BombEnd(Page):

    def is_displayed(self):

        return (
            self.round_number
            == Constants.num_rounds
        )


# ============================================================
# DEMOGRAPHICS
# ============================================================

class Demographics(Page):

    form_model = 'player'

    form_fields = [
        'age_group',
        'gender',
        'gender_self_description',
        'education',
        'student_status',
        'field_of_study',
        'race_ethnicity',
        'race_ethnicity_other',
        'economics_courses',
        'previous_experiment',
    ]

    def is_displayed(self):

        return (
            self.round_number
            == Constants.num_rounds
        )

    def error_message(self, values):

        errors = {}

        if (
            values.get('gender')
            == 'Self-describe'
            and not values.get(
                'gender_self_description'
            )
        ):

            errors[
                'gender_self_description'
            ] = (
                'Please describe your gender '
                'or choose another option.'
            )

        if (
            values.get('race_ethnicity')
            == 'Another identity'
            and not values.get(
                'race_ethnicity_other'
            )
        ):

            errors[
                'race_ethnicity_other'
            ] = (
                'Please describe your racial or ethnic '
                'identity or choose another option.'
            )

        if errors:
            return errors


    def before_next_page(self):

        self.participant.vars.update(
            dict(

                age_group=self.player.age_group,

                gender=self.player.gender,

                gender_self_description=(
                    self.player.gender_self_description
                ),

                education=self.player.education,

                student_status=(
                    self.player.student_status
                ),

                field_of_study=(
                    self.player.field_of_study
                ),

                race_ethnicity=(
                    self.player.race_ethnicity
                ),

                race_ethnicity_other=(
                    self.player.race_ethnicity_other
                ),

                economics_courses=(
                    self.player.economics_courses
                ),

                previous_experiment=(
                    self.player.previous_experiment
                ),
            )
        )


# ============================================================
# FINAL PAYMENT
# ============================================================

class FinalPayment(Page):

    def is_displayed(self):

        return (
            self.round_number
            == Constants.num_rounds
        )

    def vars_for_template(self):

        player = self.player

        player.calculate_final_payment()

        return dict(

            quiz_score=(
                self.participant.vars.get(
                    'quiz_score',
                    0,
                )
            ),

            quiz_payment_usd=(
                player.final_quiz_payment_usd
            ),

            pricing_total_points=(
                player.pricing_total_points
            ),

            pricing_payment_usd=(
                player.pricing_payment_usd
            ),

            svo_selected_question=(
                self.participant.vars.get(
                    'svo_selected_question'
                )
            ),

            svo_selected_option=(
                self.participant.vars.get(
                    'svo_selected_option'
                )
            ),

            svo_role=(
                self.participant.vars.get(
                    'svo_role'
                )
            ),

            svo_points=(
                self.participant.vars.get(
                    'svo_points',
                    0,
                )
            ),

            svo_sender_points=(
                self.participant.vars.get(
                    'svo_sender_points',
                    0,
                )
            ),

            svo_receiver_points=(
                self.participant.vars.get(
                    'svo_receiver_points',
                    0,
                )
            ),

            svo_payment_usd=(
                player.final_svo_payment_usd
            ),

            bomb_location=(
                self.participant.vars.get(
                    'bomb_location'
                )
            ),

            bomb_boxes_collected=(
                self.participant.vars.get(
                    'bomb_boxes_collected',
                    0,
                )
            ),

            bomb_exploded=(
                self.participant.vars.get(
                    'bomb_exploded',
                    False,
                )
            ),

            bomb_safe_boxes=(
                self.participant.vars.get(
                    'bomb_safe_boxes',
                    0,
                )
            ),

            bomb_payment_usd=(
                player.final_bomb_payment_usd
            ),

            show_up_fee_usd=(
                player.final_show_up_fee_usd
            ),

            final_payment_usd=(
                player.final_payment_usd
            ),
        )


# ============================================================
# PAGE SEQUENCE
# ============================================================

page_sequence = [

    Instructions1,
    Instructions2,
    Instructions3,
    Intro,

    Quiz1,
    Quiz1Answer,

    Quiz2,
    Quiz2Answer,

    Quiz3,
    Quiz3Answer,

    Quiz4,
    Quiz4Answer,

    QuizEnd,

    Investment,
    InvestmentWait,
    InvestmentResult,

    Pricing,
    ResultsWait,
    Results,
    MatchStatus,

    Part1End,

    SVO,
    SVOWait,
    SVOEnd,

    BombIntro,
    BombStart,
    BombStop,
    BombEnd,

    Demographics,

    FinalPayment,
]