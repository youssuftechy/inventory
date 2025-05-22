FROM python:3.10.12-alpine

WORKDIR /sales-and-inventory-management

# Install system dependencies for WeasyPrint and build tools
RUN apk add --no-cache \
    build-base \
    libffi-dev \
    cairo-dev \
    pango-dev \
    gdk-pixbuf-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-turbo-dev \
    zlib-dev \
    gobject-introspection-dev \
    py3-cffi \
    py3-pillow

COPY . /sales-and-inventory-management

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
