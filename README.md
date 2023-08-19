# MunicipAPI

[![build](https://github.com/halon176/MunicipAPI/workflows/CI/badge.svg)](https://github.com/halon176/MunicipAPI/blob/master/.github/workflows/docker-image.yml)
[![License: GPL v2](https://img.shields.io/badge/License-GPL_v2-blue.svg)](https://github.com/halon176/MunicipAPI/blob/master/LICENSE)

MunicipAPI è un'API che ha lo scopo di fornire i dati geografici e demografici del territorio italiano, organizzata per
giurisdizione di competenza: comuni, province e regioni.

Un'interfaccia OpenAPI del progetto [è disponibile qui](https://halon.cc/api.municipapi/docs).

Mentre un [frontend in REACT](https://github.com/halon176/municipapi-frontend) la
potete [trovare qui](https://halon.cc/municipapi/).

MunicipAPI utilizza FastAPI e Ormar per interagire con un database Postgres, garantendo prestazioni elevate e una
sintassi chiara e intuitiva per l'accesso ai dati.

Per accedere agli endpoint di MunicipAPI, gli utenti devono disporre di una chiave API generata da un utente abilitato.
L'API fornisce tutti gli strumenti necessari per la registrazione dell'utente, la gestione delle proprie chiavi API e
la possibilità di restringere l'accesso a un determinato indirizzo IP.

Sono presenti inoltre tutti gli endpoint necessari ad un amministratore che permettono sia di abilitare/gestire utenti
che le loro api key. L'autenticazione sia degli amministratori che degli utenti avviene tramite Bearer token e JWT.

Dato che il set di dati viene modificato raramente, ho introdotto il supporto alla cache con Redis per aumentare le
prestazioni dell'API

## Installazione

```
docker pull ghcr.io/halon176/municipapi:latest
```

in fase di esecuzione, al container vanno passati le seguenti variabili di ambiente:

```
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASS

REDIS_HOST

SECRET_AUTH
ALGORITHM
```

per l'esecuzione da sorgente invece fare riferimento a python 3.10

⚠️ python 3.11 [ha un problema noto con pydantic](https://github.com/tiangolo/fastapi/issues/5048) che è già stato
sistemato ma verrà incluso nelle versioni successive, quindi per ora non è funzionante.
