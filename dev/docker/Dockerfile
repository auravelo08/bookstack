FROM php:8.3-apache

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        git \
        zip \
        unzip \
        curl \
        npm \
        libfreetype-dev \
        libjpeg62-turbo-dev \
        libldap2-dev \
        libpng-dev \
        libzip-dev \
        wait-for-it && \
    rm -rf /var/lib/apt/lists/*

# Install PHP extensions
RUN docker-php-ext-configure ldap --with-libdir="lib/$(gcc -dumpmachine)" && \
    docker-php-ext-configure gd --with-freetype --with-jpeg && \
    docker-php-ext-install -j$(nproc) pdo_mysql gd ldap zip

# Install composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

ENV APACHE_DOCUMENT_ROOT="/app/public"
WORKDIR /app

# Copy dependency files first (cache-friendly)
COPY composer.json composer.lock package.json package-lock.json /app/

# Install PHP dependencies
RUN composer install --no-dev --optimize-autoloader

# Install JS dependencies
RUN npm install

# Copy the rest of the application
COPY --chown=www-data:www-data . /app

# Build frontend assets
RUN npm run build

# Configure Apache
RUN a2enmod rewrite && \
    sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf && \
    sed -ri -e 's!/var/www/!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf

# Allow access to /app/public
RUN echo "<Directory /app/public>\n\
    AllowOverride All\n\
    Require all granted\n\
</Directory>" > /etc/apache2/conf-available/bookstack.conf \
    && a2enconf bookstack

# Fix writable directories only
RUN chown -R www-data:www-data /app/storage /app/bootstrap/cache
