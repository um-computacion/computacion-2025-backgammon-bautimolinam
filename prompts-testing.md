# Prompts de Testing - Proyecto Backgammon

## Información General

- **Modelo/Herramienta:** Claude 3.5 Sonnet (Anthropic)
- **Versión:** Claude Sonnet 4.5
- **Fecha:** septiembre 2025
- **Objetivo:** Alcanzar >90% cobertura de código en el módulo core

---

## Prompt 1: Tests iniciales básicos

### Texto del prompt
```
una parte del test game que tenia unos errores
```

### Respuesta/resultado
Claude generó `test_game.py` arreglado con:

- Tests de validación de estados
- Uso de mocks para controlar dados
- Aproximadamente 15 tests básicos

### Uso
- ✅ **Usado con modificaciones**

**Modificaciones:**
- Ajusté imports para usar `exception` en lugar de `exceptions`
- Agregué más casos de prueba específicos
- Simplifiqué algunos tests redundantes

### Archivos generados


## Prompt 2: Expansión de tests

### Texto del prompt
```
me faltan tests para la clase core, yo ya tengo mas de 20 y tambien para la clase board
```

### Respuesta/resultado
Claude generó tests completos para las clases core y board

#### test_checker.py
- 5 tests cubriendo:

  - Movimientos entre posiciones
  - Transiciones de estado (tablero → barra → tablero)
  - Bear off
  - Validación de tablero casa
  - Casos edge y límites


#### test_board.py
- Tests de:
  
  - Validación de movimientos
  - Capturas
  - Reingreso desde la barra
  - Bear off con validaciones completas
  - Movimientos válidos por dado
  - Detección de victoria

### Uso
- ✅ **Usado con ajustes menores**

**Modificaciones realizadas:**
- Corrección de imports
- Ajuste de algunos asserts para casos específicos
- Agregué fixtures compartidos
- Simplifiqué configuración de tests repetitivos


## Prompt 3: Verificación de cobertura

### Texto del prompt
```
y para ver el coverage
```

### Respuesta/resultado
Claude proporcionó instrucciones completas para:
1. Instalación de pytest-cov
2. Comandos para ejecutar coverage
3. Generación de reportes HTML
4. Interpretación de resultados
5. Script de verificación automática

Comandos principales proporcionados:
```bash
pytest --cov=core --cov-report=html tests/
pytest --cov=core --cov-report=term-missing tests/
pytest --cov=core --cov-fail-under=90 tests/
```

### Archivos afectados
- Ninguno (instrucciones de uso)




## Casos de Prueba Importantes

### 1. Reglas de Backgammon
- ✅ Movimientos en dirección correcta por jugador
- ✅ Bloqueos con 2+ fichas del oponente
- ✅ Capturas de fichas solitarias
- ✅ Reingreso obligatorio desde la barra
- ✅ Bear off solo cuando todas las fichas están en casa
- ✅ Dobles permiten 4 movimientos
- ✅ Victoria al sacar las 15 fichas

### 2. Casos Edge
- ✅ Tiradas sin movimientos válidos
- ✅ Múltiples fichas en la barra
- ✅ Bear off con valor mayor al necesario
- ✅ Límites del tablero (puntos 0 y 23)
- ✅ Todas las fichas apiladas en un punto
- ✅ Cambio de turno automático

### 3. Validación de Errores
- ✅ Movimientos en dirección incorrecta
- ✅ A puntos bloqueados
- ✅ Sin tirar dados primero
- ✅ Valores de dados inválidos
- ✅ IDs de jugador inválidos
- ✅ Puntos fuera de rango

---

## Ejecución de Tests

### Comandos utilizados

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Con cobertura
pytest --cov=core tests/ -v

# Con reporte HTML
pytest --cov=core --cov-report=html tests/

# Solo un archivo
pytest tests/test_dice.py -v

# Verificar 90%
pytest --cov=core --cov-fail-under=90 tests/
```

### Resultados obtenidos
```
===================== test session starts ======================
collected 105 items

tests/test_board.py ................                    [ 15%]
tests/test_checker.py .........................         [ 39%]
tests/test_dice.py ..............................       [ 67%]
tests/test_game.py ...............                     [ 81%]
tests/test_player.py ....................               [100%]

---------- coverage: platform win32, python 3.12 -----------
Name                    Stmts   Miss  Cover
---------------------------------------------
core\__init__.py            0      0   100%
core\board.py             156     18    88%
core\checker.py            78      4    95%
core\dice.py               89      3    97%
core\exception.py          25      0   100%
core\game.py              134     17    87%
core\player.py            112      8    93%
---------------------------------------------
TOTAL                     594     50    92%

================= 105 passed in 2.34s ====================
```

---

## Conclusión

Los tests generados con ayuda de Claude cumplieron los objetivos:
- ✅ Cobertura >90% alcanzada (~92%)
- ✅ Casos normales, edge y errores cubiertos
- ✅ Documentación clara de qué se prueba
- ✅ Fácil mantenimiento y extensión

El uso de IA aceleró significativamente la creación de tests exhaustivos, identificando casos edge que podrían haber sido omitidos en desarrollo manual.