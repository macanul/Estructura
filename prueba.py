import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

DB = "finanzas_agricola.db"
VERDE = "#1f6b52"
VERDE_MED = "#8fbf9f"
VERDE_CLARO = "#cfe5d6"
FONDO = "#f6f8f5"
ROJO = "#e05a5a"
ROSA = "#f8d0d0"
MENTA = "#d4f0dc"
CULTIVOS = ["Maíz", "Elote", "Frijol", "Tomate", "Chile", "Calabaza"]
UNIDADES = ["kg", "ton", "costal", "pieza", "litro"]
CONCEPTOS = ["Fertilizante", "Semillas", "Pesticida", "Mano de obra",
             "Riego", "Combustible", "Renta de maquinaria"]

def conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c


def init_db():
    with conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS movimientos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,          -- AAAA-MM-DD
            tipo TEXT NOT NULL,           -- Ingreso / Gasto
            concepto TEXT NOT NULL,
            cultivo TEXT,
            cantidad REAL, unidad TEXT, precio REAL,
            total REAL NOT NULL,
            descripcion TEXT)""")


def money(x):
    return f"${x:,.0f}" if float(x).is_integer() else f"${x:,.2f}"


def num(s):
    return float(str(s).replace("$", "").replace(",", "").strip())


def fecha_a_iso(s):
    return datetime.strptime(s.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")


def iso_a_fecha(s):
    return datetime.strptime(s, "%Y-%m-%d").strftime("%d/%m/%Y")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Control Financiero Agrícola")
        self.geometry("980x600")
        self.minsize(900, 560)
        self.configure(bg=FONDO)
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"),
                        background="#e6eee8")
        style.configure("TCombobox", padding=4)

        self.side = tk.Frame(self, bg=VERDE_CLARO, width=200)
        self.side.pack(side="left", fill="y")
        self.side.pack_propagate(False)
        self.content = tk.Frame(self, bg=FONDO)
        self.content.pack(side="right", fill="both", expand=True)

        self.nav = {}
        items = [("inicio", "🏠  Inicio"), ("ingreso", "➕  Registrar ingreso"),
                 ("gasto", "➖  Registrar gasto"), ("mov", "☰  Movimientos"),
                 ("balance", "📊  Balance")]
        tk.Label(self.side, text="🌱 Agro Control", bg=VERDE_CLARO, fg=VERDE,
                 font=("Segoe UI", 13, "bold")).pack(pady=(18, 14))
        for key, txt in items:
            b = tk.Label(self.side, text=txt, anchor="w", padx=16, pady=9,
                         bg=VERDE_CLARO, fg="#1d3b2f", cursor="hand2",
                         font=("Segoe UI", 10))
            b.pack(fill="x", padx=8, pady=2)
            b.bind("<Button-1>", lambda e, k=key: self.ir(k))
            self.nav[key] = b
        self.ir("inicio")

    def limpiar(self):
        for w in self.content.winfo_children():
            w.destroy()

    def ir(self, pantalla, **kw):
        self.limpiar()
        activo = {"detalle": "mov"}.get(pantalla, pantalla)
        for k, b in self.nav.items():
            b.config(bg=VERDE if k == activo else VERDE_CLARO,
                     fg="white" if k == activo else "#1d3b2f")
        getattr(self, "p_" + pantalla)(**kw)

    def titulo(self, texto, icono=""):
        tk.Label(self.content, text=f"{icono} {texto}", bg=FONDO, fg="#173d31",
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=28, pady=(22, 10))

    def boton(self, parent, texto, cmd, color=VERDE, fg="white", **pk):
        b = tk.Button(parent, text=texto, command=cmd, bg=color, fg=fg, bd=0,
                      activebackground=color, padx=16, pady=7,
                      font=("Segoe UI", 10, "bold"), cursor="hand2")
        b.pack(**pk)
        return b

    def p_inicio(self):
        tk.Label(self.content, text="Control Financiero\nAgrícola", bg=FONDO,
                 fg="#173d31", justify="left",
                 font=("Segoe UI", 26, "bold")).pack(anchor="w", padx=30, pady=(28, 0))
        tk.Label(self.content, text="Tu cosecha también se planea 🌿", bg=FONDO,
                 fg=VERDE, font=("Segoe UI", 12)).pack(anchor="w", padx=30, pady=(0, 18))
        grid = tk.Frame(self.content, bg=FONDO)
        grid.pack(padx=26, anchor="w")
        tarjetas = [
            ("➕  Registrar ingreso", "Agrega una nueva venta\nde tus productos.", MENTA, "ingreso"),
            ("➖  Registrar gasto", "Registra los gastos de tu\nproducción agrícola.", ROSA, "gasto"),
            ("☰  Ver movimientos", "Consulta todos tus ingresos\ny gastos registrados.", "#d3e6f5", "mov"),
            ("📊  Ver balance", "Revisa tu ganancia o\npérdida actual.", "#e0d9f3", "balance"),
        ]
        for i, (t, d, col, dest) in enumerate(tarjetas):
            f = tk.Frame(grid, bg=col, padx=18, pady=16, cursor="hand2")
            f.grid(row=i // 2, column=i % 2, padx=8, pady=8, sticky="nsew")
            l1 = tk.Label(f, text=t, bg=col, font=("Segoe UI", 12, "bold"), anchor="w")
            l2 = tk.Label(f, text=d, bg=col, justify="left", fg="#444", anchor="w")
            l1.pack(anchor="w")
            l2.pack(anchor="w", pady=(4, 0))
            for w in (f, l1, l2):
                w.bind("<Button-1>", lambda e, k=dest: self.ir(k))
            f.config(width=300, height=110)

    def p_ingreso(self, mov=None):
        self.titulo("Editar ingreso" if mov else "Registrar ingreso", "➕")
        f = tk.Frame(self.content, bg=FONDO)
        f.pack(anchor="w", padx=34, pady=6)
        v = {k: tk.StringVar() for k in ("cultivo", "cantidad", "unidad", "precio", "total", "fecha")}
        v["unidad"].set("kg")
        v["fecha"].set(datetime.now().strftime("%d/%m/%Y"))
        if mov:
            v["cultivo"].set(mov["cultivo"] or "")
            v["cantidad"].set(f"{mov['cantidad']:g}")
            v["unidad"].set(mov["unidad"] or "kg")
            v["precio"].set(f"{mov['precio']:g}")
            v["fecha"].set(iso_a_fecha(mov["fecha"]))

        def calc(*_):
            try:
                v["total"].set(money(num(v["cantidad"].get()) * num(v["precio"].get())))
            except ValueError:
                v["total"].set("")
        v["cantidad"].trace_add("write", calc)
        v["precio"].trace_add("write", calc)

        def fila(r, txt, w):
            tk.Label(f, text=txt, bg=FONDO, anchor="w", width=18).grid(row=r, column=0, pady=8, sticky="w")
            w.grid(row=r, column=1, pady=8, sticky="w")
        fila(0, "Producto / Cultivo:", ttk.Combobox(f, textvariable=v["cultivo"], values=CULTIVOS, width=28))
        cant = tk.Frame(f, bg=FONDO)
        ttk.Entry(cant, textvariable=v["cantidad"], width=16).pack(side="left")
        ttk.Combobox(cant, textvariable=v["unidad"], values=UNIDADES, width=8).pack(side="left", padx=8)
        fila(1, "Cantidad:", cant)
        fila(2, "Precio por unidad: $", ttk.Entry(f, textvariable=v["precio"], width=30))
        fila(3, "Total:", ttk.Entry(f, textvariable=v["total"], width=30, state="readonly"))
        fila(4, "Fecha (dd/mm/aaaa):", ttk.Entry(f, textvariable=v["fecha"], width=30))
        calc()

        def guardar():
            try:
                cultivo = v["cultivo"].get().strip()
                if not cultivo:
                    raise ValueError("Escribe el producto o cultivo.")
                cant, precio = num(v["cantidad"].get()), num(v["precio"].get())
                if cant <= 0 or precio <= 0:
                    raise ValueError("Cantidad y precio deben ser mayores a 0.")
                fecha = fecha_a_iso(v["fecha"].get())
            except ValueError as e:
                msg = str(e)
                if "does not match" in msg or "could not convert" in msg:
                    msg = "Revisa los números y la fecha (dd/mm/aaaa)."
                return messagebox.showwarning("Datos incompletos", msg)
            datos = (fecha, "Ingreso", f"Venta de {cultivo.lower()}", cultivo, cant,
                     v["unidad"].get(), precio, cant * precio,
                     mov["descripcion"] if mov else f"Venta de {cultivo.lower()}.")
            with conn() as c:
                if mov:
                    c.execute("""UPDATE movimientos SET fecha=?,tipo=?,concepto=?,cultivo=?,
                        cantidad=?,unidad=?,precio=?,total=?,descripcion=? WHERE id=?""",
                              datos + (mov["id"],))
                else:
                    c.execute("""INSERT INTO movimientos(fecha,tipo,concepto,cultivo,cantidad,
                        unidad,precio,total,descripcion) VALUES(?,?,?,?,?,?,?,?,?)""", datos)
            messagebox.showinfo("Listo", "Ingreso guardado.")
            self.ir("mov")

        bar = tk.Frame(self.content, bg=FONDO)
        bar.pack(anchor="w", padx=34, pady=14)
        self.boton(bar, "💾  Guardar", guardar, side="left")
        self.boton(bar, "✕  Cancelar", lambda: self.ir("mov" if mov else "inicio"),
                   color="white", fg="#333", side="left", padx=10)

    def p_gasto(self, mov=None):
        self.titulo("Editar gasto" if mov else "Registrar gasto", "➖")
        f = tk.Frame(self.content, bg=FONDO)
        f.pack(anchor="w", padx=34, pady=6)
        v = {k: tk.StringVar() for k in ("concepto", "cultivo", "cantidad", "fecha")}
        v["fecha"].set(datetime.now().strftime("%d/%m/%Y"))
        v["cultivo"].set("General")
        if mov:
            v["concepto"].set(mov["concepto"])
            v["cultivo"].set(mov["cultivo"] or "General")
            v["cantidad"].set(f"{mov['total']:g}")
            v["fecha"].set(iso_a_fecha(mov["fecha"]))

        def fila(r, txt, w):
            tk.Label(f, text=txt, bg=FONDO, anchor="w", width=18).grid(row=r, column=0, pady=8, sticky="nw")
            w.grid(row=r, column=1, pady=8, sticky="w")
        fila(0, "Concepto:", ttk.Combobox(f, textvariable=v["concepto"], values=CONCEPTOS, width=28))
        fila(1, "Cultivo (opcional):", ttk.Combobox(f, textvariable=v["cultivo"],
                                                    values=["General"] + CULTIVOS, width=28))
        fila(2, "Cantidad: $", ttk.Entry(f, textvariable=v["cantidad"], width=30))
        fila(3, "Fecha (dd/mm/aaaa):", ttk.Entry(f, textvariable=v["fecha"], width=30))
        desc = tk.Text(f, width=32, height=4, font=("Segoe UI", 10))
        fila(4, "Descripción (opcional):", desc)
        if mov and mov["descripcion"]:
            desc.insert("1.0", mov["descripcion"])

        def guardar():
            try:
                concepto = v["concepto"].get().strip()
                if not concepto:
                    raise ValueError("Escribe el concepto del gasto.")
                monto = num(v["cantidad"].get())
                if monto <= 0:
                    raise ValueError("La cantidad debe ser mayor a 0.")
                fecha = fecha_a_iso(v["fecha"].get())
            except ValueError as e:
                msg = str(e)
                if "does not match" in msg or "could not convert" in msg:
                    msg = "Revisa la cantidad y la fecha (dd/mm/aaaa)."
                return messagebox.showwarning("Datos incompletos", msg)
            datos = (fecha, "Gasto", concepto, v["cultivo"].get().strip() or "General",
                     None, None, None, monto, desc.get("1.0", "end").strip())
            with conn() as c:
                if mov:
                    c.execute("""UPDATE movimientos SET fecha=?,tipo=?,concepto=?,cultivo=?,
                        cantidad=?,unidad=?,precio=?,total=?,descripcion=? WHERE id=?""",
                              datos + (mov["id"],))
                else:
                    c.execute("""INSERT INTO movimientos(fecha,tipo,concepto,cultivo,cantidad,
                        unidad,precio,total,descripcion) VALUES(?,?,?,?,?,?,?,?,?)""", datos)
            messagebox.showinfo("Listo", "Gasto guardado.")
            self.ir("mov")

        bar = tk.Frame(self.content, bg=FONDO)
        bar.pack(anchor="w", padx=34, pady=14)
        self.boton(bar, "💾  Guardar", guardar, side="left")
        self.boton(bar, "✕  Cancelar", lambda: self.ir("mov" if mov else "inicio"),
                   color="white", fg="#333", side="left", padx=10)
    # ------------------------------------------------------------------
    # PARTE 2: Movimientos, Detalle y Balance
    # ------------------------------------------------------------------
    def p_mov(self):
        """Tabla de movimientos con buscador, filtro de tipo y botones de acción."""
        import unicodedata

        def plano(s):
            # minúsculas y sin acentos: así "maiz" encuentra "Maíz"
            s = unicodedata.normalize("NFD", str(s or ""))
            return "".join(ch for ch in s if unicodedata.category(ch) != "Mn").lower()

        self.titulo("Movimientos", "☰")

        # --- barra superior: buscador, filtro de tipo y accesos rápidos ---
        barra = tk.Frame(self.content, bg=FONDO)
        barra.pack(fill="x", padx=28, pady=(0, 10))
        tk.Label(barra, text="🔍", bg=FONDO).pack(side="left")
        q = tk.StringVar()
        ttk.Entry(barra, textvariable=q, width=28).pack(side="left", padx=(4, 14))
        tipo = tk.StringVar(value="Todos")
        ttk.Combobox(barra, textvariable=tipo, values=["Todos", "Ingreso", "Gasto"],
                     state="readonly", width=10).pack(side="left")
        self.boton(barra, "➖  Gasto", lambda: self.ir("gasto"),
                   color=ROSA, fg="#7a2a2a", side="right", padx=(8, 0))
        self.boton(barra, "➕  Ingreso", lambda: self.ir("ingreso"),
                   color=MENTA, fg="#1d5a3a", side="right")

        # --- pie: resumen de lo que se ve + botones de acción (va ANTES de la tabla
        #     para que la tabla ocupe el espacio sobrante) ---
        pie = tk.Frame(self.content, bg=FONDO)
        pie.pack(side="bottom", fill="x", padx=28, pady=(8, 16))
        resumen = tk.Label(pie, bg=FONDO, fg="#444", anchor="w", font=("Segoe UI", 10))
        resumen.pack(side="left")

        # --- tabla ---
        marco = tk.Frame(self.content, bg=FONDO)
        marco.pack(fill="both", expand=True, padx=28)
        tabla = ttk.Treeview(marco, columns=("fecha", "tipo", "concepto", "cultivo", "total"),
                             show="headings", selectmode="browse")
        for col, txt, ancho, anc in [("fecha", "Fecha", 95, "center"), ("tipo", "Tipo", 80, "center"),
                                     ("concepto", "Concepto", 230, "w"), ("cultivo", "Cultivo", 110, "w"),
                                     ("total", "Total", 110, "e")]:
            tabla.heading(col, text=txt)
            tabla.column(col, width=ancho, anchor=anc)
        sb = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=sb.set)
        tabla.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        ttk.Style(self).map("Treeview", background=[("selected", VERDE)],
                            foreground=[("selected", "white")])
        tabla.tag_configure("Ingreso", background=MENTA)   # ingresos en menta
        tabla.tag_configure("Gasto", background=ROSA)      # gastos en rosa

        def cargar(*_):
            tabla.delete(*tabla.get_children())
            buscado, filtro = plano(q.get().strip()), tipo.get()
            n = ingresos = gastos = 0
            with conn() as c:
                filas = c.execute("SELECT * FROM movimientos ORDER BY fecha DESC, id DESC").fetchall()
            for m in filas:
                if filtro != "Todos" and m["tipo"] != filtro:
                    continue
                fecha = iso_a_fecha(m["fecha"])
                if buscado and buscado not in plano(
                        f"{fecha} {m['tipo']} {m['concepto']} {m['cultivo'] or ''} {m['descripcion'] or ''}"):
                    continue
                es_ing = m["tipo"] == "Ingreso"
                tabla.insert("", "end", iid=str(m["id"]), tags=(m["tipo"],),
                             values=(fecha, m["tipo"], m["concepto"], m["cultivo"] or "—",
                                     ("+ " if es_ing else "− ") + money(m["total"])))
                n += 1
                if es_ing:
                    ingresos += m["total"]
                else:
                    gastos += m["total"]
            resumen.config(text=f"{n} movimiento(s)   ·   Ingresos {money(round(ingresos, 2))}"
                                f"   ·   Gastos {money(round(gastos, 2))}")

        def elegido():
            sel = tabla.selection()
            if not sel:
                messagebox.showinfo("Movimientos", "Primero selecciona un movimiento de la tabla.")
                return None
            return int(sel[0])

        def ver():
            mid = elegido()
            if mid is not None:
                self.ir("detalle", mid=mid)

        def editar():
            mid = elegido()
            if mid is not None:
                self.editar(mid)

        def eliminar():
            mid = elegido()
            if mid is not None:
                self.eliminar(mid)

        self.boton(pie, "🗑  Eliminar", eliminar, color=ROJO, side="right", padx=(8, 0))
        self.boton(pie, "✏  Editar", editar, color="white", fg="#333", side="right", padx=(8, 0))
        self.boton(pie, "👁  Ver detalle", ver, side="right")

        def doble_clic(e):
            if tabla.identify_row(e.y):      # ignora el doble clic sobre el encabezado
                ver()
        tabla.bind("<Double-1>", doble_clic)
        tabla.bind("<Return>", lambda e: ver())

        q.trace_add("write", cargar)         # se filtra mientras se escribe
        tipo.trace_add("write", cargar)      # y al cambiar el tipo
        cargar()

    def p_detalle(self, mid):
        """Vista detallada de un movimiento según su ID."""
        m = self.obtener(mid)
        if m is None:
            messagebox.showwarning("Detalle", "Ese movimiento ya no existe.")
            return self.ir("mov")
        es_ing = m["tipo"] == "Ingreso"
        fondo = MENTA if es_ing else ROSA
        acento = VERDE if es_ing else "#a33a3a"

        self.titulo("Detalle del movimiento", "🔎")
        tarjeta = tk.Frame(self.content, bg=fondo, padx=28, pady=20)
        tarjeta.pack(anchor="w", padx=34, pady=(0, 14))
        tk.Label(tarjeta, text=m["tipo"].upper(), bg=fondo, fg=acento,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w")
        tk.Label(tarjeta, text=("+ " if es_ing else "− ") + money(m["total"]), bg=fondo, fg=acento,
                 font=("Segoe UI", 28, "bold")).pack(anchor="w", pady=(0, 10))

        datos = [("Fecha", iso_a_fecha(m["fecha"])), ("Concepto", m["concepto"]),
                 ("Cultivo", m["cultivo"] or "—")]
        if m["cantidad"] is not None:        # solo los ingresos guardan cantidad y precio
            datos.append(("Cantidad", f"{m['cantidad']:g} {m['unidad'] or ''}".strip()))
            datos.append(("Precio por unidad", money(m["precio"] or 0)))
        datos.append(("Descripción", m["descripcion"] or "Sin descripción."))

        rejilla = tk.Frame(tarjeta, bg=fondo)
        rejilla.pack(anchor="w")
        for r, (campo, valor) in enumerate(datos):
            tk.Label(rejilla, text=campo, bg=fondo, fg="#444", width=17, anchor="nw",
                     font=("Segoe UI", 10, "bold")).grid(row=r, column=0, sticky="nw", pady=4)
            tk.Label(rejilla, text=valor, bg=fondo, fg="#222", anchor="w", justify="left",
                     wraplength=420, font=("Segoe UI", 10)).grid(row=r, column=1, sticky="w", pady=4)

        bar = tk.Frame(self.content, bg=FONDO)
        bar.pack(anchor="w", padx=34, pady=6)
        self.boton(bar, "✏  Editar", lambda: self.editar(mid), side="left")
        self.boton(bar, "🗑  Eliminar", lambda: self.eliminar(mid), color=ROJO, side="left", padx=10)
        self.boton(bar, "←  Volver", lambda: self.ir("mov"), color="white", fg="#333", side="left")

    def p_balance(self):
        """Totales de dinero, resumen por cultivo y gráfica de barras en un tk.Canvas."""
        self.titulo("Balance", "📊")

        # --- datos: suma de cada cultivo y tipo (los gastos sin cultivo van a "General") ---
        with conn() as c:
            filas = c.execute("""SELECT COALESCE(NULLIF(TRIM(cultivo), ''), 'General') AS cultivo,
                                        tipo, SUM(total) AS suma
                                 FROM movimientos GROUP BY 1, 2""").fetchall()
        datos = {}
        for f in filas:
            datos.setdefault(f["cultivo"], {"Ingreso": 0.0, "Gasto": 0.0})[f["tipo"]] = round(f["suma"], 2)
        ingresos = round(sum(d["Ingreso"] for d in datos.values()), 2)
        gastos = round(sum(d["Gasto"] for d in datos.values()), 2)
        balance = round(ingresos - gastos, 2)

        def con_signo(x):
            return ("-" if x < 0 else "") + money(abs(x))

        # --- tarjetas con los totales ---
        tarjetas = tk.Frame(self.content, bg=FONDO)
        tarjetas.pack(anchor="w", padx=28, pady=(0, 12))
        color_bal = VERDE if balance >= 0 else "#a33a3a"
        for i, (txt, valor, fondo, fg) in enumerate([
                ("Ingresos", money(ingresos), MENTA, VERDE),
                ("Gastos", money(gastos), ROSA, "#a33a3a"),
                ("Ganancia" if balance >= 0 else "Pérdida", con_signo(balance), "#d3e6f5", color_bal)]):
            t = tk.Frame(tarjetas, bg=fondo, padx=22, pady=12)
            t.grid(row=0, column=i, padx=(0, 12))
            tk.Label(t, text=txt, bg=fondo, fg="#444", font=("Segoe UI", 10, "bold")).pack(anchor="w")
            tk.Label(t, text=valor, bg=fondo, fg=fg, font=("Segoe UI", 18, "bold")).pack(anchor="w")

        # --- parte baja: tabla por cultivo (izquierda) y gráfica (derecha) ---
        abajo = tk.Frame(self.content, bg=FONDO)
        abajo.pack(fill="both", expand=True, padx=28, pady=(0, 16))

        izq = tk.Frame(abajo, bg=FONDO)
        izq.pack(side="left", fill="y")
        tk.Label(izq, text="Resumen por cultivo", bg=FONDO, fg="#173d31",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 6))
        tabla = ttk.Treeview(izq, columns=("cultivo", "ing", "gas", "bal"), show="headings",
                             height=8, selectmode="none")
        for col, txt, ancho, anc in [("cultivo", "Cultivo", 85, "w"), ("ing", "Ingresos", 85, "e"),
                                     ("gas", "Gastos", 85, "e"), ("bal", "Balance", 90, "e")]:
            tabla.heading(col, text=txt)
            tabla.column(col, width=ancho, anchor=anc)
        tabla.tag_configure("pos", foreground=VERDE)
        tabla.tag_configure("neg", foreground="#a33a3a")
        tabla.tag_configure("total", background=VERDE_CLARO, font=("Segoe UI", 10, "bold"))
        for nombre in sorted(datos):
            ing, gas = datos[nombre]["Ingreso"], datos[nombre]["Gasto"]
            tabla.insert("", "end", values=(nombre, money(ing), money(gas), con_signo(round(ing - gas, 2))),
                         tags=("pos" if ing >= gas else "neg",))
        if datos:
            tabla.insert("", "end", values=("TOTAL", money(ingresos), money(gastos), con_signo(balance)),
                         tags=("total",))
        tabla.pack()

        der = tk.Frame(abajo, bg=FONDO)
        der.pack(side="left", fill="both", expand=True, padx=(18, 0))
        tk.Label(der, text="Ingresos vs gastos por cultivo", bg=FONDO, fg="#173d31",
                 font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 6))
        cv = tk.Canvas(der, bg="white", highlightthickness=1, highlightbackground=VERDE_CLARO)
        cv.pack(fill="both", expand=True)

        def corto(v):
            if v >= 1e6:
                return f"{v / 1e6:g}M"
            return f"{v / 1e3:g}k" if v >= 1e3 else f"{v:g}"

        def dibujar(_e=None):
            cv.delete("all")
            w, h = cv.winfo_width(), cv.winfo_height()
            if w < 60 or h < 60:             # el canvas todavía no tiene tamaño real
                return
            if not datos:
                cv.create_text(w / 2, h / 2, text="Sin movimientos todavía", fill="#777",
                               font=("Segoe UI", 11))
                return
            izq_m, der_m, arr_m, aba_m = 48, 12, 30, 38
            alto, ancho = h - arr_m - aba_m, w - izq_m - der_m
            maximo = max(max(d.values()) for d in datos.values()) or 1
            magnitud = 10 ** (len(str(int(maximo))) - 1)
            tope = next(k * magnitud for k in (1, 2, 4, 6, 8, 10) if k * magnitud >= maximo)

            for i in range(5):               # líneas guía y números del eje Y
                y = h - aba_m - alto * i / 4
                cv.create_line(izq_m, y, w - der_m, y, fill="#e3e8e4")
                cv.create_text(izq_m - 6, y, text=corto(tope * i / 4), anchor="e",
                               fill="#666", font=("Segoe UI", 8))

            nombres = sorted(datos)
            grupo = ancho / len(nombres)
            barra = min(26, grupo * 0.34)
            for i, nombre in enumerate(nombres):
                x0 = izq_m + i * grupo + (grupo - 2 * barra - 3) / 2
                for j, (clave, color) in enumerate([("Ingreso", VERDE), ("Gasto", ROJO)]):
                    valor = datos[nombre][clave]
                    if valor <= 0:
                        continue
                    x = x0 + j * (barra + 3)
                    cv.create_rectangle(x, h - aba_m - alto * valor / tope, x + barra, h - aba_m,
                                        fill=color, outline="")
                cv.create_text(izq_m + i * grupo + grupo / 2, h - aba_m + 14,
                               text=nombre if len(nombre) <= 9 else nombre[:8] + "…",
                               fill="#333", font=("Segoe UI", 8))
            cv.create_line(izq_m, h - aba_m, w - der_m, h - aba_m, fill="#999")

            for k, (txt, color) in enumerate([("Ingresos", VERDE), ("Gastos", ROJO)]):   # leyenda
                x = izq_m + k * 85
                cv.create_rectangle(x, 9, x + 11, 20, fill=color, outline="")
                cv.create_text(x + 16, 14.5, text=txt, anchor="w", font=("Segoe UI", 9), fill="#333")

        cv.bind("<Configure>", dibujar)      # se vuelve a dibujar si cambia el tamaño

    def obtener(self, mid):
        with conn() as c:
            return c.execute("SELECT * FROM movimientos WHERE id=?", (mid,)).fetchone()

    def editar(self, mid):
        m = self.obtener(mid)
        self.ir("ingreso" if m["tipo"] == "Ingreso" else "gasto", mov=m)

    def eliminar(self, mid):
        if messagebox.askyesno("Eliminar", "¿Seguro que quieres eliminar este movimiento?"):
            with conn() as c:
                c.execute("DELETE FROM movimientos WHERE id=?", (mid,))
            self.ir("mov")


if __name__ == "__main__":
    init_db()
    App().mainloop()