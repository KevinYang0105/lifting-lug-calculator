"""Shared material and allowable-stress constants."""

MATERIAL_DB = {
    "Q355B": {"fy": 355, "fu": 470},
    "Q235B": {"fy": 235, "fu": 370},
    "Q420B": {"fy": 420, "fu": 520},
    "SS400": {"fy": 245, "fu": 400},
    "自定义": {"fy": 355, "fu": 470},
}

ALLOWABLE_RULES = {
    "tensile": {
        "label": "[σ_t] = Fy / Ns",
        "compute": lambda fy, fu, ns: fy / ns,
    },
    "tear_out": {
        "label": "[τ_v] = 0.58 × Fy / Ns",
        "compute": lambda fy, fu, ns: (0.58 * fy) / ns,
    },
    "bearing": {
        "label": "[σ_b] = 1.25 × Fy / Ns",
        "compute": lambda fy, fu, ns: (1.25 * fy) / ns,
    },
    "weld": {
        "label": "[τ_w] = 0.3 × Fu",
        "compute": lambda fy, fu, ns: 0.3 * fu,
    },
}
