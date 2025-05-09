Exportar
mysqldump -u usuario -p biblioteca > biblioteca.sql
importar    
mysqldump -u tu_usuario -p biblioteca < biblioteca.sql

Monitoreo
mysqladmin -u root -p status

Optimización
OPTIMIZE TABLE libros;
Indices
CREATE INDEX idx_titulo ON libros(titulo);