#!/usr/bin/env python3
"""
generate checkerboard and charuco board images for printing.

outputs png files at 300dpi sized to fit us letter paper (8.5x11in).
print at 100% scale, no fit-to-page, to preserve physical dimensions.
"""

import cv2
import cv2.aruco as aruco
import numpy as np

DPI = 300
MARGIN_IN = 0.75
PAPER_W = int(8.5 * DPI)
PAPER_H = int(11.0 * DPI)
USABLE_W = PAPER_W - int(2 * MARGIN_IN * DPI)
USABLE_H = (
    PAPER_H - int(2 * MARGIN_IN * DPI) - int(0.4 * DPI)
)  # room for label

# checkerboard inner corners (opencv counts inner corners, not squares)
CB_INNER_COLS = 5
CB_INNER_ROWS = 8

# charuco squares and dict
CH_COLS = 5
CH_ROWS = 7
CH_DICT = aruco.DICT_6X6_250


def fit_square_size(cols, rows):
    """largest square size in px that fits cols x rows within usable area"""
    return min(USABLE_W // cols, USABLE_H // rows)


def make_canvas():
    return np.ones((PAPER_H, PAPER_W), dtype=np.uint8) * 255


def paste_centered(canvas, img):
    ih, iw = img.shape[:2]
    x = (PAPER_W - iw) // 2
    y = int(MARGIN_IN * DPI) + (USABLE_H - ih) // 2
    canvas[y : y + ih, x : x + iw] = img


def add_label(canvas, text):
    margin_px = int(MARGIN_IN * DPI)
    y = PAPER_H - int(0.3 * DPI)
    cv2.putText(
        canvas,
        text,
        (margin_px, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        0,
        2,
        cv2.LINE_AA,
    )


def make_checkerboard():
    sq_cols = CB_INNER_COLS + 1
    sq_rows = CB_INNER_ROWS + 1
    sq = fit_square_size(sq_cols, sq_rows)
    sq_mm = round(sq / DPI * 25.4, 1)

    board_w = sq_cols * sq
    board_h = sq_rows * sq
    img = np.zeros((board_h, board_w), dtype=np.uint8)
    for r in range(sq_rows):
        for c in range(sq_cols):
            if (r + c) % 2 == 0:
                img[r * sq : (r + 1) * sq, c * sq : (c + 1) * sq] = 255

    canvas = make_canvas()
    paste_centered(canvas, img)
    add_label(
        canvas,
        f"checkerboard  inner corners: {CB_INNER_COLS}x{CB_INNER_ROWS}  square: {sq_mm}mm",
    )
    return canvas


def make_charuco():
    sq = fit_square_size(CH_COLS, CH_ROWS)
    mk = int(sq * 0.75)
    sq_mm = round(sq / DPI * 25.4, 1)
    mk_mm = round(mk / DPI * 25.4, 1)

    dictionary = aruco.getPredefinedDictionary(CH_DICT)
    board = aruco.CharucoBoard((CH_COLS, CH_ROWS), sq, mk, dictionary)
    board_img = board.generateImage((CH_COLS * sq, CH_ROWS * sq))

    canvas = make_canvas()
    paste_centered(canvas, board_img)
    add_label(
        canvas,
        f"charuco  {CH_COLS}x{CH_ROWS}  square: {sq_mm}mm  marker: {mk_mm}mm  DICT_6X6_250",
    )
    return canvas


if __name__ == "__main__":
    cb = make_checkerboard()
    cv2.imwrite("checkerboard.png", cb)
    print(
        f"saved checkerboard.png  (inner corners {CB_INNER_COLS}x{CB_INNER_ROWS})"
    )

    ch = make_charuco()
    cv2.imwrite("charuco_board.png", ch)
    print(f"saved charuco_board.png  ({CH_COLS}x{CH_ROWS} DICT_6X6_250)")

    print("\nprint at 100% scale, no fit-to-page")
