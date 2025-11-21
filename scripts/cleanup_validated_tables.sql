-- ============================================================================
-- Script para Eliminar Tablas VALIDATED_* de SQL Server
-- ============================================================================
-- Este script elimina todas las tablas que empiezan con 'VALIDATED_'
-- creadas por versiones anteriores del proceso de validación.
--
-- IMPORTANTE: Ejecutar SOLO si estás seguro de que quieres eliminar estas tablas.
-- ============================================================================

-- Declarar variables
DECLARE @TableName NVARCHAR(255)
DECLARE @SQL NVARCHAR(MAX)

-- Crear cursor para recorrer todas las tablas VALIDATED_*
DECLARE table_cursor CURSOR FOR
SELECT TABLE_NAME 
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE' 
  AND TABLE_NAME LIKE 'VALIDATED_%'
ORDER BY TABLE_NAME

-- Abrir cursor
OPEN table_cursor

-- Leer primera tabla
FETCH NEXT FROM table_cursor INTO @TableName

-- Recorrer todas las tablas
WHILE @@FETCH_STATUS = 0
BEGIN
    -- Generar comando DROP TABLE
    SET @SQL = 'DROP TABLE [' + @TableName + ']'
    
    -- Imprimir comando (para auditoría)
    PRINT 'Eliminando tabla: ' + @TableName
    
    -- Ejecutar comando
    EXEC sp_executesql @SQL
    
    -- Leer siguiente tabla
    FETCH NEXT FROM table_cursor INTO @TableName
END

-- Cerrar y liberar cursor
CLOSE table_cursor
DEALLOCATE table_cursor

-- Verificar que se eliminaron todas
PRINT ''
PRINT '============================================================================'
PRINT 'RESUMEN DE ELIMINACIÓN'
PRINT '============================================================================'

SELECT COUNT(*) AS 'Tablas VALIDATED_ restantes'
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE' 
  AND TABLE_NAME LIKE 'VALIDATED_%'

PRINT '============================================================================'
PRINT 'Proceso completado.'
PRINT '============================================================================'
