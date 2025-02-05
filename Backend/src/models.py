from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.config.db import Base

class empresa_principal(Base):
    __tablename__ = "empresa_principal"

    id_emp_pri = Column(Integer, primary_key=True, index=True)
    rut_emp_pri = Column(String(25), unique=True, index=True)
    nombre_emp_pri = Column(String(255))
    correo_emp_pri = Column(String(255))
    status_emp_pri = Column(Integer)

    # Relación con empresas_unidas
    empresas_unidas = relationship("empresas_unidas", backref="empresa_principal_rel", cascade="all, delete-orphan")


class empresa_contratista(Base):
    __tablename__ = "empresa_contratista"

    id_emp_con = Column(Integer, primary_key=True, index=True)
    rut_emp_con = Column(String(25), unique=True, index=True)
    nombre_emp_con = Column(String(255))
    correo_emp_con = Column(String(255))
    status_emp_con = Column(Integer)

    # Relación con empresas_unidas
    empresas_unidas = relationship("empresas_unidas", backref="empresa_contratista_rel", cascade="all, delete-orphan")


class empresa_subcontratista(Base):
    __tablename__ = "empresa_subcontratista"

    id_emp_subcon = Column(Integer, primary_key=True, index=True)
    rut_emp_subcon = Column(String(25), unique=True, index=True)
    nombre_emp_subcon = Column(String(255))
    correo_emp_subcon = Column(String(255))
    status_emp_subcon = Column(Integer)

    # Relación con empresas_unidas
    empresas_unidas = relationship("empresas_unidas", backref="empresa_subcontratista_rel", cascade="all, delete-orphan")


class empresas_unidas(Base):
    __tablename__ = "empresas_unidas"

    id_emp_uni = Column(Integer, primary_key=True, index=True)
    rut_emp_pri = Column(String(25), ForeignKey("empresa_principal.rut_emp_pri"))
    rut_emp_con = Column(String(25), ForeignKey("empresa_contratista.rut_emp_con"))
    rut_emp_subcon = Column(String(25), ForeignKey("empresa_subcontratista.rut_emp_subcon"), nullable=True)

    # Relaciones con las empresas
    empresa_principal = relationship("empresa_principal", backref="empresas_unidas_principal", uselist=False)
    empresa_contratista = relationship("empresa_contratista", backref="empresas_unidas_contratista", uselist=False)
    empresa_subcontratista = relationship("empresa_subcontratista", backref="empresas_unidas_subcontratista", uselist=False)


class periodo(Base):
    __tablename__ = 'periodo'

    id_periodo = Column(Integer, primary_key=True, autoincrement=True, comment='ID PERIODO')
    mesanio_periodo = Column(Integer, nullable=False, comment='ANIO Y MES EJEM 202404')
    minimo_imponible_periodo = Column(Integer, nullable=False, comment='MINIMO IMPONIBLE POR PERIODOS')
    maximo_imponible_periodo = Column(Integer, nullable=False, comment='MAXIMO IMPONIBLE POR PERIODOS')
    status_periodo = Column(Integer, nullable=False, comment='0 DESACTIVADO 1 ACTIVADO')

    # Relación con solicitudes
    solicitudes = relationship("solicitud", backref="periodo_rel")


class solicitud(Base):
    __tablename__ = 'solicitud'

    id_sol = Column(Integer, primary_key=True, autoincrement=True, comment='ID SOLICITUD')
    id_emp_uni = Column(Integer, ForeignKey('empresas_unidas.id_emp_uni'), nullable=False, comment='ID EMPRESAS UNIDAS')
    nombre_contrato_sol = Column(String(255), nullable=False, comment='NOMBRE CONTRATO PROYECTO SOLICITUD')
    cant_trab_acreditar_sol = Column(Integer, nullable=False, comment='CANTIDAD TRABAJADORES CERTIFICAR SOLICITUD')
    total_trab_sol = Column(Integer, nullable=False, comment='CANTIDAD TOTALES DE LA EMPRESA')
    estado_certificacion_sol = Column(Enum('Ingresado', 'Solicitado', 'Aprobado', 'No Aprobado', 'Certificado', 
                                           'Documentado', 'Histórico', 'Completo', 'En Proceso', 'No Conforme', 
                                           'Inactivo', 'No certificado'), nullable=False, 
                                      comment='ESTADO CERTIFICACION')
    id_periodo = Column(Integer, ForeignKey('periodo.id_periodo'), nullable=False, comment='ID PERIODO')

    # Relaciones con Periodo y EmpresasUnidas
    periodo = relationship('periodo', backref='solicitudes_periodo')
    empresa_unida = relationship('empresas_unidas', backref='solicitudes_empresau')


class trabajadores(Base):
    __tablename__ = 'trabajadores'

    id_trabajador = Column(Integer, primary_key=True, autoincrement=True, comment='ID TRABAJADOR')
    rut_trabajador = Column(String(25), nullable=False, comment='RUT TRABAJADOR')
    nombre_trabajador = Column(String(25), nullable=False, comment='NOMBRE TRABAJADOR')
    apaterno_trabajador = Column(String(25), nullable=False, comment='APELLIDO PATERNO TRABAJADOR')
    amaterno_trabajador = Column(String(25), nullable=False, comment='APELLIDO MATERNO TRABAJADOR')
    id_sol = Column(Integer, ForeignKey('solicitud.id_sol'), nullable=False, comment='ID SOLICITUD')

    # Relación con Solicitud
    solicitud = relationship('solicitud', backref='trabajadores')
