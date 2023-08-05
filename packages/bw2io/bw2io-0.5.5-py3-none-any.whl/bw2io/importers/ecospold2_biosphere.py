# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from eight import *

from .base_lci import LCIImporter
from ..strategies import drop_unspecified_subcategories, normalize_units
from bw2data.utils import recursive_str_to_unicode
from lxml import objectify
import os
import json

EMISSIONS_CATEGORIES = {
    "air":   "emission",
    "soil":  "emission",
    "water": "emission",
}


class Ecospold2BiosphereImporter(LCIImporter):
    db_name = 'biosphere3'
    format = 'Ecoinvent XML'

    def __init__(self):
        self.data = self.extract()
        self.strategies = [
            normalize_units,
            drop_unspecified_subcategories,
        ]

    def extract(self):
        def extract_flow_data(o):
            ds = {
                'categories': (
                    o.compartment.compartment.text,
                    o.compartment.subcompartment.text
                ),
                'code': o.get('id'),
                'name': o.name.text,
                'database': 'biosphere3',
                'exchanges': [],
                'unit': o.unitName.text,
            }
            ds["type"] = EMISSIONS_CATEGORIES.get(
                ds['categories'][0], ds['categories'][0]
            )
            return ds

        lci_dirpath = os.path.join(os.path.dirname(__file__), "..", "data", "lci")

        fp = os.path.join(lci_dirpath, "ecoinvent elementary flows 3.3.xml")
        root = objectify.parse(open(fp, encoding='utf-8')).getroot()
        flow_data = recursive_str_to_unicode([extract_flow_data(ds)
                                              for ds in root.iterchildren()])

        previous = os.path.join(lci_dirpath, "previous elementary flows.json")
        return flow_data + json.load(open(previous))
