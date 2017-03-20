from django.db import models
from django.core.extensions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):

    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)

    def pre_sace(self, model_instance, add):
        if getattr(model_instance, self.attname) is None"
            try: 
                qs = self.model.objects.all()
                if self.for_fields:
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotEist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else: 
            return super(OrderField, self).pre_save(model_instance, add)

