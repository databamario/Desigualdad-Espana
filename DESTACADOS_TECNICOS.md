# 🚀 Destacados Técnicos: Pipeline ETL de Desigualdad Social

Este documento resume las decisiones de arquitectura, ingeniería y DevOps implementadas en este proyecto. Está diseñado para ofrecer una visión rápida de la profundidad técnica y las competencias en Ingeniería de Datos aplicadas.

## 1. DevOps y CI/CD Avanzado (GitHub Actions)
El pipeline de Integración Continua no es solo un ejecutor de scripts, sino una pieza de ingeniería robusta diseñada para entornos híbridos.

*   **Matriz de Ejecución Multiplataforma**: 
    > *"Diseñé una matriz de pruebas que aprovisiona explícitamente los drivers ODBC tanto en entornos **Ubuntu** como **Windows Server**, garantizando que el ETL es agnóstico al sistema operativo del despliegue."*
*   **Gestión Inteligente de Secretos**: Implementación de lógica condicional (`if: env.SKIP_DB_LOAD != 'true'`) que detecta automáticamente si el entorno tiene acceso a la base de datos (Prod/Local) o es un entorno volátil (CI), adaptando el flujo de ejecución sin romper el pipeline.
*   **Quality Gates Automatizados**: El código no entra a producción si no pasa los estándares de:
    *   **Black**: Formateo estricto de código (PEP 8).
    *   **Flake8**: Detección de errores lógicos y de estilo.
    *   **MyPy**: Chequeo de tipado estático para prevenir errores en tiempo de ejecución.

## 2. Ingeniería de Datos y Arquitectura ETL
El sistema está construido sobre Python y SQL Server, priorizando la mantenibilidad y la robustez.

*   **Arquitectura Modular**: Separación estricta de responsabilidades (Extract, Transform, Load, Validate). Cada etapa es independiente y testeable.
*   **Conectividad SQL Robusta**: 
    *   Migración a **ODBC Driver 18** para compatibilidad con los últimos estándares de seguridad (Ubuntu 24.04 / OpenSSL 3).
    *   Manejo de cadenas de conexión seguras con soporte para `TrustServerCertificate` y encriptación.
*   **Idempotencia y Recuperación**: Los procesos de carga están diseñados para ser re-ejecutables sin duplicar datos ni generar inconsistencias.

## 3. Framework de Calidad del Dato (Data Quality)
No solo muevo datos, aseguro su fiabilidad mediante un framework de validación personalizado.

*   **Validación Semántica y Estructural**: Scripts automatizados que verifican:
    *   **Integridad de Esquema**: Tipos de datos y columnas esperadas.
    *   **Reglas de Negocio**: Rangos válidos para indicadores (ej. Gini 0-100, Tasas de desempleo).
    *   **Continuidad Temporal**: Detección de huecos (*gaps*) en series temporales anuales.
*   **Reporting de Errores**: Generación de logs detallados que permiten identificar la raíz de los problemas de calidad en origen (INE/Eurostat).

## 4. Valor que Aporto al Equipo
Este proyecto demuestra mi capacidad para:
*   🏗️ **Construir Infraestructura Sólida**: No solo escribo scripts, creo sistemas que sobreviven a cambios de entorno y actualizaciones de dependencias.
*   🛡️ **Priorizar la Calidad**: Automatizo el testing y el linting para que el equipo se centre en la lógica de negocio, no en corregir espacios o imports.
*   🔄 **Automatizar Todo**: Desde la instalación de dependencias del sistema (apt-get/choco) hasta el despliegue y validación de datos.
