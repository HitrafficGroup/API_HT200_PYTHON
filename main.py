from web_sockets import MySocket
import test_data
run = True
controlador =  MySocket('192.168.1.122')
while run:
  
    print("1   >> Tiempo del Controlador")
    print("2   >> Phases del Controlador")
    print("3   >> Secuency del Controlador")
    print("4   >> Split del Controlador")
    print("5   >> Pattern del Controlador")
    print("6   >> Action del Controlador")
    print("7   >> Plan del Controlador")
    print("8   >> Schedule del Controlador")
    print("9   >> DeviceInfo del Controlador")
    print("10  >> BasicInfo del Controlador")
    print("11  >> Unit del Controlador")
    print("12  >> Channel del Controlador")
    print("13  >> coordinacion del Controlador")
    print("14  >> Overlap del Controlador")
    print("15  >> cargar unit1 del Controlador")
    print("16  >> cargar unit2 del Controlador")
    print("any >> Salir \n")
    option = input("\n Escoga una opcion: ")
    if option == '1':
        try:
            controlador.getTime()
        except Exception as e:
            print(e)
            print("algo ocurrio mal")
            controlador.disconnect()
    elif option == '2':
        try:
            controlador.getFases()
        except Exception as e:
            print(e)
            print("algo ocurrio mal")
            controlador.disconnect()
    elif option == '3':
        try:
            controlador.getSecuencia()
        except Exception as e:
            print(e)
            print("algo ocurrio mal")
            controlador.disconnect()
    elif option == '4':
        try:
            controlador.getSplit()
        except Exception as e:
            print(e)
            print("algo ocurrio mal")
            controlador.disconnect()
    elif option == '5':
        try:
            controlador.getPattern()
        except Exception as e:
            print(e)
            print("algo ocurrio mal")
            controlador.disconnect()
    elif option == '6':
        try:
            controlador.getAccion()
        except Exception as e:
            print(e)
            print("algo ocurrio mal")
            controlador.disconnect()
    elif option == '7':
        try:
            controlador.getPlanes()
        except Exception as e:
            print(e)
            print("algo ocurrio mal")
            controlador.disconnect()
    elif option == '8':
        try:
            controlador.getScnedule()
        except Exception as e:
            print(e)
            print("algo ocurrio mal")
            controlador.disconnect()
    elif option == '9':
        try:
            controlador.getDeviceInfo()
        except Exception as e:
            print(e)
            print("algo ocurrio mal")
            controlador.disconnect()
    elif option == '10':
        try:
            controlador.getBasicInfo()
        except Exception as e:
            print(e)
            print("algo ocurrio mal")
            controlador.disconnect()   
    elif option == '11':
        try:
            controlador.getUnit()
        except Exception as e:
            print(e)
            print("algo ocurrio mal")
            controlador.disconnect()   
    elif option == '12':
        try:
            controlador.getChannel()
        except Exception as e:
            print(e)
            print("algo ocurrio mal")
            controlador.disconnect()   
    elif option == '13':
        try:
            controlador.getCoord()
        except Exception as e:
            print(e)
            print("algo ocurrio mal")
            controlador.disconnect()   
    elif option == '14':
        try:
            controlador.getOverlap()
        except Exception as e:
            print(e)
            print("algo ocurrio mal")
            controlador.disconnect()   
    elif option == '15':
        try:
            if controlador.setUnit(test_data.unit_data_1):
                print('envio correcto')
            else:
                print('envio incorrecto')
        except Exception as e:
            print(e)
            print("algo ocurrio mal")
            controlador.disconnect()  
    elif option == '16':
        try:
            if controlador.setUnit(test_data.unit_data_2):
                print('envio correcto')
            else:
                print('envio incorrecto')
        except Exception as e:
            print(e)
            print("algo ocurrio mal")
            controlador.disconnect()  
    else:
        controlador.disconnect()
        run = False