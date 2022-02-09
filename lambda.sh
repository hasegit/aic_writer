rm -rf ./artifact.zip
poetry build
pip install --upgrade -t package dist/*.whl
cp -p lambda_function.py package/.
(cd package ; zip -r ../artifact.zip . -x '*.pyc')
