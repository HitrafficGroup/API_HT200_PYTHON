from web_socket2 import getTime,getFases,getSecuencia,getSplit,getPattern,getAccion,getPlanes,getScnedule
run = True
while run:
  
    print("1 >> Tiempo del Controlador")
    print("2 >> Phases del Controlador")
    print("3 >> Secuency del Controlador")
    print("4 >> Split del Controlador")
    print("5 >> Pattern del Controlador")
    print("6 >> Action del Controlador")
    print("7 >> Plan del Controlador")
    print("8 >> Schedule del Controlador")
    print("any >> Salir \n")
    option = input("\n Escoga una opcion: ")
    if option == '1':
        getTime()
    elif option == '2':
        getFases()
    elif option == '3':
        getSecuencia()
    elif option == '4':
        getSplit()
    elif option == '5':
        getPattern()
    elif option == '6':
        getAccion()
    elif option == '7':
        getPlanes()
    elif option == '8':
        getScnedule()
    else:
        run = False