import time
import tkinter as tk
import os
import cv2
import random
import sys
from tkinter import Label, font, Button, Entry
from PIL import Image, ImageTk

# fondos iniciales de los competidores
user_budget = 10
computer_budget = 10
table_budget = 2

# ventana inicial
root = tk.Tk()
root.title("GUAYABITA GAME!!")
root.configure(background='#27b4cd')
root.geometry('1000x700')

# Aquí se usa letra cursiva
font_style = font.Font(family="Cursive", size=40)
font_style2 = font.Font(family="Cursive", size=70)

# Obtener la ruta del directorio donde se ejecuta el script
current_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(current_dir, 'multimedia')

# Cargar la imagen original
original_image = Image.open(os.path.join(image_dir, 'guayabita_game.png'))

# Escalar la imagen a un tamaño específico, por ejemplo, (300, 200)
scaled_image = original_image.resize((1000, 500))

# Convertir la imagen escalada a ImageTk.PhotoImage
guayabita_game_img = ImageTk.PhotoImage(scaled_image)

# label imagen
guayabita_game_label = tk.Label(root, image=guayabita_game_img)

#ubicar la imagen
guayabita_game_label.grid(row=0, column=0, padx=0, pady=10)


# funcion para aceptar jugar
def click_play_game():
    root.destroy()
    second_window()


# boton star_game
play_game_button = tk.Button(root, bg='#82e0aa', text='JUGAR', height=1, width=8, font=font_style,
                             command=click_play_game)
play_game_button.grid(row=1, column=0, padx=0, pady=20)

#---------------------------------------------------------------------------------------------------#

# Variable global para almacenar la imagen capturada
image_capture = None

#variable para guardar el nombre
user_name = "".capitalize()

# Variables globales para los botones
bet_all_button_user = None
bet_minimum_button_user = None
bet_all_button_computer = None
bet_minimum_button_computer = None

# Variables para guardar resultados de lanzamientos
user_throw1 = None
user_throw2 = None
user_throw3 = None
computer_throw1 = None
computer_throw2 = None
computer_throw3 = None


#--------------------------------------------------------------------------------------#
# funcion para obtener numero aleatorio
def roll_dice():
    return random.randint(1, 6)


# Eliminar botones existentes si existen
def delete_button_user():
    global bet_all_button_user, bet_minimum_button_user
    if bet_all_button_user is not None:
        bet_all_button_user.destroy()  # O usa `destroy()` si quieres eliminar el botón completamente
        bet_all_button_user = None

    if bet_minimum_button_user is not None:
        bet_minimum_button_user.destroy()  # O usa `destroy()` si quieres eliminar el botón completamente
        bet_minimum_button_user = None


def delete_button_computer():
    global bet_all_button_computer, bet_minimum_button_computer
    if bet_all_button_computer is not None:
        bet_all_button_computer.destroy()  # O usa `destroy()` si quieres eliminar el botón completamente
        bet_all_button_computer = None

    if bet_minimum_button_computer is not None:
        bet_minimum_button_computer.destroy()  # O usa `destroy()` si quieres eliminar el botón completamente
        bet_minimum_button_computer = None


set_up_window = None


def check_budget_table():
    global table_budget, user_budget, computer_budget
    if table_budget <= 0:
        user_budget -= 1
        computer_budget -= 1
        table_budget += 2


#-----------------------------------------------------------------------------------------------------#


# funcion para abrir tercera pestaña
def third_window():
    global user_budget, table_budget

    def game_over():
        global user_budget, computer_budget
        if user_budget <= 0:
            game_window.destroy()
            lose_window = tk.Tk()
            lose_window.title('GUAYABITA_GAME')
            lose_window.configure(background='#f44331')
            lose_window.geometry('900x900')
            font_style4 = font.Font(family="Cursive", size=90)
            lose_label = tk.Label(lose_window, font=font_style4, text='PERDISTE 🙁🙁!!')
            lose_label.grid(row=1, column=1, padx=0, pady=50)

            lose_window.mainloop()

        elif computer_budget <= 0:
            game_window.destroy()
            win_window = tk.Tk()
            win_window.title('GUAYABITA_GAME')
            win_window.configure(background='#8cf431')
            win_window.geometry('900x900')
            font_style4 = font.Font(family="Cursive", size=90)
            win_label = tk.Label(win_window, font=font_style4, text='GANASTE 🥴🥳!!')
            win_label.grid(row=1, column=1, padx=0, pady=50)

            win_window.mainloop()

    # funcion para lanzar dados
    def user_round():
        global user_budget, computer_budget, table_budget
        global bet_all_button_user, bet_minimum_button_user
        global user_throw1
        user_throw1 = roll_dice()
        throw_dice_result.configure(text=user_throw1)
        turn_user.configure(bg='#58d68d')
        turn_computer.configure(bg='#ec7063')
        hide_throw_button()

        # Crear botones de apuesta si es necesario
        if user_throw1 != 1 and user_throw1 != 6:
            bet_all_button_user = tk.Button(game_window, bg='#58d68d', text='TODO', height=1, width=10,
                                            font=font_style2, command=click_bet_all_user)
            bet_all_button_user.grid(row=1, column=1, padx=0, pady=0)

            bet_minimum_button_user = tk.Button(game_window, bg='#f4d03f', text='MINIMA', height=1, width=10,
                                                font=font_style2, command=click_bet_minimum_user)
            bet_minimum_button_user.grid(row=2, column=1, padx=0, pady=0)
        else:
            # Manejo de presupuestos según el resultado del dado
            if user_throw1 == 1:
                user_budget -= 1
                table_budget += 1
                user_lose_minimum()
                update_labels()
                update_and_wait()
                throw_dice_result.configure(text='')
                update_labels()
                check_budget_table()
                update_labels()
                game_over()
                delete_button_user()
                update_and_wait()
                computer_round()
            elif user_throw1 == 6:
                user_budget -= 1
                computer_budget -= 1
                table_budget += 2
                both_lose_minimum()
                update_labels()
                update_and_wait()
                throw_dice_result.configure(text='')
                update_labels()
                check_budget_table()
                update_labels()
                game_over()
                delete_button_user()
                update_and_wait()
                game_window.update_idletasks
                game_window.update
                computer_round()

    # variable para guardar el turno
    def computer_round():
        global computer_budget, table_budget, user_budget
        global bet_all_button_user, bet_minimum_button_user
        global bet_all_button_computer, bet_minimum_button_computer
        global computer_throw1
        delete_button_user()
        update_and_wait()
        turn_user.configure(bg='#ec7063')
        turn_computer.configure(bg='#58d68d')
        game_window.update_idletasks()
        game_window.update
        update_and_wait()
        computer_throw1 = roll_dice()
        throw_dice_result.configure(text=computer_throw1)
        update_and_wait()
        if computer_throw1 != 1 and computer_throw1 != 6:
            computer_choice()
        elif computer_throw1 == 1:
            computer_budget -= 1
            table_budget += 1
            computer_lose_minimum()
            update_labels()
            update_and_wait()
            throw_dice_result.configure(text='')
            check_budget_table()
            update_labels()
            game_over()
            activate_throw_button()

        elif computer_throw1 == 6:
            user_budget -= 1
            computer_budget -= 1
            table_budget += 2
            both_lose_minimum()
            update_labels()
            update_and_wait()
            throw_dice_result.configure(text='')
            activate_throw_button()
            check_budget_table()
            update_labels()
            game_over()

    game_window = tk.Tk()
    game_window.title('GUAYABITA_GAME')
    game_window.configure(background='#8e44ad')
    game_window.geometry('1150x700')

    # Aquí se usa letra cursiva
    font_style2 = font.Font(family="Cursive", size=20)
    font_style3 = ("Helvetica", 14)
    font_style4 = font.Font(family="Cursive", size=70)
    font_style5 = font.Font(family="Cursive", size=20)
    font_style6 = ("Helvetica", 15)

    # Obtener la ruta del directorio donde se ejecuta el script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(current_dir, 'multimedia')

    # Cargar imágenes usando PIL y convertirlas en objetos ImageTk.PhotoImage
    brayan_original_image = Image.open(os.path.join(image_dir, 'brayan.png'))
    image_capture = Image.open(os.path.join(image_dir, 'captured_photo.png'))
    table_original_image = Image.open(os.path.join(image_dir, 'table.png'))
    dice_original_image = Image.open(os.path.join(image_dir, 'dice.png'))
    instructions_original_image = Image.open(os.path.join(image_dir, 'instrucciones.png'))

    # Escalar la imagen a un tamaño específico, por ejemplo, (300, 200)
    scaled_brayan_image = brayan_original_image.resize((150, 150), resample=Image.LANCZOS)
    image_capture = image_capture.resize((150, 150), resample=Image.LANCZOS)
    scaled_table_image = table_original_image.resize((450, 160), resample=Image.LANCZOS)
    scaled_dice_image = dice_original_image.resize((110, 110), resample=Image.LANCZOS)
    scaled_instrucciones_image = instructions_original_image.resize((300, 200), resample=Image.LANCZOS)
    # Convertir la imagen escalada a ImageTk.PhotoImage
    brayan_img = ImageTk.PhotoImage(scaled_brayan_image)
    photo = ImageTk.PhotoImage(image_capture)
    table_img = ImageTk.PhotoImage(scaled_table_image)
    dice_img = ImageTk.PhotoImage(scaled_dice_image)
    instructions_img = ImageTk.PhotoImage(scaled_instrucciones_image)
    # label imagen
    brayan_label = tk.Label(game_window, image=brayan_img)
    photo_label = tk.Label(game_window, image=photo)
    table_label = tk.Label(game_window, image=table_img)
    dice_label = tk.Label(game_window, image=dice_img, width=5, bg='#8e44ad')
    instructions = tk.Label(game_window, image=instructions_img)
    # Crear label para turnos
    turn_user = tk.Label(game_window, font=font_style5, text=f'{user_name} Turno')
    turn_user.grid(row=0, column=1, padx=(1, 200), pady=0)

    turn_computer = tk.Label(game_window, font=font_style5, text='BrayanPC Turno')
    turn_computer.grid(row=0, column=1, padx=(200, 1), pady=0)

    # Crear label nombre usuario
    name = tk.Label(game_window, bg='#edbb99', font=font_style2, text=user_name)
    name.grid(row=0, column=0, padx=10, pady=10)

    # crear label nombre computer
    computer_name_label = tk.Label(game_window, text='BrayanPC', font=font_style2, bg='#edbb99')
    computer_name_label.grid(row=0, column=2, padx=10, pady=10)

    # ubicar la imagen
    photo_label.grid(row=1, column=0, padx=20, pady=0)
    table_label.grid(row=4, column=1, padx=20, pady=100, sticky='nsew')
    brayan_label.grid(row=1, column=2, padx=20, pady=0)
    dice_label.grid(row=3, column=1, padx=(1, 115), pady=0, sticky='nsew')
    instructions.grid(row=4, column=0, padx=20, pady=0)

    # label para saber el resultado de los dados
    throw_dice_result = tk.Label(game_window, bg='#d5dbdb', font=font_style4, width=2, height=1)
    throw_dice_result.grid(row=3, column=1, padx=(130, 1), pady=10)

    # boton lanzar dados
    throw_user_button = tk.Button(game_window, bg='#58d68d', text='Lanzar dado', height=1, width=10, font=font_style2,
                                  command=user_round)
    throw_user_button.grid(row=3, column=0, padx=20, pady=0)

    # label para saber los fondos
    user_budget_label = tk.Label(game_window, bg='#edbb99', font=font_style3,
                                 text=f'Saldo {user_name.capitalize()}:{user_budget}$', height=2, width=18)
    user_budget_label.grid(row=2, column=0, padx=20, pady=10)

    computer_budget_label = tk.Label(game_window, bg='#edbb99', font=font_style3,
                                     text=f'Saldo BrayanPC:{computer_budget}$', height=2, width=20)
    computer_budget_label.grid(row=2, column=2, padx=0, pady=10)

    table_budget_label = tk.Label(game_window, bg='#edbb99', font=font_style2, text=f'Mesa:{table_budget}$',
                                  height=2, width=12)
    table_budget_label.grid(row=4, column=2, padx=0, pady=0)

    # funcion para apostar all usuario
    def click_bet_all_user():
        global user_budget, table_budget
        global user_throw2
        throw_dice_result.configure(text='')
        update_and_wait_longer()
        user_throw2 = roll_dice()
        throw_dice_result.configure(text=user_throw2)
        update_and_wait()
        if user_throw2 > user_throw1:
            user_budget += table_budget
            table_budget -= table_budget
            user_win_all()
            update_labels()
            update_and_wait()
            throw_dice_result.configure(text='')
            update_and_wait()
            check_budget_table()
            update_labels()
            game_over()
            delete_button_user()
            
            
        else:
            user_budget -= table_budget
            table_budget += table_budget
            user_lose_all()
            update_labels()
            update_and_wait()
            throw_dice_result.configure(text='')
            update_and_wait()
            check_budget_table()
            update_labels()
            game_over()
            delete_button_user()
        game_window.update()
        computer_round()
    

    def click_bet_minimum_user():
        global user_budget, table_budget
        global user_throw3
        throw_dice_result.configure(text='')
        update_and_wait_longer()
        user_throw3 = roll_dice()
        throw_dice_result.configure(text=user_throw3)
        update_and_wait()
        if user_throw3 > user_throw1:
            user_budget += 1
            table_budget -= 1
            user_win_minimum()
            update_labels()
            update_and_wait()
            throw_dice_result.configure(text='')
            update_and_wait()
            check_budget_table()
            update_labels()
            game_over()
            delete_button_user()
            
        else:
            user_budget -= 1
            table_budget += 1
            user_lose_minimum()
            update_labels()
            update_and_wait()
            throw_dice_result.configure(text='')
            update_and_wait()
            update_and_wait()
            check_budget_table()
            update_labels()
            game_over()
            delete_button_user()
        game_window.update()
        computer_round()
            

    # funcion para apostar all computer
    def bet_all_computer():
        global computer_budget, table_budget
        global computer_throw2
        throw_dice_result.configure(text='')
        update_and_wait_longer()
        delete_button_user()
        update_and_wait()
        computer_throw2 = roll_dice()
        throw_dice_result.configure(text=computer_throw2)
        update_and_wait()
        if computer_throw2 > computer_throw1:
            computer_budget += table_budget
            table_budget -= table_budget
            computer_win_all()
            update_labels()
            update_and_wait()
            throw_dice_result.configure(text='')
            update_and_wait()
            check_budget_table()
            update_labels()
            game_over()
            delete_button_computer()

        else:
            computer_budget -= table_budget
            table_budget += table_budget
            computer_lose_all()
            update_labels()
            update_and_wait()
            throw_dice_result.configure(text='')
            update_and_wait()
            check_budget_table()
            update_labels()
            game_over()
            delete_button_computer()

    def bet_minimum_computer():
        global computer_budget, table_budget
        global computer_throw3
        throw_dice_result.configure(text='')
        computer_throw3 = roll_dice()
        throw_dice_result.configure(text=computer_throw3)
        update_and_wait()
        if computer_throw3 > computer_throw1:
            computer_budget += 1
            table_budget -= 1
            computer_win_minimum()
            update_labels()
            update_and_wait()
            throw_dice_result.configure(text='')

        else:
            computer_budget -= 1
            table_budget += 1
            computer_lose_minimum()
            update_labels()
            update_and_wait()
            throw_dice_result.configure(text='')

    def update_labels():
        user_budget_label.config(text=f'Saldo {user_name.capitalize()}:{user_budget}$')
        computer_budget_label.config(text=f'Saldo BrayanPC:{computer_budget}$')
        table_budget_label.config(text=f'Mesa:{table_budget}$')
        update_and_wait()

    def hide_throw_button():
        throw_user_button.config(state='disabled')

    def activate_throw_button():
        throw_user_button.config(state='normal')

    def computer_choice():
        options = ['bet_all', 'bet_minimum']
        computer_result = random.choice(options)
        update_and_wait()
        if computer_result == 'bet_all':
            update_and_wait()
            computer_choice_bet_all()
            throw_dice_result.configure(text='')
            update_and_wait()
            activate_throw_button()
        else:
            update_and_wait()
            computer_choice_bet_minimum()
            throw_dice_result.configure(text='')
            update_and_wait()
            activate_throw_button()

    def update_and_wait():
        game_window.update_idletasks()
        time.sleep(1)

    def update_and_wait_longer():
        game_window.update_idletasks()
        time.sleep(2)

    def computer_choice_bet_all():
        global bet_all_button_computer
        bet_all_button_computer = tk.Label(game_window, bg='#58d68d', text='TODO', height=1, width=10,
                                           font=font_style2)
        bet_all_button_computer.grid(row=1, column=1, padx=0, pady=0)
        update_and_wait()
        bet_all_computer()
        delete_button_computer()
        update_and_wait()

    def computer_choice_bet_minimum():
        global bet_minimum_button_computer
        bet_minimum_button_computer = tk.Label(game_window, bg='#f4d03f', text='MINIMA', height=1, width=10,
                                               font=font_style2)
        bet_minimum_button_computer.grid(row=2, column=1, padx=0, pady=0)
        update_and_wait()
        bet_minimum_computer()
        delete_button_computer()
        update_and_wait()

    def user_win_all():
        user_win_all_label = tk.Label(game_window, bg='#f44331', text=f'{user_name} Gana Todo!!', height=1, width=20,
                                      font=font_style6)
        user_win_all_label.grid(row=3, column=2, padx=0, pady=0)
        update_and_wait_longer()
        user_win_all_label.destroy()

    def computer_win_all():
        computer_win_all_label = tk.Label(game_window, bg='#f44331', text=f'BrayanPC Gana Todo!!', height=1, width=20,
                                          font=font_style6)
        computer_win_all_label.grid(row=3, column=2, padx=0, pady=0)
        update_and_wait_longer()
        computer_win_all_label.destroy()

    def user_lose_all():
        user_win_lose_label = tk.Label(game_window, bg='#f44331', text=f'{user_name} Pierde saldo!!', height=1,
                                       width=20,
                                       font=font_style6)
        user_win_lose_label.grid(row=3, column=2, padx=0, pady=0)
        update_and_wait_longer()
        user_win_lose_label.destroy()

    def computer_lose_all():
        computer_lose_all_label = tk.Label(game_window, bg='#f44331', text=f'BrayanPC Pierde saldo!!', height=1,
                                           width=20,
                                           font=font_style6)
        computer_lose_all_label.grid(row=3, column=2, padx=0, pady=0)
        update_and_wait_longer()
        computer_lose_all_label.destroy()

    def user_win_minimum():
        user_win_minimum_label = tk.Label(game_window, bg='#f44331', text=f'{user_name} Gana 1$!!', height=1, width=20,
                                          font=font_style6)
        user_win_minimum_label.grid(row=3, column=2, padx=0, pady=0)
        update_and_wait_longer()
        user_win_minimum_label.destroy()

    def computer_win_minimum():
        computer_win_minimum_label = tk.Label(game_window, bg='#f44331', text='BrayanPC Gana 1$!!', height=1,
                                              width=20,
                                              font=font_style6)
        computer_win_minimum_label.grid(row=3, column=2, padx=0, pady=0)
        update_and_wait_longer()
        computer_win_minimum_label.destroy()

    def user_lose_minimum():
        user_lose_minimum_label = tk.Label(game_window, bg='#f44331', text=f'{user_name} pierde 1$!!', height=1,
                                           width=20,
                                           font=font_style6)
        user_lose_minimum_label.grid(row=3, column=2, padx=0, pady=0)
        update_and_wait_longer()
        user_lose_minimum_label.destroy()

    def computer_lose_minimum():
        computer_lose_minimum_label = tk.Label(game_window, bg='#f44331', text='Brayan PC pierde 1$!!', height=1,
                                               width=20,
                                               font=font_style6)
        computer_lose_minimum_label.grid(row=3, column=2, padx=0, pady=0)
        update_and_wait_longer()
        computer_lose_minimum_label.destroy()

    def both_lose_minimum():
        both_lose_minimum_label = tk.Label(game_window, bg='#f44331', text='Ambos pierden 1$!!', height=1, width=20,
                                           font=font_style6)
        both_lose_minimum_label.grid(row=3, column=2, padx=0, pady=0)
        update_and_wait_longer()
        both_lose_minimum_label.destroy()

    game_window.mainloop()


# funcion para abrir la segunda pestaña
def second_window():
    global image_capture
    set_up_window = tk.Tk()
    set_up_window.title("GUAYABITA GAME!!")
    set_up_window.configure(background='#edbb99')
    set_up_window.geometry('1000x700')

    # Aquí se usa letra cursiva
    font_style2 = font.Font(family="Cursive", size=20)
    font_style3 = ("Helvetica", 15)

    # funcion para
    def close_window():
        get_text()
        set_up_window.destroy()
        third_window()

    # Función que guarda el nombre
    def get_text():
        global user_name
        entered_text = entry.get()  # Obtener el texto ingresado
        if entered_text:
            user_name = entered_text.capitalize().lower()[:7]

    # Función para capturar  foto
    def capture_photo():
        global set_up_window
        # Inicializar la cámara
        cap = cv2.VideoCapture(0)  # 0 indica la cámara predeterminada del sistema

        # Capturar una imagen
        ret, frame = cap.read()

        # Guardar la imagen capturada en un archivo
        if ret:
            # Obtener la ruta del directorio donde se ejecuta el script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_dir = os.path.join(current_dir, 'multimedia')

            if not os.path.exists(image_dir):
                os.makedirs(image_dir)

            filename =  filename = os.path.join(image_dir, 'captured_photo.png')
            
            cv2.imwrite(filename, frame)
            cap.release()  # Liberar la cámara

            # Mostrar la imagen capturada en tkinter
            image_capture = Image.open(os.path.join(image_dir, filename))
            image_capture = image_capture.resize((200, 200), resample=Image.LANCZOS)
            photo = ImageTk.PhotoImage(image_capture)

            # Actualizar la etiqueta existente o crear una nueva si es necesario
            if hasattr(capture_photo, 'captured_label'):
                capture_photo.captured_label.configure(image=photo)
                capture_photo.captured_label.image = photo  # Mantener referencia al objeto ImageTk
            else:
                capture_photo.captured_label = Label(set_up_window, image=photo)
                capture_photo.captured_label.grid(row=1, column=0, padx=(1, 400), pady=20)
            # Forzar una pequeña pausa para permitir que tkinter actualice la imagen
            # Forzar una actualización de la interfaz
            set_up_window.update_idletasks()
            set_up_window.update()
    
    # Obtener la ruta del directorio donde se ejecuta el script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(current_dir, 'multimedia')

    # Cargar la imagen original
    original_image = Image.open(os.path.join(image_dir, 'guayabita.png'))
    brayan_original_image = Image.open(os.path.join(image_dir, 'brayan.png'))

    # Escalar la imagen a un tamaño específico, por ejemplo, (300, 200)
    scaled_image = original_image.resize((998, 200))
    scaled_brayan_image = brayan_original_image.resize((200, 200))

    # Convertir la imagen escalada a ImageTk.PhotoImage
    guayabita_img = ImageTk.PhotoImage(scaled_image)
    brayan_img = ImageTk.PhotoImage(scaled_brayan_image)

    # label imagen
    guayabita_label = tk.Label(set_up_window, image=guayabita_img)
    brayan_label = tk.Label(set_up_window, image=brayan_img)

    # ubicar la imagen
    guayabita_label.grid(row=0, column=0, padx=0, pady=0)
    brayan_label.grid(row=1, column=0, padx=(550, 1), pady=20)

    # boton empezar
    empezar_button = tk.Button(set_up_window, bg='#82e0aa', text='EMPEZAR', height=1, width=10,
                               font=font_style2, command=close_window)
    empezar_button.grid(row=4, column=0, padx=(70, 1), pady=0)

    # crear cuadro de texto
    entry = tk.Entry(set_up_window, width=12, font=font_style2, bg="white")
    entry.grid(row=2, column=0, padx=(1, 400), pady=0)

    # Crear label nombre usuario
    name = tk.Label(set_up_window, bg='#edbb99', font=font_style3, text="¿NOMBRE?")
    name.grid(row=2, column=0, padx=(1, 800), pady=10)

    # boton insertar imagen usuario
    foto_usuario_button = tk.Button(set_up_window, bg='white', text='INSERTAR IMG', height=1, width=13,
                                    font=font_style3, command=capture_photo)
    foto_usuario_button.grid(row=3, column=0, padx=(1, 400), pady=30)

    # crear label nombre computer
    computer_name_label = tk.Label(set_up_window, text='BrayanPC', font=font_style2, bg='#edbb99')
    computer_name_label.grid(row=2, column=0, padx=(550, 1), pady=0)
    set_up_window.mainloop()


root.mainloop()
