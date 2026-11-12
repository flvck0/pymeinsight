# ADR-001: Monorepo polyglot

**Estado:** Aceptado · **Fecha:** 2026-11-11

## Contexto
PymeInsight combina Java, TypeScript y Python. Los cambios suelen cruzar servicios
(por ejemplo, un campo nuevo en la API que consume la web y el servicio de ML).

## Decisión
Un solo repositorio con una carpeta por servicio y un pipeline de CI por servicio.

## Alternativas
- **Varios repositorios:** más aislamiento, pero cambios coordinados más lentos y un perfil de GitHub disperso.

## Consecuencias
- Un `docker compose up` levanta todo el sistema.
- El CI debe ejecutar solo lo que cambió cuando el repo crezca (filtros por ruta).
