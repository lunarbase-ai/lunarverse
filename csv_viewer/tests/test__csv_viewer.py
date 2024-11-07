from csv_viewer import CsvViewer
import pytest
class TestCsvViewer:
    def setup_method(self):
        self.csv_viewer = CsvViewer()

    def test_simple_csv(self):
        input_text = "col1,col2\nval1,val2\nval3,val4"
        expected_output = "col1,col2\nval1,val2\nval3,val4\n"
        assert self.csv_viewer.run(input_text) == expected_output

    def test_alternative_separator(self):
        self.csv_viewer = CsvViewer(sep=';')
        input_text = "col1;col2\nval1;val2\nval3;val4"
        expected_output = "col1;col2\nval1;val2\nval3;val4\n"
        assert self.csv_viewer.run(input_text) == expected_output

    def test_alternative_lineterminator(self):
        self.csv_viewer = CsvViewer(lineterminator='\r')
        input_text = "col1,col2\rval1,val2\rval3,val4"
        expected_output = "col1,col2\nval1,val2\nval3,val4\n"
        assert self.csv_viewer.run(input_text) == expected_output

    def test_invalid_two_lines_lineterminator(self):
        self.csv_viewer = CsvViewer(lineterminator='\r\n')
        input_text = "col1,col2\r\nval1,val2\r\nval3,val4"
        with pytest.raises(ValueError, match="Only length-1 line terminators supported"):
            self.csv_viewer.run(input_text)

    def test_with_quotes(self):
        input_text = '"col1","col2"\n"val1","val2"\n"val3","val4"'
        expected_output = "col1,col2\nval1,val2\nval3,val4\n"
        assert self.csv_viewer.run(input_text) == expected_output

    def test_with_empty_fields(self):
        input_text = "col1,col2\nval1,\n,val4"
        expected_output = "col1,col2\nval1,\n,val4\n"
        assert self.csv_viewer.run(input_text) == expected_output

    def test_with_whitespace(self):
        input_text = " col1 , col2 \n val1 , val2 \n val3 , val4 "
        expected_output = " col1 , col2 \n val1 , val2 \n val3 , val4 \n"
        assert self.csv_viewer.run(input_text) == expected_output