"""
Script para eliminar tablas VALIDATED_* de SQL Server
=====================================================
Este script elimina todas las tablas creadas por versiones antiguas
del proceso de validación que guardaba datos en SQL Server.

Uso:
    python cleanup_validated_tables.py

Autor: Proyecto Desigualdad Social ETL
Fecha: 2025-11-13
"""

import pyodbc
import sys
import os
# Añadir la ruta base del proyecto al sys.path para importar utils correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config import DB_CONNECTION_STRING


def cleanup_validated_tables():
    """Elimina todas las tablas VALIDATED_* de SQL Server"""
    
    print("="*80)
    print("LIMPIEZA DE TABLAS VALIDATED_*")
    print("="*80)
    
    # Conectar a SQL Server
    try:
        conn = pyodbc.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        print("✅ Conectado a SQL Server\n")
    except Exception as e:
        print(f"❌ Error al conectar a SQL Server: {e}")
        return False
    
    # Listar tablas VALIDATED_* existentes
    cursor.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE' 
          AND TABLE_NAME LIKE 'VALIDATED_%'
        ORDER BY TABLE_NAME
    """)
    
    tables = [row[0] for row in cursor.fetchall()]
    
    if not tables:
        print("ℹ️  No se encontraron tablas VALIDATED_* para eliminar")
        conn.close()
        return True
    
    print(f"📋 Tablas VALIDATED_* encontradas: {len(tables)}\n")
    for i, table in enumerate(tables, 1):
        print(f"   {i}. {table}")
    
    # Confirmar eliminación
    print("\n" + "="*80)
    response = input("⚠️  ¿Confirmas que quieres eliminar estas tablas? (SI/NO): ")
    
    if response.upper() != 'SI':
        print("❌ Operación cancelada por el usuario")
        conn.close()
        return False
    
    # Eliminar tablas
    print("\n" + "="*80)
    print("ELIMINANDO TABLAS")
    print("="*80)
    
    deleted_count = 0
    errors = []
    
    for table in tables:
        try:
            cursor.execute(f"DROP TABLE [{table}]")
            conn.commit()
            print(f"✅ Eliminada: {table}")
            deleted_count += 1
        except Exception as e:
            print(f"❌ Error al eliminar {table}: {e}")
            errors.append((table, str(e)))
    
    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DE LIMPIEZA")
    print("="*80)
    print(f"✅ Tablas eliminadas: {deleted_count}")
    print(f"❌ Errores: {len(errors)}")
    
    if errors:
        print("\n⚠️  Errores encontrados:")
        for table, error in errors:
            print(f"   - {table}: {error}")
    
    # Verificar
    cursor.execute("""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE' 
          AND TABLE_NAME LIKE 'VALIDATED_%'
    """)
    
    remaining = cursor.fetchone()[0]
    
    if remaining == 0:
        print("\n🎉 Limpieza completada exitosamente. No quedan tablas VALIDATED_*")
    else:
        print(f"\n⚠️  Quedan {remaining} tablas VALIDATED_* sin eliminar")
    
    conn.close()
    return True


if __name__ == "__main__":
    cleanup_validated_tables()
