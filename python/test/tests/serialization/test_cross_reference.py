'''read and validate trade state specified by cdm_sample'''
import sys
import os
import inspect
from pathlib import Path

from cdm.base.staticdata.party.Party import Party
from cdm.event.common.TradeState import TradeState
from rosetta.runtime.utils import BaseDataClass, AttributeWithReference, AttributeWithMeta, \
    AttributeWithScheme, AttributeWithLocation, AttributeWithAddress

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)))
from test_helpers.config import CDM_JSON_SAMPLE_SOURCE
from serialization.cdm_comparison_test import cdm_comparison_test_from_file



def test_trade_state_reference_pos (cdm_sample_in=None):
    '''test resolving key/id references'''
    dir_path = os.path.dirname(__file__)
    if cdm_sample_in is None:
        sys.path.append(os.path.join(dir_path))
        cdm_sample_in = os.path.join(dir_path, CDM_JSON_SAMPLE_SOURCE, 'rates', 'EUR-Vanilla-account.json')
    json_str = Path(cdm_sample_in).read_text()
    tradestate = TradeState.model_validate_json(json_str)
    assert isinstance(tradestate.trade.tradableProduct.product.contractualProduct.economicTerms.payout.interestRatePayout[1].resetDates.fixingDates.dateRelativeTo, AttributeWithReference), "calculationPeriodDatesReference is not an instance of calculationPeriodDates"
    tradestate.resolve_references()
    assert 'globalKey' in tradestate.trade.tradableProduct.product.contractualProduct.economicTerms.payout.interestRatePayout[1].resetDates.fixingDates.dateRelativeTo.meta, "reference is not resolved"
def test_trade_state_reference_neg (cdm_sample_in = None):
    '''negative test resolving key/id references'''
    dir_path = os.path.dirname(__file__)
    if cdm_sample_in is None:
        sys.path.append(os.path.join(dir_path))
        cdm_sample_in = os.path.join(dir_path, CDM_JSON_SAMPLE_SOURCE, 'rates', 'EUR-Vanilla-account.json')
    json_str = Path(cdm_sample_in).read_text()
    tradestate = TradeState.model_validate_json(json_str)
    tradestate.resolve_references()
    assert 'globalKey' in tradestate.trade.account[0].partyReference.meta #the reference key has to be changed for the error!

def test_trade_state_meta (cdm_sample_in=None):
    '''test AttributeWithMeta'''
    dir_path = os.path.dirname(__file__)
    if cdm_sample_in is None:
        sys.path.append(os.path.join(dir_path))
        cdm_sample_in = os.path.join(dir_path, CDM_JSON_SAMPLE_SOURCE, 'rates', 'EUR-Vanilla-account.json')
    json_str = Path(cdm_sample_in).read_text()
    tradestate = TradeState.model_validate_json(json_str)
    assert isinstance(tradestate.trade.tradeDate, AttributeWithMeta), "tradeDate has no meta"

def test_trade_state_scheme (cdm_sample_in=None):
    '''test AttributeWithScheme'''
    dir_path = os.path.dirname(__file__)
    if cdm_sample_in is None:
        sys.path.append(os.path.join(dir_path))
        cdm_sample_in = os.path.join(dir_path, CDM_JSON_SAMPLE_SOURCE, 'rates', 'EUR-Vanilla-account.json')
    json_str = Path(cdm_sample_in).read_text()
    tradestate = TradeState.model_validate_json(json_str)
    assert isinstance(tradestate.trade.party[0].partyId[0].identifier, AttributeWithScheme), "identifier is not meta scheme"

def test_trade_state_address_location (cdm_sample_in=None):
    '''test AttributeWithAddress/Location'''
    dir_path = os.path.dirname(__file__)
    if cdm_sample_in is None:
        sys.path.append(os.path.join(dir_path))
        cdm_sample_in = os.path.join(dir_path, CDM_JSON_SAMPLE_SOURCE, 'rates', 'EUR-Vanilla-account.json')
    json_str = Path(cdm_sample_in).read_text()
    tradestate = TradeState.model_validate_json(json_str)
    assert isinstance(tradestate.trade.tradableProduct.tradeLot[0].priceQuantity[0].price[0], AttributeWithLocation), "not of type location"
    assert isinstance(tradestate.trade.tradableProduct.product.contractualProduct.economicTerms.payout.interestRatePayout[0].priceQuantity.quantitySchedule,AttributeWithAddress), "not an address"

def test_trade_state_address_location_reference (cdm_sample_in=None):
    '''resolving address/location reference'''
    dir_path = os.path.dirname(__file__)
    if cdm_sample_in is None:
        sys.path.append(os.path.join(dir_path))
        cdm_sample_in = os.path.join(dir_path, CDM_JSON_SAMPLE_SOURCE, 'rates', 'EUR-Vanilla-account.json')
    json_str = Path(cdm_sample_in).read_text()
    tradestate = TradeState.model_validate_json(json_str) #interestRatePayout[0].priceQuantity.quantitySchedule #interestRatePayout[1].rateSpecification.floatingRate.rateOption
    assert isinstance(tradestate.trade.tradableProduct.product.contractualProduct.economicTerms.payout.interestRatePayout[0].priceQuantity.quantitySchedule, AttributeWithAddress )
    tradestate.resolve_references()
    assert isinstance(tradestate.trade.tradableProduct.product.contractualProduct.economicTerms.payout.interestRatePayout[0].priceQuantity.quantitySchedule, AttributeWithLocation)



if __name__ == "__main__":
    cdm_sample = sys.argv[1] if len(sys.argv) > 1 else None
    test_trade_state_reference_pos(cdm_sample)
    test_trade_state_reference_neg(cdm_sample)
    test_trade_state_meta(cdm_sample)
    test_trade_state_scheme(cdm_sample)
    test_trade_state_address_location(cdm_sample)
    test_trade_state_address_location_reference(cdm_sample)