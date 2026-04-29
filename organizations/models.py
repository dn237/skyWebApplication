from django.db import models

# This model represents the 'Department' entity from the Logical ERD.
# Each department manages teams and is headed by a specific user.
class Department(models.Model):
    # dept_id is handled automatically by Django as a Primary Key (PK).
    
    # dept_name: Unique name of the department (e.g., 'Technology', 'HR').
    # According to the CW1 draft, this field must be NOT NULL and UNIQUE.
    dept_name = models.CharField(
        max_length=100, 
        unique=True, 
        null=False, 
        verbose_name="Department Name"
    )
    
    # head_user: The name of the Department Head.
  
    head_user = models.CharField(
        max_length=100,
        null=False,
        verbose_name="Head of Department"
    )

    # Returns the name of the department when the object is referenced as a string.
    def __str__(self):
        return self.dept_name

    # Metadata for the model to define correct plural names in the admin panel.
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"