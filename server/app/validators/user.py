from marshmallow.exceptions import ValidationError
from marshmallow import validates

from app import ma


class NLPSchema(ma.Schema):
    text = ma.String(required=True)

    @validates('text')
    def validate_text(self, text):
        if len(text) == 0 or text == '':
            raise ValidationError(f'text field can not be empty')
        elif type(text).__name__ != 'str':
            raise ValidationError(f'expected a string and not:"{type(text)}')


nlp_validation_schema = NLPSchema()
