from django.db import models


# Create your models here.
class Lender(models.Model):
  id = models.AutoField(
    primary_key=True
  )
  name = models.TextField()

  code = models.TextField()

  upfront_comm_rate = models.DecimalField(max_digits= 5, decimal_places= 2)

  trail_comm_rate = models.DecimalField(max_digits= 5, decimal_places= 2)

  is_active = models.BooleanField()

  class Meta:
    db_table = 'Lender'




