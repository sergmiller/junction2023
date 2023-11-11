from django.db import models


class MenuSection(models.Model):
    """
    We want to give a granular access to section in a main menu.
    """

    title = models.CharField("Title", max_length=256)
