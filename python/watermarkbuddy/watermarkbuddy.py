# stdlib modules
import json
import subprocess


# TODO: validate_position
# TODO: validate_offset
# TODO: validate_blend_mode
# TODO: validate_ffmpeg (use -version)
# TODO: validate_ffprobe (use -version)


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

    # TODO: double check return type
    :rtype: tuple(int, int)
    """
    cmd = ["ffprobe",
           "-print_format", "json",
           "-show_streams",
           "-hide_banner",
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
    # TODO: document
    overlay = _get_overlay(position, offset_x=offset_x, offset_y=offset_y)

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

    args = ["ffmpeg",
            "-y",  # overwrite output without asking
            "-i", input_file,  # source media
            "-i", watermark_file,  # watermak
            "-filter_complex", fitlers_complex,
            output_file]
    print(" ".join(args))
    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    stdout, _ = proc.communicate()
    print(stdout)
