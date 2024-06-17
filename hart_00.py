import serial
import time
import matplotlib.pyplot as plt

def communicate_with_device():
    responses = []

    try:
        # Open the serial port
        ser = serial.Serial(
            port='COM1',         # COM port name
            baudrate=2400,       # Baud rate
            bytesize=serial.EIGHTBITS,  # Data bits
            parity=serial.PARITY_NONE,  # No parity
            stopbits=serial.STOPBITS_ONE, # Stop bits
            timeout=2            # Timeout for read
        )

        # Ensure the port is open
        if ser.isOpen():
            print("Serial port opened successfully.")
        
            # Initialize and configure the device
            ser.write(b'ROUT:CLOS (@1)\r\n')
            print("Command sent: ROUT:CLOS (@1)")
            time.sleep(1)

            ser.write(b'INIT:CONT ON\r\n')
            print("Command sent: INIT:CONT ON")
            time.sleep(1)

            ser.write(b'*CLS\r\n')
            print("Command sent: *CLS")
            time.sleep(1)

            while True:
                # Check STAT:OPER? to see if the measurement is complete
                ser.write(b'STAT:OPER?\r\n')
                #print("Command sent: STAT:OPER?")
                
                # Wait for the response
                time.sleep(0.5)  # Short delay to allow the device to respond
                response_stat = ser.read(ser.in_waiting).decode('ascii').strip()
                if response_stat:
                    status = int(response_stat.split()[-1])
                    #print("Status response received: ", bin(status))
                    
                    # If measurement is complete, fetch the latest temperature
                    if status == 0:
                        ser.write(b'FETC?\r\n')
                        #print("Command sent: FETC?")
                        
                        # Wait for the response
                        time.sleep(0.5)  # Short delay to allow the device to respond
                        response = ser.read(ser.in_waiting).decode('ascii').strip()
                        if response:
                            print("Response received: ", response)
                            responses.append(float(response.split()[0]))  # Convert response to float

                            # Update the plot with new data
                            update_plot(responses)
                    
                time.sleep(1)  # Delay before next status check
            
            # Close the serial port
            ser.close()
            print("Serial port closed.")
        
        else:
            print("Failed to open serial port.")
    
    except Exception as e:
        print("Error: ", str(e))
    
    finally:
        return responses

def update_plot(data):
    plt.clf()  # Clear the plot
    plt.plot(data, marker='o', linestyle='-')
    plt.title('Real-Time Temperature Measurements')
    plt.xlabel('Measurement Number')
    plt.ylabel('Temperature (°C)')
    plt.grid(True)
    plt.pause(0.1)  # Pause to allow the plot to update

if __name__ == "__main__":
    plt.ion()  # Turn on interactive mode for live updating plot
    fig = plt.figure()
    
    # Start communication with the device and plot the data
    communicate_with_device()
    
    # Keep the plot open
    plt.show(block=True)
