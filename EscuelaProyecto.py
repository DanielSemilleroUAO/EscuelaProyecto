# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 22:07:16 2020

@author: danie
"""

import csv
import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Time, Sequence
from sqlalchemy.orm import sessionmaker

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import exists


Base = declarative_base()


class Curso(Base):
    __tablename__ = 'curso'

    id = Column(Integer, Sequence('author_id_seq'), primary_key=True)
    nombre = Column(String)

    estudiante = relationship('Estudiante', order_by='Estudiante.id', back_populates='curso')
    curso_horario = relationship('Horario', order_by='Horario.hora_inicio', back_populates='curso')

    def __repr__(self):
        return "{} {}".format(self.nombre)


class Estudiante(Base):
    __tablename__ = 'estudiante'

    id = Column(Integer, Sequence('author_id_seq'), primary_key=True)
    nombre = Column(String)
    apellidos = Column(String)
    curso_id = Column(Integer, ForeignKey('curso.id'))

    curso = relationship('Curso', back_populates='estudiante')

    def __repr__(self):
        return "{} {}".format(self.nombre, self.apellidos)


class Profesor(Base):
    __tablename__ = 'profesor'

    id = Column(Integer, Sequence('author_id_seq'), primary_key=True)
    nombre = Column(String)
    apellidos = Column(String)

    profesor_horario = relationship('Horario', order_by='Horario.hora_inicio', back_populates='profesor')

    def __repr__(self):
        return "{} {}".format(self.nombre, self.apellidos)


class Horario(Base):
    __tablename__ = 'horario'
    
    id = Column(Integer, Sequence('author_id_seq'), primary_key=True)
    dia = Column(Integer)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    curso_id = Column(Integer, ForeignKey('curso.id'))
    profesor_id = Column(Integer, ForeignKey('profesor.id'))

    curso = relationship('Curso', back_populates='curso_horario')
    profesor = relationship('Profesor', back_populates='profesor_horario')

    def __repr__(self):
        return "{} {}".format(self.nombre)


class ReporteCurso(object):

    def __init__(self, path):
        self.path = path

    def export(self, curso):
        estudiantes = curso.estudiante
        with open(self.path, 'w') as a_file:
            writer = csv.writer(a_file)
            for estudiantes in estudiantes:
                writer.writerow([str(estudiantes)])


class ReporteHorarioCursos(object):

    def __init__(self, path):
        self.path = path

    def export(self, curso):
        horarios = curso.curso_horario
        with open(self.path, 'w') as a_file:
            writer = csv.writer(a_file)
            for horario in horarios:
                writer.writerow([horario.dia, horario.hora_inicio, horario.hora_fin, horario.profesor])


class ReporteProfesorHorario(object):
    
    def __init__(self, path):
        self.path = path

    def export(self, profesor):
        horarios = profesor.profesor_horario
        with open(self.path, 'w') as a_file:
            writer = csv.writer(a_file)
            for horario in horarios:
                writer.writerow([horario.dia, horario.hora_inicio, horario.hora_fin, horario.curso.nombre])


def main(*args, **kwargs):
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    curso_uno = Curso(nombre='1')
    curso_dos = Curso(nombre='2')

    estudiante_uno = Estudiante(nombre='Daniel', apellidos='Delgado', curso=curso_uno)
    estudiante_dos = Estudiante(nombre='Jorge', apellidos='Pinzón', curso=curso_dos)
    estudiante_tres = Estudiante(nombre='Jennifer', apellidos='Estrella', curso=curso_uno)

    profesor_uno = Profesor(nombre='Daniel', apellidos='Jimnes')

    horario_uno = datetime.time(8, 0, 0)
    horario_dos = datetime.time(10, 0, 0)
    horario_tres = datetime.time(12, 0, 0)

    horario_primero = Horario(dia=1, hora_inicio=horario_uno, hora_fin=horario_dos, curso=curso_uno, profesor=profesor_uno)
    horario_segundo = Horario(dia=1, hora_inicio=horario_dos, hora_fin=horario_tres,curso=curso_dos, profesor=profesor_uno)
    
    session.add(curso_uno)
    session.add(curso_dos)

    session.add(estudiante_uno)
    session.add(estudiante_dos)
    session.add(estudiante_tres)

    session.add(profesor_uno)

    session.add(horario_primero)
    session.add(horario_segundo)

    session.commit()

    ReporteCurso('curso_{}.csv'.format(curso_uno.nombre)).export(curso_uno)
    ReporteCurso('curso_{}.csv'.format(curso_dos.nombre)).export(curso_dos)

    ReporteHorarioCursos('horario_curso_{}.csv'.format(curso_uno.nombre)).export(curso_uno)
    ReporteHorarioCursos('horario_curso_{}.csv'.format(curso_dos.nombre)).export(curso_dos)

    ReporteProfesorHorario('horario_profesor_{}.csv'.format(profesor_uno)).export(profesor_uno)


if __name__ == "__main__":
    main()