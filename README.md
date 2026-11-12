# PymeInsight

Plataforma de inventario y ventas para PYMEs chilenas, con predicción de demanda
y asistente de IA. Monorepo con varias tecnologías, construido por fases.

## Arquitectura

| Carpeta | Tecnología | Estado |
|---|---|---|
| `services/core-api` | Spring Boot 3, Java 21, PostgreSQL, Flyway | Fase 1 |
| `web` | React, Vite, TypeScript | Fase 1 |
| `services/ml-service` | FastAPI, scikit-learn, TensorFlow | Fase 2 |
| MongoDB (eventos y conversaciones) | MongoDB | Fase 2 |
| `infra/k8s` | Kubernetes, AWS | Fase 3 |
| `.github/workflows` | GitHub Actions (CI) | Fase 1 |

Decisiones de arquitectura en [`docs/adr`](docs/adr).

## Ejecutar con Docker

```bash
cp .env.example .env
docker compose up --build
```

- Web: http://localhost:5173
- API: http://localhost:8080/api/products
- Salud: http://localhost:8080/actuator/health

## Desarrollo local

```bash
# Base de datos
docker compose up db

# API (requiere Java 21 y Maven)
cd services/core-api && mvn spring-boot:run

# Web
cd web && npm install && npm run dev
```

## Endpoints de la Fase 1

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/products` | Lista productos |
| GET | `/api/products/low-stock` | Productos con stock bajo el mínimo |
| POST | `/api/products` | Crea un producto |
| PUT | `/api/products/{id}` | Actualiza un producto |
| DELETE | `/api/products/{id}` | Elimina un producto |
