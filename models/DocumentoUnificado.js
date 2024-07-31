const mongoose = require('mongoose');

const VotacionSchema = new mongoose.Schema({
  // Define los campos específicos de votaciones aquí
});

const DocumentoUnificadoSchema = new mongoose.Schema({
  boletin: String,
  fecha: Date,
  votaciones: [VotacionSchema]
});

module.exports = mongoose.model('DocumentoUnificado', DocumentoUnificadoSchema);