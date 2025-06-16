import unittest
from datetime import datetime
from clinica import Paciente, Medico, Especialidad, Turno, Receta, HistoriaClinica, Clinica, PacienteYaExisteError, MedicoYaExisteError, PacienteNoExisteError, MedicoNoExisteError, TurnoDuplicadoError, RecetaInvalidaError

class TestClinica(unittest.TestCase):
    def setUp(self):
        
        self.clinica = Clinica()
        self.paciente = Paciente("Juan Perez", "12345678", "01/01/2000")
        self.medico = Medico("Dra. López", "M001")
        self.especialidad = Especialidad("Cardiología", ["lunes", "miércoles"])
        self.medico.agregar_especialidad(self.especialidad)
        self.clinica.agregar_paciente(self.paciente)
        self.clinica.agregar_medico(self.medico)

    def test_registrar_paciente_exitoso(self):
        paciente_nuevo = Paciente("Ana Díaz", "87654321", "02/02/1999")
        self.clinica.agregar_paciente(paciente_nuevo)
        self.assertIn("87654321", [p.obtener_dni() for p in self.clinica.obtener_pacientes()])

    def test_no_permite_pacientes_duplicados(self):
        with self.assertRaises(PacienteYaExisteError):
            self.clinica.agregar_paciente(self.paciente)

    def test_registrar_medico_exitoso(self):
        medico_nuevo = Medico("Dr. García", "M002")
        self.clinica.agregar_medico(medico_nuevo)
        self.assertIn("M002", [m.obtener_matricula() for m in self.clinica.obtener_medicos()])

    def test_no_permite_medicos_duplicados(self):
        with self.assertRaises(MedicoYaExisteError):
            self.clinica.agregar_medico(self.medico)

    def test_agendar_turno_exitoso(self):
        fecha = datetime(2025, 6, 16, 10, 0)
        self.clinica.agendar_turno(self.paciente.obtener_dni(), self.medico.obtener_matricula(), self.especialidad, fecha)
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 1)

    def test_no_permite_turnos_duplicados(self):
        fecha = datetime(2025, 6, 16, 10, 0)
        self.clinica.agendar_turno(self.paciente.obtener_dni(), self.medico.obtener_matricula(), self.especialidad, fecha)
        with self.assertRaises(TurnoDuplicadoError):
            self.clinica.agendar_turno(self.paciente.obtener_dni(), self.medico.obtener_matricula(), self.especialidad, fecha)

    def test_emitir_receta_exitosa(self):
        fecha = datetime(2025, 6, 16, 10, 0)
        self.clinica.agendar_turno(self.paciente.obtener_dni(), self.medico.obtener_matricula(), self.especialidad, fecha)
        self.clinica.emitir_receta(self.paciente.obtener_dni(), self.medico.obtener_matricula(), ["Ibuprofeno"])
        historia = self.clinica.obtener_historia_clinica(self.paciente.obtener_dni())
        self.assertEqual(len(historia.obtener_recetas()), 1)

    def test_emitir_receta_falla_sin_medicamentos(self):
        with self.assertRaises(RecetaInvalidaError):
            self.clinica.emitir_receta(self.paciente.obtener_dni(), self.medico.obtener_matricula(), [])


if __name__ == '__main__':
    unittest.main()
