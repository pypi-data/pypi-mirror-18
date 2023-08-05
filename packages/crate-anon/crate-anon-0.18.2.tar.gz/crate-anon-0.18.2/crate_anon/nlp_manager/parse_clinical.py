#!/usr/bin/env python
# crate_anon/nlp_manager/parse_clinical.py

import logging
from typing import Any, Dict, Iterator, List, Optional, Tuple

from sqlalchemy import Column, Integer, Float, String, Text

from crate_anon.nlp_manager.nlp_definition import NlpDefinition
from crate_anon.nlp_manager.regex_parser import (
    BaseNlpParser,
    common_tense,
    compile_regex,
    NumericalResultParser,
    OPTIONAL_RESULTS_IGNORABLES,
    PAST,
    PRESENT,
    RELATION,
    SimpleNumericalResultParser,
    TENSE_INDICATOR,
    to_float,
    to_pos_float,
    ValidatorBase,
    WORD_BOUNDARY,
)
from crate_anon.nlp_manager.regex_numbers import SIGNED_FLOAT
from crate_anon.nlp_manager.regex_units import (
    CM,
    FEET,
    INCHES,
    KG,
    kg_from_st_lb_oz,
    KG_PER_SQ_M,
    LB,
    M,
    m_from_ft_in,
    m_from_m_cm,
    MM_HG,
    STONES,
)

log = logging.getLogger(__name__)


# =============================================================================
#  Anthropometrics
# =============================================================================

# -----------------------------------------------------------------------------
# Height
# -----------------------------------------------------------------------------

class Height(NumericalResultParser):
    """Height. Handles metric and imperial."""
    METRIC_HEIGHT = r"""
        (                           # capture group
            (?:
                ( {SIGNED_FLOAT} )          # capture group
                {OPTIONAL_RESULTS_IGNORABLES}
                {M}
                {OPTIONAL_RESULTS_IGNORABLES}
                ( {SIGNED_FLOAT} )          # capture group
                {OPTIONAL_RESULTS_IGNORABLES}
                {CM}
            )
            | (?:
                ( {SIGNED_FLOAT} )          # capture group
                {OPTIONAL_RESULTS_IGNORABLES}
                {M}
            )
            | (?:
                ( {SIGNED_FLOAT} )          # capture group
                {OPTIONAL_RESULTS_IGNORABLES}
                {CM}
            )
        )
    """.format(SIGNED_FLOAT=SIGNED_FLOAT,
               OPTIONAL_RESULTS_IGNORABLES=OPTIONAL_RESULTS_IGNORABLES,
               M=M,
               CM=CM)
    IMPERIAL_HEIGHT = r"""
        (                           # capture group
            (?:
                ( {SIGNED_FLOAT} )      # capture group
                {OPTIONAL_RESULTS_IGNORABLES}
                {FEET}
                {OPTIONAL_RESULTS_IGNORABLES}
                ( {SIGNED_FLOAT} )      # capture group
                {OPTIONAL_RESULTS_IGNORABLES}
                {INCHES}
            )
            | (?:
                ( {SIGNED_FLOAT} )      # capture group
                {OPTIONAL_RESULTS_IGNORABLES}
                {FEET}
            )
            | (?:
                ( {SIGNED_FLOAT} )      # capture group
                {OPTIONAL_RESULTS_IGNORABLES}
                {INCHES}
            )
        )
    """.format(SIGNED_FLOAT=SIGNED_FLOAT,
               OPTIONAL_RESULTS_IGNORABLES=OPTIONAL_RESULTS_IGNORABLES,
               FEET=FEET,
               INCHES=INCHES)
    HEIGHT = r"""
        (?:
            \b height \b
        )
    """
    REGEX = r"""
        ( {HEIGHT} )                       # group for "BMI" or equivalent
        {OPTIONAL_RESULTS_IGNORABLES}
        ( {TENSE_INDICATOR} )?             # optional group for tense indicator
        {OPTIONAL_RESULTS_IGNORABLES}
        ( {RELATION} )?                    # optional group for relation
        {OPTIONAL_RESULTS_IGNORABLES}
        (?:
            {METRIC_HEIGHT}
            | {IMPERIAL_HEIGHT}
        )
    """.format(
        HEIGHT=HEIGHT,
        OPTIONAL_RESULTS_IGNORABLES=OPTIONAL_RESULTS_IGNORABLES,
        TENSE_INDICATOR=TENSE_INDICATOR,
        RELATION=RELATION,
        METRIC_HEIGHT=METRIC_HEIGHT,
        IMPERIAL_HEIGHT=IMPERIAL_HEIGHT,
        SIGNED_FLOAT=SIGNED_FLOAT,
        KG_PER_SQ_M=KG_PER_SQ_M,
    )

    COMPILED_REGEX = compile_regex(REGEX)
    NAME = "Height"
    PREFERRED_UNIT_COLUMN = "value_m"

    def __init__(self,
                 nlpdef: Optional[NlpDefinition],
                 cfgsection: Optional[str],
                 commit: bool = False,
                 debug: bool = False) -> None:
        super().__init__(
            nlpdef=nlpdef,
            cfgsection=cfgsection,
            variable=self.NAME,
            target_unit=self.PREFERRED_UNIT_COLUMN,
            commit=commit
        )
        if debug:
            print("Regex for {}: {}".format(type(self).__name__, self.REGEX))

    def parse(self, text: str,
              debug: bool = False) -> Iterator[Tuple[str, Dict[str, Any]]]:
        for m in self.COMPILED_REGEX.finditer(text):  # watch out: 'm'/metres
            if debug:
                print("Match {} for {}".format(m, repr(text)))
            startpos = m.start()
            endpos = m.end()
            matching_text = m.group(0)  # the whole thing
            variable_text = m.group(1)
            tense_indicator = m.group(2)
            relation = m.group(3)
            metric_expression = m.group(4)
            metric_m_and_cm_m = m.group(5)
            metric_m_and_cm_cm = m.group(6)
            metric_m_only_m = m.group(7)
            metric_cm_only_cm = m.group(8)
            imperial_expression = m.group(9)
            imperial_ft_and_in_ft = m.group(10)
            imperial_ft_and_in_in = m.group(11)
            imperial_ft_only_ft = m.group(12)
            imperial_in_only_in = m.group(13)

            expression = None
            value_m = None
            if metric_expression:
                expression = metric_expression
                if metric_m_and_cm_m and metric_m_and_cm_cm:
                    metres = to_pos_float(metric_m_and_cm_m)  # beware: 'm' above
                    cm = to_pos_float(metric_m_and_cm_cm)
                    value_m = m_from_m_cm(metres=metres, centimetres=cm)
                elif metric_m_only_m:
                    value_m = to_pos_float(metric_m_only_m)
                elif metric_cm_only_cm:
                    cm = to_pos_float(metric_cm_only_cm)
                    value_m = m_from_m_cm(centimetres=cm)
            elif imperial_expression:
                expression = imperial_expression
                if imperial_ft_and_in_ft and imperial_ft_and_in_in:
                    ft = to_pos_float(imperial_ft_and_in_ft)
                    inches = to_pos_float(imperial_ft_and_in_in)
                    value_m = m_from_ft_in(feet=ft, inches=inches)
                elif imperial_ft_only_ft:
                    ft = to_pos_float(imperial_ft_only_ft)
                    value_m = m_from_ft_in(feet=ft)
                elif imperial_in_only_in:
                    inches = to_pos_float(imperial_in_only_in)
                    value_m = m_from_ft_in(inches=inches)

            tense, relation = common_tense(tense_indicator, relation)

            yield self.tablename, {
                self.FN_VARIABLE_NAME: self.variable,
                self.FN_CONTENT: matching_text,
                self.FN_START: startpos,
                self.FN_END: endpos,
                self.FN_VARIABLE_TEXT: variable_text,
                self.FN_RELATION: relation,
                self.FN_VALUE_TEXT: expression,
                self.target_unit: value_m,
                self.FN_TENSE: tense,
            }

    def test(self):
        self.test_numerical_parser([
            ("Height", []),  # should fail; no values
            ("her height was 1.6m", [1.6]),
            ("Height = 1.23 m", [1.23]),
            ("her height is 1.5m", [1.5]),
            ('''Height 5'8" ''', [m_from_ft_in(feet=5, inches=8)]),
            ("Height 5 ft 8 in", [m_from_ft_in(feet=5, inches=8)]),
            ("Height 5 feet 8 inches", [m_from_ft_in(feet=5, inches=8)]),
        ])
        # *** deal with "tall" and plain "is", e.g.
        # she is 6'2"; she is 1.5m tall


class HeightValidator(ValidatorBase):
    """Validator for Height (see ValidatorBase for explanation)."""
    def __init__(self,
                 nlpdef: Optional[NlpDefinition],
                 cfgsection: Optional[str],
                 commit: bool = False) -> None:
        super().__init__(nlpdef=nlpdef,
                         cfgsection=cfgsection,
                         regex_str_list=[Height.HEIGHT],
                         validated_variable=Height.NAME,
                         commit=commit)


# -----------------------------------------------------------------------------
# Weight (mass)
# -----------------------------------------------------------------------------

class Weight(NumericalResultParser):
    """Weight. Handles metric and imperial."""
    METRIC_WEIGHT = r"""
        (                           # capture group
            ( {SIGNED_FLOAT} )          # capture group
            {OPTIONAL_RESULTS_IGNORABLES}
            {KG}
        )
    """.format(SIGNED_FLOAT=SIGNED_FLOAT,
               OPTIONAL_RESULTS_IGNORABLES=OPTIONAL_RESULTS_IGNORABLES,
               KG=KG)
    IMPERIAL_WEIGHT = r"""
        (                           # capture group
            (?:
                ( {SIGNED_FLOAT} )      # capture group
                {OPTIONAL_RESULTS_IGNORABLES}
                {STONES}
                {OPTIONAL_RESULTS_IGNORABLES}
                ( {SIGNED_FLOAT} )      # capture group
                {OPTIONAL_RESULTS_IGNORABLES}
                {LB}
            )
            | (?:
                ( {SIGNED_FLOAT} )      # capture group
                {OPTIONAL_RESULTS_IGNORABLES}
                {STONES}
            )
            | (?:
                ( {SIGNED_FLOAT} )      # capture group
                {OPTIONAL_RESULTS_IGNORABLES}
                {LB}
            )
        )
    """.format(SIGNED_FLOAT=SIGNED_FLOAT,
               OPTIONAL_RESULTS_IGNORABLES=OPTIONAL_RESULTS_IGNORABLES,
               STONES=STONES,
               LB=LB)
    WEIGHT = r"""
        (?:
            \b weigh[ts] \b       # weight, weighs
        )
    """
    REGEX = r"""
        ( {WEIGHT} )                       # group for "BMI" or equivalent
        {OPTIONAL_RESULTS_IGNORABLES}
        ( {TENSE_INDICATOR} )?             # optional group for tense indicator
        {OPTIONAL_RESULTS_IGNORABLES}
        ( {RELATION} )?                    # optional group for relation
        {OPTIONAL_RESULTS_IGNORABLES}
        (?:
            {METRIC_WEIGHT}
            | {IMPERIAL_WEIGHT}
        )
    """.format(
        WEIGHT=WEIGHT,
        OPTIONAL_RESULTS_IGNORABLES=OPTIONAL_RESULTS_IGNORABLES,
        TENSE_INDICATOR=TENSE_INDICATOR,
        RELATION=RELATION,
        METRIC_WEIGHT=METRIC_WEIGHT,
        IMPERIAL_WEIGHT=IMPERIAL_WEIGHT,
        SIGNED_FLOAT=SIGNED_FLOAT,
        KG_PER_SQ_M=KG_PER_SQ_M,
    )

    COMPILED_REGEX = compile_regex(REGEX)
    NAME = "Weight"
    PREFERRED_UNIT_COLUMN = "value_kg"

    def __init__(self,
                 nlpdef: Optional[NlpDefinition],
                 cfgsection: Optional[str],
                 commit: bool = False,
                 debug: bool = False) -> None:
        super().__init__(
            nlpdef=nlpdef,
            cfgsection=cfgsection,
            variable=self.NAME,
            target_unit=self.PREFERRED_UNIT_COLUMN,
            commit=commit
        )
        if debug:
            print("Regex for {}: {}".format(type(self).__name__, self.REGEX))

    def parse(self, text: str,
              debug: bool = False) -> Iterator[Tuple[str, Dict[str, Any]]]:
        for m in self.COMPILED_REGEX.finditer(text):
            if debug:
                print("Match {} for {}".format(m, repr(text)))
            startpos = m.start()
            endpos = m.end()
            matching_text = m.group(0)  # the whole thing
            variable_text = m.group(1)
            tense_indicator = m.group(2)
            relation = m.group(3)
            metric_expression = m.group(4)
            metric_value = m.group(5)
            imperial_expression = m.group(6)
            imperial_st_and_lb_st = m.group(7)
            imperial_st_and_lb_lb = m.group(8)
            imperial_st_only_st = m.group(9)
            imperial_lb_only_lb = m.group(10)

            expression = None
            value_kg = None
            if metric_expression:
                expression = metric_expression
                value_kg = to_float(metric_value)
            elif imperial_expression:
                expression = imperial_expression
                if imperial_st_and_lb_st and imperial_st_and_lb_lb:
                    st = to_float(imperial_st_and_lb_st)
                    lb = to_float(imperial_st_and_lb_lb)
                    value_kg = kg_from_st_lb_oz(stones=st, pounds=lb)
                elif imperial_st_only_st:
                    st = to_float(imperial_st_only_st)
                    value_kg = kg_from_st_lb_oz(stones=st)
                elif imperial_lb_only_lb:
                    lb = to_float(imperial_lb_only_lb)
                    value_kg = kg_from_st_lb_oz(pounds=lb)

            # All left as signed float, as you definitely see things like
            # "weight -0.3 kg" for weight changes.

            tense, relation = common_tense(tense_indicator, relation)

            yield self.tablename, {
                self.FN_VARIABLE_NAME: self.variable,
                self.FN_CONTENT: matching_text,
                self.FN_START: startpos,
                self.FN_END: endpos,
                self.FN_VARIABLE_TEXT: variable_text,
                self.FN_RELATION: relation,
                self.FN_VALUE_TEXT: expression,
                self.target_unit: value_kg,
                self.FN_TENSE: tense,
            }

    def test(self):
        self.test_numerical_parser([
            ("Weight", []),  # should fail; no values
            ("her weight was 60.2kg", [60.2]),
            ("Weight = 52.3kg", [52.3]),
            ("she weighs 61kg", [61]),
            ("she weighs 61 kg", [61]),
            ("she weighs 61 kgs", [61]),
            ("she weighs 61 kilo", [61]),
            ("she weighs 61 kilos", [61]),
            ("she weighs 8 stones ", [kg_from_st_lb_oz(stones=8)]),
            ("she weighs 200 lb", [kg_from_st_lb_oz(pounds=200)]),
            ("she weighs 200 pounds", [kg_from_st_lb_oz(pounds=200)]),
            ("she weighs 6 st 12 lb", [kg_from_st_lb_oz(stones=6, pounds=12)]),
        ])


class WeightValidator(ValidatorBase):
    """Validator for Weight (see ValidatorBase for explanation)."""
    def __init__(self,
                 nlpdef: Optional[NlpDefinition],
                 cfgsection: Optional[str],
                 commit: bool = False) -> None:
        super().__init__(nlpdef=nlpdef,
                         cfgsection=cfgsection,
                         regex_str_list=[Weight.WEIGHT],
                         validated_variable=Weight.NAME,
                         commit=commit)


# -----------------------------------------------------------------------------
# Body mass index (BMI)
# -----------------------------------------------------------------------------

class Bmi(SimpleNumericalResultParser):
    """Body mass index (in kg / m^2)."""
    BMI = r"""
        (?:
            {WORD_BOUNDARY}
            (?:
                BMI
                | body \s+ mass \s+ index
            )
            {WORD_BOUNDARY}
        )
    """.format(WORD_BOUNDARY=WORD_BOUNDARY)
    REGEX = r"""
        ( {BMI} )                          # group for "BMI" or equivalent
        {OPTIONAL_RESULTS_IGNORABLES}
        ( {TENSE_INDICATOR} )?             # optional group for tense indicator
        {OPTIONAL_RESULTS_IGNORABLES}
        ( {RELATION} )?                    # optional group for relation
        {OPTIONAL_RESULTS_IGNORABLES}
        ( {SIGNED_FLOAT} )                 # group for value
        {OPTIONAL_RESULTS_IGNORABLES}
        (                                  # group for units
            {KG_PER_SQ_M}
        )?
    """.format(
        BMI=BMI,
        OPTIONAL_RESULTS_IGNORABLES=OPTIONAL_RESULTS_IGNORABLES,
        TENSE_INDICATOR=TENSE_INDICATOR,
        RELATION=RELATION,
        SIGNED_FLOAT=SIGNED_FLOAT,
        KG_PER_SQ_M=KG_PER_SQ_M,
    )
    NAME = "BMI"
    PREFERRED_UNIT_COLUMN = "value_kg_per_sq_m"
    UNIT_MAPPING = {
        KG_PER_SQ_M: 1,       # preferred unit
    }
    # deal with "a BMI of 30"?

    def __init__(self,
                 nlpdef: Optional[NlpDefinition],
                 cfgsection: Optional[str],
                 commit: bool = False) -> None:
        super().__init__(
            nlpdef=nlpdef,
            cfgsection=cfgsection,
            regex_str=self.REGEX,
            variable=self.NAME,
            target_unit=self.PREFERRED_UNIT_COLUMN,
            units_to_factor=self.UNIT_MAPPING,
            commit=commit
        )

    def test(self):
        self.test_numerical_parser([
            ("BMI", []),  # should fail; no values
            ("body mass index was 30", [30]),
            ("his BMI (30) is too high", [30]),
            ("BMI 25 kg/sq m", [25]),
            ("BMI was 18.4 kg/m^-2", [18.4]),
            ("ACE 79", []),
        ])


class BmiValidator(ValidatorBase):
    """Validator for Bmi (see ValidatorBase for explanation)."""
    def __init__(self,
                 nlpdef: Optional[NlpDefinition],
                 cfgsection: Optional[str],
                 commit: bool = False) -> None:
        super().__init__(nlpdef=nlpdef,
                         cfgsection=cfgsection,
                         regex_str_list=[Bmi.BMI],
                         validated_variable=Bmi.NAME,
                         commit=commit)


# =============================================================================
#  Bedside investigations: BP
# =============================================================================

class Bp(BaseNlpParser):
    """Blood pressure, in mmHg. (Since we produce two variables, SBP and DBP,
    we subclass BaseNlpParser directly.)"""
    BP = r"""
        (?:
            \b blood \s+ pressure \b
            | \b B\.?P\.? \b
        )
    """
    SYSTOLIC_BP = r"""
        (?:
            \b systolic \s+ {BP}
            | \b S\.?B\.?P\.? \b
        )
    """.format(BP=BP)
    DIASTOLIC_BP = r"""
        (?:
            \b diastolic \s+ {BP}
            | \b D\.?B\.?P\.? \b
        )
    """.format(BP=BP)

    TWO_NUMBER_BP = r"""
        ( {SIGNED_FLOAT} )
        (?:
            \b over \b
            | \/
        )
        ( {SIGNED_FLOAT} )
    """.format(SIGNED_FLOAT=SIGNED_FLOAT)
    ONE_NUMBER_BP = SIGNED_FLOAT

    COMPILED_BP = compile_regex(BP)
    COMPILED_SBP = compile_regex(SYSTOLIC_BP)
    COMPILED_DBP = compile_regex(DIASTOLIC_BP)
    COMPILED_ONE_NUMBER_BP = compile_regex(ONE_NUMBER_BP)
    COMPILED_TWO_NUMBER_BP = compile_regex(TWO_NUMBER_BP)
    REGEX = r"""
        (                               # group for "BP" or equivalent
            {SYSTOLIC_BP}               # ... from more to less specific
            | {DIASTOLIC_BP}
            | {BP}
        )
        {OPTIONAL_RESULTS_IGNORABLES}
        ( {TENSE_INDICATOR} )?         # optional group for tense indicator
        {OPTIONAL_RESULTS_IGNORABLES}
        ( {RELATION} )?                # optional group for relation
        {OPTIONAL_RESULTS_IGNORABLES}
        (                              # BP
            {SIGNED_FLOAT}                  # 120
            (?:
                \s*
                (?: \b over \b | \/ )       # /
                \s*
                {SIGNED_FLOAT}              # 80
            )?
        )
        {OPTIONAL_RESULTS_IGNORABLES}
        (                              # group for units
            {MM_HG}
        )?
    """.format(
        BP=BP,
        SYSTOLIC_BP=SYSTOLIC_BP,
        DIASTOLIC_BP=DIASTOLIC_BP,
        OPTIONAL_RESULTS_IGNORABLES=OPTIONAL_RESULTS_IGNORABLES,
        TENSE_INDICATOR=TENSE_INDICATOR,
        RELATION=RELATION,
        SIGNED_FLOAT=SIGNED_FLOAT,
        MM_HG=MM_HG,
    )
    COMPILED_REGEX = compile_regex(REGEX)

    FN_SYSTOLIC_BP_MMHG = 'systolic_bp_mmhg'
    FN_DIASTOLIC_BP_MMHG = 'diastolic_bp_mmhg'

    NAME = "BP"
    UNIT_MAPPING = {
        MM_HG: 1,       # preferred unit
    }

    def __init__(self,
                 nlpdef: Optional[NlpDefinition],
                 cfgsection: Optional[str],
                 commit: bool = False) -> None:
        super().__init__(
            nlpdef=nlpdef,
            cfgsection=cfgsection,
            commit=commit
        )
        if nlpdef is None:  # only None for debugging!
            self.tablename = ''
        else:
            self.tablename = nlpdef.opt_str(
                cfgsection, 'desttable', required=True)

    def dest_tables_columns(self) -> Dict[str, List[Column]]:
        return {self.tablename: [
            Column(NumericalResultParser.FN_CONTENT, Text,
                   doc="Matching text contents"),
            Column(NumericalResultParser.FN_START, Integer,
                   doc="Start position (of matching string within whole "
                       "text)"),
            Column(NumericalResultParser.FN_END, Integer,
                   doc="End position (of matching string within whole text)"),
            Column(NumericalResultParser.FN_VARIABLE_TEXT, Text,
                   doc="Text that matched the variable name"),
            Column(NumericalResultParser.FN_RELATION,
                   String(NumericalResultParser.MAX_RELATION_LENGTH),
                   doc="Text that matched the mathematical relationship "
                       "between variable and value (e.g. '=', '<='"),
            Column(NumericalResultParser.FN_VALUE_TEXT,
                   String(NumericalResultParser.MAX_VALUE_TEXT_LENGTH),
                   doc="Matched numerical value, as text"),
            Column(NumericalResultParser.FN_UNITS,
                   String(NumericalResultParser.MAX_UNITS_LENGTH),
                   doc="Matched units, as text"),
            Column(self.FN_SYSTOLIC_BP_MMHG, Float,
                   doc="Systolic BP in mmHg"),
            Column(self.FN_DIASTOLIC_BP_MMHG, Float,
                   doc="Diastolic BP in mmHg"),
            Column(NumericalResultParser.FN_TENSE,
                   String(NumericalResultParser.MAX_TENSE_LENGTH),
                   doc="Tense indicator, if known (e.g. '{}', '{}')".format(
                       PAST, PRESENT)),
        ]}

    def parse(self, text: str,
              debug: bool = False) -> Iterator[Tuple[str, Dict[str, Any]]]:
        for m in self.COMPILED_REGEX.finditer(text):
            if debug:
                print("Match {} for {}".format(m, repr(text)))
            startpos = m.start()
            endpos = m.end()
            matching_text = m.group(0)  # the whole thing
            variable_text = m.group(1)
            tense_indicator = m.group(2)
            relation = m.group(3)
            value_text = m.group(4)
            units = m.group(5)

            sbp = None
            dbp = None
            if self.COMPILED_SBP.match(variable_text):
                if self.COMPILED_ONE_NUMBER_BP.match(value_text):
                    sbp = to_pos_float(value_text)
            elif self.COMPILED_DBP.match(variable_text):
                if self.COMPILED_ONE_NUMBER_BP.match(value_text):
                    dbp = to_pos_float(value_text)
            elif self.COMPILED_BP.match(variable_text):
                bpmatch = self.COMPILED_TWO_NUMBER_BP.match(value_text)
                if bpmatch:
                    sbp = to_pos_float(bpmatch.group(1))
                    dbp = to_pos_float(bpmatch.group(2))
            if sbp is None and dbp is None:
                log.warning("Failed interpretation: {}".format(matching_text))
                continue

            tense, relation = common_tense(tense_indicator, relation)

            yield self.tablename, {
                NumericalResultParser.FN_CONTENT: matching_text,
                NumericalResultParser.FN_START: startpos,
                NumericalResultParser.FN_END: endpos,
                NumericalResultParser.FN_VARIABLE_TEXT: variable_text,
                NumericalResultParser.FN_RELATION: relation,
                NumericalResultParser.FN_VALUE_TEXT: value_text,
                NumericalResultParser.FN_UNITS: units,
                self.FN_SYSTOLIC_BP_MMHG: sbp,
                self.FN_DIASTOLIC_BP_MMHG: dbp,
                NumericalResultParser.FN_TENSE: tense,
            }

    def test_bp_parser(
            self,
            test_expected_list: List[Tuple[str, List[Tuple[float,
                                                           float]]]]) -> None:
        print("Testing parser: {}".format(type(self).__name__))
        for test_string, expected_values in test_expected_list:
            actual_values = list(
                (x[self.FN_SYSTOLIC_BP_MMHG], x[self.FN_DIASTOLIC_BP_MMHG])
                for t, x in self.parse(test_string)
            )
            assert actual_values == expected_values, (
                """Parser {}: Expected {}, got {}, when parsing {}""".format(
                    type(self).__name__,
                    expected_values,
                    actual_values,
                    repr(test_string)
                )
            )
        print("... OK")

    def test(self):
        self.test_bp_parser([
            ("BP", []),  # should fail; no values
            ("his blood pressure was 120/80", [(120, 80)]),
            ("BP 120/80 mmhg", [(120, 80)]),
            ("systolic BP 120", [(120, None)]),
            ("diastolic BP 80", [(None, 80)]),
            ("BP-130/70", [(130, 70)]),
            # Unsure if best to take abs value.
            # One reason not to might be if people express changes, e.g.
            # "BP change -40/-10", but I very much doubt it.
            # Went with abs value using to_pos_float().
        ])


class BpValidator(ValidatorBase):
    """Validator for Bp (see ValidatorBase for explanation)."""
    def __init__(self,
                 nlpdef: Optional[NlpDefinition],
                 cfgsection: Optional[str],
                 commit: bool = False) -> None:
        super().__init__(nlpdef=nlpdef,
                         cfgsection=cfgsection,
                         regex_str_list=[Bp.REGEX],
                         validated_variable=Bp.NAME,
                         commit=commit)


# =============================================================================
#  Command-line entry point
# =============================================================================

if __name__ == '__main__':
    height = Height(None, None)
    height.test()
    weight = Weight(None, None)
    weight.test()
    bmi = Bmi(None, None)
    bmi.test()
    bp = Bp(None, None)
    bp.test()
