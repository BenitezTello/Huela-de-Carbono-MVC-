CREATE PROCEDURE sp_insert_emission
    @datos NVARCHAR(255),
    @fecha_monitoreo DATE,
    @id_usuario INT,
    @energia FLOAT,
    @transporte FLOAT,
    @recursos_naturales FLOAT,
    @residuos FLOAT
AS
BEGIN
    INSERT INTO Emisiones (datos, fecha_monitoreo, id_usuario, energia, transporte, recursos_naturales, residuos)
    VALUES (@datos, @fecha_monitoreo, @id_usuario, @energia, @transporte, @recursos_naturales, @residuos);
END;


CREATE PROCEDURE sp_insert_carbon_footprint
    @id_usuario INT,
    @resultado FLOAT
AS
BEGIN
    INSERT INTO Huella_Carbono (id_usuario, fecha_calculo, resultado)
    OUTPUT INSERTED.id_huella
    VALUES (@id_usuario, GETDATE(), @resultado);
END;


CREATE PROCEDURE sp_assign_project
    @id_huella INT,
    @nombre NVARCHAR(255),
    @descripcion NVARCHAR(255),
    @estado NVARCHAR(50)
AS
BEGIN
    INSERT INTO Proyectos (nombre, descripcion, estado, id_huella)
    VALUES (@nombre, @descripcion, @estado, @id_huella);
END;


CREATE PROCEDURE sp_get_carbon_footprints_by_user
    @id_usuario INT
AS
BEGIN
    SELECT id_huella, fecha_calculo, resultado
    FROM Huella_Carbono
    WHERE id_usuario = @id_usuario
    ORDER BY fecha_calculo DESC;
END;


CREATE PROCEDURE sp_get_all_carbon_footprints
AS
BEGIN
    SELECT h.id_huella, h.fecha_calculo, h.resultado, u.id AS id_usuario, u.username
    FROM Huella_Carbono h
    INNER JOIN users u ON h.id_usuario = u.id
    ORDER BY h.fecha_calculo DESC;
END;
