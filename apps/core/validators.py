from typing import List

from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.validators import FileExtensionValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileValidator(FileExtensionValidator):

    def __init__(self, allowed_extensions: List = None, max_file_size_mega_bit: int = None,file_type_error_message=None):
        if max_file_size_mega_bit is not None and max_file_size_mega_bit <= 0:
            raise Exception("max_file_size can not be lower than 1")
        self.max_file_size = max_file_size_mega_bit
        super().__init__(allowed_extensions=allowed_extensions,message=file_type_error_message)

    def __call__(self,file:File):
        self.validate_file_size(file)
        super().__call__(file)

    def validate_file_size(self,file:File):
        if self.max_file_size is not None:
            max_file_size = self.max_file_size * 1024 * 1024
            if file.size > max_file_size:
                raise ValidationError(
                      _("File size must not exceed %(max_file_size_in_mb)s MB.") ,
                    params= {
                        "max_file_size_in_mb": f"{self.max_file_size}"
                    }
                )
