-- ====================================================================
-- EcoLogistica Lima - Esquema de base de datos PostgreSQL
-- Generado automaticamente desde los modelos SQLAlchemy. NO editar a mano.
-- Fuente: src/backend/app/models/__init__.py
-- Motor objetivo: PostgreSQL 16
-- ====================================================================

CREATE TABLE parametros_vehiculo (
	id_vehiculo SERIAL NOT NULL, 
	placa VARCHAR(20) NOT NULL, 
	capacidad_kg DECIMAL(10, 3) NOT NULL, 
	factor_emision_co2 DECIMAL(6, 3) NOT NULL, 
	consumo_litros_km DECIMAL(6, 3) NOT NULL, 
	velocidad_promedio_kmh DECIMAL(6, 2) NOT NULL, 
	tipo_combustible VARCHAR(30) NOT NULL, 
	PRIMARY KEY (id_vehiculo), 
	UNIQUE (placa)
);

CREATE TABLE roles (
	id_rol SERIAL NOT NULL, 
	nombre VARCHAR(50) NOT NULL, 
	descripcion VARCHAR(255), 
	PRIMARY KEY (id_rol), 
	UNIQUE (nombre)
);

CREATE TABLE usuarios (
	id_usuario UUID NOT NULL, 
	nombre VARCHAR(100) NOT NULL, 
	correo VARCHAR(150) NOT NULL, 
	contrasena_hash VARCHAR(255) NOT NULL, 
	id_rol INTEGER NOT NULL, 
	fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	PRIMARY KEY (id_usuario), 
	UNIQUE (correo), 
	FOREIGN KEY(id_rol) REFERENCES roles (id_rol)
);

CREATE TABLE puntos_entrega (
	id_punto UUID NOT NULL, 
	direccion VARCHAR(255) NOT NULL, 
	latitud DECIMAL(10, 7) NOT NULL, 
	longitud DECIMAL(10, 7) NOT NULL, 
	peso_kg DECIMAL(10, 3) NOT NULL, 
	destinatario VARCHAR(150) NOT NULL, 
	id_operador UUID NOT NULL, 
	fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	PRIMARY KEY (id_punto), 
	FOREIGN KEY(id_operador) REFERENCES usuarios (id_usuario)
);

CREATE TABLE rutas (
	id_ruta UUID NOT NULL, 
	id_operador UUID NOT NULL, 
	id_vehiculo INTEGER NOT NULL, 
	distancia_total_km DECIMAL(10, 3) NOT NULL, 
	tiempo_estimado_min DECIMAL(10, 2) NOT NULL, 
	co2_estimado_kg DECIMAL(10, 3) NOT NULL, 
	distancia_sin_optimizar_km DECIMAL(10, 3) NOT NULL, 
	tiempo_sin_optimizar_min DECIMAL(10, 2) NOT NULL, 
	co2_sin_optimizar_kg DECIMAL(10, 3) NOT NULL, 
	estado VARCHAR(20) NOT NULL, 
	fecha_generacion TIMESTAMP WITH TIME ZONE DEFAULT now(), 
	PRIMARY KEY (id_ruta), 
	FOREIGN KEY(id_operador) REFERENCES usuarios (id_usuario), 
	FOREIGN KEY(id_vehiculo) REFERENCES parametros_vehiculo (id_vehiculo)
);

CREATE TABLE ruta_puntos (
	id_ruta_punto UUID NOT NULL, 
	id_ruta UUID NOT NULL, 
	id_punto UUID NOT NULL, 
	orden INTEGER NOT NULL, 
	PRIMARY KEY (id_ruta_punto), 
	CONSTRAINT uq_ruta_puntos_orden UNIQUE (id_ruta, orden), 
	CONSTRAINT ck_orden_positivo CHECK (orden > 0), 
	FOREIGN KEY(id_ruta) REFERENCES rutas (id_ruta), 
	FOREIGN KEY(id_punto) REFERENCES puntos_entrega (id_punto)
);
