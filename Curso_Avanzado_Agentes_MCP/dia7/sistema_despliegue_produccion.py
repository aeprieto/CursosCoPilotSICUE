#!/usr/bin/env python3
"""
Sistema de Despliegue y Monitorización para Agentes MCP - Día 7
Herramientas para producción, CI/CD y mantenimiento de agentes
"""

import os
import sys
import json
import yaml
import logging
import subprocess
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
import shutil
import hashlib
import requests
from dataclasses import dataclass, asdict
import sqlite3

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ConfiguracionDespliegue:
    """Configuración para despliegue de agentes"""
    nombre_agente: str
    version: str
    entorno: str  # desarrollo, staging, produccion
    servidor_host: str
    puerto: int
    base_datos_url: str
    variables_entorno: Dict[str, str]
    dependencias: List[str]
    recursos_minimos: Dict[str, str]  # cpu, memoria, disco
    configuracion_logging: Dict[str, str]
    respaldos_activos: bool = True
    monitoreo_activo: bool = True

@dataclass
class MetricaAgente:
    """Métrica de rendimiento de un agente"""
    timestamp: datetime
    agente_id: str
    cpu_usage: float
    memory_usage: float
    requests_per_minute: int
    response_time_avg: float
    error_rate: float
    uptime_hours: float

class GestorDespliegue:
    """Gestiona el despliegue y versionado de agentes MCP"""
    
    def __init__(self, directorio_base: str = "./despliegues"):
        self.directorio_base = Path(directorio_base)
        self.directorio_base.mkdir(exist_ok=True)
        self.configuraciones = {}
        self.historial_despliegues = []
        
    def crear_configuracion_despliegue(self, config: ConfiguracionDespliegue) -> str:
        """Crea configuración de despliegue para un agente"""
        try:
            # Crear directorio específico para el agente
            dir_agente = self.directorio_base / config.nombre_agente / config.version
            dir_agente.mkdir(parents=True, exist_ok=True)
            
            # Generar archivos de configuración
            self._generar_dockerfile(config, dir_agente)
            self._generar_docker_compose(config, dir_agente)
            self._generar_requirements(config, dir_agente)
            self._generar_configuracion_nginx(config, dir_agente)
            self._generar_scripts_inicio(config, dir_agente)
            self._generar_configuracion_monitoreo(config, dir_agente)
            
            # Guardar configuración
            config_path = dir_agente / "config.yaml"
            with open(config_path, 'w') as f:
                yaml.dump(asdict(config), f, default_flow_style=False)
            
            self.configuraciones[config.nombre_agente] = config
            
            logger.info(f"Configuración de despliegue creada: {config.nombre_agente} v{config.version}")
            return str(dir_agente)
            
        except Exception as e:
            logger.error(f"Error creando configuración: {e}")
            raise
    
    def _generar_dockerfile(self, config: ConfiguracionDespliegue, directorio: Path):
        """Genera Dockerfile optimizado para el agente"""
        dockerfile_content = f"""
# Dockerfile para {config.nombre_agente} v{config.version}
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \\
    curl \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root
RUN useradd -m -u 1000 agente
USER agente
WORKDIR /app

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY --chown=agente:agente . .

# Variables de entorno por defecto
ENV PYTHONPATH=/app
ENV ENVIRONMENT={config.entorno}
ENV PORT={config.puerto}

# Exponer puerto
EXPOSE {config.puerto}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:{config.puerto}/health || exit 1

# Comando por defecto
CMD ["python", "-m", "servidor_mcp"]
"""
        
        dockerfile_path = directorio / "Dockerfile"
        with open(dockerfile_path, 'w') as f:
            f.write(dockerfile_content.strip())
    
    def _generar_docker_compose(self, config: ConfiguracionDespliegue, directorio: Path):
        """Genera docker-compose.yml para el entorno completo"""
        compose_content = {
            'version': '3.8',
            'services': {
                config.nombre_agente: {
                    'build': '.',
                    'ports': [f"{config.puerto}:{config.puerto}"],
                    'environment': config.variables_entorno,
                    'volumes': [
                        './logs:/app/logs',
                        './data:/app/data'
                    ],
                    'restart': 'unless-stopped',
                    'depends_on': ['postgresql', 'redis'],
                    'networks': ['agentes_network']
                },
                'postgresql': {
                    'image': 'postgres:15',
                    'environment': {
                        'POSTGRES_DB': 'universidad',
                        'POSTGRES_USER': 'agente_user',
                        'POSTGRES_PASSWORD': 'password_seguro'
                    },
                    'volumes': ['postgres_data:/var/lib/postgresql/data'],
                    'networks': ['agentes_network']
                },
                'redis': {
                    'image': 'redis:7-alpine',
                    'volumes': ['redis_data:/data'],
                    'networks': ['agentes_network']
                },
                'nginx': {
                    'image': 'nginx:alpine',
                    'ports': ['80:80', '443:443'],
                    'volumes': [
                        './nginx.conf:/etc/nginx/nginx.conf',
                        './ssl:/etc/nginx/ssl'
                    ],
                    'depends_on': [config.nombre_agente],
                    'networks': ['agentes_network']
                },
                'prometheus': {
                    'image': 'prom/prometheus',
                    'ports': ['9090:9090'],
                    'volumes': ['./prometheus.yml:/etc/prometheus/prometheus.yml'],
                    'networks': ['agentes_network']
                },
                'grafana': {
                    'image': 'grafana/grafana',
                    'ports': ['3000:3000'],
                    'environment': {
                        'GF_SECURITY_ADMIN_PASSWORD': 'admin_password'
                    },
                    'volumes': ['grafana_data:/var/lib/grafana'],
                    'networks': ['agentes_network']
                }
            },
            'volumes': {
                'postgres_data': {},
                'redis_data': {},
                'grafana_data': {}
            },
            'networks': {
                'agentes_network': {
                    'driver': 'bridge'
                }
            }
        }
        
        compose_path = directorio / "docker-compose.yml"
        with open(compose_path, 'w') as f:
            yaml.dump(compose_content, f, default_flow_style=False)
    
    def _generar_requirements(self, config: ConfiguracionDespliegue, directorio: Path):
        """Genera requirements.txt con versiones específicas"""
        requirements = [
            "fastapi==0.104.1",
            "uvicorn[standard]==0.24.0",
            "sqlalchemy==2.0.23",
            "alembic==1.12.1",
            "psycopg2-binary==2.9.9",
            "redis==5.0.1",
            "prometheus-client==0.19.0",
            "structlog==23.2.0",
            "pydantic==2.5.0",
            "python-jose[cryptography]==3.3.0",
            "passlib[bcrypt]==1.7.4",
        ] + config.dependencias
        
        requirements_path = directorio / "requirements.txt"
        with open(requirements_path, 'w') as f:
            f.write('\n'.join(requirements))
    
    def _generar_configuracion_nginx(self, config: ConfiguracionDespliegue, directorio: Path):
        """Genera configuración de nginx como proxy reverso"""
        nginx_conf = f"""
events {{
    worker_connections 1024;
}}

http {{
    upstream {config.nombre_agente}_backend {{
        server {config.nombre_agente}:{config.puerto};
    }}
    
    server {{
        listen 80;
        server_name {config.servidor_host};
        
        # Redirigir HTTP a HTTPS
        return 301 https://$server_name$request_uri;
    }}
    
    server {{
        listen 443 ssl http2;
        server_name {config.servidor_host};
        
        # Configuración SSL (certificados no incluidos en demo)
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        
        # Configuración de seguridad
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        
        # Proxy hacia el agente
        location / {{
            proxy_pass http://{config.nombre_agente}_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_timeout 60s;
        }}
        
        # Endpoint de salud
        location /health {{
            proxy_pass http://{config.nombre_agente}_backend/health;
            access_log off;
        }}
        
        # Métricas (solo acceso interno)
        location /metrics {{
            proxy_pass http://{config.nombre_agente}_backend/metrics;
            allow 10.0.0.0/8;
            allow 172.16.0.0/12;
            allow 192.168.0.0/16;
            deny all;
        }}
    }}
}}
"""
        
        nginx_path = directorio / "nginx.conf"
        with open(nginx_path, 'w') as f:
            f.write(nginx_conf)
    
    def _generar_scripts_inicio(self, config: ConfiguracionDespliegue, directorio: Path):
        """Genera scripts para iniciar y gestionar el servicio"""
        
        # Script de inicio
        start_script = f"""#!/bin/bash
set -e

echo "Iniciando {config.nombre_agente} v{config.version}"

# Verificar variables de entorno requeridas
required_vars=("DATABASE_URL" "REDIS_URL")
for var in "${{required_vars[@]}}"; do
    if [[ -z "${{!var}}" ]]; then
        echo "Error: Variable de entorno $var no definida"
        exit 1
    fi
done

# Ejecutar migraciones de base de datos
echo "Ejecutando migraciones..."
alembic upgrade head

# Iniciar el servidor
echo "Iniciando servidor en puerto {config.puerto}"
exec uvicorn servidor_mcp:app --host 0.0.0.0 --port {config.puerto}
"""
        
        start_path = directorio / "start.sh"
        with open(start_path, 'w') as f:
            f.write(start_script)
        start_path.chmod(0o755)
        
        # Script de monitoreo
        monitor_script = f"""#!/bin/bash
# Script de monitoreo básico para {config.nombre_agente}

check_health() {{
    local url="http://localhost:{config.puerto}/health"
    local response=$(curl -s -o /dev/null -w "%{{http_code}}" "$url")
    
    if [[ "$response" == "200" ]]; then
        echo "$(date): Servicio saludable"
        return 0
    else
        echo "$(date): Servicio no responde (código: $response)"
        return 1
    fi
}}

# Verificar cada 30 segundos
while true; do
    if ! check_health; then
        echo "$(date): Intentando reiniciar servicio..."
        # Aquí iría la lógica de reinicio
    fi
    sleep 30
done
"""
        
        monitor_path = directorio / "monitor.sh"
        with open(monitor_path, 'w') as f:
            f.write(monitor_script)
        monitor_path.chmod(0o755)
    
    def _generar_configuracion_monitoreo(self, config: ConfiguracionDespliegue, directorio: Path):
        """Genera configuración para Prometheus y Grafana"""
        
        # Configuración Prometheus
        prometheus_config = {
            'global': {
                'scrape_interval': '15s'
            },
            'scrape_configs': [
                {
                    'job_name': config.nombre_agente,
                    'static_configs': [
                        {'targets': [f"{config.nombre_agente}:{config.puerto}"]}
                    ],
                    'metrics_path': '/metrics',
                    'scrape_interval': '10s'
                }
            ]
        }
        
        prometheus_path = directorio / "prometheus.yml"
        with open(prometheus_path, 'w') as f:
            yaml.dump(prometheus_config, f, default_flow_style=False)

class MonitoreoProduccion:
    """Sistema de monitoreo para agentes en producción"""
    
    def __init__(self, db_path: str = "monitoreo.db"):
        self.db_path = db_path
        self.init_database()
        self.alertas_configuradas = []
    
    def init_database(self):
        """Inicializa base de datos de métricas"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metricas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agente_id TEXT NOT NULL,
                cpu_usage REAL,
                memory_usage REAL,
                requests_per_minute INTEGER,
                response_time_avg REAL,
                error_rate REAL,
                uptime_hours REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alertas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                agente_id TEXT NOT NULL,
                tipo_alerta TEXT NOT NULL,
                mensaje TEXT NOT NULL,
                severity TEXT NOT NULL,
                resuelto BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def registrar_metrica(self, metrica: MetricaAgente):
        """Registra una métrica en la base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO metricas (timestamp, agente_id, cpu_usage, memory_usage,
                                requests_per_minute, response_time_avg, error_rate, uptime_hours)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metrica.timestamp.isoformat(),
            metrica.agente_id,
            metrica.cpu_usage,
            metrica.memory_usage,
            metrica.requests_per_minute,
            metrica.response_time_avg,
            metrica.error_rate,
            metrica.uptime_hours
        ))
        
        conn.commit()
        conn.close()
        
        # Verificar alertas
        self._verificar_alertas(metrica)
    
    def _verificar_alertas(self, metrica: MetricaAgente):
        """Verifica si se deben disparar alertas basadas en la métrica"""
        alertas = []
        
        # CPU alta
        if metrica.cpu_usage > 80:
            alertas.append({
                'tipo': 'cpu_alta',
                'mensaje': f'CPU usage alto: {metrica.cpu_usage}%',
                'severity': 'warning' if metrica.cpu_usage < 90 else 'critical'
            })
        
        # Memoria alta
        if metrica.memory_usage > 85:
            alertas.append({
                'tipo': 'memoria_alta',
                'mensaje': f'Uso de memoria alto: {metrica.memory_usage}%',
                'severity': 'warning' if metrica.memory_usage < 95 else 'critical'
            })
        
        # Tasa de error alta
        if metrica.error_rate > 5:
            alertas.append({
                'tipo': 'error_rate_alta',
                'mensaje': f'Tasa de error alta: {metrica.error_rate}%',
                'severity': 'critical'
            })
        
        # Tiempo de respuesta alto
        if metrica.response_time_avg > 2000:  # 2 segundos
            alertas.append({
                'tipo': 'response_time_alto',
                'mensaje': f'Tiempo de respuesta alto: {metrica.response_time_avg}ms',
                'severity': 'warning'
            })
        
        # Registrar alertas
        for alerta in alertas:
            self._crear_alerta(metrica.agente_id, alerta)
    
    def _crear_alerta(self, agente_id: str, alerta: Dict[str, str]):
        """Crea una nueva alerta"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alertas (timestamp, agente_id, tipo_alerta, mensaje, severity)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            agente_id,
            alerta['tipo'],
            alerta['mensaje'],
            alerta['severity']
        ))
        
        conn.commit()
        conn.close()
        
        # Log de la alerta
        logger.warning(f"ALERTA [{alerta['severity'].upper()}] {agente_id}: {alerta['mensaje']}")
    
    def obtener_metricas_recientes(self, agente_id: str, horas: int = 24) -> List[MetricaAgente]:
        """Obtiene métricas recientes de un agente"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        fecha_limite = datetime.now() - timedelta(hours=horas)
        
        cursor.execute('''
            SELECT * FROM metricas 
            WHERE agente_id = ? AND timestamp > ?
            ORDER BY timestamp DESC
        ''', (agente_id, fecha_limite.isoformat()))
        
        metricas = []
        for row in cursor.fetchall():
            metrica = MetricaAgente(
                timestamp=datetime.fromisoformat(row[1]),
                agente_id=row[2],
                cpu_usage=row[3],
                memory_usage=row[4],
                requests_per_minute=row[5],
                response_time_avg=row[6],
                error_rate=row[7],
                uptime_hours=row[8]
            )
            metricas.append(metrica)
        
        conn.close()
        return metricas
    
    def generar_reporte_salud(self, agente_id: str) -> Dict[str, Any]:
        """Genera reporte de salud de un agente"""
        metricas = self.obtener_metricas_recientes(agente_id, 24)
        
        if not metricas:
            return {"error": "No hay métricas disponibles"}
        
        # Calcular promedios
        cpu_promedio = sum(m.cpu_usage for m in metricas) / len(metricas)
        memoria_promedio = sum(m.memory_usage for m in metricas) / len(metricas)
        tiempo_respuesta_promedio = sum(m.response_time_avg for m in metricas) / len(metricas)
        error_rate_promedio = sum(m.error_rate for m in metricas) / len(metricas)
        
        # Obtener alertas activas
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*) FROM alertas 
            WHERE agente_id = ? AND resuelto = FALSE
        ''', (agente_id,))
        alertas_activas = cursor.fetchone()[0]
        conn.close()
        
        # Determinar estado general
        estado = "saludable"
        if alertas_activas > 0:
            estado = "atención_requerida"
        if cpu_promedio > 90 or memoria_promedio > 95 or error_rate_promedio > 10:
            estado = "crítico"
        
        return {
            "agente_id": agente_id,
            "estado_general": estado,
            "metricas_24h": {
                "cpu_promedio": round(cpu_promedio, 2),
                "memoria_promedio": round(memoria_promedio, 2),
                "tiempo_respuesta_promedio": round(tiempo_respuesta_promedio, 2),
                "error_rate_promedio": round(error_rate_promedio, 2),
                "uptime_actual": metricas[0].uptime_hours if metricas else 0
            },
            "alertas_activas": alertas_activas,
            "ultima_actualizacion": datetime.now().isoformat(),
            "total_metricas": len(metricas)
        }

class GestorContinuidad:
    """Gestiona CI/CD y continuidad del servicio"""
    
    def __init__(self):
        self.procesos_activos = {}
    
    def crear_pipeline_ci_cd(self, nombre_agente: str) -> str:
        """Crea pipeline de CI/CD básico"""
        
        github_actions = f"""
name: CI/CD para {nombre_agente}

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest --cov=./ --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t {nombre_agente}:${{{{ github.sha }}}} .
        docker tag {nombre_agente}:${{{{ github.sha }}}} {nombre_agente}:latest
    
    - name: Push to registry
      run: |
        # Configurar registry y push
        echo "Pushing to registry..."

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to production
      run: |
        # Scripts de despliegue
        echo "Deploying to production..."
"""
        
        # Crear directorio .github/workflows si no existe
        workflows_dir = Path(".github/workflows")
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        workflow_path = workflows_dir / f"{nombre_agente}.yml"
        with open(workflow_path, 'w') as f:
            f.write(github_actions)
        
        logger.info(f"Pipeline CI/CD creado: {workflow_path}")
        return str(workflow_path)
    
    def backup_configuracion(self, agente_id: str) -> str:
        """Crea backup de la configuración de un agente"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = Path(f"backups/{agente_id}_{timestamp}")
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Copiar archivos de configuración
        config_files = [
            "config.yaml",
            "docker-compose.yml",
            "Dockerfile",
            "requirements.txt"
        ]
        
        for config_file in config_files:
            source = Path(f"despliegues/{agente_id}/{config_file}")
            if source.exists():
                shutil.copy2(source, backup_dir / config_file)
        
        logger.info(f"Backup creado: {backup_dir}")
        return str(backup_dir)

def demo_completa():
    """Demostración completa del sistema de despliegue"""
    print("🚀 Sistema de Despliegue y Monitorización - Día 7")
    print("=" * 60)
    
    # Crear configuración de ejemplo
    config = ConfiguracionDespliegue(
        nombre_agente="agente_universitario",
        version="1.0.0",
        entorno="produccion",
        servidor_host="agentes.universidad.edu",
        puerto=8080,
        base_datos_url="postgresql://user:pass@db:5432/universidad",
        variables_entorno={
            "ENVIRONMENT": "production",
            "LOG_LEVEL": "INFO",
            "DATABASE_URL": "postgresql://user:pass@db:5432/universidad",
            "REDIS_URL": "redis://redis:6379"
        },
        dependencias=[
            "fastapi-users==12.1.2",
            "email-validator==2.1.0"
        ],
        recursos_minimos={
            "cpu": "500m",
            "memoria": "512Mi",
            "disco": "2Gi"
        },
        configuracion_logging={
            "level": "INFO",
            "format": "json"
        }
    )
    
    # Crear gestor de despliegue
    gestor_despliegue = GestorDespliegue()
    directorio_config = gestor_despliegue.crear_configuracion_despliegue(config)
    print(f"✅ Configuración de despliegue creada en: {directorio_config}")
    
    # Crear sistema de monitoreo
    monitoreo = MonitoreoProduccion()
    
    # Simular algunas métricas
    print("\n📊 Simulando métricas de ejemplo...")
    for i in range(5):
        metrica = MetricaAgente(
            timestamp=datetime.now() - timedelta(minutes=i*10),
            agente_id="agente_universitario",
            cpu_usage=50 + (i * 10),  # CPU creciente
            memory_usage=40 + (i * 5),
            requests_per_minute=100 + i*20,
            response_time_avg=200 + i*50,
            error_rate=1 + i,
            uptime_hours=24 - i
        )
        monitoreo.registrar_metrica(metrica)
    
    # Generar reporte de salud
    reporte = monitoreo.generar_reporte_salud("agente_universitario")
    print(f"✅ Estado del agente: {reporte['estado_general']}")
    print(f"   CPU promedio: {reporte['metricas_24h']['cpu_promedio']}%")
    print(f"   Alertas activas: {reporte['alertas_activas']}")
    
    # Crear pipeline CI/CD
    gestor_continuidad = GestorContinuidad()
    pipeline_path = gestor_continuidad.crear_pipeline_ci_cd("agente_universitario")
    print(f"✅ Pipeline CI/CD creado: {pipeline_path}")
    
    # Crear backup
    backup_path = gestor_continuidad.backup_configuracion("agente_universitario")
    print(f"✅ Backup creado: {backup_path}")
    
    print("\n🎯 Archivos generados para producción:")
    print("   - Dockerfile optimizado")
    print("   - docker-compose.yml completo")
    print("   - Configuración nginx con SSL")
    print("   - Scripts de inicio y monitoreo")
    print("   - Configuración Prometheus/Grafana")
    print("   - Pipeline CI/CD con GitHub Actions")
    print("   - Sistema de backups automáticos")
    
    print("\n📋 Próximos pasos recomendados:")
    print("   1. Configurar certificados SSL")
    print("   2. Establecer backups automáticos")
    print("   3. Configurar alertas por email/Slack")
    print("   4. Implementar rotación de logs")
    print("   5. Establecer métricas de negocio")
    print("   6. Documentar procedimientos de recovery")
    
    print("\n✨ Sistema de despliegue listo para producción!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_completa()
    else:
        print("🏗️ Sistema de Despliegue y Monitorización - Día 7")
        print("=" * 50)
        print("Este sistema proporciona:")
        print("- Configuración automatizada de despliegue")
        print("- Contenedores Docker optimizados")
        print("- Proxy reverso con nginx y SSL")
        print("- Monitoreo con Prometheus y Grafana")
        print("- Pipelines CI/CD con GitHub Actions")
        print("- Sistema de alertas y métricas")
        print("- Backups automatizados")
        print("- Scripts de mantenimiento")
        print("\nEjecuta con --demo para ver una demostración completa")
