from django.db import models

class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)

    access_token = models.CharField(max_length=500)
    expires_in = models.IntegerField()
    expires_at = models.FloatField()
    refresh_token = models.CharField(max_length=500)

    def __str__(self):
        return f"""
            access_token: {self.access_token},
            expires_in: {self.expires_in},
            expires_at: {self.expires_at},
            refresh_token: {self.refresh_token},
        """
