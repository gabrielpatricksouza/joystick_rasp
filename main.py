from pynput.keyboard import Controller, Key
import bluetooth
import pygame
import sys

DEAD_ZONE = 0.35  # Definindo a DEAD ZONE

# Cria o controlador de teclado
keyboard = Controller()

def value_from_axis(joystick, axis, position):
    """Captura o valor do eixo quando o usuário o move para um valor específico."""
    print(f"Mova o eixo {axis} para seu {position} e pressione o Gatilho.")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == axis:
                    print(f"\rEixo {axis}: {joystick.get_axis(axis):.2f}", end="")
            if event.type == pygame.JOYBUTTONDOWN:
                print()
                return joystick.get_axis(axis)

def is_within_dead_zone(value):
    """Verifica se o valor do eixo está dentro da DEAD ZONE."""
    return -DEAD_ZONE < value < DEAD_ZONE

def monitor_joystick(joystick, joystick_index, axes_limits):
    """Monitora os movimentos dos eixos do joystick até que o botão 7 seja pressionado."""
    print(f"Monitorando movimentos do joystick {joystick_index + 1}. Pressione o botão 7 para sair.")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                for axis in range(joystick.get_numaxes()):
                    # Ignora o eixo 3
                    if axis == 3:
                        continue

                    axis_value = joystick.get_axis(axis)

                    axis_center = axes_limits[axis]
                    print(f"[{axis_value} / {axis_center}]")
                    if axis == 0:
                        if is_within_dead_zone(axis_value):
                            keyboard.release(Key.left)
                            keyboard.release(Key.right)
                        elif axis_value < axis_center:
                            keyboard.release(Key.right)
                            keyboard.press(Key.left)
                            print(f"Joystick {joystick_index + 1} - Eixo {axis}: Press => 'left'")
                        elif axis_value > axis_center:
                            keyboard.release(Key.left)
                            keyboard.press(Key.right)
                            print(f"Joystick {joystick_index + 1} - Eixo {axis}: Press => 'right'")
                    if axis == 1:
                        if is_within_dead_zone(axis_value):
                            keyboard.release(Key.up)
                            keyboard.release(Key.down)
                        elif axis_value < axis_center:
                            keyboard.release(Key.down)
                            keyboard.press(Key.up)
                            print(f"Joystick {joystick_index + 1} - Eixo {axis}: Press => 'up'")
                        elif axis_value > axis_center:
                            keyboard.release(Key.up)
                            keyboard.press(Key.down)
                            print(f"Joystick {joystick_index + 1} - Eixo {axis}: Press => 'down'")

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 6:  # Botão 7, normalmente indexado como 6
                    print(f"Saindo do joystick {joystick_index + 1}...")
                    return

def main():
    # Inicializa o pygame e o módulo de joysticks
    pygame.init()
    pygame.joystick.init()

    num_joysticks = pygame.joystick.get_count()
    if num_joysticks == 0:
        print("Nenhum joystick conectado.")
        pygame.quit()
        sys.exit()

    joysticks = []
    axes_limits = []

    for i in range(num_joysticks):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
        joysticks.append(joystick)
        print(f"Joystick {i + 1}: {joystick.get_name()} conectado.")

        # Captura os valores mínimo, médio e máximo para cada eixo
        limits = []
        for axis in range(joystick.get_numaxes()):
            # Ignora o eixo 3
            if axis == 3:
                continue

            axis_center = value_from_axis(joystick, axis, "centro")
            limits.append(axis_center)
            print(f"Valores ajustados para o joystick {i + 1}, eixo {axis}: {axis_center:.2f}")
        axes_limits.append(limits)

    print("Calibração concluída.")

    # Inicia o monitoramento dos movimentos de todos os joysticks
    for i, joystick in enumerate(joysticks):
        monitor_joystick(joystick, i, axes_limits[i])

    pygame.quit()

if __name__ == "__main__":
    main()
