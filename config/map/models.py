from django.db import models

# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=50)
    # 메인에 담을
    formainlat = models.CharField(max_length=25, blank=True)
    formainlng = models.CharField(max_length=25, blank=True)

    lat = models.CharField(max_length=25)
    lng = models.CharField(max_length=25)
    gu = models.CharField(max_length=25,default=1)

    image = models.URLField(blank=True)
    description = models.CharField(blank=True,max_length=100)

    trip_url = models.URLField(blank=True)

    def __str__(self):
        return str(self.name) if self.name else ''

class Seoul_detail(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=125)
    url = models.URLField(blank=True)
    photo = models.ImageField(blank=True)
    marker_thum = models.ImageField(blank=True)


    lat = models.CharField(max_length=30)
    lng = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class detail_route(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True)
    lat = models.CharField(max_length=30)
    lng = models.CharField(max_length=30)

    def __str__(self):
        return self.place.name


class My_position(models.Model):
    lat = models.CharField(max_length=25)
    lng = models.CharField(max_length=25)

    def __str__(self):
        return self.id


class YoutubeData(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null=True, related_name='place')
    title = models.CharField(max_length=200)
    link = models.URLField(blank=True)
    thumb = models.ImageField(blank=True)

    def __str__(self):
        return self.title

class TourReview(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, null = True)
    info_title = models.TextField(max_length= 200)
    info = models.TextField(max_length = 2500)
    score = models.IntegerField(default=0)
    visit_date = models.CharField(max_length = 20)

    def __str__(self):
        return self.place.name