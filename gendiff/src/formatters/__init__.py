import gendiff.src.constants as constants
from gendiff.src.formatters.stylish import format_stylish
from gendiff.src.formatters.plain import format_plain
from gendiff.src.formatters.json import format_json

formats_formatters_map = {
    constants.FORMAT_STYLISH: format_stylish,
    constants.FORMAT_PLAIN: format_plain,
    constants.FORMAT_JSON: format_json,
}
