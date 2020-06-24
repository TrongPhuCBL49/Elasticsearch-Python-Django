from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'es_index_name', 'es_type_name', 'es_mapping'
)

class University(models.Model):
    name = models.CharField(max_length=255, unique=True)
class Course(models.Model):
    name = models.CharField(max_length=255, unique=True)
class Student(models.Model):
    YEAR_IN_SCHOOL_CHOICES = (
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
    )
    # note: incorrect choice in MyModel.create leads to creation of incorrect record
    year_in_school = models.CharField(
        max_length=2, choices=YEAR_IN_SCHOOL_CHOICES)
    age = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    # various relationships models
    university = models.ForeignKey(University, null=True, blank=True, on_delete=models.DO_NOTHING)
    courses = models.ManyToManyField(Course, null=True, blank=True)
    class Meta:
        es_index_name = 'django'
        es_type_name = 'student'
        es_mapping = {
            'properties': {
                'university': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'keyword'},
                    }
                },
                'first_name': {'type': 'keyword'},
                'last_name': {'type': 'keyword'},
                'age': {'type': 'short'},
                'year_in_school': {'type': 'text'},
                'name_complete': {
                    'type': 'completion',
                    'analyzer': 'simple',
                    #'payloads': True,
                    'preserve_separators': True,
                    'preserve_position_increments': True,
                    'max_input_length': 50,
                },
                "course_names": {
                    "type": "keyword", "store": True,
                },
            }
        }
    def es_repr(self):
        data = {}
        mapping = self._meta.es_mapping
        data['_id'] = self.pk
        for field_name in mapping['properties'].keys():
            data[field_name] = self.field_es_repr(field_name)
        return data
    def field_es_repr(self, field_name):
        config = self._meta.es_mapping['properties'][field_name]
        if hasattr(self, 'get_es_%s' % field_name):
            field_es_value = getattr(self, 'get_es_%s' % field_name)()
        else:
            if config['type'] == 'object':
                related_object = getattr(self, field_name)
                field_es_value = {}
                field_es_value['_id'] = related_object.pk
                for prop in config['properties'].keys():
                    field_es_value[prop] = getattr(related_object, prop)
            else:
                field_es_value = getattr(self, field_name)
        return field_es_value
    def get_es_name_complete(self):
        return {
            "input": [self.first_name, self.last_name],
            "output": "%s %s" % (self.first_name, self.last_name),
            "payload": {"pk": self.pk},
        }
    def get_es_course_names(self):
        if not self.courses.exists():
            return []
        return [c.name for c in self.courses.all()]
