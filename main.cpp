#include "mbed.h"
#include "easy-connect.h"
#include "MQTTNetwork.h"
#include "MQTTmbed.h"
#include "MQTTClient.h"
#include <string.h>
#include "C12832.h"
#include "stm32f413h_discovery_ts.h"
#include "stm32f413h_discovery_lcd.h"

#define TEMARSS "ugradbeni/aprljaca1/"

char* novostiString;

void messageArrived(MQTT::MessageData& md)
{
    MQTT::Message &message = md.message;
    novostiString = (char*)message.payload;
}


int main(int argc, char* argv[])
{
    NetworkInterface *network;
    network = NetworkInterface::get_default_instance();
    
    if (!network) {
        return -1;
    }

    MQTTNetwork mqttNetwork(network);

    MQTT::Client<MQTTNetwork, Countdown, 1000000> client(mqttNetwork);

    const char* hostname = "broker.hivemq.com";
    int port = 1883;
    printf("Connecting to %s:%d\r\n", hostname, port);
    int rc = mqttNetwork.connect(hostname, port);
    if (rc != 0)
        printf("rc from TCP connect is %d\r\n", rc);

    MQTTPacket_connectData data = MQTTPacket_connectData_initializer;
    data.MQTTVersion = 3;
    data.clientID.cstring = "ugradbeni";
    data.username.cstring = "";
    data.password.cstring = "";
    if ((rc = client.connect(data)) != 0)
        printf("rc from MQTT connect is %d\r\n", rc);

    if ((rc = client.subscribe(TEMARSS, MQTT::QOS2, messageArrived)) != 0)
        printf("rc from MQTT subscribe is %d\r\n", rc);


    BSP_LCD_Init();
    BSP_LCD_Clear(LCD_COLOR_WHITE);
    // BSP_LCD_DisplayStringAt(10, 215, (uint8_t*)"0", LEFT_MODE);

    while(1) {
        
        
        char *novosti = strtok(novostiString, "|");
        while( novosti != NULL ) {
            printf( " %s\n", novosti ); 
            novosti = strtok(NULL, "|");
        }
        
        rc = client.subscribe(TEMARSS, MQTT::QOS0, messageArrived);
        wait(1);
    }
}
