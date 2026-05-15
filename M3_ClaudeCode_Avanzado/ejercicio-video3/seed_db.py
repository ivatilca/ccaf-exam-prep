#!/usr/bin/env python3
"""Crea y pobla la base de datos rebel_ops.db para la demo."""
import sqlite3

conn = sqlite3.connect('rebel_ops.db')

conn.executescript("""
CREATE TABLE IF NOT EXISTS missions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    status TEXT,
    priority TEXT
);

CREATE TABLE IF NOT EXISTS agents (
    id INTEGER PRIMARY KEY,
    codename TEXT,
    status TEXT,
    mission_id INTEGER
);

CREATE TABLE IF NOT EXISTS resources (
    id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,
    available INTEGER
);

DELETE FROM missions;
DELETE FROM agents;
DELETE FROM resources;

INSERT INTO missions VALUES
(1,'Operacion Alba','activa','alta'),
(2,'Proyecto Nexus','activa','alta'),
(3,'Mision Sombra','completada','media'),
(4,'Operacion Tormenta','activa','critica'),
(5,'Plan Fenix','en_espera','baja'),
(6,'Operacion Escudo','activa','alta'),
(7,'Mision Centinela','activa','media'),
(8,'Proyecto Hidra','cancelada','alta'),
(9,'Operacion Eco','activa','media'),
(10,'Plan Quimera','activa','critica'),
(11,'Mision Lazaro','completada','alta'),
(12,'Operacion Vortex','activa','alta'),
(13,'Proyecto Atlas','en_espera','media'),
(14,'Operacion Relámpago','activa','critica');

INSERT INTO agents VALUES
(1,'Falcon','activo',1),
(2,'Viper','activo',2),
(3,'Ghost','inactivo',NULL),
(4,'Storm','activo',4),
(5,'Raven','activo',10);

INSERT INTO resources VALUES
(1,'Servidor Alpha','infraestructura',1),
(2,'Base de datos principal','infraestructura',1),
(3,'Canal seguro','comunicaciones',0),
(4,'Vehiculo de extraccion','transporte',1);
""")

conn.commit()
conn.close()
print("DB creada: rebel_ops.db con 14 misiones, 5 agentes, 4 recursos.")
