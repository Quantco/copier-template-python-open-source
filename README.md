# copier-template-python-open-source

A copier template for python packages developed at QuantCo using the [pixi](https://github.com/prefix-dev/pixi) package manager.
For documentation on pixi see [here](https://pixi.sh).

## Usage

```bash
pixi exec --spec copier --spec ruamel.yaml -- copier copy --trust https://github.com/quantco/copier-template-python-open-source <destination-path>
```

To update to a newer template version:

```bash
pixi exec --spec copier --spec ruamel.yaml -- copier update --defaults --trust
```

Note that copier will show `Conflict` for files that have manual changes.
This is normal. As long as there are no merge conflict markers in the files all patches applied cleanly.
