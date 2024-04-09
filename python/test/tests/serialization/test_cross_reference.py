'''read and validate trade state specified by cdm_sample'''
import sys
import os
import inspect
from pathlib import Path

from cdm.base.staticdata.party.Party import Party
from cdm.event.common.TradeState import TradeState
from rosetta.runtime.utils import BaseDataClass, AttributeWithReference

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)))
from test_helpers.config import CDM_JSON_SAMPLE_SOURCE
from serialization.cdm_comparison_test import cdm_comparison_test_from_file


def test_trade_state (cdm_sample_in=None):
    '''test trade state'''
    dir_path = os.path.dirname(__file__)
    if cdm_sample_in is None:
        sys.path.append(os.path.join(dir_path))
        cdm_sample_in = os.path.join(dir_path, CDM_JSON_SAMPLE_SOURCE, 'rates', 'EUR-Vanilla-account.json')
    json_str = Path(cdm_sample_in).read_text()
    tradestate = TradeState.model_validate_json(json_str)

    assert isinstance(tradestate.trade.account[0].partyReference, AttributeWithReference), "partyReference is not an instance of Party"

    tradestate.resolve_references()

    assert isinstance(tradestate.trade.account[0].partyReference, Party), "partyReference is not an instance of Party"


if __name__ == "__main__":
    cdm_sample = sys.argv[1] if len(sys.argv) > 1 else None
    test_trade_state(cdm_sample)