Dataset **FGVD** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzM1MjFfRkdWRC9mZ3ZkLURhdGFzZXROaW5qYS50YXIiLCAic2lnIjogIjFXYXpEMHF2MjcyZloxQWxnWjltZnRjQU1QK0ViOTh0cGtqb3BCNGw5UW89In0=)

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