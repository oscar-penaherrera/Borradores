# =============================================================================
#  PROYECTO 1 - APLICACIÓN EN STREAMLIT
#  Especialización en Python for Analytics - Módulo 1: Python Fundamentals
#
#  Autor : Oscar David Peñaherrera Córdova
#  Curso : Python Fundamentals - Especialización Python for Analytics
#  Enfoque: Finanzas / Negocios
#
#  Descripción general
#  -------------------
#  Aplicación interactiva desarrollada con Streamlit que integra los conceptos
#  fundamentales del Módulo 1:
#     - Variables y tipos de datos
#     - Estructuras de datos (listas, diccionarios)
#     - Control de flujo (if / for)
#     - Funciones y programación funcional
#     - Programación Orientada a Objetos (POO)
#     - Uso de librerías externas (NumPy, Pandas) y librerías propias del curso
#
#  La navegación se realiza mediante un menú lateral (st.sidebar.selectbox)
#  con las secciones: Home, Ejercicio 1, Ejercicio 2, Ejercicio 3 y Ejercicio 4.
#
#  Para ejecutar localmente:
#       streamlit run app.py
# =============================================================================

# -----------------------------------------------------------------------------
# 1. IMPORTACIÓN DE LIBRERÍAS
# -----------------------------------------------------------------------------
# streamlit -> construcción de la interfaz web interactiva
# numpy     -> manejo de arreglos (arrays) numéricos (Ejercicio 2)
# pandas    -> creación y visualización de tablas tipo DataFrame
import streamlit as st
import numpy as np
import pandas as pd

# Librerías EXTERNAS entregadas por el curso.
# libreria_funciones_proyecto1 -> colección de funciones (usada en Ejercicio 3)
# libreria_clases_proyecto1    -> colección de clases (usada en Ejercicio 4)
import libreria_funciones_proyecto1 as lib_fun
from libreria_clases_proyecto1 import ProyectoInversion


# -----------------------------------------------------------------------------
# 2. CONFIGURACIÓN GENERAL DE LA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Proyecto 1 - Python for Analytics | Oscar Peñaherrera",
    page_icon="📊",
    layout="wide",
)


# -----------------------------------------------------------------------------
# 3. INICIALIZACIÓN DEL ESTADO DE LA SESIÓN (st.session_state)
# -----------------------------------------------------------------------------
# En Streamlit, cada interacción del usuario vuelve a ejecutar TODO el script.
# Para NO perder los datos ingresados (listas, arrays, históricos y registros
# del CRUD) se guardan dentro de st.session_state, que sí persiste entre
# ejecuciones mientras la sesión esté abierta.

def inicializar_estado():
    """Crea las claves necesarias en session_state si aún no existen."""
    # Ejercicio 1: lista de movimientos del flujo de caja
    if "movimientos" not in st.session_state:
        st.session_state.movimientos = []          # lista de diccionarios

    # Ejercicio 2: registros de productos (se guardan como listas y luego
    # se transforman en arrays de NumPy y en un DataFrame)
    if "registros_np" not in st.session_state:
        st.session_state.registros_np = []          # lista de diccionarios

    # Ejercicio 3: histórico de resultados de las funciones ejecutadas
    if "historico_funciones" not in st.session_state:
        st.session_state.historico_funciones = []   # lista de diccionarios

    # Ejercicio 4: registros del CRUD de proyectos de inversión
    if "proyectos_inv" not in st.session_state:
        st.session_state.proyectos_inv = []         # lista de diccionarios


inicializar_estado()


# =============================================================================
#  SECCIÓN: HOME
# =============================================================================
def mostrar_home():
    """Página de presentación del proyecto."""
    st.title("📊 Proyecto 1 - Aplicación en Streamlit")
    st.subheader("Especialización en Python for Analytics · Módulo 1: Python Fundamentals")

    st.markdown("---")

    # Dos columnas: información del estudiante e imagen/logo representativo
    col_izq, col_der = st.columns([2, 1])

    with col_izq:
        st.markdown(
            """
            ### 👤 Información general del estudiante
            - **Nombre completo:** Oscar David Peñaherrera Córdova
            - **Módulo:** Python Fundamentals (Módulo 1)
            - **Curso:** Especialización en Python for Analytics
            - **Enfoque del proyecto:** Finanzas / Negocios
            - **Año:** 2026
            """
        )

        st.markdown(
            """
            ### 📝 Breve descripción del proyecto
            Esta aplicación integra los conceptos fundamentales de Python aprendidos
            en el módulo mediante **cuatro ejercicios prácticos** más una página de
            presentación. Cada ejercicio evidencia el uso de **estructuras de datos,
            widgets, funciones, clases y lógica de programación** dentro de una
            interfaz interactiva construida con Streamlit.
            """
        )

    with col_der:
        # Imagen/logo representativo del proyecto. Se usa un archivo LOCAL (logo.png)
        # incluido en el repositorio para que funcione también en Streamlit Cloud
        # sin depender de una conexión externa. Es opcional según el enunciado.
        import os
        if os.path.exists("logo.png"):
            st.image("logo.png", caption="Python for Analytics", width=200)
        else:
            st.markdown("## 📊 PY · Analytics")

    st.markdown("---")

    st.markdown(
        """
        ### 🛠️ Tecnologías utilizadas
        | Tecnología | Uso en el proyecto |
        |------------|--------------------|
        | **Python 3** | Lenguaje base de todo el desarrollo |
        | **Streamlit** | Interfaz web interactiva y widgets |
        | **NumPy** | Manejo de arreglos numéricos (Ejercicio 2) |
        | **Pandas** | Tablas tipo DataFrame para mostrar resultados |
        | **Librerías del curso** | Funciones y clases externas (Ejercicios 3 y 4) |
        """
    )

    st.info(
        "Usa el **menú lateral izquierdo** para navegar entre la página Home "
        "y los cuatro ejercicios de la aplicación."
    )


# =============================================================================
#  SECCIÓN: EJERCICIO 1 - Flujo de caja con listas
# =============================================================================
def mostrar_ejercicio1():
    """
    Registra movimientos financieros (ingresos/gastos) en una LISTA vacía y
    calcula totales y saldo final indicando si el flujo está a favor o en contra.
    Conceptos: listas, diccionarios, control de flujo, funciones y widgets.
    """
    st.title("💵 Ejercicio 1 - Flujo de caja con listas")
    st.markdown(
        """
        En este ejercicio se registran **movimientos financieros** dentro de una
        **lista**. Cada movimiento guarda un *concepto*, un *tipo* (Ingreso o Gasto)
        y un *valor*. Al final se calculan el **total de ingresos**, el **total de
        gastos**, el **saldo final** y se indica si el flujo de caja está
        **a favor** o **en contra**.
        """
    )

    st.markdown("### ➕ Registrar un nuevo movimiento")

    # --- Widgets de entrada de datos ---
    col1, col2, col3 = st.columns(3)
    with col1:
        concepto = st.text_input("Concepto", placeholder="Ej: Venta de producto")
    with col2:
        tipo = st.selectbox("Tipo de movimiento", ["Ingreso", "Gasto"])
    with col3:
        valor = st.number_input("Valor", min_value=0.0, step=10.0, format="%.2f")

    # --- Botón para agregar el movimiento a la lista ---
    if st.button("Agregar movimiento", type="primary"):
        # Validación de entradas antes de procesar
        if concepto.strip() == "":
            st.error("⚠️ El concepto no puede estar vacío.")
        elif valor <= 0:
            st.error("⚠️ El valor debe ser mayor que cero.")
        else:
            # Se agrega un diccionario a la lista de movimientos
            st.session_state.movimientos.append(
                {"Concepto": concepto.strip(), "Tipo": tipo, "Valor": float(valor)}
            )
            st.success(f"✅ Movimiento agregado: {concepto} ({tipo}) por S/ {valor:,.2f}")

    # Botón auxiliar para limpiar la lista (mejora la usabilidad)
    if st.session_state.movimientos:
        if st.button("🗑️ Limpiar todos los movimientos"):
            st.session_state.movimientos = []
            st.rerun()

    st.markdown("---")
    st.markdown("### 📋 Movimientos registrados")

    # --- Mostrar la lista de movimientos y los resultados ---
    if not st.session_state.movimientos:
        st.info("Aún no hay movimientos registrados. Agrega el primero arriba. ⬆️")
        return

    # Convertimos la lista de diccionarios en un DataFrame para mostrarla como tabla
    df_mov = pd.DataFrame(st.session_state.movimientos)
    st.dataframe(df_mov, width='stretch')

    # --- Cálculos con programación funcional (sum + comprensión de listas) ---
    total_ingresos = sum(m["Valor"] for m in st.session_state.movimientos if m["Tipo"] == "Ingreso")
    total_gastos = sum(m["Valor"] for m in st.session_state.movimientos if m["Tipo"] == "Gasto")
    saldo_final = total_ingresos - total_gastos

    # --- Mostrar métricas ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Total ingresos", f"S/ {total_ingresos:,.2f}")
    c2.metric("Total gastos", f"S/ {total_gastos:,.2f}")
    c3.metric("Saldo final", f"S/ {saldo_final:,.2f}", delta=f"{saldo_final:,.2f}")

    # --- Resultado final del flujo de caja ---
    if saldo_final > 0:
        st.success(f"🟢 El flujo de caja está **A FAVOR** con un saldo de S/ {saldo_final:,.2f}.")
    elif saldo_final < 0:
        st.error(f"🔴 El flujo de caja está **EN CONTRA** con un déficit de S/ {abs(saldo_final):,.2f}.")
    else:
        st.warning("🟡 El flujo de caja está **EQUILIBRADO** (saldo = 0).")


# =============================================================================
#  SECCIÓN: EJERCICIO 2 - Registro con NumPy, arrays y DataFrame
# =============================================================================
def mostrar_ejercicio2():
    """
    Registra productos usando arreglos de NumPy y muestra un DataFrame de Pandas
    actualizado. Conceptos: arrays de NumPy, operaciones vectorizadas y DataFrames.
    """
    st.title("🧮 Ejercicio 2 - Registro con NumPy, arrays y DataFrame")
    st.markdown(
        """
        En este ejercicio se registran **productos** mediante un formulario. Cada
        registro (nombre, categoría, precio y cantidad) se almacena y el **total**
        se calcula con **NumPy** (`precio * cantidad`). Toda la información se
        convierte en un **DataFrame de Pandas** que se actualiza en pantalla.
        """
    )

    st.markdown("### ➕ Registrar un nuevo producto")

    # --- Formulario de ingreso de datos ---
    col1, col2 = st.columns(2)
    with col1:
        nombre = st.text_input("Nombre del producto", placeholder="Ej: Laptop")
        categoria = st.selectbox(
            "Categoría", ["Tecnología", "Alimentos", "Ropa", "Hogar", "Servicios", "Otros"]
        )
    with col2:
        precio = st.number_input("Precio (S/)", min_value=0.0, step=1.0, format="%.2f")
        cantidad = st.number_input("Cantidad", min_value=0, step=1)

    if st.button("Agregar registro", type="primary"):
        if nombre.strip() == "":
            st.error("⚠️ El nombre del producto no puede estar vacío.")
        elif precio <= 0 or cantidad <= 0:
            st.error("⚠️ El precio y la cantidad deben ser mayores que cero.")
        else:
            st.session_state.registros_np.append(
                {
                    "Producto": nombre.strip(),
                    "Categoría": categoria,
                    "Precio": float(precio),
                    "Cantidad": int(cantidad),
                }
            )
            st.success(f"✅ Producto '{nombre}' agregado correctamente.")

    if st.session_state.registros_np:
        if st.button("🗑️ Limpiar registros"):
            st.session_state.registros_np = []
            st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Tabla de registros (DataFrame)")

    if not st.session_state.registros_np:
        st.info("Aún no hay productos registrados. Agrega el primero arriba. ⬆️")
        return

    # --- Uso de NumPy: se crean ARRAYS a partir de los registros ---
    precios = np.array([r["Precio"] for r in st.session_state.registros_np])
    cantidades = np.array([r["Cantidad"] for r in st.session_state.registros_np])

    # Operación VECTORIZADA de NumPy: multiplica elemento a elemento
    totales = precios * cantidades

    # --- Construcción del DataFrame de Pandas ---
    df = pd.DataFrame(st.session_state.registros_np)
    df["Total"] = totales                       # columna calculada con NumPy
    st.dataframe(df, width='stretch')

    # --- Resumen usando funciones de NumPy ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Productos registrados", f"{len(df)}")
    c2.metric("Total inventario", f"S/ {totales.sum():,.2f}")
    c3.metric("Precio promedio", f"S/ {precios.mean():,.2f}")


# =============================================================================
#  SECCIÓN: EJERCICIO 3 - Uso de funciones desde una librería externa
# =============================================================================

# Registro (diccionario) que describe las funciones FINANCIERAS/NEGOCIOS
# disponibles. Para cada función se define:
#   - "func"    : la función real de la librería
#   - "params"  : lista de parámetros (etiqueta, valor por defecto, formato)
# Esto permite construir los widgets de forma DINÁMICA según la función elegida.
FUNCIONES_FINANZAS = {
    "Cuota de préstamo (Sistema Francés)": {
        "func": lib_fun.calcular_cuota_prestamo_frances,
        "params": [
            ("monto", "Monto del préstamo (S/)", 10000.0),
            ("tasa_anual_pct", "Tasa anual (%)", 18.0),
            ("plazo_meses", "Plazo (meses)", 12),
        ],
    },
    "ROI - Retorno sobre la inversión": {
        "func": lib_fun.calcular_roi,
        "params": [
            ("ganancia_neta", "Ganancia neta (S/)", 3000.0),
            ("inversion", "Inversión (S/)", 10000.0),
        ],
    },
    "Valor futuro (interés compuesto)": {
        "func": lib_fun.calcular_valor_futuro,
        "params": [
            ("monto_inicial", "Monto inicial (S/)", 5000.0),
            ("tasa_anual_pct", "Tasa anual (%)", 12.0),
            ("anios", "Años", 5.0),
            ("capitalizaciones_por_anio", "Capitalizaciones por año", 12),
        ],
    },
    "Punto de equilibrio": {
        "func": lib_fun.calcular_punto_equilibrio,
        "params": [
            ("costos_fijos", "Costos fijos (S/)", 20000.0),
            ("precio_unitario", "Precio unitario (S/)", 50.0),
            ("costo_variable_unitario", "Costo variable unitario (S/)", 30.0),
        ],
    },
    "WACC - Costo promedio ponderado de capital": {
        "func": lib_fun.calcular_wacc,
        "params": [
            ("deuda", "Deuda (S/)", 40000.0),
            ("patrimonio", "Patrimonio (S/)", 60000.0),
            ("costo_deuda_pct", "Costo de la deuda (%)", 10.0),
            ("costo_patrimonio_pct", "Costo del patrimonio (%)", 15.0),
            ("impuesto_pct", "Impuesto (%)", 30.0),
        ],
    },
}


def mostrar_ejercicio3():
    """
    Conecta funciones de la librería externa (área Finanzas/Negocios) con widgets
    de Streamlit, ejecuta la función seleccionada y guarda un histórico en un
    DataFrame. Conceptos: importación de librerías, funciones, diccionarios.
    """
    st.title("🏦 Ejercicio 3 - Funciones desde una librería externa (Finanzas)")
    st.markdown(
        """
        Este ejercicio utiliza el archivo **`libreria_funciones_proyecto1.py`**.
        Se seleccionó el área de **Finanzas / Negocios**. Elige una función,
        ingresa sus parámetros, ejecútala y observa el resultado. Cada ejecución
        se guarda en una **tabla histórica**.
        """
    )

    # --- Selector de función ---
    nombre_func = st.selectbox("Selecciona una función", list(FUNCIONES_FINANZAS.keys()))
    config = FUNCIONES_FINANZAS[nombre_func]

    st.markdown(f"**Función seleccionada:** `{config['func'].__name__}`")

    # --- Widgets dinámicos para ingresar los parámetros ---
    st.markdown("### ✏️ Parámetros de entrada")
    valores = {}
    columnas = st.columns(2)
    for i, (clave, etiqueta, valor_def) in enumerate(config["params"]):
        with columnas[i % 2]:
            # Si el valor por defecto es entero, se usa paso entero
            if isinstance(valor_def, int):
                valores[clave] = st.number_input(etiqueta, value=valor_def, step=1, key=f"e3_{clave}")
            else:
                valores[clave] = st.number_input(
                    etiqueta, value=valor_def, step=1.0, format="%.2f", key=f"e3_{clave}"
                )

    # --- Botón para ejecutar la función ---
    if st.button("Ejecutar función", type="primary"):
        try:
            # Se llama a la función con los parámetros ingresados (desempaquetado **)
            resultado = config["func"](**valores)

            st.markdown("### ✅ Resultado")
            st.write(resultado)              # muestra el diccionario de resultados

            # Se muestra el resultado también como métricas legibles
            cols = st.columns(len(resultado))
            for col, (k, v) in zip(cols, resultado.items()):
                col.metric(k.replace("_", " ").title(), f"{v}")

            # --- Guardar en el histórico (DataFrame) ---
            fila = {"Función": nombre_func}
            fila.update({k: v for k, v in valores.items()})   # parámetros usados
            fila.update({f"→ {k}": v for k, v in resultado.items()})  # resultados
            st.session_state.historico_funciones.append(fila)

        except ValueError as e:
            # La librería lanza ValueError cuando una validación falla
            st.error(f"⚠️ Error de validación: {e}")
        except Exception as e:
            st.error(f"⚠️ Ocurrió un error inesperado: {e}")

    # --- Tabla histórica de resultados ---
    st.markdown("---")
    st.markdown("### 🗂️ Histórico de resultados")
    if st.session_state.historico_funciones:
        df_hist = pd.DataFrame(st.session_state.historico_funciones)
        st.dataframe(df_hist, width='stretch')
        if st.button("🗑️ Limpiar histórico"):
            st.session_state.historico_funciones = []
            st.rerun()
    else:
        st.info("Aún no se ha ejecutado ninguna función.")


# =============================================================================
#  SECCIÓN: EJERCICIO 4 - Uso de clases desde una librería externa con CRUD
# =============================================================================
def mostrar_ejercicio4():
    """
    Utiliza la clase ProyectoInversion de la librería de clases e implementa un
    CRUD completo (Crear, Leer, Actualizar, Eliminar) sobre proyectos de inversión.
    Conceptos: POO (instanciar objetos, llamar métodos) + CRUD con listas.
    """
    st.title("📈 Ejercicio 4 - Clases externas con CRUD (Proyectos de inversión)")
    st.markdown(
        """
        Este ejercicio utiliza la clase **`ProyectoInversion`** del archivo
        **`libreria_clases_proyecto1.py`**. Se implementa un **CRUD** completo:
        **C**rear, **L**eer, **A**ctualizar y **E**liminar proyectos de inversión.
        Para cada proyecto la clase calcula automáticamente el **VPN**, el **ROI**,
        el **Payback** y la **decisión** (Viable / No viable).
        """
    )

    # Se organiza el CRUD en pestañas (st.tabs) para mayor claridad.
    tab_crear, tab_leer, tab_actualizar, tab_eliminar = st.tabs(
        ["🟢 Crear", "🔵 Leer", "🟡 Actualizar", "🔴 Eliminar"]
    )

    # ---------------------------------------------------------------------
    # CREAR
    # ---------------------------------------------------------------------
    with tab_crear:
        st.markdown("### 🟢 Crear un nuevo proyecto de inversión")
        nombre = st.text_input("Nombre del proyecto", placeholder="Ej: Planta Solar")
        col1, col2 = st.columns(2)
        with col1:
            inversion = st.number_input("Inversión inicial (S/)", min_value=0.0, value=10000.0, step=100.0)
            tasa = st.number_input("Tasa de descuento (%)", min_value=0.0, max_value=100.0, value=12.0, step=0.5)
        with col2:
            flujos_texto = st.text_input(
                "Flujos anuales (separados por coma)", value="3000, 4000, 5000, 4000"
            )

        if st.button("Crear proyecto", type="primary"):
            try:
                if nombre.strip() == "":
                    st.error("⚠️ El nombre del proyecto no puede estar vacío.")
                else:
                    # Convertimos el texto "3000, 4000" a una lista de números
                    flujos = [float(x.strip()) for x in flujos_texto.split(",") if x.strip() != ""]

                    # --- Instanciamos el OBJETO de la clase ProyectoInversion ---
                    proyecto = ProyectoInversion(nombre.strip(), inversion, flujos, tasa)

                    # El método resumen() devuelve un diccionario con los cálculos
                    datos = proyecto.resumen()
                    # Guardamos también los flujos y la tasa para poder actualizar luego
                    datos["_inversion"] = inversion
                    datos["_flujos"] = flujos
                    datos["_tasa"] = tasa

                    st.session_state.proyectos_inv.append(datos)
                    st.success(f"✅ Proyecto '{nombre}' creado correctamente.")
                    st.write(proyecto.resumen())
            except ValueError as e:
                st.error(f"⚠️ Error de validación: {e}")
            except Exception as e:
                st.error(f"⚠️ Error: {e}")

    # ---------------------------------------------------------------------
    # LEER
    # ---------------------------------------------------------------------
    with tab_leer:
        st.markdown("### 🔵 Proyectos registrados")
        if st.session_state.proyectos_inv:
            # Mostramos solo las columnas visibles (ocultamos las que empiezan con "_")
            df = pd.DataFrame(st.session_state.proyectos_inv)
            columnas_visibles = [c for c in df.columns if not c.startswith("_")]
            st.dataframe(df[columnas_visibles], width='stretch')

            # Pequeño resumen: cuántos proyectos son viables
            viables = sum(1 for p in st.session_state.proyectos_inv if p["decision"] == "Viable")
            c1, c2 = st.columns(2)
            c1.metric("Proyectos registrados", len(st.session_state.proyectos_inv))
            c2.metric("Proyectos viables", viables)
        else:
            st.info("Aún no hay proyectos registrados. Crea uno en la pestaña '🟢 Crear'.")

    # ---------------------------------------------------------------------
    # ACTUALIZAR
    # ---------------------------------------------------------------------
    with tab_actualizar:
        st.markdown("### 🟡 Actualizar un proyecto existente")
        if st.session_state.proyectos_inv:
            nombres = [p["proyecto"] for p in st.session_state.proyectos_inv]
            seleccionado = st.selectbox("Selecciona el proyecto a actualizar", nombres, key="upd_sel")
            idx = nombres.index(seleccionado)
            actual = st.session_state.proyectos_inv[idx]

            col1, col2 = st.columns(2)
            with col1:
                nueva_inv = st.number_input(
                    "Nueva inversión inicial (S/)", min_value=0.0, value=float(actual["_inversion"]), step=100.0
                )
                nueva_tasa = st.number_input(
                    "Nueva tasa de descuento (%)", min_value=0.0, max_value=100.0,
                    value=float(actual["_tasa"]), step=0.5
                )
            with col2:
                nuevos_flujos_txt = st.text_input(
                    "Nuevos flujos (separados por coma)",
                    value=", ".join(str(f) for f in actual["_flujos"]),
                )

            if st.button("Actualizar proyecto", type="primary"):
                try:
                    flujos = [float(x.strip()) for x in nuevos_flujos_txt.split(",") if x.strip() != ""]
                    # Se vuelve a instanciar el objeto con los nuevos datos
                    proyecto = ProyectoInversion(seleccionado, nueva_inv, flujos, nueva_tasa)
                    datos = proyecto.resumen()
                    datos["_inversion"] = nueva_inv
                    datos["_flujos"] = flujos
                    datos["_tasa"] = nueva_tasa
                    st.session_state.proyectos_inv[idx] = datos
                    st.success(f"✅ Proyecto '{seleccionado}' actualizado correctamente.")
                    st.write(proyecto.resumen())
                except ValueError as e:
                    st.error(f"⚠️ Error de validación: {e}")
                except Exception as e:
                    st.error(f"⚠️ Error: {e}")
        else:
            st.info("No hay proyectos para actualizar.")

    # ---------------------------------------------------------------------
    # ELIMINAR
    # ---------------------------------------------------------------------
    with tab_eliminar:
        st.markdown("### 🔴 Eliminar un proyecto")
        if st.session_state.proyectos_inv:
            nombres = [p["proyecto"] for p in st.session_state.proyectos_inv]
            a_eliminar = st.selectbox("Selecciona el proyecto a eliminar", nombres, key="del_sel")
            if st.button("Eliminar proyecto", type="primary"):
                idx = nombres.index(a_eliminar)
                st.session_state.proyectos_inv.pop(idx)
                st.success(f"🗑️ Proyecto '{a_eliminar}' eliminado correctamente.")
                st.rerun()
        else:
            st.info("No hay proyectos para eliminar.")


# =============================================================================
#  MENÚ LATERAL Y ENRUTAMIENTO PRINCIPAL
# =============================================================================
def main():
    """Función principal: dibuja el menú lateral y llama a la sección elegida."""
    st.sidebar.title("📌 Navegación")
    st.sidebar.markdown("Proyecto 1 · Python Fundamentals")

    # Menú lateral con selectbox (requisito obligatorio del proyecto)
    seccion = st.sidebar.selectbox(
        "Selecciona una sección:",
        ["Home", "Ejercicio 1", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"],
    )

    st.sidebar.markdown("---")
    st.sidebar.info("**Autor:** Oscar David Peñaherrera Córdova")

    # Enrutamiento: se ejecuta la función correspondiente a la sección elegida
    if seccion == "Home":
        mostrar_home()
    elif seccion == "Ejercicio 1":
        mostrar_ejercicio1()
    elif seccion == "Ejercicio 2":
        mostrar_ejercicio2()
    elif seccion == "Ejercicio 3":
        mostrar_ejercicio3()
    elif seccion == "Ejercicio 4":
        mostrar_ejercicio4()


# Punto de entrada de la aplicación
if __name__ == "__main__":
    main()
