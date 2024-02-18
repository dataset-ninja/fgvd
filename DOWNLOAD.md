Dataset **FGVD** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/D/X/Ww/a1JaYrzHnj7trF7Ot4w1k15u3pebtIrRkVdG1F7DA04tIxda5TxEux6bwaZWmhDankHfoPzySYASJF8gP2AB7gmpVA6AKMimQ0Xi9iA8ymhydiDX1KDK0mJiKUro.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='FGVD', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://zenodo.org/records/7488960/files/IDD_FGVD.tar.gz?download=1).