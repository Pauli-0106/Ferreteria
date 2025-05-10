const db = require('../config/db');

const verificarCredenciales = (username, password, callback) => {
  const sql = 'SELECT * FROM Usuarios WHERE username = ? AND password = ?';
  db.query(sql, [username, password], (err, results) => {
    if (err) return callback(err);
    callback(null, results);
  });
};

const crearUsuario = (usuario, callback) => {
  const sql = `INSERT INTO Usuarios 
    (rut, username, password, nombres, ap_paterno, ap_materno, esta_suscrito, id_rol) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)`;

  const valores = [
    usuario.rut,
    usuario.username,
    usuario.password,
    usuario.nombres,
    usuario.ap_paterno,
    usuario.ap_materno,
    usuario.esta_suscrito,
    usuario.id_rol
  ];

  db.query(sql, valores, (err, result) => {
    if (err) return callback(err);
    callback(null, result.insertId);
  });
};

const editarUsuario = (id, usuario, callback) => {
  const sql = `UPDATE Usuarios 
    SET rut = ?, username = ?, password = ?, nombres = ?, ap_paterno = ?, ap_materno = ?, esta_suscrito = ?, id_rol = ? 
    WHERE id_usuario = ?`;

  const valores = [
    usuario.rut,
    usuario.username,
    usuario.password,
    usuario.nombres,
    usuario.ap_paterno,
    usuario.ap_materno,
    usuario.esta_suscrito,
    usuario.id_rol,
    id
  ];

  db.query(sql, valores, (err, result) => {
    if (err) return callback(err);
    callback(null, result);
  });
};

const eliminarUsuario = (id, callback) => {
  const sql = 'DELETE FROM Usuarios WHERE id_usuario = ?';
  db.query(sql, [id], (err, result) => {
    if (err) return callback(err);
    callback(null, result);
  });
};

module.exports = {
  verificarCredenciales,
  crearUsuario,
  editarUsuario,
  eliminarUsuario
};
