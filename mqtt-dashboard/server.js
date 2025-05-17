const express = require('express');
const mqtt = require('mqtt');
const WebSocket = require('ws');

const app = express();
const port = 3000;

// Servir arquivos estáticos (HTML, CSS, JS)
app.use(express.static('public'));

// Iniciar o servidor HTTP
const server = app.listen(port, () => {
  console.log(`Servidor rodando em http://localhost:${port}`);
});

// Iniciar o servidor WebSocket
const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
  console.log('Cliente WebSocket conectado');

  // Conectar ao broker MQTT
  const client = mqtt.connect('mqtt://localhost');

  client.on('connect', () => {
    console.log('Conectado ao broker MQTT');
    client.subscribe('topico/teste');
  });

  client.on('message', (topic, message) => {
    console.log(`Mensagem recebida do MQTT: ${message.toString()}`);
    ws.send(message.toString());
  });

  ws.on('close', () => {
    console.log('Cliente WebSocket desconectado');
    client.end();
  });
});
