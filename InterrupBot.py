import network, time, urequests
from machine import Pin, PWM, ADC
from utelegram import Bot

token = '5277477910:AAFs2hl2PfarI0dwV4DHpXdRsXj1-wEaUQ8'
bot = Bot (token)
servomotor = PWM (Pin (13), freq=50)
ldr = ADC (Pin (36))
ldr.atten (ADC.ATTN_11DB)
ldr.width (ADC.WIDTH_12BIT)

def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():
          miRed.active(True)
          miRed.connect(red, password)
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True

if conectaWifi ("TIGO-4F85", "2NB112101412"):
    print ("¡Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
      
    @bot.add_message_handler ('Hola')
    def saludo (update):
        update.reply ('¡Hola! Bienvenido al bot de InterrupBot' '\n'
        '¡Escribe Menú para desplegar las opciones!')
        
    @bot.add_message_handler ('Menú')
    def menu (update):
        update.reply ('¡Hola! Bienvenido al menú de InterrupBot' '\n'
        '1) Escribir Sensor para saber si está de día o de noche.' '\n'
        '2) Escribir On para encender la luz.''\n'
        '3) Escribir Off para apagar la luz.' '\n')

    def map (x):
        return int ((x - 0) * (130-34) / (180 - 0) + 34)
    
    @bot.add_message_handler ('Sensor')
    def lectura_ldr (update):
        lectura = ldr.read ()
        print (lectura)
        if lectura > 1023:
            update.reply ('Es de noche')
            m = map (0)
            servomotor.duty (m)
            
        if lectura < 1023:
            update.reply ('Es de día')
            m = map(180)
            servomotor.duty (m)

    
    @bot.add_message_handler ('On')
    def on (update):
        update.reply ('Luz encendida')
        m = map(0)
        servomotor.duty(m)

    @bot.add_message_handler ('Off')
    def off (update):
        update.reply ('Luz apagada')
        m = map (180)
        servomotor.duty (m)
        
    bot.start_loop ()