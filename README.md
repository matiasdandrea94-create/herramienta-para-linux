# 🛡️ PENTEST ASSISTANT CLI

```
              ░░░░░░░░░░░░░░░░░░░░░░░
            ░░                       ░░
           ░░   ███████████████████   ░░
          ░░   ██  ▄▀▄  ██  ▄▀▄  ██   ░░
          ░░   ██  █▀█  ██  █▀█  ██   ░░
          ░░   ██   ▄███████▄   ██    ░░
          ░░   ██  █  ▀▀▀  █  ██    ░░
          ░░   ██   ▀███████▀   ██    ░░
              ░░░░░░░░░░░░░░░░░░░░░░░

  ██████╗ ███████╗███╗  ██╗████████╗███████╗███████╗████████╗
  ██╔══██╗██╔════╝████╗ ██║╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝
  ██████╔╝█████╗  ██╔██╗██║   ██║   █████╗  ███████╗   ██║
  ██╔═══╝ ██╔══╝  ██║╚████║   ██║   ██╔══╝  ╚════██║   ██║
  ██║     ███████╗██║ ╚███║   ██║   ███████╗███████║   ██║
  ╚═╝     ╚══════╝╚═╝  ╚══╝   ╚═╝   ╚══════╝╚══════╝   ╚═╝
```

> ⚠️ **Solo para uso en entornos con autorización explícita del propietario.**
> El uso no autorizado de estas herramientas puede ser ilegal.

---

## ¿Qué es?

**Pentest Assistant CLI** es una herramienta de línea de comandos interactiva
para asistir en tareas de penetration testing. Está diseñada para facilitar
el flujo de trabajo de un pentester: desde el reconocimiento inicial hasta la
generación del reporte final.

**No requiere dependencias externas** — solo Python 3 estándar. La herramienta
actúa como un asistente que genera los comandos correctos para las herramientas
de pentest que ya tenés instaladas (nmap, sqlmap, ffuf, etc.).

---

## Módulos disponibles

| # | Módulo | Descripción |
|---|--------|-------------|
| 1 | **nmap helper** | Genera comandos nmap con presets optimizados (quick, full, vuln, OS, UDP, stealth) |
| 2 | **Subdominios** | Comandos para subfinder, amass, ffuf, gobuster y cert transparency |
| 3 | **SQLi payloads** | Payloads para detección, union, blind, error-based, WAF bypass y sqlmap |
| 4 | **Bruteforce** | Generador de comandos para hydra, ffuf, gobuster y medusa con selector de wordlist |
| 5 | **OWASP Checklist** | Checklist interactivo del OWASP Top 10 con barra de progreso y severidad |
| 6 | **Reporte** | Genera un reporte de pentest en formato Markdown listo para exportar |

---

## Instalación

### Requisitos

- Python 3.6 o superior
- Terminal Linux con soporte UTF-8 y colores ANSI (cualquier terminal moderna)

### Paso 1 — Descargar el script

```bash
# opción A: copiar el archivo directamente a tu máquina
cp pentest_cli.py ~/tools/pentest_cli.py

# opción B: clonar desde un repo (si lo subiste a GitHub)
git clone https://github.com/tuusuario/pentest-cli
cd pentest-cli
```

### Paso 2 — Dar permisos de ejecución

```bash
chmod +x pentest_cli.py
```

### Paso 3 — Ejecutar

```bash
python3 pentest_cli.py
```

### Opcional — Instalar como comando global

Para poder ejecutarlo desde cualquier directorio con solo escribir `pentest`:

```bash
# copiar al PATH del sistema
sudo cp pentest_cli.py /usr/local/bin/pentest

# dar permisos de ejecución
sudo chmod +x /usr/local/bin/pentest

# verificar
pentest
```

---

## Herramientas externas recomendadas

La CLI genera comandos para estas herramientas. Instalá las que necesites:

```bash
# reconocimiento
sudo apt install nmap
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/owasp-amass/amass/v4/...@master
go install github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest

# fuzzing y directorios
sudo apt install ffuf gobuster

# bruteforce
sudo apt install hydra medusa

# SQL injection
sudo apt install sqlmap

# wordlists
sudo apt install seclists wordlists
```

> **Kali Linux** y **Parrot OS** ya incluyen la mayoría de estas herramientas preinstaladas.

---

## Uso rápido

```
  ┌────────────────────────────────────────────────────────┐
  │  RECONOCIMIENTO                                        │
  │  1. nmap helper                                        │
  │  2. enumeración de subdominios                         │
  ├────────────────────────────────────────────────────────┤
  │  EXPLOTACIÓN                                           │
  │  3. SQLi payloads                                      │
  │  4. bruteforce / fuzzing                               │
  ├────────────────────────────────────────────────────────┤
  │  ANÁLISIS                                              │
  │  5. OWASP Top 10 checklist                             │
  │  6. generar reporte (.md)                              │
  └────────────────────────────────────────────────────────┘
```

Navegás con los números del menú. Cada módulo te pide los datos necesarios
(target, dominio, URL, etc.) y genera el comando listo para copiar o ejecutar.

### Ejemplo de flujo típico

```
1. Iniciás con nmap → quick scan para mapear puertos
2. Enumerás subdominios → modo pasivo con subfinder + amass
3. Identificás parámetros → probás SQLi payloads
4. Bruteforce de directorios → ffuf con SecLists
5. Completás el OWASP checklist
6. Generás el reporte .md → lo exportás con pandoc
```

---

## Exportar el reporte

El módulo de reporte genera un archivo `.md`. Para convertirlo:

```bash
# a PDF
pandoc pentest_reporte.md -o reporte.pdf

# a Word (.docx)
pandoc pentest_reporte.md -o reporte.docx

# a HTML
pandoc pentest_reporte.md -o reporte.html

# instalar pandoc si no lo tenés
sudo apt install pandoc
```

---

## Disclaimer

Esta herramienta fue creada exclusivamente para uso en **entornos autorizados**:
- Laboratorios de práctica (HackTheBox, TryHackMe, VulnHub)
- Auditorías con contrato firmado
- Infraestructura propia

El uso contra sistemas sin autorización explícita es **ilegal** y puede tener
consecuencias legales graves. Los autores no se responsabilizan por el uso
indebido de esta herramienta.

---

*Pentest Assistant CLI v1.0 — Python 3 — sin dependencias externas*
