const express = require('express');
const router = express.Router();
const DocumentoUnificado = require('../models/DocumentoUnificado');

// Obtener todos los documentos
router.get('/', async (req, res) => {
  try {
    const documentos = await DocumentoUnificado.find({}, '_id boletin fecha votaciones');
    res.json(documentos);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Obtener un documento por _id
router.get('/:id', async (req, res) => {
  try {
    const documento = await DocumentoUnificado.findById(req.params.id, '_id boletin fecha votaciones');
    if (!documento) return res.status(404).json({ message: 'Documento no encontrado' });
    res.json(documento);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Otros endpoints para CRUD (Crear, Actualizar, Eliminar, etc.)

module.exports = router;