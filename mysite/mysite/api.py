from rest_framework.routers import DefaultRouter
from svs.responses import test, test1, camera_urls
from rest_framework_extensions.routers import NestedRouterMixin


router = DefaultRouter()

class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass

router = NestedDefaultRouter()

camera_router = router.register('camera', test)
test_router = router.register('cameras', camera_urls)
zones_router = router.register('zones', test1)

camera_router.register(
    'zones', test1,
    base_name='camera-zones',
    parents_query_lookups=['origin_camera'])
