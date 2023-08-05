==============
Django BigFeat
==============

Django BigFeat is custom field to add up to 63 boolean features using a BigIntegerField.

Quick start
-----------

    from django.db import models
    from bigfeat import BigFeatField

    class ModelWithOptionalFeatures(models.Model):
        FEATURES = {
            'FEATURE_1'  : 0x0000000000000001,
            'FEATURE_2'  : 0x0000000000000002,
            'FEATURE_3'  : 0x0000000000000004,
            'FEATURE_4'  : 0x0000000000000008,
            ...
            'FEATURE_61' : 0x1000000000000000,
            'FEATURE_62' : 0x2000000000000000,
            'FEATURE_63' : 0x4000000000000000,
        }
        features = BigFeatField(masks=FEATURES)

    m = ModelWithOptionalFeatures.objects.get(id=1)
    print m.features.feature_1
    if m.features.feature_2:
        print m.features.feature_3 if m.features.feature_4 else m.features.feature_5
    print m.features

Notes
-----

The most significant bit (0x8000000000000000) cannot be used since
BigIntegerField is stored as a signed integer and will cause an OverflowError


