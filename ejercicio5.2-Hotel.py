import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime

class Huesped:
    def __init__(self, nombres, apellidos, documentoIdentidad):
        self.nombres = nombres
        self.apellidos = apellidos
        self.documentoIdentidad = documentoIdentidad
        self.fechaIngreso = None
        self.fechaSalida = None

    def setFechaIngreso(self, fecha):
        self.fechaIngreso = fecha

    def getFechaIngreso(self):
        return self.fechaIngreso

    def setFechaSalida(self, fecha):
        self.fechaSalida = fecha

    def obtenerDiasAlojamiento(self):
        diferencia = self.fechaSalida - self.fechaIngreso
        return diferencia.days


class Habitacion:
    def __init__(self, numeroHabitacion, disponible, precioDia):
        self.numeroHabitacion = numeroHabitacion
        self.disponible = disponible
        self.precioDia = precioDia
        self.huesped = None

    def getNumeroHabitacion(self):
        return self.numeroHabitacion

    def getDisponible(self):
        return self.disponible

    def setDisponible(self, disponible):
        self.disponible = disponible

    def getPrecioDia(self):
        return self.precioDia

    def getHuesped(self):
        return self.huesped

    def setHuesped(self, huesped):
        self.huesped = huesped


class Hotel:
    def __init__(self):
        self.listaHabitaciones = []
        for i in range(1, 11):
            if i <= 5:
                hab = Habitacion(i, True, 120000)
            else:
                hab = Habitacion(i, True, 160000)
            self.listaHabitaciones.append(hab)

    def buscarFechaIngresoHabitacion(self, numero):
        for hab in self.listaHabitaciones:
            if hab.getNumeroHabitacion() == numero:
                fecha = hab.getHuesped().getFechaIngreso()
                return fecha.strftime("%Y/%m/%d")
        return ""

    def buscarHabitacionOcupada(self, numero):
        for hab in self.listaHabitaciones:
            if hab.getNumeroHabitacion() == numero and not hab.getDisponible():
                return True
        return False


class VentanaIngreso(tk.Toplevel):
    def __init__(self, master, hotel, numeroHabitacionReservada):
        super().__init__(master)
        self.hotel = hotel
        self.numeroHabitacionReservada = numeroHabitacionReservada
        self.title("Ingreso")
        self.geometry("300x240")
        self.resizable(False, False)
        self.inicio()

    def inicio(self):
        tk.Label(self, text="Habitación: " + str(self.numeroHabitacionReservada)).grid(row=0, column=0, sticky="w", padx=8, pady=4)

        tk.Label(self, text="Fecha (aaaa-mm-dd):").grid(row=1, column=0, sticky="w", padx=8, pady=4)
        self.campoFechaIngreso = tk.Entry(self)
        self.campoFechaIngreso.grid(row=1, column=1, padx=8, pady=4)

        tk.Label(self, text="Huesped").grid(row=2, column=0, sticky="w", padx=8, pady=4)

        tk.Label(self, text="Nombre:").grid(row=3, column=0, sticky="w", padx=8, pady=4)
        self.campoNombre = tk.Entry(self)
        self.campoNombre.grid(row=3, column=1, padx=8, pady=4)

        tk.Label(self, text="Apellidos:").grid(row=4, column=0, sticky="w", padx=8, pady=4)
        self.campoApellidos = tk.Entry(self)
        self.campoApellidos.grid(row=4, column=1, padx=8, pady=4)

        tk.Label(self, text="Doc. Identidad:").grid(row=5, column=0, sticky="w", padx=8, pady=4)
        self.campoDocumento = tk.Entry(self)
        self.campoDocumento.grid(row=5, column=1, padx=8, pady=4)

        self.aceptar = tk.Button(self, text="Aceptar", command=self.registrar_ingreso)
        self.aceptar.grid(row=6, column=0, pady=12, padx=8, sticky="ew")

        self.cancelar = tk.Button(self, text="Cancelar", command=self.destroy)
        self.cancelar.grid(row=6, column=1, pady=12, padx=8, sticky="ew")

    def registrar_ingreso(self):
        for hab in self.hotel.listaHabitaciones:
            if hab.getNumeroHabitacion() == self.numeroHabitacionReservada:
                try:
                    fecha_txt = self.campoFechaIngreso.get().strip()
                    fecha = datetime.strptime(fecha_txt, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Mensaje", "La fecha no está en el formato solicitado", parent=self)
                    return

                try:
                    nom = self.campoNombre.get().strip()
                    ape = self.campoApellidos.get().strip()
                    doc = int(self.campoDocumento.get().strip())
                    if nom == "" or ape == "":
                        raise Exception("vacio")

                    huesped = Huesped(nom, ape, doc)
                    huesped.setFechaIngreso(fecha)
                    hab.setHuesped(huesped)
                    hab.setDisponible(False)

                    messagebox.showinfo("Mensaje", "El huésped ha sido registrado", parent=self)
                    self.destroy()
                    break
                except:
                    messagebox.showerror("Error", "Campo nulo o error en formato de numero", parent=self)
                    return


class VentanaHabitaciones(tk.Toplevel):
    def __init__(self, master, hotel):
        super().__init__(master)
        self.hotel = hotel
        self.title("Habitaciones")
        self.geometry("720x230")
        self.resizable(False, False)
        self.inicio()

    def inicio(self):
        for i in range(10):
            hab = self.hotel.listaHabitaciones[i]
            if i < 5:
                x_pos = 20 + (i * 140)
                y_pos = 25
            else:
                x_pos = 20 + ((i - 5) * 140)
                y_pos = 100

            tk.Label(self, text="Habitación " + str(hab.getNumeroHabitacion())).place(x=x_pos, y=y_pos)
            estado = "Disponible" if hab.getDisponible() else "No disponible"
            tk.Label(self, text=estado).place(x=x_pos, y=y_pos + 22)

        tk.Label(self, text="Habitación a reservar:").place(x=220, y=175)
        self.campoHabitacion = tk.Spinbox(self, from_=1, to=10)
        self.campoHabitacion.place(x=360, y=175, width=45)

        self.botonAceptar = tk.Button(self, text="Aceptar", command=self.seleccionar_habitacion)
        self.botonAceptar.place(x=440, y=172, width=90)

    def seleccionar_habitacion(self):
        try:
            num = int(self.campoHabitacion.get())
            if num < 1 or num > 10:
                messagebox.showerror("Error", "Numero de habitacion invalido", parent=self)
                return

            if not self.hotel.buscarHabitacionOcupada(num):
                VentanaIngreso(self.master, self.hotel, num)
                self.destroy()
            else:
                messagebox.showinfo("Mensaje", "La habitación está ocupada", parent=self)
        except:
            messagebox.showerror("Error", "Ingrese un numero valido", parent=self)


class VentanaSalida(tk.Toplevel):
    def __init__(self, master, hotel, numero):
        super().__init__(master)
        self.hotel = hotel
        self.numeroHabitacion = numero
        self.habitacionOcupada = None
        self.title("Salida huéspedes")
        self.geometry("270x260")
        self.resizable(False, False)
        self.inicio()

    def inicio(self):
        tk.Label(self, text="Habitación: " + str(self.numeroHabitacion)).grid(row=0, column=0, sticky="w", padx=12, pady=4)

        fecha = self.hotel.buscarFechaIngresoHabitacion(self.numeroHabitacion)
        tk.Label(self, text="Fecha de ingreso: " + fecha).grid(row=1, column=0, sticky="w", padx=12, pady=4)

        tk.Label(self, text="Fecha de salida (aaaa-mm-dd):").grid(row=2, column=0, sticky="w", padx=12, pady=4)
        self.campoFechaSalida = tk.Entry(self)
        self.campoFechaSalida.grid(row=3, column=0, sticky="ew", padx=12, pady=4)

        self.calcular = tk.Button(self, text="Calcular", command=self.calcular_pago)
        self.calcular.grid(row=4, column=0, sticky="ew", padx=12, pady=6)

        self.cantidadDias = tk.Label(self, text="Cantidad de días: ")
        self.cantidadDias.grid(row=5, column=0, sticky="w", padx=12, pady=4)

        self.totalPago = tk.Label(self, text="Total: $")
        self.totalPago.grid(row=6, column=0, sticky="w", padx=12, pady=4)

        self.registrarSalida = tk.Button(self, text="Registrar Salida", state="disabled", command=self.hacer_salida)
        self.registrarSalida.grid(row=7, column=0, sticky="ew", padx=12, pady=6)

    def calcular_pago(self):
        fechaS = self.campoFechaSalida.get().strip()
        for hab in self.hotel.listaHabitaciones:
            if hab.getNumeroHabitacion() == self.numeroHabitacion:
                self.habitacionOcupada = hab
                try:
                    fecha2 = datetime.strptime(fechaS, "%Y-%m-%d")
                    hab.getHuesped().setFechaSalida(fecha2)
                    fecha1 = hab.getHuesped().getFechaIngreso()

                    if fecha1 < fecha2:
                        cantidad = hab.getHuesped().obtenerDiasAlojamiento()
                        self.cantidadDias.config(text="Cantidad de días: " + str(cantidad))
                        valor = cantidad * hab.getPrecioDia()
                        self.totalPago.config(text="Total: $" + str(float(valor)))
                        self.registrarSalida.config(state="normal")
                    else:
                        messagebox.showerror("Mensaje", "La fecha de salida es menor que la de ingreso", parent=self)
                except ValueError:
                    messagebox.showerror("Mensaje", "La fecha no está en el formato solicitado", parent=self)
                break

    def hacer_salida(self):
        self.habitacionOcupada.setHuesped(None)
        self.habitacionOcupada.setDisponible(True)
        messagebox.showinfo("Mensaje", "Se ha registrado la salida del huésped", parent=self)
        self.destroy()


class VentanaPrincipal(tk.Tk):
    def __init__(self, hotel):
        super().__init__()
        self.hotel = hotel
        self.title("Hotel")
        self.geometry("280x350")
        self.resizable(False, False)
        self.inicio()

    def inicio(self):
        self.barraMenu = tk.Menu(self)
        self.menuOpciones = tk.Menu(self.barraMenu, tearoff=0)

        self.menuOpciones.add_command(label="Consultar habitaciones", command=self.consultar_habitaciones)
        self.menuOpciones.add_command(label="Salida de huéspedes", command=self.salida_huespedes)

        self.barraMenu.add_cascade(label="Menú", menu=self.menuOpciones)
        self.config(menu=self.barraMenu)

    def consultar_habitaciones(self):
        VentanaHabitaciones(self, self.hotel)

    def salida_huespedes(self):
        num_txt = simpledialog.askstring("Salida de huéspedes", "Ingrese número de habitación", parent=self)
        if num_txt is None:
            return
        try:
            numero = int(num_txt)
            if numero < 1 or numero > 10:
                messagebox.showinfo("Mensaje", "El número de habitación debe estar entre 1 y 10")
            elif self.hotel.buscarHabitacionOcupada(numero):
                VentanaSalida(self, self.hotel, numero)
            else:
                messagebox.showinfo("Mensaje", "La habitación ingresada no ha sido ocupada")
        except:
            messagebox.showerror("Error", "Campo nulo o error en formato de numero")


if __name__ == "__main__":
    hotel = Hotel()
    miVentanaPrincipal = VentanaPrincipal(hotel)
    miVentanaPrincipal.mainloop()