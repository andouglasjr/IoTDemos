import express from "express";

const app = express();
const port = 3000;

app.get('/', (req, res) => {
	res.json({'Aplication':'IoT', 'Temperatura':Math.random()*100, 'Umidade':Math.random()*80});	
});

app.get('/temperatura', (req, res) => {
	res.send('20°C');
});

app.listen(port, () => {
	console.log('Servidor rodando na porta ${port}');
});


