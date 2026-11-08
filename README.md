# Mis juegos

App sencilla (pensada para iPhone) para seguir juegos de mesa: los que tengo, los que me interesan, sus precios en Mathom y Amazon, y etiquetas para filtrar (tipo, dificultad, jugadores, mejor con…).

- La web se publica en GitHub Pages, **cifrada con contraseña** (StatiCrypt, secret `SITE_PASSWORD`).
- **Los juegos no están en este repo**: la app los lee y guarda en el repo privado `orzull/boardgames-data` (`games.json`) usando un token de GitHub que se pega en *Ajustes* en cada dispositivo. El token solo se guarda en ese dispositivo.
- Sin token, la app funciona igual pero guarda solo en el dispositivo.

## Archivos

- `src/app.html`: la app.
- `src/lock.html`: pantalla de contraseña.
- `build.mjs`: genera `build/index.html` y `build/version.json` (la app se recarga sola cuando hay versión nueva).
- `.github/workflows/deploy.yml`: en cada push a `main` construye, cifra y publica.

## Formato de `games.json` (repo de datos)

```json
{ "games": [ {
  "id": "…", "name": "Cascadia", "owned": false,
  "types": ["Familiar"], "difficulty": "Baja",
  "minPlayers": 1, "maxPlayers": 4, "bestWith": [2],
  "mathomPrice": 32.95, "mathomUrl": "…", "mathomPriceAt": "2026-11-08",
  "amazonPrice": 29.9, "amazonUrl": "…", "amazonPriceAt": "2026-11-08",
  "notes": "", "createdAt": "…", "updatedAt": "…"
} ] }
```

Los borrados se guardan como `{ "id", "deleted": true, "updatedAt" }` para que la sincronización entre dispositivos no los resucite.
