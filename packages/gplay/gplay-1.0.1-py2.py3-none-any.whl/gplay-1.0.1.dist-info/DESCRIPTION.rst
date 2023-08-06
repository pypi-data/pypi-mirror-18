# Google Play CLI

## Install

```
pip install gplay
```

## Usage
```
Interact with Google Play services
Usage:
  gplay.py track active
    (--service-p12=FILE | --service-json=FILE | --oauth-json=FILE | (--oauth --client-id=ID --client-secret=SECRET))
    [--track=TRACK] PACKAGE_NAME
  gplay.py rollout
    (--service-p12=FILE | --service-json=FILE | --oauth-json=FILE | (--oauth --client-id=ID --client-secret=SECRET))
    [--track=TRACK] [--version-code=CODE] PACKAGE_NAME FRACTION
  gplay.py reviews
    (--service-p12=FILE | --service-json=FILE | --oauth-json=FILE | (--oauth --client-id=ID --client-secret=SECRET))
    [--review-id=ID] PACKAGE_NAME
  gplay.py entitlements
    (--service-p12=FILE | --service-json=FILE | --oauth-json=FILE | (--oauth --client-id=ID --client-secret=SECRET))
    PACKAGE_NAME
  gplay.py upload
    (--service-p12=FILE | --service-json=FILE | --oauth-json=FILE | (--oauth --client-id=ID --client-secret=SECRET))
    [--track=TRACK] [--faction=FRACTION] PACKAGE_NAME FILE

Commands:
  track active             get the active version code (defaults to 'production' track)
  rollout                  increase the rollout percentage
  reviews                  get list of reviews
  entitlements             get in app entitlements
  upload                   upload APK (defaults to 'production' track)

Options:
  --service-p12=FILE       uses a p12 file for service account credentials
  --service-json=FILE      uses a json file for service account credentials
  --oauth-json=FILE        uses a client-secret json file for oauth credentials (opens browser)
  --oauth                  uses a client-secret supplied with --client-id and --client-secret (opens browser)
  --client-id=ID
  --client-secret=SECRET

  --track=TRACK            select track (production, beta or alpha)  [default: production]
  --version-code=CODE      app version code to select [default: latest]
  --fraction=FRACTION      the percentage of users that receives this update (0.2 .. 1)

  --review-id=ID           get a single review

```

