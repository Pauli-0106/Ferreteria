const UsuarioModel = require('../models/usuarioModel');

exports.login = (req, res) => {
  const { username, password } = req.body;
  UsuarioModel.verificarCredenciales(username, password, (err, results) => {
    if (err) return res.status(500).json({ error: 'Error en la base de datos' });
    if (results.length > 0) {
      return res.status(200).json({ message: 'Login correcto', usuario: results[0] });
    } else {
      return res.status(401).json({ error: 'Credenciales incorrectas' });
    }
  });
};

exports.crear = (req, res) => {
  const usuario = req.body;
  UsuarioModel.crearUsuario(usuario, (err, insertId) => {
    if (err) return res.status(500).json({ error: 'Error al crear usuario' });
    res.status(201).json({ message: 'Usuario creado', id: insertId });
  });
};

exports.editar = (req, res) => {
  const id = req.params.id;
  const usuario = req.body;
  UsuarioModel.editarUsuario(id, usuario, (err, result) => {
    if (err) return res.status(500).json({ error: 'Error al editar usuario' });
    res.status(200).json({ message: 'Usuario actualizado' });
  });
};

exports.eliminar = (req, res) => {
  const id = req.params.id;
  UsuarioModel.eliminarUsuario(id, (err, result) => {
    if (err) return res.status(500).json({ error: 'Error al eliminar usuario' });
    res.status(200).json({ message: 'Usuario eliminado' });
  });
};
