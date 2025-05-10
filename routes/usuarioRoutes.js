const express = require('express');
const router = express.Router();
const usuarioController = require('../controllers/usuarioController');

router.post('/login', usuarioController.login);
router.post('/crear', usuarioController.crear);
router.put('/editar/:id', usuarioController.editar);
router.delete('/eliminar/:id', usuarioController.eliminar);

module.exports = router;
