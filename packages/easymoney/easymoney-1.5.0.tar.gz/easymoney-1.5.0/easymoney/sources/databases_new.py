# coding: utf-8

"""

    Tools for Processing Included Databases
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""

# adds currency transitions
# Not complete. To finish this, pycountry_wrap and options() will need to be altered.

# Imports
import pandas as pd
import pkg_resources

from datetime import datetime
from collections import defaultdict
from easymoney.support_tools import cln


DEFAULT_DATA_PATH = pkg_resources.resource_filename('easymoney', 'sources/data')


def _path_selector(path_to_data):
    """

    Select path to the data.

    :param path_to_data: a path to the databases required by EasyMoney.
    :type path_to_data: ``str`` or ``None``
    :return: DEFAULT_DATA_PATH if `path_to_data` is None; else path_to_data.
    :rtype: ``str``
    """
    if isinstance(path_to_data, str):
        return (path_to_data if not path_to_data.endswith("/") else path_to_data[:-1])
    else:
        return DEFAULT_DATA_PATH


def currency_transitions(path_to_data, date_format="%d/%m/%Y"):
    """

    Tool to created a nested Dictionary of currency transitions of the form:
    ``{CountryAlpha2 : {'old': CUR_1, 'new': CUR_2, 'date': 'DD/MM/YYYY'}``.

    :param path_to_data: path to the 'CurrencyRelationshipsDB.csv' database.
    :type path_to_data: ``str``
    :return: a dictionary mapping alpha2 codes to currency codes.
    :rtype: ``dict``
    """
    # Read in the data
    transitions = pd.read_csv(_path_selector(path_to_data) + "/CurrencyTransitionDB.csv",
                              usecols=['Alpha2', 'OldCurrency', 'NewCurrency', 'Date'])

    transitions['Date'] = pd.Series(pd.to_datetime(transitions['Date'], format="%Y")).map(
        lambda x: x.strftime(date_format)
    )

    cols = zip(*[transitions[c] for c in ('Alpha2', 'OldCurrency', 'NewCurrency', 'Date')])
    return {country: {'old': old, 'new': new, 'date': date} for country, old, new, date in cols}


def _new_old_order(alpha2, currencies, transitions):
    """

    Sort regions with multiple known currencies into [NEW, OLD].
    Note: This will not handle multiple currency transitions.

    :param alpha2: an ISO alpha 2 region code.
    :type alpha2: ``str``
    :param currencies: an iterable of currencies.
    :type currencies: ``iterable``
    :param transitions: yeild of currency_transitions().
    :type transitions: ``dict``
    :return: list of the form [NEW CURRENCY, OLD CURRENCY].
    :rtype: ``list``
    """
    if len(currencies) > 1 and all(transitions[alpha2][i] in currencies for i in ['new', 'old']):
        new_old = [transitions[alpha2]['new'], transitions[alpha2]['old']]
        return new_old + [j for j in currencies if j not in new_old]
    else:
        return currencies


def currency_mapping_to_dict(path_to_data, date_format="%d/%m/%Y"):
    """

    Constructs a mapping between country ISO Alpha 2 codes and currency ISO Alpha 3 codes
    of the form:
    ``{CountryAlpha2 : {[Currencies]}``.

    :param path_to_data: path to the 'CurrencyRelationshipsDB.csv' database.
    :type path_to_data: ``str``
    :return: a dictionary mapping alpha2 codes to currency codes.
    :rtype: ``dict``
    """
    # Read in the data
    currency_mappings = pd.read_csv(_path_selector(path_to_data) + "/CurrencyRelationshipsDB.csv",
                                    usecols=['Alpha2', 'CurrencyCode'])

    # Initialize a default dict
    alpha2_currency = defaultdict(list)

    # Loop though to generate a
    for all_alpha2, currency in zip(*[currency_mappings[c] for c in ['Alpha2', 'CurrencyCode']]):
        if not any(pd.isnull(i) for i in [all_alpha2, currency]):
            for alpha2 in cln(all_alpha2).split(", "):
                if currency.upper() not in alpha2_currency[alpha2.upper()]:
                    alpha2_currency[alpha2.upper()].append(currency.upper())

    # Get currency transitions
    transitions = currency_transitions(path_to_data, date_format=date_format)

    # Add Currency Transitions
    for k, v in alpha2_currency.items():
        if k in transitions:
            for i in ['old', 'new']:
                if not transitions[k][i] in alpha2_currency[k]:
                    alpha2_currency[k].append(transitions[k][i])

    # Sort regions with currency transitions and Return
    return {k: _new_old_order(k, v, transitions) for k, v in alpha2_currency.items()}

























