import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os

class Empleado:
    def __init__(self, nombre, apellidos, cargo, genero, salarioDia, diasTrabajados, otrosIngresos, pagosSalud, aportePensiones):
        self.nombre = nombre
        self.apellidos = apellidos
        self.cargo = cargo
        self.genero = genero
        self.salarioDia = salarioDia
        self.diasTrabajados = diasTrabajados
        self.otrosIngresos = otrosIngresos
        self.pagosSalud = pagosSalud
        self.aportePensiones = aportePensiones

    def calcularNomina(self):
        # Formula del enunciado
        salario = (self.salarioDia * self.diasTrabajados) + self.otrosIngresos - self.pagosSalud - self.aportePensiones
        return salario


class ListaEmpleados:
    def __init__(self):
        self.lista = []
        self.totalNomina = 0.0

    def agregarEmpleado(self, emp):
        self.lista.append(emp)

    def calcularTotalNomina(self):
        self.totalNomina = 0.0
        for e in self.lista:
            self.totalNomina = self.totalNomina + e.calcularNomina()
        return self.totalNomina

    def obtenerMatriz(self):
        datos = []
        self.totalNomina = 0.0
        for e in self.lista:
            sueldo = e.calcularNomina()
            datos.append((e.nombre, e.apellidos, str(round(sueldo, 2))))
            self.totalNomina = self.totalNomina + sueldo
        return datos

    def convertirTexto(self):
        texto = ""
        for e in self.lista:
            texto = texto + "Nombre = " + e.nombre + "\n"
            texto = texto + "Apellidos = " + e.apellidos + "\n"
            texto = texto + "Cargo = " + e.cargo + "\n"
            texto = texto + "Género = " + e.genero + "\n"
            texto = texto + "Salario = $" + str(e.salarioDia) + "\n"
            texto = texto + "Días trabajados = " + str(e.diasTrabajados) + "\n"
            texto = texto + "Otros ingresos = $" + str(e.otrosIngresos) + "\n"
            texto = texto + "Pagos saludo = $" + str(e.pagosSalud) + "\n"
            texto = texto + "Aportes pensiones = $" + str(e.aportePensiones) + "\n---------\n"
        
        texto = texto + "Total nómina = $" + f"{self.calcularTotalNomina():.2f}"
        return texto


class VentanaAgregarEmpleado(tk.Toplevel):
    def __init__(self, master, lista):
        super().__init__(master)
        self.lista = lista
        self.title("Agregar Empleado")
        self.geometry("320x390")
        self.resizable(False, False)
        self.inicio()

    def inicio(self):
       
        tk.Label(self, text="Nombre:").place(x=20, y=20)
        self.campoNombre = tk.Entry(self)
        self.campoNombre.place(x=160, y=20, width=120)

        tk.Label(self, text="Apellidos:").place(x=20, y=50)
        self.campoApellidos = tk.Entry(self)
        self.campoApellidos.place(x=160, y=50, width=120)

        tk.Label(self, text="Cargo:").place(x=20, y=80)
        self.campoCargo = ttk.Combobox(self, values=["Directivo", "Estratégico", "Operativo"], state="readonly")
        self.campoCargo.current(0)
        self.campoCargo.place(x=160, y=80, width=120)

        tk.Label(self, text="Género:").place(x=20, y=115)
        self.var_genero = tk.StringVar(value="MASCULINO")
        self.masculino = tk.Radiobutton(self, text="Masculino", variable=self.var_genero, value="MASCULINO")
        self.masculino.place(x=160, y=110)
        self.femenino = tk.Radiobutton(self, text="Femenino", variable=self.var_genero, value="FEMENINO")
        self.femenino.place(x=160, y=135)

        tk.Label(self, text="Salario por día:").place(x=20, y=170)
        self.campoSalarioDia = tk.Entry(self)
        self.campoSalarioDia.place(x=160, y=170, width=120)

        tk.Label(self, text="Días trabajados al mes:").place(x=20, y=200)
        self.campoNumeroDias = tk.Spinbox(self, from_=1, to=31)
        self.campoNumeroDias.delete(0, tk.END)
        self.campoNumeroDias.insert(0, "30")
        self.campoNumeroDias.place(x=160, y=200, width=50)

        tk.Label(self, text="Otros ingresos:").place(x=20, y=230)
        self.campoOtrosIngresos = tk.Entry(self)
        self.campoOtrosIngresos.place(x=160, y=230, width=120)

        tk.Label(self, text="Pagos por salud:").place(x=20, y=260)
        self.campoAportesSalud = tk.Entry(self)
        self.campoAportesSalud.place(x=160, y=260, width=120)

        tk.Label(self, text="Aportes pensiones:").place(x=20, y=290)
        self.campoPensiones = tk.Entry(self)
        self.campoPensiones.place(x=160, y=290, width=120)

        self.agregar = tk.Button(self, text="Agregar", command=self.anadirEmpleado)
        self.agregar.place(x=40, y=335, width=90)

        self.limpiar = tk.Button(self, text="Borrar", command=self.limpiarCampos)
        self.limpiar.place(x=170, y=335, width=90)

    def limpiarCampos(self):
        self.campoNombre.delete(0, tk.END)
        self.campoApellidos.delete(0, tk.END)
        self.campoSalarioDia.delete(0, tk.END)
        self.campoNumeroDias.delete(0, tk.END)
        self.campoNumeroDias.insert(0, "30")
        self.campoOtrosIngresos.delete(0, tk.END)
        self.campoAportesSalud.delete(0, tk.END)
        self.campoPensiones.delete(0, tk.END)

    def anadirEmpleado(self):
        try:
            valor1 = self.campoNombre.get()
            valor2 = self.campoApellidos.get()
            cargo_sel = self.campoCargo.get().upper()
            genero_sel = self.var_genero.get()
            valor3 = float(self.campoSalarioDia.get())
            valor4 = int(self.campoNumeroDias.get())
            valor5 = float(self.campoOtrosIngresos.get())
            valor6 = float(self.campoAportesSalud.get())
            valor7 = float(self.campoPensiones.get())

            e = Empleado(valor1, valor2, cargo_sel, genero_sel, valor3, valor4, valor5, valor6, valor7)
            self.lista.agregarEmpleado(e)
            messagebox.showinfo("Mensaje", "El empleado ha sido agregado", parent=self)
            self.limpiarCampos()
        except:
            messagebox.showerror("Error", "Campo nulo o error en formato de numero", parent=self)


class VentanaNomina(tk.Toplevel):
    def __init__(self, master, lista):
        super().__init__(master)
        self.lista = lista
        self.title("Nómina de Empleados")
        self.geometry("380x260")
        self.resizable(False, False)
        self.inicio()

    def inicio(self):
        tk.Label(self, text="Lista de empleados:").place(x=20, y=10)

        columnas = ("NOMBRE", "APELLIDOS", "SUELDO")
        self.tabla = ttk.Treeview(self, columns=columnas, show="headings", height=6)
        self.tabla.heading("NOMBRE", text="NOMBRE")
        self.tabla.heading("APELLIDOS", text="APELLIDOS")
        self.tabla.heading("SUELDO", text="SUELDO")

        self.tabla.column("NOMBRE", width=110)
        self.tabla.column("APELLIDOS", width=110)
        self.tabla.column("SUELDO", width=110)

        datos = self.lista.obtenerMatriz()
        for fila in datos:
            self.tabla.insert("", tk.END, values=fila)

        self.tabla.place(x=20, y=40, width=335, height=150)

        total_txt = f"Total nómina mensual = $ {self.lista.totalNomina:.2f}"
        self.nomina = tk.Label(self, text=total_txt)
        self.nomina.place(x=20, y=210)


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.empleados = ListaEmpleados()
        self.title("Nómina")
        self.geometry("280x350")
        self.resizable(False, False)
        self.inicio()

    def inicio(self):
        self.barraMenu = tk.Menu(self)
        self.menuOpciones = tk.Menu(self.barraMenu, tearoff=0)

        self.menuOpciones.add_command(label="Agregar empleado", command=self.abrir_agregar)
        self.menuOpciones.add_command(label="Calcular nómina", command=self.abrir_nomina)
        self.menuOpciones.add_separator()
        self.menuOpciones.add_command(label="Guardar archivo", command=self.guardar_archivo)

        self.barraMenu.add_cascade(label="Menú", menu=self.menuOpciones)
        self.config(menu=self.barraMenu)

    def abrir_agregar(self):
        v = VentanaAgregarEmpleado(self, self.empleados)

    def abrir_nomina(self):
        v = VentanaNomina(self, self.empleados)

    def guardar_archivo(self):
        carpeta = filedialog.askdirectory(title="Seleccione carpeta para guardar")
        if carpeta != "":
            try:
                contenido = self.empleados.convertirTexto()
                ruta = os.path.join(carpeta, "Nómina.txt")
                archivo = open(ruta, "w", encoding="utf-8")
                archivo.write(contenido)
                archivo.close()
                messagebox.showinfo("Mensaje", "El archivo de la nómina Nómina.txt se ha creado en " + carpeta)
            except Exception as e:
                print(e)
                messagebox.showerror("Error", "No se pudo guardar el archivo")


if __name__ == "__main__":
    miVentanaPrincipal = VentanaPrincipal()
    miVentanaPrincipal.mainloop()