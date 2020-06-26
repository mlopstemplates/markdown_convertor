FROM marvinbuss/aml-docker:1.7.0

LABEL maintainer="azure/gh-aml"

RUN python -m pip install pybars3

COPY /code /code
ENTRYPOINT ["/code/entrypoint.sh"]
