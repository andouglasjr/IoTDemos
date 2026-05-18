#include <SPI.h>
#include <Ethernet.h>
// Atribuindo um endereço MAC ao Shield Ethernet
byte mac[] = {0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED};
// IP baseado na configuração de rede do seu roteador
byte ip[] = {192, 168, 0, 175};
// Gateway de conexão
byte gateway[] = {192, 168, 0, 1};
// Máscara de Rede
byte subnet[] = {255, 255, 255, 0};
// Inicialização do server na porta padrão 80
EthernetServer server(80);
// Pino onde o relé está conectado a placa
const int relay = 3;
// Variável para leitura da url
String readString = String(30);
void setup()
{
    // Inicia a biblioteca eo servidor
    Ethernet.begin(mac, ip, gateway, subnet);
    server.begin();
    // Inicia o pino do relé em nível baixo
    digitalWrite(relay, LOW);
}
void loop()
{
    // Cria uma conexão com o cliente
    EthernetClient client = server.available();
    // Se o cliente existe, enquanto ele estiver conectado e disponível
    if (client)
    {
        while (client.connected())
        {
            if (client.available())
            {
                // Lê o caracter da requisição HTTP
                char c = client.read();
                if (readString.length() < 100)
                {
                    // "readstring" recebe o valor da URL
                    readString += c;
                }
                // Quando encontra o "\n" significa que é o fim do cabeçalho da requisição
                if (c == '\n')
                {
                    // Procura o caracter ? para encontrar os parâmetros
                    if (readString.indexOf("?") < 0)
                    {
                    }
                    // Se relayParam=1 aciona o relé
                    else if (readString.indexOf("relayParam=1") > 0)
                    {
                        digitalWrite(relay, HIGH); // Aciona o relé
                    }
                    else
                    {
                        // Desativa o relé
                        digitalWrite(relay, LOW);
                    }
                    // Variável é reinicializada
                    readString = "";
                    //Finaliza a conexão com o cliente
                    client.stop();
                }
            }
        }
    }
}