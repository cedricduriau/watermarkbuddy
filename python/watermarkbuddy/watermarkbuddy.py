# stdlib modules
import os
import json
import tempfile
import subprocess

try:
    basestring
except NameError:
    basestring = str


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


def _get_stream_data(file_path):
    """
    Gets the video stream data of a file.

    :param file_path: file to read
    :type file_path: str

    :rtype: dict
    """
    args = ["ffprobe",
            "-show_streams",  # display stream information
            "-print_format", "json",  # json string format
            "-v", "quiet",  # ensure no lib data gets printed
            "-hide_banner",  # ensure no banner gets printed
            "-select_streams", "v:0",  # read first video stream
            file_path]
    stdout = _execute_cmd(args)
    src_data = json.loads(stdout)
    return src_data["streams"][0]


def _execute_cmd(args):
    """
    Executes a command in a subprocess.

    :param args: arguments representing the command to execute
    :type args: list

    :raises RuntimeError: if an error occurred during the execution

    :return: stdout of the executed process
    :rtype: str
    """
    proc = subprocess.Popen(args,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    stdout, _ = proc.communicate()
    if proc.returncode != 0:
        msg = stdout.rstrip("\n")
        raise RuntimeError(msg)
    return stdout


# =============================================================================
# public
# =============================================================================
def validate_offset(offset):
    """
    Validates the offset used to determine the overlay.

    :param offset: offset to validate
    :type offset: int

    :raises ValueError: if offset cannot be converted to an int
    """
    try:
        int(offset)
    except ValueError:
        msg = "could not convert offset to integer"
        raise ValueError(msg.format(offset))


def validate_position(position):
    """
    Validates the position used to determine the overlay.

    :param position: position to validate
    :type position: str

    :raises ValueError: if position is not defined in supported list
    """
    valid_values = set(get_positions())
    if position not in valid_values:
        raise ValueError("invalid position {!r}".format(position))


def validate_blend_mode(blend_mode):
    """
    Validates the blend mode to use as video filter.

    :param blend_mode: blend mode to validate
    :type blend_mode: str

    :raises ValueError: if blend mode is not defined in supported list
    """
    blend_modes = set(get_blend_modes())
    if blend_mode not in blend_modes:
        raise ValueError("invalid blend mode {!r}".format(blend_mode))


def validate_ffmpeg():
    """
    Validates ffmpeg is installed.

    :raises RuntimeError: if ffmpeg is not installed
    """
    try:
        _execute_cmd(["ffmpeg", "-version"])
    except RuntimeError:
        raise RuntimeError("ffmpeg not found")


def validate_ffprobe():
    """
    Validates ffprobe is installed.

    :raises RuntimeError: if ffprobe is not installed
    """
    try:
        _execute_cmd(["ffprobe", "-version"])
    except RuntimeError:
        raise RuntimeError("ffprobe not found")


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
    # validate dirs/files exists
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

    # validate values for ffmpeg
    validate_position(position)
    validate_offset(offset_x)
    validate_offset(offset_y)
    validate_blend_mode(blend_mode)

    # set filters template
    fitler_complex = ("[0:v]overlay={overlay}[over];"
                      "[over][0:v]blend=all_mode={blend_mode}")
    fitler_data = {"blend_mode": blend_mode}

    # to delete later
    watermark = watermark_file
    tmp_watermark = None

    if autoscale:
        # create tmp watermark file
        ext = os.path.splitext(watermark_file)[1]
        fp, tmp_watermark = tempfile.mkstemp(suffix=ext)

        # create tmp scaled version of watermark
        stream_data = _get_stream_data(input_file)
        width = stream_data["width"]
        sar = stream_data["sample_aspect_ratio"]
        sar = sar.replace(":", "/")

        tmp_filter = "scale={width}:{height},setsar={sar}"
        tmp_filter = tmp_filter.format(width=width,
                                       height=-1,
                                       sar=sar)

        # build arguments
        args = ["ffmpeg",
                "-hide_banner",
                "-y",
                "-i", watermark_file,
                "-vf", tmp_filter,
                tmp_watermark]
        _execute_cmd(args)
        watermark = tmp_watermark

        # build overlay top-left without offset
        overlay = _get_overlay("top-left", offset_x=0, offset_y=0)
    else:
        # build overlay from position and offset
        overlay = _get_overlay(position, offset_x=offset_x, offset_y=offset_y)

    fitler_data["overlay"] = overlay
    fitler_complex = fitler_complex.format(**fitler_data)

    # build arguments
    args = ["ffmpeg",
            "-hide_banner",  # hide ffmpeg version info
            "-y",  # overwrite output without asking
            "-i", input_file,  # source media
            "-i", watermark,  # watermark
            "-filter_complex", fitler_complex,
            output_file]

    # execute command
    _execute_cmd(args)

    # remove tmp scaled watermark
    if tmp_watermark:
        os.remove(tmp_watermark)
