import os
import sys


class flight_fare_exception(Exception):

    def __init__(self,error_message:Exception,error_details:sys):
        super().__init__(error_message)
        self.error_message = flight_fare_exemption.get_detailed_error_message(error_message:error_message,
                                                                              error_details:error_details)



     @staticmethod
     def get_detailed_error_message(self,error_message:Exception,error_details:sys) ->str:
        """
        error_message: Exception object
        error_details: sys object
        """
        _,_,exec_tb = error_details.exc_info()
        exception_block_line = exec_tb.tb_frame.f_lineno
        try_block_line = exec_tb.tb_lineno
        file_name = exec_tb.tb_frame.f_code.co_filename
        error_message = f"""
        error occurd in script:
        [{file_name}] at try block line.no: [{try_block_line}] and 
        exception block line.no: [{exception_block_line}]
        error message: [{error_message}]"""

        return error_message

     def __str__(self):
        return self.error_message

    def __repr__(self)->str:
        return flight_fare_exception.__name__.str()
