import gendiff.src.constants as constants
from gendiff.src.formatters.stylish import stylish
from gendiff.src.formatters.plain import plain

formats_formatters_map = {
    constants.FORMAT_STYLISH: stylish,
    constants.FORMAT_PLAIN: plain,
}
