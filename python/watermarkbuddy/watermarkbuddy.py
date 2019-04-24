# stdlib modules
import os
import json
import subprocess

try:
    basestring
except NameError:
    basestring = str


# TODO: validate_ffmpeg (use -version)
# TODO: validate_ffprobe (use -version)
# TODO: auto scale issue when in PAR does not match out PAR


# =============================================================================
# private
# =============================================================================
def _get_overlay(position, offset_x, offset_y):
    """
    Builds the ffmpeg overlay syntax from position and axis offset.

    :rtype: str
    """
    # top-left:     x=offset:y=offset
    # top-right:    x=W-w-offset:y=offset
    # bottom-left:  x=offset:H-h-offset
    # bottom-right: x=W-w-offset:y=H-h-offset
    if position == "top-left":
        overlay = "x={offset_x}:y={offset_y}"
    elif position == "top-right":
        overlay = "x=W-w-{offset_x}:y={offset_y}"
    elif position == "bottom-left":
        overlay = "x={offset_x}:H-h-{offset_y}"
    elif position == "bottom-right":
        overlay = "x=W-w-{offset_x}:y=H-h-{offset_y}"
    return overlay.format(offset_x=offset_x, offset_y=offset_y)


# =============================================================================
# public
# =============================================================================
def validate_offset(offset):
    try:
        int(offset)
    except Exception as e:
        msg = "could not convert offset to integer"
        raise ValueError(msg.format(offset))


def validate_position(position):
    valid_values = set(get_positions())
    if position not in valid_values:
        raise ValueError("invalid position {!r}".format(position))


def validate_blend_mode(blend_mode):
    blend_modes = set(get_blend_modes())
    if blend_mode not in blend_modes:
        raise ValueError("invalid blend mode {!r}".format(blend_mode))


def get_blend_modes():
    """
    Returns the ffmpeg supported blend modes.

    More details: https://ffmpeg.org/ffmpeg-filters.html#blend_002c-tblend

    :rtype: list[str]
    """
    return ["addition",
            "grainmerge",
            "and",
            "average",
            "burn",
            "darken",
            "difference",
            "grainextract",
            "divide",
            "dodge",
            "freeze",
            "exclusion",
            "extremity",
            "glow",
            "hardlight",
            "hardmix",
            "heat",
            "lighten",
            "linearlight",
            "multiply",
            "multiply128",
            "negation",
            "normal",
            "or",
            "overlay",
            "phoenix",
            "pinlight",
            "reflect",
            "screen",
            "softlight",
            "subtract",
            "vividlight",
            "xor"]


def get_positions():
    """
    Returns the supported positions for the watermark placement.

    :rtype: list[str]
    """
    return ["top-left", "top-right", "bottom-left", "bottom-right"]


def get_resolution(input_file):
    """
    Gets the resolution of a file using ffprobe.

    :rtype: tuple(int, int)
    """
    cmd = ["ffprobe",
           "-show_streams",
           "-print_format", "json",
           "-v", "quiet",  # ensure no lib data gets printed
           "-hide_banner",  # ensure no banner gets printed
           "-select_streams", "v:0",
           input_file]
    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    stdout, _ = process.communicate()
    src_data = json.loads(stdout)
    video_data = src_data["streams"][0]
    return video_data["width"], video_data["height"]


def add_watermark(input_file,
                  watermark_file,
                  output_file,
                  autoscale=False,
                  position="top-left",
                  offset_x=0,
                  offset_y=0,
                  blend_mode="normal"):
    """
    Add a watermark to a file.

    :param input_file: file to add watermark to
    :type input_file: str

    :param watermark_file: file to use as watermark
    :type watermark_file: str

    :param output_file: output file path
    :type output_file: str

    :param autoscale: set True to resize watermark to input file
    :type autoscale: bool

    :param position: initial position of the watermark
    :type position: str

    :param offset_x: X-axis offset of the watermark
    :type offset_x: int

    :param offset_y: Y-axis offset of the watermark
    :type offset_y: int

    :param blend_mode: video filter to apply watermark with
    :type blend_mode: str
    """
    if not os.path.exists(input_file):
        msg = "input file does not exist: {}"
        raise ValueError(msg.format(input_file))

    if not os.path.exists(watermark_file):
        msg = "watermark file does not exist: {}"
        raise ValueError(msg.format(watermark_file))

    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        msg = "output directory does not exist: {}"
        raise ValueError(msg.format(output_dir))

    validate_position(position)
    validate_offset(offset_x)
    validate_offset(offset_y)
    validate_blend_mode(blend_mode)

    # get overlay from position and offset
    overlay = _get_overlay(position, offset_x=offset_x, offset_y=offset_y)

    # build complex filters
    format_data = {"overlay": overlay, "blend_mode": blend_mode}
    if autoscale:
        src_width, _src_height = get_resolution(input_file)
        fitlers_complex = ("[1:v]scale=w={width}:h=-1[wm_scaled];"
                           "[wm_scaled][0:v]overlay={overlay}[wm_moved];"
                           "[wm_moved][0:v]blend=all_mode={blend_mode}")
        format_data["width"] = src_width
    else:
        fitlers_complex = ("[0:v]overlay={overlay}[wm_moved];"
                           "[wm_moved][0:v]blend=all_mode={blend_mode}")
    fitlers_complex = fitlers_complex.format(**format_data)

    # build arguments
    args = ["ffmpeg",
            "-y",  # overwrite output without asking
            "-i", input_file,  # source media
            "-i", watermark_file,  # watermark
            "-filter_complex", fitlers_complex,
            output_file]

    # execute command
    print(" ".join(args))
    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    stdout, _ = proc.communicate()
    print(stdout)
