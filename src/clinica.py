from datetime import datetime

class PacienteNoExisteError(Exception): pass
class PacienteYaExisteError(Exception): pass
class MedicoNoExisteError(Exception): pass
class MedicoYaExisteError(Exception): pass
class TurnoDuplicadoError(Exception): pass
class RecetaInvalidaError(Exception): pass


class Paciente:
    def __init__(self, nombre: str, dni: str, fecha_nacimiento: str):
        self.__nombre__ = nombre
        self.__dni__ = dni
        self.__fecha_nacimiento__ = fecha_nacimiento

    def obtener_dni(self) -> str:
        return self.__dni__

    def __str__(self) -> str:
        return f"Paciente: {self.__nombre__} (DNI: {self.__dni__}) - Nacimiento: {self.__fecha_nacimiento__}"

class Medico:
    def __init__(self, nombre: str, matricula: str):
        self.__nombre__ = nombre
        self.__matricula__ = matricula
        self.__especialidades__ = []  # Lista de Especialidad

    def agregar_especialidad(self, especialidad):
        self.__especialidades__.append(especialidad)

    def obtener_matricula(self) -> str:
        return self.__matricula__

    def obtener_especialidad_para_dia(self, dia: str) -> str | None:
        for especialidad in self.__especialidades__:
            if especialidad.verificar_dia(dia):
                return especialidad.obtener_especialidad()
        return None

    def __str__(self) -> str:
        especialidades_str = ", ".join([str(esp) for esp in self.__especialidades__])
        return f"Medico: {self.__nombre__} (Matrícula: {self.__matricula__}) - Especialidades: {especialidades_str}"

class Especialidad:
    def __init__(self, tipo: str, dias: list[str]):
        self.__tipo__ = tipo
        self.__dias__ = [d.lower() for d in dias]  # Guarda todos los días en minúsculas

    def obtener_especialidad(self) -> str:
        return self.__tipo__

    def verificar_dia(self, dia: str) -> bool:
        # Devuelve True si la especialidad está disponible ese día
        return dia.lower() in self.__dias__

    def __str__(self) -> str:
        dias_str = ", ".join(self.__dias__)
        return f"{self.__tipo__} (Días: {dias_str})"

class Turno:
    def __init__(self, paciente, medico, especialidad, fecha_hora: datetime):
        self.__paciente__ = paciente          
        self.__medico__ = medico              
        self.__especialidad__ = especialidad  
        self.__fecha_hora__ = fecha_hora      
    def obtener_medico(self):
        return self.__medico__

    def obtener_fecha_hora(self):
        return self.__fecha_hora__

    def __str__(self):
        fecha_str = self.__fecha_hora__.strftime("%d/%m/%Y %H:%M")
        return (f"Turno: {self.__paciente__} | "
                f"{self.__medico__} | "
                f"Especialidad: {self.__especialidad__} | "
                f"Fecha y hora: {fecha_str}")
    

class Receta:
    def __init__(self, paciente, medico, medicamentos: list[str], fecha: datetime = None):
        self.__paciente__ = paciente       
        self.__medico__ = medico            
        self.__medicamentos__ = medicamentos  
        self.__fecha__ = fecha if fecha else datetime.now()

    def __str__(self):
        fecha_str = self.__fecha__.strftime("%d/%m/%Y")
        meds_str = ", ".join(self.__medicamentos__)
        return (f"Receta [{fecha_str}]: {meds_str} - "
                f"Prescrita por {self.__medico__.__nombre__} para {self.__paciente__.__nombre__}")


class HistoriaClinica:
    def __init__(self, paciente):
        self.__paciente__ = paciente
        self.__turnos__ = []  
        self.__recetas__ = []  

    def agregar_turno(self, turno):
        self.__turnos__.append(turno)

    def agregar_receta(self, receta):
        self.__recetas__.append(receta)

    def obtener_turnos(self):
        # Devuelve una copia de la lista de turnos
        return self.__turnos__[:]

    def obtener_recetas(self):
        # Devuelve una copia de la lista de recetas
        return self.__recetas__[:]

    def __str__(self):
        turnos_str = "\n  ".join([str(turno) for turno in self.__turnos__]) if self.__turnos__ else "Sin turnos"
        recetas_str = "\n  ".join([str(receta) for receta in self.__recetas__]) if self.__recetas__ else "Sin recetas"
        return (f"Historia Clínica de {self.__paciente__.__nombre__}:\n"
                f"Turnos:\n  {turnos_str}\nRecetas:\n  {recetas_str}")


class Clinica:
    def __init__(self):
        self.__pacientes__ = {}            
        self.__medicos__ = {}              
        self.__turnos__ = []               
        self.__historias_clinicas__ = {}   
        pass
 
    def obtener_dia_semana_en_espanol(self, fecha_hora):
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        return dias[fecha_hora.weekday()]
    
    def agregar_paciente(self, paciente: Paciente):
        dni = paciente.obtener_dni()
        if dni in self.__pacientes__:
            raise PacienteYaExisteError("Ya existe un paciente con ese DNI.")
        self.__pacientes__[dni] = paciente
        self.__historias_clinicas__[dni] = HistoriaClinica(paciente)

    def obtener_pacientes(self):
        return list(self.__pacientes__.values())


    def agregar_medico(self, medico: Medico):
        matricula = medico.obtener_matricula()
        if matricula in self.__medicos__:
            raise MedicoYaExisteError("Ya existe un médico con esa matrícula.")
        self.__medicos__[matricula] = medico

    def obtener_medicos(self):
        return list(self.__medicos__.values())

    def obtener_medico_por_matricula(self, matricula: str):
        if matricula not in self.__medicos__:
            raise MedicoNoExisteError("No existe médico con esa matrícula.")
        return self.__medicos__[matricula]


    def agendar_turno(self, dni: str, matricula: str, especialidad: Especialidad, fecha_hora: datetime):

        if dni not in self.__pacientes__:
            raise PacienteNoExisteError("No existe paciente con ese DNI.")
        if matricula not in self.__medicos__:
            raise MedicoNoExisteError("No existe médico con esa matrícula.")

        for turno in self.__turnos__:
            if (turno.obtener_medico().obtener_matricula() == matricula and
                    turno.obtener_fecha_hora() == fecha_hora):
                raise TurnoDuplicadoError("Ya existe un turno con ese médico en esa fecha y hora.")

        medico = self.__medicos__[matricula]
        paciente = self.__pacientes__[dni]

        dia_semana = self.obtener_dia_semana_en_espanol(fecha_hora)

        if not medico.obtener_especialidad_para_dia(dia_semana):
            raise Exception("El médico no atiende esa especialidad ese día.")

        turno = Turno(paciente, medico, especialidad, fecha_hora)
        self.__turnos__.append(turno)
        self.__historias_clinicas__[dni].agregar_turno(turno)

    def obtener_turnos(self):
        return self.__turnos__[:]

    def emitir_receta(self, dni: str, matricula: str, medicamentos: list[str]):
        if dni not in self.__pacientes__:
            raise PacienteNoExisteError("No existe paciente con ese DNI.")
        if matricula not in self.__medicos__:
            raise MedicoNoExisteError("No existe médico con esa matrícula.")
        if not medicamentos:
            raise RecetaInvalidaError("Debe indicar al menos un medicamento.")
        paciente = self.__pacientes__[dni]
        medico = self.__medicos__[matricula]
        receta = Receta(paciente, medico, medicamentos)
        self.__historias_clinicas__[dni].agregar_receta(receta)

    def obtener_historia_clinica(self, dni: str):
        if dni not in self.__historias_clinicas__:
            raise PacienteNoExisteError("No existe paciente con ese DNI.")
        return self.__historias_clinicas__[dni]

class CLI:
    def __init__(self):
        self.clinica = Clinica()

    def mostrar_menu(self):
        print("\n--- Menú Clínica ---")
        print("1) Agregar paciente")
        print("2) Agregar médico")
        print("3) Agendar turno")
        print("4) Agregar especialidad a médico")
        print("5) Emitir receta")
        print("6) Ver historia clínica")
        print("7) Ver todos los turnos")
        print("8) Ver todos los pacientes")
        print("9) Ver todos los médicos")
        print("0) Salir")

    def ejecutar(self):
        while True:
            self.mostrar_menu()
            opcion = input("Elija una opción: ").strip()
            if opcion == "1":
                self.agregar_paciente()
            elif opcion == "2":
                self.agregar_medico()
            elif opcion == "3":
                self.agendar_turno()
            elif opcion == "4":
                self.agregar_especialidad_a_medico()
            elif opcion == "5":
                self.emitir_receta()
            elif opcion == "6":
                self.ver_historia_clinica()
            elif opcion == "7":
                self.ver_todos_los_turnos()
            elif opcion == "8":
                self.ver_todos_los_pacientes()
            elif opcion == "9":
                self.ver_todos_los_medicos()
            elif opcion == "0":
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida. Intente de nuevo.")

    def agregar_paciente(self):
        try:
            nombre = input("Nombre completo: ")
            dni = input("DNI: ")
            fecha_nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ")
            paciente = Paciente(nombre, dni, fecha_nacimiento)
            self.clinica.agregar_paciente(paciente)
            print("Paciente agregado correctamente.")
        except Exception as e:
            print(f"Error: {e}")

    def agregar_medico(self):
        try:
            nombre = input("Nombre completo: ")
            matricula = input("Matrícula: ")
            medico = Medico(nombre, matricula)
            self.clinica.agregar_medico(medico)
            print("Médico agregado correctamente.")
        except Exception as e:
            print(f"Error: {e}")

    def agendar_turno(self):
        try:
            dni = input("DNI del paciente: ")
            matricula = input("Matrícula del médico: ")
            tipo = input("Especialidad: ")
            dias = []  
            especialidad = Especialidad(tipo, dias)
            fecha_str = input("Fecha y hora (dd/mm/aaaa HH:MM): ")
            fecha_hora = datetime.strptime(fecha_str, "%d/%m/%Y %H:%M")
            self.clinica.agendar_turno(dni, matricula, especialidad, fecha_hora)
            print("Turno agendado correctamente.")
        except Exception as e:
            print(f"Error: {e}")

    def agregar_especialidad_a_medico(self):
        try:
            matricula = input("Matrícula del médico: ")
            tipo = input("Nombre de la especialidad: ")
            print("Días de atención (uno por línea, vacío para terminar):")
            dias = []
            while True:
                dia = input("Día: ").strip()
                if dia == "":
                    break
                dias.append(dia)
            especialidad = Especialidad(tipo, dias)
            medico = self.clinica.obtener_medico_por_matricula(matricula)
            medico.agregar_especialidad(especialidad)
            print("Especialidad agregada correctamente.")
        except Exception as e:
            print(f"Error: {e}")

    def emitir_receta(self):
        try:
            dni = input("DNI del paciente: ")
            matricula = input("Matrícula del médico: ")
            medicamentos_str = input("Medicamentos (separados por coma): ")
            medicamentos = [med.strip() for med in medicamentos_str.split(",") if med.strip()]
            self.clinica.emitir_receta(dni, matricula, medicamentos)
            print("Receta emitida correctamente.")
        except Exception as e:
            print(f"Error: {e}")

    def ver_historia_clinica(self):
        try:
            dni = input("DNI del paciente: ")
            historia = self.clinica.obtener_historia_clinica(dni) # Llamada al método correcto
            print(historia)
        except Exception as e:
            print(f"Error: {e}")

    def ver_todos_los_turnos(self):
        turnos = self.clinica.obtener_turnos()
        if turnos:
            for turno in turnos:
                print(turno)
        else:
            print("No hay turnos registrados.")

    def ver_todos_los_pacientes(self): 
        pacientes = self.clinica.obtener_pacientes() # Llamada al método correcto
        if pacientes:
            for paciente in pacientes:
                print(paciente)
        else:
            print("No hay pacientes registrados.")

    def ver_todos_los_medicos(self):
        medicos = self.clinica.obtener_medicos() # Llamada al método correcto
        if medicos:
            for medico in medicos:
                print(medico)
        else:
            print("No hay médicos registrados.")

if __name__ == "__main__":
    cli = CLI()
    cli.ejecutar()
