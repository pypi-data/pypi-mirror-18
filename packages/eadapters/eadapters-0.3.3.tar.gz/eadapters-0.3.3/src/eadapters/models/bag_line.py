#!/usr/bin/python
# -*- coding: utf-8 -*-

import appier

from . import base

class EBagLine(base.EBase):

    quantity = appier.field(
        type = float
    )

    total = appier.field(
        type = float
    )

    size = appier.field(
        type = int
    )

    scale = appier.field(
        type = int
    )

    meta = appier.field(
        type = dict
    )

    meta_j = appier.field()

    product = appier.field(
        type = appier.reference(
            "EProduct",
            name = "id"
        )
    )

    @classmethod
    def _build(cls, model, map):
        super(EBagLine, cls)._build(model, map)

        meta = model.get("meta", {}) or {}
        image_url = meta.get("image_url", None)
        embossing = meta.get("embossing", None)

        if image_url:
            product = model["product"]
            for size in ("thumbnail", "large"):
                size_i = size + "_image"
                image = product[size_i] or {}
                image["url"] = image_url
                product[size_i] = image

        if embossing:
            embossing_s = embossing.replace("_", " ")
            embossing_s = embossing_s.capitalize()
            meta["embossing_s"] = embossing_s
