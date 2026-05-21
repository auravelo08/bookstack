# Utilisation de l'image de base PHP Apache
FROM php:8.3-apache

# Installation des dépendances système
RUN apt-get update && \
    apt-get install -y \
        git \
        zip \
        unzip \
        libfreetype-dev \
        libjpeg62-turbo-dev \
        libldap2-dev \
        libpng-dev \
        libzip-dev \
        libpq-dev \
        wait-for-it && \
    rm -rf /var/lib/apt/lists/*

# Installation des extensions PHP nécessaires
RUN docker-php-ext-configure ldap --with-libdir="lib/$(gcc -dumpmachine)" && \
    docker-php-ext-configure gd --with-freetype --with-jpeg && \
    docker-php-ext-install -j$(nproc) pdo_pgsql gd ldap zip

# Installation de Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Configuration d'Apache pour pointer vers /app/public
ENV APACHE_DOCUMENT_ROOT=/app/public
RUN a2enmod rewrite && \
    sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf && \
    sed -ri -e 's!/var/www/!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf

# Configuration PHP pour la production
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini" && \
    sed -i 's/memory_limit = 128M/memory_limit = 512M/g' "$PHP_INI_DIR/php.ini"

# Création du répertoire de travail
WORKDIR /app

# Copie du code source dans l'image (cela remplace le volume ./ ./:/app)
COPY . /app

# Installation des dépendances PHP (ignore les dev pour gagner de la place)
RUN composer install --no-dev --no-interaction --optimize-autoloader

# Correction des droits d'accès pour Apache
RUN chown -R www-data:www-data /app && \
    chmod -R 755 /app/storage /app/bootstrap/cache /app/public/uploads

# Configuration du point d'entrée
# Assurez-vous que le script est exécutable
RUN chmod +x /app/dev/docker/entrypoint.app.sh

ENTRYPOINT ["/app/dev/docker/entrypoint.app.sh"]
CMD ["apache2-foreground"]