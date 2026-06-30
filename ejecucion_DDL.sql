CREATE DATABASE IF NOT EXISTS clinica_db DEFAULT CHARACTER SET utf8mb4;
USE clinica_db;

CREATE TABLE USUARIOS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    is_medico BOOLEAN DEFAULT FALSE,
    is_paciente BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP NULL,
    -- Auditoría
    estado_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modif INT NULL
) ENGINE=InnoDB;

CREATE TABLE CLINICAS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    calle VARCHAR(100) NOT NULL,
    num_ext VARCHAR(20) NOT NULL,
    num_int VARCHAR(20) NULL,
    colonia VARCHAR(100) NOT NULL,
    alcaldia VARCHAR(100) NOT NULL,
    estado_ciudad VARCHAR(100) NOT NULL,
    cp VARCHAR(10) NOT NULL,
    hora_apertura TIME NOT NULL,
    hora_cierre TIME NOT NULL,
    -- Auditoría
    estado_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modif INT NULL
) ENGINE=InnoDB;

CREATE TABLE PACIENTES (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT UNIQUE NOT NULL,
    nombres VARCHAR(150) NOT NULL,
    apellidos VARCHAR(150) NOT NULL,
    num_telefono VARCHAR(20) NULL,
    fecha_nacim DATE NOT NULL,
    curp VARCHAR(18) UNIQUE NOT NULL,
    calle VARCHAR(100) NOT NULL,
    num_ext VARCHAR(20) NOT NULL,
    num_int VARCHAR(20) NULL,
    colonia VARCHAR(100) NOT NULL,
    alcaldia VARCHAR(100) NOT NULL,
    estado_ciudad VARCHAR(100) NOT NULL,
    cp VARCHAR(10) NOT NULL,
    nss VARCHAR(20) UNIQUE NULL,
    tipo_sangre VARCHAR(5) NULL,
    FOREIGN KEY (usuario_id) REFERENCES USUARIOS(id) ON DELETE CASCADE,
    -- Auditoría
    estado_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modif INT NULL
) ENGINE=InnoDB;

CREATE TABLE MEDICOS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT UNIQUE NOT NULL,
    nombres VARCHAR(150) NOT NULL,
    apellidos VARCHAR(150) NOT NULL,
    num_telefono VARCHAR(20) NULL,
    cedula_profesional VARCHAR(50) UNIQUE NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES USUARIOS(id) ON DELETE CASCADE,
    -- Auditoría
    estado_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modif INT NULL
) ENGINE=InnoDB;

CREATE TABLE ESPECIALIDADES (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_especialidad VARCHAR(100) UNIQUE NOT NULL,
    -- Auditoría
    estado_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modif INT NULL
) ENGINE=InnoDB;

CREATE TABLE PADECIMIENTOS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_padecimiento VARCHAR(150) UNIQUE NOT NULL,
    -- Auditoría
    estado_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modif INT NULL
) ENGINE=InnoDB;

CREATE TABLE FARMACIAS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    calle VARCHAR(100) NOT NULL,
    num_ext VARCHAR(20) NOT NULL,
    colonia VARCHAR(100) NOT NULL,
    alcaldia VARCHAR(100) NOT NULL,
    estado_ciudad VARCHAR(100) NOT NULL,
    cp VARCHAR(10) NOT NULL,
    hora_apertura TIME NOT NULL,
    hora_cierre TIME NOT NULL,
    -- Auditoría
    estado_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modif INT NULL
) ENGINE=InnoDB;

CREATE TABLE FABRICANTES_MEDICAMENTOS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    num_telefono_contacto VARCHAR(20) NULL,
    -- Auditoría
    estado_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modif INT NULL
) ENGINE=InnoDB;

CREATE TABLE LABORATORIOS_CLINICOS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    calle VARCHAR(100) NOT NULL,
    num_ext VARCHAR(20) NOT NULL,
    colonia VARCHAR(100) NOT NULL,
    alcaldia VARCHAR(100) NOT NULL,
    estado_ciudad VARCHAR(100) NOT NULL,
    cp VARCHAR(10) NOT NULL,
    -- Auditoría
    estado_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modif INT NULL
) ENGINE=InnoDB;

CREATE TABLE MEDICO_ESPECIALIDAD (
    medico_id INT NOT NULL,
    especialidad_id INT NOT NULL,
    PRIMARY KEY (medico_id, especialidad_id),
    FOREIGN KEY (medico_id) REFERENCES MEDICOS(id) ON DELETE CASCADE,
    FOREIGN KEY (especialidad_id) REFERENCES ESPECIALIDADES(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE PACIENTE_PADECIMIENTO (
    paciente_id INT NOT NULL,
    padecimiento_id INT NOT NULL,
    PRIMARY KEY (paciente_id, padecimiento_id),
    FOREIGN KEY (paciente_id) REFERENCES PACIENTES(id) ON DELETE CASCADE,
    FOREIGN KEY (padecimiento_id) REFERENCES PADECIMIENTOS(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE MEDICAMENTOS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fabricante_id INT NOT NULL,
    nombre_generico VARCHAR(150) NOT NULL,
    nombre_comercial VARCHAR(150) NULL,
    contenido_neto VARCHAR(50) NULL,
    FOREIGN KEY (fabricante_id) REFERENCES FABRICANTES_MEDICAMENTOS(id) ON DELETE RESTRICT,
    -- Auditoría
    estado_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modif INT NULL
) ENGINE=InnoDB;

CREATE TABLE INVENTARIOS (
    farmacia_id INT NOT NULL,
    medicamento_id INT NOT NULL,
    stock_actual INT DEFAULT 0,
    precio_unitario DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (farmacia_id, medicamento_id),
    FOREIGN KEY (farmacia_id) REFERENCES FARMACIAS(id) ON DELETE CASCADE,
    FOREIGN KEY (medicamento_id) REFERENCES MEDICAMENTOS(id) ON DELETE CASCADE,
    CHECK (stock_actual >= 0),
    CHECK (precio_unitario >= 0)
) ENGINE=InnoDB;

CREATE TABLE AGENDA_MEDICOS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    medico_id INT NOT NULL,
    clinica_id INT NOT NULL,
    dia_semana INT NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    FOREIGN KEY (medico_id) REFERENCES MEDICOS(id) ON DELETE CASCADE,
    FOREIGN KEY (clinica_id) REFERENCES CLINICAS(id) ON DELETE CASCADE,
    CHECK (dia_semana BETWEEN 0 AND 6),
    -- Auditoría
    estado_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modif INT NULL
) ENGINE=InnoDB;

CREATE TABLE CITAS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    agenda_id INT NOT NULL,
    fecha_hora_timestamp TIMESTAMP NOT NULL,
    motivo TEXT NOT NULL,
    estado VARCHAR(20) DEFAULT 'Agendada',
    FOREIGN KEY (paciente_id) REFERENCES PACIENTES(id) ON DELETE CASCADE,
    FOREIGN KEY (agenda_id) REFERENCES AGENDA_MEDICOS(id) ON DELETE RESTRICT,
    CHECK (estado IN ('Agendada', 'Cancelada', 'Atendida')),
    -- Auditoría
    estado_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modif INT NULL
) ENGINE=InnoDB;

CREATE TABLE RECETAS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cita_id INT UNIQUE NOT NULL,
    fecha_emision DATE NOT NULL,
    indicaciones_generales TEXT NULL,
    FOREIGN KEY (cita_id) REFERENCES CITAS(id) ON DELETE CASCADE,
    -- Auditoría
    estado_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modif INT NULL
) ENGINE=InnoDB;

CREATE TABLE RECETA_MEDICAMENTO (
    receta_id INT NOT NULL,
    medicamento_id INT NOT NULL,
    dosis VARCHAR(100) NOT NULL,
    frecuencia VARCHAR(100) NOT NULL,
    duracion_dias INT NOT NULL,
    PRIMARY KEY (receta_id, medicamento_id),
    FOREIGN KEY (receta_id) REFERENCES RECETAS(id) ON DELETE CASCADE,
    FOREIGN KEY (medicamento_id) REFERENCES MEDICAMENTOS(id) ON DELETE RESTRICT,
    CHECK (duracion_dias > 0)
) ENGINE=InnoDB;

CREATE TABLE SOLICITUDES_ESTUDIO (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cita_id INT NOT NULL,
    laboratorio_clinico_id INT NOT NULL,
    tipo_estudio VARCHAR(150) NOT NULL,
    indicaciones TEXT NULL,
    FOREIGN KEY (cita_id) REFERENCES CITAS(id) ON DELETE CASCADE,
    FOREIGN KEY (laboratorio_clinico_id) REFERENCES LABORATORIOS_CLINICOS(id) ON DELETE RESTRICT,
    -- Auditoría
    estado_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modif INT NULL
) ENGINE=InnoDB;

-- ==========================================
-- MÓDULO DE MENSAJERÍA (CHATS)
-- ==========================================

CREATE TABLE SALAS_CHAT (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cita_id INT UNIQUE NOT NULL,
    activa BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (cita_id) REFERENCES CITAS(id) ON DELETE CASCADE,
    -- Campos de Auditoría
    estado_activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_modif TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    usuario_creacion INT NULL,
    usuario_modif INT NULL
) ENGINE=InnoDB;

CREATE TABLE MENSAJES (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sala_id INT NOT NULL,
    remitente_id INT NOT NULL,
    contenido TEXT NOT NULL,
    leido BOOLEAN DEFAULT FALSE,
    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sala_id) REFERENCES SALAS_CHAT(id) ON DELETE CASCADE,
    FOREIGN KEY (remitente_id) REFERENCES USUARIOS(id) ON DELETE CASCADE
    -- NOTA ARQUITECTÓNICA: Esta tabla omite intencionalmente los 5 campos de auditoría estándar 
    -- por ser de "Ultra Alto Volumen de Transacciones". El registro de 'fecha_envio' funge como auditoría.
) ENGINE=InnoDB;