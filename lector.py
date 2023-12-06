#Declaración de librerías
from tkinter import *; #LIBRERÍA PARA LA INTERFAZ DEL PROGRAMA
from tkinter import messagebox as MessageBox; #LIBRERÍA PARA LA INTERFAZ DEL PROGRAMA
from tkinter import filedialog; #LIBRERÍA PARA LA INTERFAZ DEL PROGRAMA
import xml.etree.ElementTree as ET; #LIBRERÍA PARA LEER Y MODIFICAR ARCHIVOS XML
from datetime import date, timedelta; #FUNCION PARA MANIPULAR FECHA
from tkinter import ttk;
 
#Declaración de variables globales para el ImporteDR y el ImporteP.
global ImpDR; #ImporteDR
global ImpP; #ImporteP
global FechaXML; #Obtener la fecha del archivo XML;
global nomrec; #Nombre Receptor

#EN ESTA LISTA SE GUARDAN LOS REGIMENES CAPITALES QUE SE VAN A BUSCAR EN EL NOMBRE DEL RECEPTOR.
regimenes = (" SAS DE CV", " SA DE CV", " SA DE C V"," S DE RL DE CV", " SAPI DE CV", " S A DE C V", " S A",  " SAS", " SA", " SC DE RL DE CV", " SC")



#Función para abrir los archivos xml a modificar.
def AbrirArchivo():
    global abierto; #Declaraciòn de la variable global que contendrá la ruta al directorio de los archivos.
    abierto = filedialog.askopenfilenames(initialdir="C:", title="Seleccione archivo", filetypes=(("XML Files", ".xml"),("All Files", "*.*"))); # Aquí se obtiene las rutas de los archivos a modificar.
    ruta.set(str(abierto)); #A la variable global ruta, se le asignan los valores de la variable abierto, convirtiendolo a string para poder usar dichos valores.

#Función para modificar los archivos xml seleccionados
def modificarArchivo():
    progress = ttk.Progressbar(raiz, orient="horizontal", length=300, mode="determinate")
    progress.pack()
    ET.register_namespace('cfdi','http://www.sat.gob.mx/cfd/4'); #Se registra el namespace cfdi
    ET.register_namespace('pago20','http://www.sat.gob.mx/Pagos20'); #Se registra el namespace pago20
    a = 0; #Variable contadora para el ciclo for
    for cadena in abierto:   #Ciclo for para recorrer la lista de las rutas de los archivos.
        cadena = abierto[a]; #Variable para asignar un valor de la lista, de acuerdo al valor del contador
        cadena = str(cadena); #El valor obtenido se convierte a String
        tree = ET.parse(cadena); #Se lee el archivo xml
        root = tree.getroot(); #Obtener el archivo xml para usarlo en el programa
        ImpuestoTotal = 0; #Declaraciòn de variable acumuladora para calcular el TotalTrasladosImpuestoIVA16 y el ImpuestoP
        for ImpDR in root.iter('{http://www.sat.gob.mx/Pagos20}TrasladoDR'): #Ciclo for para corregir cada uno de los valores del ImporteDR en el documento.
            B = ImpDR.get("BaseDR"); #En esta variable se obtiene el valor del BaseDR
            B = float(B); #El valor de la variable se convierte a flotante para poder hacer operaciones
            ValorDR = round((float(B*0.160000)), 2); #En esta variable se hace la operación de BaseDR por el IVA, redondeando a 2 decimales
            ImpuestoTotal += ValorDR; #En la variable acumuladora se le va sumando el valor de la operación
            ValorDR= str(ValorDR); #Se convierte a string para poder reemplazarlo en el documento.
            ImpDR.set("ImporteDR", ValorDR); #Se reemplaza en el apartado "ImporteDR" el Valor obtenido de la operación (ValorDR)
            tree.write(abierto[a], encoding="utf-8"); #Se sobreescribe la información en el mismo archivo xml, estableciendole la ruta y el como debe codificarlo.
        for child in root.iter('{http://www.sat.gob.mx/Pagos20}Totales'): #Ciclo for para corregir el valor del TotalTrasladosImpuestoIVA16
            B = round(ImpuestoTotal,2); #En esta variable se le asigna el valor de la variable acumuladora (ImpuestoTotal), redondeando a 2 decimales.
            A = str(float(B)); #En esta variable se le asigna el valor anterior (B) convirtiendolo a string
            child.set("TotalTrasladosImpuestoIVA16", A); #Se reemplaza en el apartado TotalTrasladosImpuestoIVA16 el valor del string (A)
            tree.write(abierto[a], encoding="utf-8"); #Se sobreescribe la información en el mismo archivo xml, estableciendole la ruta y el como debe codificarlo.
        for ImpP in root.iter('{http://www.sat.gob.mx/Pagos20}TrasladoP'): #Ciclo for para corregir el valor del ImporteP
            B = round(ImpuestoTotal,2); #En esta variable se le asigna el valor de la variable acumuladora (ImpuestoTotal), redondeando a 2 decimales.
            A = str(float(B)); #En esta variable se le asigna el valor anterior (B) convirtiendolo a string
            ImpP.set("ImporteP", A); #Se reemplaza en el apartado ImporteP el valor del string (A)
            tree.write(abierto[a], encoding="utf-8"); #Se sobreescribe la información en el mismo archivo xml, estableciendole la ruta y el como debe codificarlo.
        for FechaXML in root.iter('{http://www.sat.gob.mx/cfd/4}Comprobante'): #Ciclo for para obtener y corregir el valor de la fecha del archivo xml.
            F = FechaXML.get("Fecha"); #En esta variable se obtiene el valor de la fecha obteniendo el siguiente formato "FechaTHora"
            Separador = F.split("T"); #En esta variable partimos el valor obtenido de la fecha en la letra T, donde dividirá la fecha en 2 strings: fecha y hora.
            fechax = Separador[0]; #En esta variable se guarda el valor de la fecha
            horax = Separador[1]; #En esta variable se guarda el valor de la hora
            hoy = date.today(); #Con esta linea se obtiene la fecha de hoy.
            menos = timedelta(-1); # Variable para restar un día a la fecha de hoy.
            ayer = hoy + menos; #Se hace la operacion de restar un día para obtener la fecha del día anterior.
            #dia = date.strftime(ayer, "%d");
            #dia = str(dia);
            ayer = str(ayer); #Se convierte a string la variable del día anterior.
            FechaXML.set("Fecha", ayer+"T"+horax); #Se reemplaza el vaor de la fecha concatenando el valor de la fecha de ayer mas la letra T mas la hora que se obtuvo anteriormente.
            tree.write(abierto[a], encoding="utf-8"); #Se sobreescribe la información en el mismo archivo xml, estableciendole la ruta y el como debe codificarlo.
        for nomrec in root.iter("{http://www.sat.gob.mx/cfd/4}Receptor"): #Ciclo for para obtener y corregir el nombre del receptor.
            k = nomrec.get("Nombre"); #En esta varialble se obtiene el nombre del receptor del archivo xml.
            k = str(k); #Se convierte a string la variable del nombre.
            nombreoriginal = k; #Agregamos una variable en donde se almacenará el nombre obtenido
            ad=0 #Inicializamos variable contadora
            for s in regimenes: #ciclo for para buscar si el nombre contiene algún regímen capital
                k = k.replace(regimenes[ad],"") #Si lo tiene, se reemplaza por un string vacío
                ad+=1; #Se incrementa en 1 la variable contadora
            #nomrec.set("Nombre", k); #Se reemplaza el nombre del receptor con el nombre ya corregido.
            #tree.write(abierto[a], encoding="utf-8"); #Se sobreescribe la información en el mismo archivo xml, estableciendole la ruta y el como debe codificarlo.
            if(nombreoriginal != k): #En este if se condiciona si el nombre original (nombreoriginal) es igual al nombre que se modificó (k)
                #MessageBox.showinfo("LECTOR ARCHIVOS XML", "CAMBIO A NOMBRE RECEPTOR EN ARCHIVO: \n"+abierto[a]+"\nNOMBRE ORIGINAL: "+nombreoriginal + "\nNOMBRE NUEVO: " +k); #Si es verdadera la condición se mostrará un cambio en el nombre de receptor indicando que archivo se le midificó dicho valor
                resp = MessageBox.askquestion("LECTOR ARCHIVOS XML", "CAMBIO A NOMBRE RECEPTOR EN ARCHIVO: \n"+abierto[a]+"\nNOMBRE ORIGINAL: "+nombreoriginal + "\nNOMBRE NUEVO: " +k + "\n¿DESEAS REALIZAR EL CAMBIO?"); #En este cuadro de dialogo se muestra los cambios de nombre que se van a hacer y se pregunta si se quiere que se hagan esos cambios, teniendo como opciones si o no
                if resp == 'yes': #if para cuando la respuesta sea si
                    nomrec.set("Nombre", k); #Se reemplaza el nombre del receptor con el nombre ya corregido.
                    tree.write(abierto[a], encoding="utf-8"); #Se sobreescribe la información en el mismo archivo xml, estableciendole la ruta y el como debe codificarlo.
                elif resp == 'no': #if para cuando la respuesta sea no
                    nomrec.set("Nombre", nombreoriginal); #Se reemplaza el nombre del receptor con el nombre original.
                    tree.write(abierto[a], encoding="utf-8"); #Se sobreescribe la información en el mismo archivo xml, estableciendole la ruta y el como debe codificarlo.
                else: #else para cualquier otro caso que se presente
                    MessageBox.showwarning('Error', 'ALGO SALIÓ MAL, INTENTALO NUEVAMENTE') #Mensaje de alerta para errores.
        a+=1; #Se incrementa en 1 el valor de la variable contadora.
        progress["value"] = a * 100 / len(abierto)
        raiz.update_idletasks()
    MessageBox.showinfo("LECTOR ARCHIVOS XML", "ARCHIVO(S) MODIFICADO CON EXITO"); #Esta linea muestra una ventana de información una vez finalizados todos los ciclos for
    ruta.set(""); #Se establece el valor de la variable global ruta a su valor original.
    progress["value"] = 0;
    progress.config(length=0);
    raiz.update_idletasks()

    
#Código para la interfaz
raiz = Tk(); #Declaración de la ventana

wtotal = raiz.winfo_screenwidth()
htotal = raiz.winfo_screenheight()
wapp = 450;
happ = 200;

wapp = round((wtotal-wapp)/2)
happ = round((htotal-happ)/2)
print(str(wapp));
print(str(happ));

raiz.geometry("450x200+" + str(wapp) + "+" + str(happ)); #Se establece los tamaños ("Ancho x alto + posicion x de la ventana + posicion y de la ventana")
raiz.title("LECTOR ARCHIVOS XML"); #Titulo de la ventana
raiz.resizable(False, False); 
raiz.config(bg="white"); #Se establece el color del fondo de la ventana
raiz.iconbitmap('MRM.ico'); #Se define una ruta para el icono

#Declaración de variables globales
global ImpuestoTotal;
global ruta;
global TTIVA;
ruta = StringVar(); #Se define el tipo de valor como StringVar, lo cual significa StringVariable, para poder usarlo en la caja de texto.

botonabrir = Button(raiz, text="Abrir Archivo", command=AbrirArchivo, bg="red", fg="white", font=("Cambria", 12), activebackground="red", cursor="hand2", borderwidth=1).place(x=320, y=45, width=120, height=35); #Boton para ejecutar la funcion de abrir archivo
botonmodi = Button(raiz, text="Modificar", command=modificarArchivo, bg="red", fg="white", font=("Cambria", 12), activebackground="red", cursor="hand2", borderwidth=1).place(x=165, y=130, width=120, height=40); #Boton para ejecutar la funcion de modificar archivo
EtiquetaRuta = Label(raiz, text="RUTA", bg="white", fg="black", font=("Cambria", 16)).place(x=20, y=45); #Texto para mostrar en ventana
CajaRuta = Entry(raiz, textvariable=ruta, bg="white", fg="black", font=("Cambria", 12), state="readonly").place(x=80, y=45, width=230, height=35); #En esta caja de texto se muestra las rutas de los archivos seleccionados

#progress = ttk.Progressbar(raiz, orient="horizontal", length=300, mode="determinate")
#progress.pack()

raiz.mainloop(); #Línea que sirve para que la ventana aparezca en pantalla.

#CÓDIGO ANTERIOR PARA MODIFICAR FACTURAS ELECTRONICAS DE UNA SOLA LINEA
""" def modificarArchivo():
    ET.register_namespace('cfdi','http://www.sat.gob.mx/cfd/4');
    ET.register_namespace('pago20','http://www.sat.gob.mx/Pagos20');
    cadena = str(abierto);
    tree = ET.parse(cadena);
    root = tree.getroot();
    ImpuestoTotal = 0;
    for ImpDR in root.iter('{http://www.sat.gob.mx/Pagos20}TrasladoDR'):
        B = ImpDR.get("BaseDR");
        B = float(B);
        ValorDR = round((float(B*0.160000)), 2);
        ImpuestoTotal += ValorDR;
        ValorDR= str(ValorDR);
        ImpDR.set("ImporteDR", ValorDR);
        tree.write(abierto, encoding="utf-8");
    for child in root.iter('{http://www.sat.gob.mx/Pagos20}Totales'):
        B = round(ImpuestoTotal,2);
        A = str(float(B));
        child.set("TotalTrasladosImpuestoIVA16", A);
        tree.write(abierto, encoding="utf-8");
    for ImpP in root.iter('{http://www.sat.gob.mx/Pagos20}TrasladoP'):
        B = round(ImpuestoTotal,2);
        A = str(float(B));
        ImpP.set("ImporteP", A);
        tree.write(abierto, encoding="utf-8");
        #print(round(ImpuestoTotal, 2));
        MessageBox.showinfo("LECTOR ARCHIVOS XML", "ARCHIVO MODIFICADO CON EXITO");
        ruta.set(""); """
