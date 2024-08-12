'''Tests of the local registration of conditions'''
import inspect
from sqlite3 import Date

import pytest
import datetime
from cdm.base.datetime.DateList import DateList
from rosetta.runtime.utils import all_elements, any_elements, rosetta_count, rosetta_filter, _resolve_rosetta_attr, \
    flatten_list, join, set_rosetta_attr
from rosetta.runtime.utils import execute_local_conditions
from rosetta.runtime.utils import ConditionViolationError

from target.python.src.cdm.event.common.Reset import Reset
from target.python.src.cdm.event.common.SettlementOrigin import SettlementOrigin
from target.python.src.cdm.event.common.TradeState import TradeState
from target.python.src.cdm.event.common.functions.InterestCashSettlementAmount import InterestCashSettlementAmount
from target.python.src.cdm.product.asset.InterestRatePayout import InterestRatePayout


def test_binary_operations():
    class T:
        def __init__(self):
            self.cleared = 'Y'
            self.counterparty1FinancialEntityIndicator = None
            self.counterparty1FinancialEntityIndicator = None
            self.actionType = "NEWT"
            self.eventType = "CLRG"
            self.originalSwapUTI = 1
            self.originalSwapUSI = 'OKI'
            self.openTradeStates = 2

    self = T()
    #equals
    res = all_elements(self.eventType,"=","CLRG")
    assert res
    res=self.eventType=="CLRG"
    assert res
    #not_equals
    res=any_elements(self.actionType,"<>","NEWT")
    assert not res
    res=self.actionType!="NEWT"
    assert not res
    #greaterthan
    res=all_elements(self.openTradeStates,">",1)
    assert res
def test_count_operation():
    class T:
        def __init__(self):
            self.tradeState=None
            self.openTradeStates = [self.tradeState , self.tradeState]
            self.closedTradeStates = 1

    self = T()
    res = rosetta_count(self.openTradeStates)
    assert res == 2

def test_max_min_operation():
    class T:
        def __init__(self):
            self.tradeState=None
            self.openTradeStates = [self.tradeState , self.tradeState]
            self.closedTradeStates = [self.tradeState]

    self = T()
    res_max = max(len(self.openTradeStates),len(self.closedTradeStates))
    res_min= min(len(self.openTradeStates),len(self.closedTradeStates))
    assert res_max>res_min
def test_sum_operation():
    class T:
        def __init__(self):
            self.tradeState=None
            self.openTradeStates = [self.tradeState , self.tradeState]
            self.closedTradeStates = 1

    self = T()
    res = sum(1 for ots in self.openTradeStates if ots is None)
    assert res==2
def test_filteroperation():
    class T:
        def __init__(self):
            self.partyRole1={'role':"Seller"}
            self.partyRole2={'role':None}
            self.partyRole3={'role':"Client"}
            self.partyRoles=[self.partyRole1,self.partyRole2,self.partyRole3]
            self.partyRoleEnum=["Seller","Client"]

    self = T()
    res = rosetta_filter(_resolve_rosetta_attr(self, "partyRoles"), lambda item: all_elements(
        _resolve_rosetta_attr(_resolve_rosetta_attr(self, "partyRoles"), "role"), "=",
        _resolve_rosetta_attr(self,  "partyRoleEnum")))
    assert self.partyRole1 in res and self.partyRole3 in res

def test_distinct_operation():
    class T:
        def __init__(self):
            None
            self.businessCenterEnums=["A","B","B","C"]
    self = T()
    res=set(_resolve_rosetta_attr(self, "businessCenterEnums"))
    assert len(res)==3

def test_ascending_sort_operation():
    class T:
        def __init__(self):
            self.date1=datetime.date(2021, 2, 2)
            self.date2=datetime.date(2021,2,4)
            self.date3=datetime.date(2019,11,24)
            self.adjustedValuationDates=[self.date1,self.date2,self.date3]
    self = T()
    self.sortedAdjustedValuationDates = sorted(self.adjustedValuationDates)
    firstExpectedDate=datetime.date(2019,11,24)
    assert self.sortedAdjustedValuationDates[0] == firstExpectedDate

def test_descending_sort_operation():
    class T:
        def __init__(self):
            self.date1=datetime.date(2021, 2, 2)
            self.date2=datetime.date(2021,2,4)
            self.date3=datetime.date(2019,11,24)
            self.adjustedValuationDates=[self.date1,self.date2,self.date3]
    self = T()
    self.sortedAdjustedValuationDates = sorted(self.adjustedValuationDates, reverse=True)
    firstExpectedDate=datetime.date(2021,2,4)
    assert self.sortedAdjustedValuationDates[0] == firstExpectedDate

def test_last_operation():
    class T:
        def __init__(self):
            self.date1=datetime.date(2021, 2, 2)
            self.date2=datetime.date(2021,2,4)
            self.date3=datetime.date(2019,11,24)
            self.adjustedValuationDates=[self.date1,self.date2,self.date3]
    self = T()
    self.sortedAdjustedValuationDates = sorted(self.adjustedValuationDates, reverse=True)
    expectedLastDate=datetime.date(2019,11,24)
    assert self.sortedAdjustedValuationDates[-1] == expectedLastDate

def test_flatten_operation():
    class T:
        def __init__(self):
            self.date1=datetime.date(2021, 2, 2)
            self.date2=datetime.date(2021,2,4)
            self.date3=datetime.date(2019,11,24)
            self.date4=datetime.date(2024,4,15)
            self.adjustedValuationDates1=[self.date1,self.date2]
            self.adjustedValuationDates2= [self.date3, self.date4]
            self.adjustedValuationDates=[self.adjustedValuationDates1,self.adjustedValuationDates2]
    self = T()
    res = flatten_list(self.adjustedValuationDates)
    assert len(res)==4

def test_reverse_operation():
    class T:
        def __init__(self):
            self.businessCenters=['AEAB','BBBR','INKO']
    self = T()
    res = list(reversed(self.businessCenters))
    assert res[0]=='INKO'

def test_join_operation():
    class T:
        def __init__(self):
            self.businessCenters=['AEAB','BBBR','INKO']

    self=T()
    res=join(self.businessCenters,'CAVA')
    assert 'CAVA' in res



if __name__ == '__main__':
    test_binary_operations()
    test_max_min_operation()
    test_filteroperation()
    test_join_operation()
    test_last_operation()
    test_sum_operation()
    test_ascending_sort_operation()
    test_descending_sort_operation()
    test_count_operation()
    test_distinct_operation()
    test_flatten_operation()
    test_reverse_operation()
    print('...passed')
# EOF
