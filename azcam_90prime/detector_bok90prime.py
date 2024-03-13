###############################################################################
# old mosaic below
###############################################################################

gapX = 118.074  # gaps between amplifiers and CCDs (in pixels)
gapY = 363.978

detector_bok90prime = {
    "name": "bok90prime",
    "description": "90prime mosaic",
    "ref_pixel": [4091.04, 4277.99],
    "format": [4032 * 2, 6, 0, 20, 4096 * 2, 0, 0, 0, 0],
    "focalplane": [2, 2, 4, 4, [3, 2, 1, 0, 3, 2, 1, 0, 0, 1, 2, 3, 0, 1, 2, 3]],
    "roi": [1, 4032 * 2, 1, 4096 * 2, 1, 1],
    "ext_position": [
        [2, 2],
        [1, 2],
        [2, 1],
        [1, 1],
        [4, 2],
        [3, 2],
        [4, 1],
        [3, 1],
        [1, 3],
        [2, 3],
        [1, 4],
        [2, 4],
        [3, 3],
        [4, 3],
        [3, 4],
        [4, 4],
    ],
    "jpg_order": [4, 3, 8, 7, 2, 1, 6, 5, 9, 10, 13, 14, 11, 12, 15, 16],
    "det_number": [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4],
    "det_position": [
        [1, 1],
        [1, 1],
        [1, 1],
        [1, 1],
        [2, 1],
        [2, 1],
        [2, 1],
        [2, 1],
        [1, 2],
        [1, 2],
        [1, 2],
        [1, 2],
        [2, 2],
        [2, 2],
        [2, 2],
        [2, 2],
    ],
    "det_gap": [
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [gapX, 0],
        [gapX, 0],
        [gapX, 0],
        [gapX, 0],
        [0, gapY],
        [0, gapY],
        [0, gapY],
        [0, gapY],
        [gapX, gapY],
        [gapX, gapY],
        [gapX, gapY],
        [gapX, gapY],
    ],
    "ext_name": [
        "im4",
        "im3",
        "im2",
        "im1",
        "im8",
        "im7",
        "im6",
        "im5",
        "im9",
        "im10",
        "im11",
        "im12",
        "im13",
        "im14",
        "im15",
        "im16",
    ],
    "ext_number": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
}

detector_bok90prime_one = {
    "name": "bok90prime_one",
    "description": "90prime mosaic in single chip mode",
    "ref_pixel": [2016.0, 2048.0],
    "format": [4032, 6, 0, 20, 4096, 0, 0, 0, 0],
    "focalplane": [1, 1, 2, 2, [0, 1, 2, 3]],
    "roi": [1, 4032, 1, 4096, 1, 1],
    "ext_position": [[1, 1], [2, 1], [1, 2], [2, 2]],
    "jpg_order": [1, 2, 3, 4],
}

###############################################################################
# new mosaic below
###############################################################################

gapX_new = 2.959 / 0.015  # gaps between amplifiers and CCDs (in pixels)
gapY_new = 1.820 / 0.015

detector_bok90prime_archon = {
    "name": "90prime2",
    "description": "90prime new mosaic",
    "ref_pixel": [4080.0, 4080.0],
    "format": [4080 * 2, 4, 0, 20, 4080 * 2, 0, 0, 0, 0],
    "focalplane": [2, 2, 4, 2, [0, 1, 0, 1, 0, 1, 0, 1]],
    "roi": [1, 4080 * 2, 1, 4080 * 2, 1, 1],
    "jpg_order": [1, 2, 3, 4, 5, 6, 7, 8],
    "det_number": [1, 1, 2, 2, 3, 3, 4, 4],
    "amp_pixel_position": [
        [1, 1],
        [4080, 1],
        [4081, 1],
        [8160, 1],
        [1, 8160],
        [4080, 8160],
        [4081, 8160],
        [8160, 8160],
    ],
    "det_gap": [
        [0, 0],
        [0, 0],
        [gapX_new, 0],
        [gapX_new, 0],
        [0, gapY_new],
        [0, gapY_new],
        [gapX_new, gapY_new],
        [gapX_new, gapY_new],
    ],
    # should change both location
    "det_position": [
        [1, 1],
        [1, 1],
        [2, 1],
        [2, 1],
        [1, 2],
        [1, 2],
        [2, 2],
        [2, 2],
    ],
    "ext_position": [
        [1, 1],
        [2, 1],
        [3, 1],
        [4, 1],
        [1, 2],
        [2, 2],
        [3, 2],
        [4, 2],
    ],
    "ext_name": [
        "im1",
        "im2",
        "im3",
        "im4",
        "im5",
        "im6",
        "im7",
        "im8",
    ],
    "ext_number": [1, 2, 3, 4, 5, 6, 7, 8],
}
