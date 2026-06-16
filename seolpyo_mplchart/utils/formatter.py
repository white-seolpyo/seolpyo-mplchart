from .num import num_to_str, unit_data, unit_data_en, unit_info_data, unit_info_data_en


class Formatter:
    price_word = '원'
    volume_word = '주'

    unit_data = unit_data
    unit_info_data = unit_info_data

    def price_formatter(self, x, pos, /):
        return num_to_str(x, pos=pos, word=self.price_word, unit_data=self.unit_data)

    def volume_formatter(self, x, pos, /):
        return num_to_str(x, pos=pos, word=self.volume_word, unit_data=self.unit_data)

    def info_price_formatter(self, x, pos, /):
        return num_to_str(x, pos=pos, word=self.price_word, unit_data=self.unit_info_data)

    def info_volume_formatter(self, x, pos, /):
        return num_to_str(x, pos=pos, word=self.volume_word, unit_data=self.unit_info_data)


class FormatterEN(Formatter):
    price_word = '$'
    volume_word = ' Vol.'

    unit_data = unit_data_en
    unit_info_data = unit_info_data_en

FORMATTER = Formatter()
FORMATTER_EN = FormatterEN()

