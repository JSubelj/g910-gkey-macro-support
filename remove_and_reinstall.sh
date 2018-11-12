deactivate
rm -rf venv
rm -rf build
rm -rf dist
rm -rf g910_gkey_macro_support*
python -m venv venv
source venv/bin/activate
python setup.py install
venv/bin/g910-gkeys