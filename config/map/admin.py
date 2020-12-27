from django.contrib import admin

# Register your models here.
from .models import YoutubeData, Place, Seoul_detail, detail_route, TourReview

# 아래의 코드를 입력하면 BlogData를 admin 페이지에서 관리할 수 있습니다.
class TourReviewInline(admin.TabularInline):
    model = TourReview 

class SeoulDataInline(admin.TabularInline):
    model = Seoul_detail

class YoutubeDataInline(admin.TabularInline):
    model = YoutubeData

class DeatilRouteInline(admin.TabularInline):
    model = detail_route

class PlaceAdmin(admin.ModelAdmin):
    inlines = [
        YoutubeDataInline,
        SeoulDataInline,
        DeatilRouteInline,
        TourReviewInline
    ]

class Seoul_detailAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(TourReview)
admin.site.register(detail_route)
admin.site.register(Seoul_detail, Seoul_detailAdmin)
admin.site.register(YoutubeData)
admin.site.register(Place, PlaceAdmin)